import json
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

model_name = "ml6team/keyphrase-extraction-distilbert-inspec"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Load dictionary from JSON
with open("skills.json", "r") as f:
    skills_dict = json.load(f)

# Flatten all skill values to lowercase
KNOWN_SKILLS = set()
for category in skills_dict.values():
    KNOWN_SKILLS.update(skill.lower() for skill in category)

def extract_entities_ner(text: str):
    try:
        results = ner_pipeline(text)
        keywords = set(ent.get("word", "").lower().strip() for ent in results if len(ent.get("word", "")) > 1)

        # Fallback match
        text_lower = text.lower()
        for skill in KNOWN_SKILLS:
            if skill in text_lower:
                keywords.add(skill)

        return sorted(keywords)

    except Exception as e:
        raise RuntimeError(f"NER error: {e}")
