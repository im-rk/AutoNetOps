import os
from datetime import datetime
import yaml
def save_file(yaml_content:str):
    timestamp=datetime.now().strftime("%Y_%m_%d_%H%M%S")
    filename=f"policy_{timestamp}.yaml"
    dir_path=os.path.join("data","policy")
    save_path=os.path.join(dir_path,filename)

    os.makedirs(dir_path,exist_ok=True)
    with open(save_path,"w") as fp:
        fp.write(yaml_content)
    
    print(f"file saved to {save_path}")

def load_policies(file_path):
    with open(file_path,"r") as f:
        data=yaml.safe_load(f)
    return data.get("intents",{})
