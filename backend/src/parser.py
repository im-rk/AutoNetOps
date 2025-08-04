import spacy
import re
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

APPLICATIONS = ["zoom", "youtube", "teams", "netflix", "skype"]
ACTIONS = {
    "block": ["block", "ban", "stop", "prevent"],
    "allow": ["allow", "permit", "enable", "access"],
    "prioritize": ["prioritize", "prefer", "boost", "give priority"]
}

app_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
app_patterns = [nlp.make_doc(app) for app in APPLICATIONS]
app_matcher.add("APP", app_patterns)

def extract_intent_and_entities(text):
    doc = nlp(text.lower())

    app_matches = app_matcher(doc)
    apps = {doc[start:end].text: start for match_id, start, end in app_matches}

    action_positions = []
    for action, keywords in ACTIONS.items():
        for kw in keywords:
            for match in re.finditer(rf"\b{re.escape(kw)}\b", text.lower()):
                action_positions.append((action, match.start()))

    intents = []
    for app, app_pos in apps.items():
        closest_action = None
        min_dist = float("inf")
        for action, act_pos in action_positions:
            dist = abs(app_pos - act_pos)
            if dist < min_dist:
                min_dist = dist
                closest_action = action
        if closest_action:
            intents.append({
                "application": app,
                "action": closest_action
            })

    return {
        "original_text": text,
        "intents": intents
    }

if __name__ == "__main__":
    query = "Block YouTube and allow Zoom for meetings"
    result = extract_intent_and_entities(query)
    print(result)
