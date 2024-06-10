import json
import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to validate JSON data
def validate_data(data):
    required_node_fields = {'name', 'labels'}
    required_rel_fields = {'start_node', 'end_node', 'type'}
    for command in data['commands']:
        if 'create' in command:
            if 'node' in command['create']:
                node = command['create']['node']
                if not required_node_fields.issubset(node.keys()):
                    raise ValueError(f"Node is missing required fields: {required_node_fields}")
            elif 'relationship' in command['create']:
                relationship = command['create']['relationship']
                if not required_rel_fields.issubset(relationship.keys()):
                    raise ValueError(f"Relationship is missing required fields: {required_rel_fields}")
            else:
                raise ValueError("Invalid JSON format: 'create' must contain 'node' or 'relationship'")

def execute_single_command(command, uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        session.run(command)
    driver.close()
    
# Function to generate Cypher commands from JSON data
def generate_cypher_commands(data):
    cypher_commands = []
    for command in data['commands']:
        if 'create' in command:
            if 'node' in command['create']:
                node = command['create']['node']
                labels = ":".join(node['labels'])
                properties = node.get('properties', {})
                properties_str = ", ".join([f'{key}: ${key}' for key in properties])
                cypher_commands.append((f'CREATE (n:{labels} {{name: $name, {properties_str}}})', node))
            elif 'relationship' in command['create']:
                relationship = command['create']['relationship']
                cypher_commands.append(
                    (f'MATCH (a {{name: $start_node}}), (b {{name: $end_node}}) '
                     f'CREATE (a)-[:{relationship["type"]}]->(b)', relationship)
                )
    return cypher_commands

# Function to execute Cypher commands in Neo4j
def execute_cypher_commands(cypher_commands, uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        for command in cypher_commands:
            try:
                session.run(command)
            except ServiceUnavailable as e:
                logger.error(f"Failed to execute command: {command}. Error: {e}")
    driver.close()