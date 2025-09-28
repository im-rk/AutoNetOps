# file: rules_installer.py

import requests
import json
import time
import os
import sys

# -----------------------------
# Import rule generator
# -----------------------------
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from translator.rule import intents_to_rules   # adjust path if needed

# Paths for YAML intents + mappings



# -----------------------------
# Install rules into controller
# -----------------------------
def install_rules(rules):
    controller_url = "http://127.0.0.1:8080/stats/flowentry/add"

    for rule in rules:
        try:
            res = requests.post(controller_url, data=json.dumps(rule))
            print(f"✅ Sent rule {rule['match']} -> {res.status_code}")
        except Exception as e:
            print(f"❌ Cannot send rule {rule['match']}: {e}")

    # Verify rules
    try:
        res = requests.get("http://127.0.0.1:8080/stats/flow/1")
        print("\n📋 Installed flows on switch 1:")
        print(json.dumps(res.json(), indent=2))
    except Exception as e:
        print("⚠️ Cannot fetch installed flows:", e)


# -----------------------------
# Main
# -----------------------------
def run_installer(policy_file=None):
    MAPPING_FILE = os.path.join(SRC_DIR, "mappings", "app_mappings.json")

    BASE_DIR = os.path.dirname(SRC_DIR)
    INTENT_DIR = os.path.join(BASE_DIR, "data", "policy")
    policy_file = os.path.join(INTENT_DIR, policy_file)

    print("\n=== Generating and Installing OpenFlow rules from intents ===")
    time.sleep(1)

    try:
        requests.delete("http://127.0.0.1:8080/stats/flowentry/clear/1")
        print("🧹 Cleared old flows.")
    except Exception as e:
        print("⚠️ Cannot clear flows:", e)

    rules, app_to_ip = intents_to_rules(policy_file, MAPPING_FILE)

    print("\nGenerated Rules:")
    print(json.dumps(rules, indent=2))

    print("\nApplication → Mininet IP mapping:")
    print(json.dumps(app_to_ip, indent=2))

    install_rules(rules)

    print("\n=== Now test in Mininet ===")
    print("  h1 ping -c 2 h2   # should FAIL (if deny rule applied)")
    print("  h1 ping -c 2 h3   # should SUCCEED (if allow rule applied)")
    print("  h1 ping -c 2 hX   # other hosts follow default rule")

