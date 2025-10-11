# import sys
# import os
# import json
# import socket


# SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
# BASE_DIR = os.path.dirname(SRC_DIR)  # backend/

# if SRC_DIR not in sys.path:
#     sys.path.append(SRC_DIR)

# INTENT_DIR = os.path.join(BASE_DIR, "data", "policy")
# MAPPING_FILE = os.path.join(SRC_DIR, "mappings", "app_mappings.json")

# from utils.util import load_policies 


# def load_app_mappings(mapping_file):
#     with open(mapping_file, 'r') as fp:
#         return json.load(fp)

# def resolve_application_ips(domains):
#     ips = set() 
#     for domain in domains:
#         try:
#             resolved_ips = socket.getaddrinfo(domain, None)
#             ips.update(ip[4][0] for ip in resolved_ips)
#         except socket.gaierror:
#             print(f"[WARN] Could not resolve domain: {domain}")
#     return list(ips)

# def intent_to_rules(yaml_file, mapping_file):
#     rules = []
#     intents = load_policies(yaml_file)
#     mappings = load_app_mappings(mapping_file)

#     for intent in intents:
#         app = intent['application']
#         action = intent['action']
#         time_condition = intent.get('condition', {}).get('time', {})

#         domains = mappings.get(app, [])
#         ips = resolve_application_ips(domains)

#         for ip in ips:
#             rules.append({
#                 "ip_dst": ip,
#                 "action": action,
#                 "priority": 100 if action.lower() == "prioritize" else 10,
#                 "time": time_condition
#             })
#     return rules



# if __name__ == "__main__":
#     yaml_file = os.path.join(INTENT_DIR, "policy_2025_08_09_120920.yaml")
#     rules = intent_to_rules(yaml_file, MAPPING_FILE)
#     print(rules)
