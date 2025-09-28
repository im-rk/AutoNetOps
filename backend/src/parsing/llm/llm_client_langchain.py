from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from ...utils.util import save_file
load_dotenv()

class LLMClientLangChain:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),  
            convert_system_message_to_human=True,
            temperature=0.65
        )
    
    def generate(self,prompt):
        system_template="You are a YAML policy generator for a network automation system. Given a user query describing network intent, output a structured YAML policy. Include a `description` and a list of `intents`, each with `application`, `action`, and optionally `condition`.\n\nOutput YAML only, no explanation."
        chat_prompt=ChatPromptTemplate.from_messages([
            ("system",system_template),
            ("user","{prompt}")
        ])
        messages=chat_prompt.invoke({"prompt":prompt})
        response=self.model.invoke(messages)
        content=response.content
        save_path=save_file(content)
        print(content)
        return save_path
# if __name__ == "__main__":
#     client = LLMClientLangChain()
#     query = "Block YouTube and prioritize Zoom during work hours"
    # yaml_output = client.generate(query)
    