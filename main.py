from flask import Flask, request, jsonify
import re

def main():


    url = "https://{server}/ns-api/v2/Domains/{domain}/MAC-Addresses"
    # Find a dollar amount
    matches = re.search(r"\{\w+\}", url)
    while True:
        match = re.search(r"\{\w+\}", url)
        if not match:
            break
        print(f"Found: {match.group()}")
        if "server" in match.group():
            url = url.replace(match.group(), "crexnmsdev1.solint.net")
        else:
            start,end=match.span()
            tmp=url[start:end]
            question = input("Enter : "+tmp)
            url = url.replace(match.group(), "mgoud")
            print(question)

    print(url)

if __name__ == '__main__':
  main()
