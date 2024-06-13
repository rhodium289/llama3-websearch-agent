from langchain.prompts import PromptTemplate
from models.llm_models import llama3_json
from langchain_core.output_parsers import JsonOutputParser

#You should then use suitable relationship to connect these togther. 

generate_enr_prompt_template = PromptTemplate(
    template="""
    
    <|begin_of_text|>
    
    <|start_header_id|>system<|end_header_id|> 
    
    Generate a prompt for a LLM so that it can take a piece of text and extract all the entities out of it and generate commands to populate a neo4j graph database. This is my attempt;
    You are an AI data scientist skilled in the use of Neo4j working on collecting information relating to a Research Question Tasks, that synthesizes web search results. 
    Strictly use the following pieces of web search context to generate neo4j instructions to create the nodes and relationships for a knowledge graph based on the websearch context.
    If you don't know the answer, do not generate anything.
    You should focus on entities such as people, places, times, dates and roles. Don't worry about the relationships yet.
    Only make nodes from direct references to material if provided in the context.
    Return the JSON with a single key 'commands' with no preamble or explanation which contains an array of neo4j commands.
    Please make sure that you exhaustively generate the commands for all of the  nodes. Please also make sure that you avoid any possessive nouns and use double quotes for strings. For every node
    please make sure that you consistently use a name and label in the form name:label.
    
    <|eot_id|>
    
    <|start_header_id|>user<|end_header_id|>
    
    Question: {question} 
    Web Search Context: {context} 
    Neo4j Commands:
    
    <|eot_id|>
    
    <|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "context"],
)


#generate_enr_prompt_template = PromptTemplate(
#    template="""
#    
#    <|begin_of_text|>
#    
#    <|start_header_id|>system<|end_header_id|> 
#    
#    You are an AI data scientist skilled in the use of Neo4j, working on collecting information relating to a Research Question Task 
#    that synthesizes web search results. Strictly use the following pieces of web search context to generate Neo4j instructions to 
#    create the nodes and relationships for a knowledge graph based on the web search context.
#
#    If you don't know the answer, do not generate anything.
#
#    You should focus on entities such as people, places, times, dates, and roles. Use suitable relationships to connect these together. 
#    Only make direct references to material provided in the context.
#
#    Return the JSON with a single key 'commands' with no preamble or explanation, which contains an array of Neo4j commands. Ensure you 
#    exhaustively generate the commands for all the relationships between all the nodes. Avoid any possessive nouns and use double quotes 
#    for strings. For every node, consistently use a name and label in the form `name:label` and ensure the relationships are linked correctly 
#    by using these identifiers.
#
#    ### Example Input:
#    Henry Ford was born on July 30, 1863, in Wayne County, Michigan. He founded the Ford Motor Company. He died on April 7, 1947, in Dearborn, 
#    Michigan. The company produced the Model T automobile.
#
#    ### Example Output:
#    json
#    {
#        "commands": [
#            "CREATE (henry_ford:Person {name: \"Henry Ford\", birthdate: \"1863-07-30\", deathdate: \"1947-04-07\"})",
#            "CREATE (wayne_county:Location {name: \"Wayne County, Michigan\"})",
#            "CREATE (dearborn:Location {name: \"Dearborn, Michigan\"})",
#            "CREATE (ford_motor_company:Organization {name: \"Ford Motor Company\"})",
#            "CREATE (model_t:Vehicle {name: \"Model T\"})",
#            "CREATE (henry_ford:Person)-[:BORN_IN]->(wayne_county:Location)",
#            "CREATE (henry_ford:Person)-[:DIED_IN]->(dearborn:Location)",
#            "CREATE (henry_ford:Person)-[:FOUNDED]->(ford_motor_company:Organization)",
#            "CREATE (ford_motor_company:Organization)-[:PRODUCED]->(model_t:Vehicle)"
#        ]
#    }
#    
#    <|eot_id|>
#    
#    <|start_header_id|>user<|end_header_id|>
#    
#    Question: {question} 
#    Web Search Context: {context} 
#    Neo4j Commands:
#    
#    <|eot_id|>
#    
#    <|start_header_id|>assistant<|end_header_id|>""",
#    input_variables=["question", "context"],
#)
