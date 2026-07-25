import os
from typing import TypedDict, Annotated, Sequence
import operator

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Import our custom weather tool
from weather_tool import get_weather_forecast

# 1. Define the Agent State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    crop_type: str
    farm_location: str

# 2. Define Tools and LLM
tools = [get_weather_forecast]
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
).bind_tools(tools)

# 3. Define Nodes
def agent_node(state: AgentState):
    """The reasoning node where the LLM decides to call a tool or make a recommendation."""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    """Determines if the agent needs to run a tool or if it has reached a final answer."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# 4. Build the LangGraph Workflow
workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

app = workflow.compile()

# 5. Function to Run the Farm Advisor Agent
def run_farm_advisor(crop_type="Wheat", location="Midnapore, West Bengal"):
    system_prompt = SystemMessage(
        content=(
            "You are AgroSmart AI, an autonomous virtual agronomist. "
            "Your goal is water conservation (SDG 6) and crop productivity (SDG 2). "
            "When given a farm location, ALWAYS check the daily weather forecast using your tool. "
            "If predicted rainfall is greater than 5.0 mm, explicitly advise to SKIP irrigation to save water. "
            "Provide a concise, practical, professional recommendation for the farmer."
        )
    )
    
    user_prompt = HumanMessage(
        content=f"Please analyze the irrigation needs for my {crop_type} farm in {location} today."
    )
    
    inputs = {
        "messages": [system_prompt, user_prompt],
        "crop_type": crop_type,
        "farm_location": location
    }
    
    print("\n--- Running AgroSmart LangGraph Agent ---")
    result = app.invoke(inputs)
    
    print("\n=== AGENT FINAL RECOMMENDATION ===")
    print(result["messages"][-1].content)
    print("===================================\n")

if __name__ == "__main__":
    run_farm_advisor()