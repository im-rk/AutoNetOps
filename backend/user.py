import sys
import os

from .src.rules_installation.rule_installer import run_installer
from .src.parsing.llm.llm_client_langchain import LLMClientLangChain



user_intent=input("Enter your intent in plain English :")
clinet=LLMClientLangChain()
policy_yaml=clinet.generate(user_intent)
#print(type(policy_yaml))

run_installer(policy_yaml)