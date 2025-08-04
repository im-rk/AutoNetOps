import re
from model_loder import nlp_pipeline

APPLICATIONS=["zoom","youtube","teams","netflix","skype"]
ACTIONS={
    "block":["block","stop","ban","prevent"],
    "prioritize":["prioritize","prefer","give priority","boost"],
    "allow":["allow","permit","enable","access"]
}

def extract_intent_and_entities(text):
    text=text.lower()
    new_result=nlp_pipeline(text)

    found_apps=[]
    intents=[]

    app_positions=[]
    for entity in new_result:
        word=entity['word'].lower()
        for app in APPLICATIONS:
            if app in word:
                start=text.find(app)
                app_positions.append((app,start))
    
    action_positions=[]
    for act, keywords in ACTIONS.items():
        for kw in keywords:
            for match in re.finditer(rf"\b{re.escape(kw)}\b", text):
                action_positions.append((act, match.start()))

    
    for app,app_pos in app_positions:
        closest_action=None
        min_dist=float('inf')
        for act,act_pos in action_positions:
            dist=abs(app_pos-act_pos)
            if dist<min_dist:
                min_dist=dist
                closest_action=act
        if closest_action:
            intents.append({
                "application":app,
                "action":closest_action
            })
    return {
        "original_text":text,
        "intents":intents
    }

        
print(extract_intent_and_entities("Block YouTube and allow Zoom for meetings"))
