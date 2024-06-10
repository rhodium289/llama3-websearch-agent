import json
import logging
from config.config import neo4j_uri, neo4j_user, neo4j_password
from  tools.neo4j import validate_data, generate_cypher_commands, execute_cypher_commands, execute_single_command

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def populate_neo4j(state):
    commands = state['commands']
    
    # Print out the commands
    for command in commands:
        logger.info(f"Command: {command}")

    # Execute each Cypher command individually
    for command in commands:
        try:
            execute_single_command(command, neo4j_uri, neo4j_user, neo4j_password)
            logger.info(f"Command executed successfully: {command}")
        except Exception as e:
            logger.error(f"An error occurred while executing command: {command}. Error: {e}")