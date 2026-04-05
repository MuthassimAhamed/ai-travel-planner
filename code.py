from typing import TypedDict
from langgraph.graph import StateGraph
from langchain_ollama import ChatOllama

# -------------------------------
# LLM (LOCAL - OLLAMA)
# -------------------------------
llm = ChatOllama(model="llama3")

# -------------------------------
# STATE
# -------------------------------
class TravelState(TypedDict):
    user_input: str
    flights: str
    hotels: str
    itinerary: str
    budget_check: str
    final_plan: str

# -------------------------------
# AGENTS
# -------------------------------

def flight_agent(state: TravelState):
    prompt = f"""
    Find 2 flight options for:
    {state['user_input']}
    Include approximate price in INR.
    """
    response = llm.invoke(prompt)
    return {"flights": response.content}


def hotel_agent(state: TravelState):
    prompt = f"""
    Suggest 2 hotels for:
    {state['user_input']}
    Include price per night in INR.
    """
    response = llm.invoke(prompt)
    return {"hotels": response.content}


def itinerary_agent(state: TravelState):
    prompt = f"""
    Create a 3-day itinerary for:
    {state['user_input']}

    Format:
    Day 1:
    Day 2:
    Day 3:
    """
    response = llm.invoke(prompt)
    return {"itinerary": response.content}


def budget_agent(state: TravelState):
    prompt = f"""
    Check if trip fits budget:

    User Request:
    {state['user_input']}

    Flights:
    {state['flights']}

    Hotels:
    {state['hotels']}

    Suggest cheaper options if needed.
    """
    response = llm.invoke(prompt)
    return {"budget_check": response.content}


def final_agent(state: TravelState):
    prompt = f"""
    Create a structured travel plan:

    Flights:
    {state['flights']}

    Hotels:
    {state['hotels']}

    Itinerary:
    {state['itinerary']}

    Budget:
    {state['budget_check']}
    """
    response = llm.invoke(prompt)
    return {"final_plan": response.content}

# -------------------------------
# LANGGRAPH FLOW
# -------------------------------
builder = StateGraph(TravelState)

builder.add_node("flight", flight_agent)
builder.add_node("hotel", hotel_agent)
builder.add_node("itinerary", itinerary_agent)
builder.add_node("budget", budget_agent)
builder.add_node("final", final_agent)

builder.set_entry_point("flight")

builder.add_edge("flight", "hotel")
builder.add_edge("hotel", "itinerary")
builder.add_edge("itinerary", "budget")
builder.add_edge("budget", "final")

graph = builder.compile()