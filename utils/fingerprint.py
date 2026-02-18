import hashlib
import random
import base64
import json

def generate_simple_fingerprint():
    seed = str(random.random()) + str(time.time())
    canvas = hashlib.md5(seed.encode()).hexdigest()
    return {
        "canvas": canvas,
        "hardwareConcurrency": random.choice([4, 8, 12]),
        "deviceMemory": random.choice([4, 8]),
        "timezone": random.choice(["Europe/Oslo", "Europe/Berlin", "America/Los_Angeles"])
    }

def generate_x_fingerprint():
    data = generate_simple_fingerprint()
    return base64.urlsafe_b64encode(json.dumps(data, separators=(',', ':')).encode()).decode().rstrip("=")
