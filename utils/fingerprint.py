import hashlib
import random
import base64
import json
from datetime import datetime

def generate_canvas_hash():
    # fake canvas fingerprint (different every time but realistic)
    seed = str(random.random()) + str(datetime.now().timestamp())
    return hashlib.md5(seed.encode()).hexdigest()[:32]

def generate_webgl_vendor():
    vendors = ["Google Inc.", "Intel Inc.", "NVIDIA Corporation", "Apple Inc.", "AMD"]
    renderers = ["ANGLE (Intel, Intel(R) UHD Graphics, Direct3D11 vs_5_0 ps_5_0)", 
                 "WebKit WebGL", "Mozilla", "Google SwiftShader"]
    return random.choice(vendors), random.choice(renderers)

def generate_hardware():
    return {
        "hardwareConcurrency": random.choice([2, 4, 8, 12, 16]),
        "deviceMemory": random.choice([4, 8, 16]),
        "screen": {
            "width": random.choice([1920, 1366, 1440, 1536, 2560]),
            "height": random.choice([1080, 768, 900, 864, 1440]),
            "availWidth": 0, "availHeight": 0  # filled later
        }
    }

def generate_x_fingerprint():
    # simplified — real ones pull from creepjs-style values
    data = {
        "canvas": generate_canvas_hash(),
        "webgl": generate_webgl_vendor(),
        "hardware": generate_hardware(),
        "timezone": random.choice(["Europe/Oslo", "Europe/Berlin", "America/New_York"]),
        "fonts": len(["Arial", "Times New Roman", "Comic Sans MS"]) + random.randint(10, 40)
    }
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip("=")

def get_tls_client_hello():
    # use tls-client library with chrome impersonate
    # pip install tls-client
    from tls_client import Session
    session = Session(client_identifier="chrome124")  # or chrome122, edge120 etc.
    return session  # return the session object for requests
