from typing import TypedDict

from SimpleGraph import my_obj


class PortfolioState(TypedDict):
    amount_usd:float

def main():
    print("Hello from agent-langgraph!")
    my_obj:PortfolioState ={
        'amount_usd':100
    }
    print(my_obj['amount_usd'])


if __name__ == "__main__":
    main()
