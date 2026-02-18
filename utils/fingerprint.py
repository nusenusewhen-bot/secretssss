import hashlib
import random
import base64
import json

def generate_x_fingerprint():
    data = {
        "canvas": hashlib.md5(str(random.random() + time.time()).encode()).hexdigest(),
        "hardwareConcurrency": random.choice([4, 8, 12, 16]),
        "deviceMemory": random.choice([4, 8, 16]),
        "timezone": random.choice(["Europe/Oslo", "Europe/Berlin", "America/New_York"]),
        "fonts": random.randint(20, 50)
    }
    return base64.urlsafe_b64encode(json.dumps(data, separators=(',', ':')).encode()).decode().rstrip("=")

def get_tls_session():
    from tls_client import Session
    return Session(client_identifier=random.choice(["chrome124", "chrome123", "chrome122"]))
