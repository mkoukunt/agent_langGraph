from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


class PortfolioState(TypedDict):
    amount_usd:float
    total_usd:float
    total_inr:float

my_obj: PortfolioState ={
    'amount_usd':100,
    'total_usd':100,
    'total_inr':100
}

def calc_total(state:PortfolioState) ->PortfolioState:
    state['total_usd']=state['amount_usd']*1.08
    return state

def conver_to_inr(state:PortfolioState) ->PortfolioState:
    state['total_inr']=state['total_usd']*85
    return state

builder=StateGraph(PortfolioState)
builder.add_node("calc_total_node",calc_total)
builder.add_node("conver_to_inr_node",conver_to_inr)
builder.add_edge(START,"calc_total_node")
builder.add_edge("calc_total_node","conver_to_inr_node")
builder.add_edge("conver_to_inr_node",END)

graph=builder.compile()
graph.invoke(my_obj)
print(my_obj['total_inr'])