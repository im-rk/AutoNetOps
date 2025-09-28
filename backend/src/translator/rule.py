import sys
import os
import json


from utils.util import load_policies


# -----------------------------
# Helpers
# -----------------------------
def assign_mininet_ips(intents, base="10.0.0."):
    """Assigns sequential Mininet IPs (10.0.0.x) to applications in intents."""
    app_to_ip = {}
    for i, intent in enumerate(intents, start=2):
        app = intent.get("application")
        if app and app not in app_to_ip:
            app_to_ip[app] = f"{base}{i}"
    return app_to_ip


# -----------------------------
# Intents → OpenFlow rules
# -----------------------------
def intents_to_rules(yaml_file, mapping_file):
    rules = []

    # ✅ Always allow ARP
    rules.append({
        "dpid": 1,
        "priority": 300,
        "match": {"eth_type": 2054},  # ARP
        "actions": [{"type": "OUTPUT", "port": "ALL"}]
    })

    # Load policy file (YAML → dict/list)
    policy = load_policies(yaml_file)

    if isinstance(policy, dict):
        intents = policy.get("intents", [])
    elif isinstance(policy, list):
        intents = policy
    else:
        intents = []

    # 🔹 Assign synthetic Mininet IPs
    app_to_ip = assign_mininet_ips(intents)

    for intent in intents:
        app = intent.get("application")
        action = intent.get("action")

        if not app or not action:
            continue

        ip = app_to_ip.get(app)
        if not ip:
            continue

        if action.lower() == "deny":
            rules.append({
                "dpid": 1,
                "priority": 200,
                "match": {"eth_type": 2048, "ipv4_dst": ip},
                "actions": []  # drop
            })
        elif action.lower() == "prioritize":
            rules.append({
                "dpid": 1,
                "priority": 250,
                "match": {"eth_type": 2048, "ipv4_dst": ip},
                "actions": [{"type": "OUTPUT", "port": "NORMAL"}]
            })

    # 🌐 Default allow
    rules.append({
        "dpid": 1,
        "priority": 0,
        "match": {},
        "actions": [{"type": "OUTPUT", "port": "NORMAL"}]
    })

    return rules, app_to_ip  # also return mapping for reference


# -----------------------------
# Main
# -----------------------------
# if __name__ == "__main__":
#     yaml_file = os.path.join(INTENT_DIR, "policy_2025_08_09_120920.yaml")
#     rules, app_map = intents_to_rules(yaml_file, MAPPING_FILE)

#     print("Generated Rules:")
#     print(json.dumps(rules, indent=2))

#     print("\nApplication → Mininet IP mapping:")
#     print(json.dumps(app_map, indent=2))
