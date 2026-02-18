import requests
import random
import base64
from pathlib import Path

def humanize_account(token, proxy_dict=None):
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }

    # Username
    prefixes = ["x", "", "i", ""]
    names = ["Nova", "Zoe", "Kai", "Luna", "Jax", "Aria"]
    username = random.choice(prefixes) + random.choice(names) + str(random.randint(0, 99))
    try:
        requests.patch("https://discord.com/api/v9/users/@me", headers=headers, json={"username": username}, proxies=proxy_dict)
    except:
        pass

    # Avatar
    pfps = list(Path("data/pfps").glob("*.[jp][pn]g"))
    if pfps:
        try:
            img_path = random.choice(pfps)
            with open(img_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            requests.patch("https://discord.com/api/v9/users/@me", headers=headers,
                           json={"avatar": f"data:image/jpeg;base64,{img_b64}"}, proxies=proxy_dict)
        except:
            pass

    # Bio
    bios = []
    try:
        with open("data/bios.txt", "r", encoding="utf-8") as f:
            bios = [line.strip() for line in f if line.strip()]
    except:
        pass
    if bios:
        try:
            bio = random.choice(bios)
            requests.patch("https://discord.com/api/v9/users/@me/profile", headers=headers,
                           json={"bio": bio}, proxies=proxy_dict)
        except:
            pass

    time.sleep(random.uniform(4, 12))
