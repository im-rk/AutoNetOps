from utils.util import load_policies

INTENT_DIR="data/intents"
OUTPUT_RULES_FILE="artifacts/final_rules.json"

def intent_to_rules(policy):
    rules=[]
    for intent in policy.get('intents',[]):
        app=intent['application']
        action=intent['action']
        condition=intent.get('condition',{})

        if action=="deny":
            rules.append(f"block all traffic for {app} during {condition}")
        elif action=="prioritize":
            rules.append(f"Prioritize traffic for {app} during {condition}")
    return rules
