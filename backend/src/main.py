# file: intent_based_windows.py

import requests
import json
import time

def install_rules():
    rules = [
        # ✅ Allow ARP (so hosts can resolve MAC addresses)
        {
            "dpid": 1,
            "priority": 300,
            "match": {"eth_type": 2054},  # ARP
            "actions": [{"type": "OUTPUT", "port": "ALL"}]
        },
        # ❌ Drop all IPv4 packets going to h2 (10.0.0.2)
        {
            "dpid": 1,
            "priority": 200,
            "match": {"eth_type": 2048, "ipv4_dst": "10.0.0.2"},
            "actions": []  # drop
        },
        # ✅ Allow IPv4 packets going to h3 (10.0.0.3)
        {
            "dpid": 1,
            "priority": 150,
            "match": {"eth_type": 2048, "ipv4_dst": "10.0.0.3"},
            "actions": [{"type": "OUTPUT", "port": "NORMAL"}]
        },
        # 🌐 Default rule: forward everything else normally
        {
            "dpid": 1,
            "priority": 0,
            "match": {},
            "actions": [{"type": "OUTPUT", "port": "NORMAL"}]
        }
    ]

    controller_url = "http://127.0.0.1:8080/stats/flowentry/add"

    for rule in rules:
        try:    
            res = requests.post(controller_url, data=json.dumps(rule))
            print(f"Sent rule {rule['match']} -> {res.status_code}")
        except Exception as e:
            print(f"Cannot send rule {rule['match']}: {e}")

    # Verify rules
    try:
        res = requests.get("http://127.0.0.1:8080/stats/flow/1")
        print("\nInstalled flows on switch 1:")
        print(json.dumps(res.json(), indent=2))
    except Exception as e:
        print("Cannot fetch installed flows:", e)


if __name__ == "__main__":
    print("\n=== Installing OpenFlow rules ===")
    time.sleep(2)

    # ✅ Clear old flows first
    try:
        requests.delete("http://127.0.0.1:8080/stats/flowentry/clear/1")
        print("Cleared old flows.")
    except Exception as e:
        print("Cannot clear flows:", e)

    install_rules()
    print("\n=== Now test in Mininet ===")
    print("  h1 ping -c 2 h2   # should FAIL (blocked)")
    print("  h1 ping -c 2 h3   # should SUCCEED (allowed)")
    print("  h1 ping -c 2 hX   # other hosts still work normally")
