from collections import defaultdict
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def extract_keywords_by_category(text: str, skills_dict: dict):
    text = text.lower()
    matched = defaultdict(list)
    missing = defaultdict(list)

    for category, keywords in skills_dict.items():
        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
            if re.search(pattern, text):
                matched[category].append(keyword)
            else:
                missing[category].append(keyword)

    return dict(matched), dict(missing)




def extract_unrecognized_keywords(jd_text, skills_dict, matched_dict):
    all_keywords = set()
    for keywords in skills_dict.values():
        all_keywords.update(keywords)

    # Also remove those already matched
    for cat_keywords in matched_dict.values():
        all_keywords.update(cat_keywords)

    # Remove ignored terms explicitly
    ignore_set = set(skills_dict.get("ignore", []))
    words = set(jd_text.lower().split())
    unrecognized = words - all_keywords - ignore_set

    # Optional: filter out short/common words
    return [word for word in unrecognized if word.isalpha() and len(word) > 2]

