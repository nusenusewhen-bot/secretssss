import requests
import random
import base64
from pathlib import Path

def humanize(token, proxy=None, config=None):
    if not config["humanize"]:
        return

    headers = {
        "Authorization": token,
        "User-Agent": config["user_agent"],
        "Content-Type": "application/json"
    }

    # Username
    name = random.choice(["Kai", "Luna", "Zoe", "Jax", "Aria"]) + str(random.randint(0, 99))
    requests.patch("https://discord.com/api/v9/users/@me", headers=headers, json={"username": name}, proxies=proxy)

    # PFP
    pfps = list(Path(config["pfp_folder"]).glob("*.[jp][pn]g"))
    if pfps:
        p = random.choice(pfps)
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        requests.patch("https://discord.com/api/v9/users/@me", headers=headers,
                       json={"avatar": f"data:image/jpeg;base64,{b64}"}, proxies=proxy)

    # Bio
    try:
        bios = open(config["bios_file"]).read().splitlines()
        if bios:
            bio = random.choice(bios)
            requests.patch("https://discord.com/api/v9/users/@me/profile", headers=headers,
                           json={"bio": bio}, proxies=proxy)
    except:
        pass

    time.sleep(random.uniform(5, 15))
