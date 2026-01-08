from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import subprocess
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Docker Variables
docker_compose_file_name = "docker-compose.yml"
docker_command = f"docker compose -f {docker_compose_file_name} up -d"

userQuery = input("Enter your research query: ")
workerNodes = int(input("Enter the Number of Worker Nodes: "))
useDocument = input("Do you want to use a document for research? (yes/no): ")


if(useDocument.lower() == "yes"):
    try:
        print("\nMake Sure you Have Docker installed on your System!!")
        print("\nRunning the docker script to load Qdrant DB")
        subprocess.run(docker_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("\nDocker Compose file executed successfully.")
        
        print("\nLoading the Document , Running Required Scripts: \n")
        import sys
        subprocess.run([sys.executable, "documentLoader.py"], capture_output=True, text=True, check=True)
        
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

        vector_db = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            url = "http://localhost:6333",
            collection_name="DocumentsforAI"
        )

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Docker Compose or RAG System : {e.stderr}")
        exit(1)
    except FileNotFoundError:
        print(f"Error: The command 'docker' was not found. Please ensure Docker is installed and in your system's PATH.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)



# Helper Functions

def merge_dicts(old: dict, new: dict) -> dict:
    if old is None:
        old = {}
    return {**old, **new}

def extract_json(text: str) -> dict:
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in model output")
    return json.loads(match.group())

#Graph State

class State(TypedDict):
    Query: str
    HeadNodes: Annotated[list, add_messages]
    DistributedWork: dict          
    currentTask: str              
    currentKey: str                 
    worker_outputs: Annotated[dict, merge_dicts]     

     
#LLM Used

llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

#1st Node

def StartNode(state: dict):
    if(useDocument.lower() == "yes"):
        search_results = vector_db.similarity_search(userQuery)
        context = "\n\n\n".join([f"Page Content : {result.page_content} \n Page Number : {result.metadata['page_label']} \n File Location :{result.metadata['source']}" for result in search_results])
        messages = [
        SystemMessage(content=f"Perform deep research and provide a detailed response. use the Following Content:{context}"),
        HumanMessage(content=state["Query"])
        ] 
        deepResearch = llm_gemini.invoke(messages)
        print(deepResearch)
        return {
            "HeadNodes": [deepResearch]
        }

    messages = [
        SystemMessage(content="Perform deep research and provide a detailed response."),
        HumanMessage(content=state["Query"])
    ] 
    deepResearch = llm_gemini.invoke(messages)
    print(deepResearch)
    return {
        "HeadNodes": [deepResearch]
    }

#2nd Node

def DividerNode(state: dict):
    if(useDocument.lower()=="yes"):
        search_results = vector_db.similarity_search(userQuery)
        context = "\n\n\n".join([f"Page Content : {result.page_content} \n Page Number : {result.metadata['page_label']} \n File Location :{result.metadata['source']}" for result in search_results])
        messages = [
        SystemMessage(content=f"You are a professional research coordinator.and your work is to divide the research into {workerNodes} so that Each Node can Perform Seperate and In depth Research , You can use the Following Insights from the Document {context}"),
        HumanMessage(
            content=f"""Research:{state["HeadNodes"][0].content} Query:{state["Query"]} Workers: {workerNodes}Return ONLY valid JSON in this format: {{"Node1": "...", "Node2": "..."}} """
        )
        ]
        response = llm_gemini.invoke(messages)
        distributedWork = extract_json(response.content)
        print(distributedWork)
        return {
            "DistributedWork": distributedWork
        }

    messages = [
        SystemMessage(content=f"You are a professional research coordinator.and your work is to divide the research into {workerNodes} so that Each Node can Perform Seperate and In depth Research "),
        HumanMessage(
            content=f"""Research:{state["HeadNodes"][0].content} Query:{state["Query"]} Workers: {workerNodes}Return ONLY valid JSON in this format: {{"Node1": "...", "Node2": "..."}} """
        )
    ]
    response = llm_gemini.invoke(messages)
    distributedWork = extract_json(response.content)
    print(distributedWork)
    return {
        "DistributedWork": distributedWork
    }

#3rd Node
#Fanin-Fout Pattern

def WorkerNode(state:dict):
    if(useDocument.lower()=="yes"):
        task=state["currentTask"]
        search_results = vector_db.similarity_search(task)
        context = "\n\n\n".join([f"Page Content : {result.page_content} \n Page Number : {result.metadata['page_label']} \n File Location :{result.metadata['source']}" for result in search_results])
        messages = [
            SystemMessage(content=f"You are a research assistant. The user will provide a topic or a section of text. Your task is to expand on it, polish it, and provide a detailed explanation. Return the refined content., and Use the Content from the Following : {context}"),
            HumanMessage(content=str(task))
        ]
        result = llm_gemini.invoke(messages)
        return {
            "worker_outputs": {
                state["currentKey"]: result.content
            }
        }

    task=state["currentTask"]
    messages = [
        SystemMessage(content="You are a research assistant. The user will provide a topic or a section of text. Your task is to expand on it, polish it, and provide a detailed explanation. Return the refined content."),
        HumanMessage(content=str(task))
    ]
    result = llm_gemini.invoke(messages)
    return {
        "worker_outputs": {
            state["currentKey"]: result.content
        }
    }


def route_to_workers(state: dict):
    return [
        Send(
            "WorkerNode",
            {
                "currentKey": key,
                "currentTask": task
            }
        )
        for key, task in state["DistributedWork"].items()
    ]

#Final Node

def finalNode(state:dict):
    print(f"DEBUG: worker_outputs keys: {list(state['worker_outputs'].keys())}")
    combinedReport = "\n\n".join(
        f"--- {key} ---\n{content}" for key, content in state["worker_outputs"].items()
    )
    print(f" The Final Output: \n{combinedReport}")


#Graph Construction

graph_builder = StateGraph(State)
graph_builder.add_node("StartNode", StartNode)
graph_builder.add_node("DividerNode", DividerNode)
graph_builder.add_node("WorkerNode", WorkerNode)
graph_builder.add_node("finalNode", finalNode)

graph_builder.add_edge(START, "StartNode")
graph_builder.add_edge("StartNode", "DividerNode")
graph_builder.add_conditional_edges("DividerNode", route_to_workers)
graph_builder.add_edge("WorkerNode", "finalNode")
graph_builder.add_edge("finalNode", END)


graph = graph_builder.compile()

#Initial State
initial_state = {
    "Heads": 0,
    "Query": f"{userQuery}",
    "HeadNodes": [],
    "Worker": 0,
    "WorkerNodes": [],
    "DistributedWork":{}
}

# Graph Invocation
graph.invoke(initial_state)


