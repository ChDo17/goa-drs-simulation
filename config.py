import json

def load_assumptions():
    with open("data/assumptions.json", "r") as file:
        return json.load(file)
