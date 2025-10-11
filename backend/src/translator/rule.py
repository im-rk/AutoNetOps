
import sys
import os
import json
import requests
import time
from datetime import datetime

from utils.util import load_policies

# Helpers
def assign_mininet_ips(intents, base="10.0.0."):
    """Assigns sequential Mininet IPs (10.0.0.x) to applications in intents."""
    app_to_ip = {}
    for i, intent in enumerate(intents, start=2):
        app = intent.get("application")
        if app and app not in app_to_ip:
            app_to_ip[app] = f"{base}{i}"
    return app_to_ip





def remaining_seconds(intent):
    """Return remaining seconds until end of intent's time window or duration."""
    try:
        cond = intent.get("condition", {})

        # 1: duration in seconds
        duration = cond.get("duration")
        if duration:
            return max(int(duration), 0)

        # 2: time_range with start_time and end_time
        time_range = cond.get("time_range")
        if time_range:
            start_str = time_range.get("start_time")
            end_str = time_range.get("end_time")
            if start_str and end_str:
                now = datetime.now()
                start_h, start_m = map(int, start_str.split(":"))
                end_h, end_m = map(int, end_str.split(":"))
                start_time = now.replace(hour=start_h, minute=start_m, second=0, microsecond=0)
                end_time = now.replace(hour=end_h, minute=end_m, second=0, microsecond=0)
                if now < start_time:
                    wait_sec = (start_time - now).total_seconds()
                    print(f"Waiting {wait_sec} seconds until intent start...")
                    time.sleep(wait_sec)  
                    delta = (end_time - start_time).total_seconds()
                else:
                    delta = (end_time - now).total_seconds()
                return max(int(delta), 0)

        # Default: no timeout
        return 0

    except Exception as e:
        print(f"Error calculating remaining seconds in intent {intent}: {e}")
        return 0



# Intents → OpenFlow rules
def intents_to_rules(yaml_file):
    rules = []

    # Always allow ARP
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

    # Assign synthetic Mininet IPs
    app_to_ip = assign_mininet_ips(intents)

    for intent in intents:
        # if not intent_in_time(intent):
        #     continue  # Skip this intent outside its time range

        app = intent.get("application")
        action = intent.get("action")

        if not app or not action:
            continue

        ip = app_to_ip.get(app)
        if not ip:
            continue

        # Compute hard_timeout so rules auto-delete after intent end_time
        timeout = remaining_seconds(intent)

        if action.lower() == "deny" or action.lower()=="block":
            rules.append({
                "dpid": 1,
                "priority": 200,
                "match": {"eth_type": 2048, "ipv4_dst": ip},
                "actions": [],  # drop
                "hard_timeout": timeout   
            })
        elif action.lower() == "prioritize":
            rules.append({
                "dpid": 1,
                "priority": 250,
                "match": {"eth_type": 2048, "ipv4_dst": ip},
                "actions": [{"type": "OUTPUT", "port": "NORMAL"}],
                "hard_timeout": timeout  
            })

    # Default allow
    rules.append({
        "dpid": 1,
        "priority": 0,
        "match": {},
        "actions": [{"type": "OUTPUT", "port": "NORMAL"}]
    })

    return rules, app_to_ip
