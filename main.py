from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import json
import re
from dotenv import load_dotenv

load_dotenv()

userQuery = input("Enter your research query: ")
workerNodes = int(input("Enter the Number of Worker Nodes: "))

def merge_dicts(old: dict, new: dict) -> dict:
    if old is None:
        old = {}
    return {**old, **new}


class State(TypedDict):
    Query: str
    HeadNodes: Annotated[list, add_messages]
    DistributedWork: dict          
    currentTask: str              
    currentKey: str                 
    worker_outputs: Annotated[dict, merge_dicts]          


llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)


def StartNode(state: dict):
    messages = [
        SystemMessage(content="Perform deep research and provide a detailed response."),
        HumanMessage(content=state["Query"])
    ] 
    deepResearch = llm_gemini.invoke(messages)
    print(deepResearch)
    return {
        "HeadNodes": [deepResearch]
    }

def extract_json(text: str) -> dict:
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in model output")
    return json.loads(match.group())

def DividerNode(state: dict):
    messages = [
        SystemMessage(content="You are a professional research coordinator."),
        HumanMessage(
            content=f"""Research:{state["HeadNodes"][0].content} Query:{state["Query"]} Workers: {workerNodes}Return ONLY valid JSON in this format: {{"Node1": "...", "Node2": "..."}} """
        )
    ]
    response = llm_gemini.invoke(messages)
    distributedWork = extract_json(response.content)
    return {
        "DistributedWork": distributedWork
    }

def WorkerNode(state:dict):
    task=state["currentTask"]
    messages = [
        SystemMessage(content="You are a worker node.ONLY answer the assigned task.Do NOT summarize other areas.Do NOT provide conclusions.Return concise, focused output."),
        HumanMessage(content=task)
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


def finalNode(state:dict):
    combinedReport = "\n\n".join(
        msg.content for msg in state["WorkerNodes"]
    )
    print(f" The Final Output: {combinedReport}")



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

initial_state = {
    "Heads": 0,
    "Query": f"{userQuery}",
    "HeadNodes": [],
    "Worker": 0,
    "WorkerNodes": [],
    "DistributedWork":{}
}

graph.invoke(initial_state)


