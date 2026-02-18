import hashlib
import random
import base64
import json
from datetime import datetime

def generate_canvas_hash():
    seed = str(random.random()) + str(datetime.now().timestamp())
    return hashlib.md5(seed.encode()).hexdigest()[:32]

def generate_webgl():
    vendors = ["Google Inc.", "Intel Inc.", "NVIDIA Corporation", "Apple Inc."]
    renderers = [
        "ANGLE (Intel, Intel(R) UHD Graphics 630, Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA, NVIDIA GeForce GTX 1650, Direct3D11 vs_5_0 ps_5_0)",
        "WebKit WebGL"
    ]
    return random.choice(vendors), random.choice(renderers)

def generate_x_fingerprint():
    data = {
        "canvas": generate_canvas_hash(),
        "webgl_vendor": generate_webgl()[0],
        "webgl_renderer": generate_webgl()[1],
        "hardwareConcurrency": random.choice([4, 8, 12, 16]),
        "deviceMemory": random.choice([4, 8, 16]),
        "timezone": random.choice(["Europe/Oslo", "Europe/Berlin", "America/New_York"]),
        "fonts": random.randint(25, 55)
    }
    return base64.urlsafe_b64encode(json.dumps(data, separators=(',', ':')).encode()).decode().rstrip("=")

def get_tls_session():
    from tls_client import Session
    return Session(client_identifier=random.choice(["chrome124", "chrome123", "chrome122", "edge122"]))
