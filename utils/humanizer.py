import requests
import random
import base64
from pathlib import Path

def humanize(token, proxy=None, config=None):
    if not config["humanize"]:
        return

    headers = {
        "Authorization": token,
        "User-Agent": config.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0"),
        "Content-Type": "application/json"
    }
    prox = proxy

    # username
    prefixes = ["xX", "", "i", "The", "Real"]
    names = ["Nova", "Zephyr", "Kai", "Luna", "Jax", "Aria"]
    new_name = random.choice(prefixes) + random.choice(names) + str(random.randint(0, 99))
    requests.patch("https://discord.com/api/v9/users/@me", headers=headers, json={"username": new_name}, proxies=prox)

    # avatar
    pfps = list(Path(config["pfp_folder"]).glob("*.[jp][pn]g"))
    if pfps:
        p = random.choice(pfps)
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        requests.patch("https://discord.com/api/v9/users/@me", headers=headers,
                       json={"avatar": f"data:image/jpeg;base64,{b64}"}, proxies=prox)

    # bio
    bios = open(config["bios_file"]).read().splitlines()
    if bios:
        bio = random.choice(bios)
        requests.patch("https://discord.com/api/v9/users/@me/profile", headers=headers,
                       json={"bio": bio}, proxies=prox)

    time.sleep(random.uniform(4, 12))
