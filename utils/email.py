import requests
import time
import re

def create_temp_email():
    try:
        r = requests.get("https://api.tempmail.lol/generate").json()
        if r.get("success"):
            return r["address"], r["token"]
    except:
        pass
    return None, None

def poll_for_verification(token, timeout=90):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"https://api.tempmail.lol/check?token={token}").json()
            for email in r.get("emails", []):
                if "discord" in email.get("from", "").lower():
                    match = re.search(r'https://discord\.com/verify\?token=[^"\s&]+', email.get("body", ""))
                    if match:
                        return match.group(0)
        except:
            pass
        time.sleep(6)
    return None
