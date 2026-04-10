from typing import TypedDict

import requests
from langgraph.constants import START, END
from langgraph.graph import StateGraph
import re

class PortfolioState(TypedDict):
    steps:str
    url:str
    res:str


my_obj: PortfolioState ={
    'steps':'',
    'url':'',
    'res':''

}

def calc_url(state:PortfolioState) ->PortfolioState:
    #print("in calc_url")
    print(state['steps'])
    spaceitems = re.split(r'\d+\.\s*', state['steps'])
    spaceitems = [item for item in spaceitems if item]
    spaceitems = [item for item in spaceitems  if item != '\n']
    # The URL of the API endpoint
    print(spaceitems)
    url = 'http://rabini.org:5001/generate'
    body = {
        "question": spaceitems[0]+'?'
    }
    # Execute the GET request
    response = requests.post(url, json=body)
    print(response.text)
    # Convert the JSON response into a Python dictionary
    state['url'] = response.text
    return state

def calc_reasoning(state:PortfolioState) ->PortfolioState:
    question = input("Enter your question: ")
    #print(f"Hello, {question}!")
    # The URL of the API endpoint
    url = 'http://rabini.org:5000/generate'
    body={
    "question":question
    }
    # Execute the GET request
    response = requests.post(url,json=body)

    # Convert the JSON response into a Python dictionary
    state['steps'] = response.text
    return state


def calc_data(state:PortfolioState) ->PortfolioState:
   # domain=input("Enter your domain: ")
    print(state['url'])
    # The URL of the API endpoint
    url=state['url'].split()[1]
    print(url)
    matches = re.finditer(r"\{\w+\}", url)
    while True:
        match = re.search(r"\{\w+\}", url)
        if not match:
            break
        if "server" in match.group():
            url = url.replace(match.group(), "crexnmsdev1.solint.net")
        else:
            start, end = match.span()
            tmp = url[start+1:end-1]
            ans = input("Enter : " + tmp)
            url = url.replace(match.group(), ans)

    #url = 'https://crexnmsdev1.solint.net/ns-api/v2/domains/'+ domain+'/phones'
    print(url)
    headers = {
        "Authorization": f"Bearer 21769fe6f8d3f3b44b3253aae249934c",
    }
    # Execute the GET request
    response = requests.get(url,headers=headers)

    # Convert the JSON response into a Python dictionary
    state['res'] = response.text
    return state

builder=StateGraph(PortfolioState)
builder.add_node("calc_reasoning_node",calc_reasoning)
builder.add_node("calc_url_node",calc_url)
builder.add_node("calc_data_node",calc_data)
builder.add_edge(START,"calc_reasoning_node")
builder.add_edge("calc_reasoning_node","calc_url_node")
builder.add_edge("calc_url_node","calc_data_node")
builder.add_edge("calc_data_node",END)

graph=builder.compile()
my_obj=graph.invoke(my_obj)
print(my_obj['steps'])
print(my_obj['url'])
print(my_obj['res'])