import json

def load_categorized_skills(filepath="skills.json"):
    with open(filepath, "r") as f:
        return json.load(f)
