import asyncio
import json
import random
import requests
from utils.proxy import ProxyManager
from utils.captcha import RazorCap
from utils.fingerprint import generate_x_fingerprint
from utils.humanizer import humanize

with open("config.json") as f:
    config = json.load(f)

proxy_mgr = ProxyManager(config["proxies_file"])
captcha = RazorCap(config["captcha"]["api_key"], config["captcha"]["base_url"])

async def create():
    proxy_dict = proxy_mgr.get_proxy()
    proxy_str = proxy_mgr.get_proxy_str()

    fp = generate_x_fingerprint()

    # REPLACE WITH REAL EMAIL LOGIC (tempmail.lol, catch-all, outlook bulk, etc.)
    email = f"test{random.randint(1000000,9999999)}@example.com"

    captcha_key = captcha.solve_hcaptcha(
        "4c672d35-0701-42b2-88c3-78380b0db560",
        "https://discord.com/register",
        proxy_str
    )

    if not captcha_key:
        print("Captcha failed")
        return

    payload = {
        "fingerprint": fp,
        "email": email,
        "username": f"user{random.randint(100000,999999)}",
        "password": config["password"],
        "consent": True,
        "date_of_birth": config["dob"],
        "captcha_key": captcha_key
    }

    headers = {
        "User-Agent": config["user_agent"],
        "X-Fingerprint": fp,
        "X-Super-Properties": "eyJvc0ZhbGxiYWNrIjoib3NfZmFsbGJhY2sifQ=="  # REPLACE WITH REAL SCRAPED VALUE
    }

    try:
        r = requests.post(
            "https://discord.com/api/v9/auth/register",
            json=payload,
            headers=headers,
            proxies=proxy_dict,
            timeout=20
        )
        data = r.json()
        token = data.get("token")
        if token:
            print(f"[+] {token}")
            with open(config["output_file"], "a") as f:
                f.write(token + "\n")
            humanize(token, proxy_dict, config)
        else:
            print("[-]", data.get("message", r.text))
    except Exception as e:
        print("Error:", e)

    await asyncio.sleep(random.uniform(config["min_delay"], config["max_delay"]))

async def main():
    while True:
        tasks = [create() for _ in range(config["threads"])]
        await asyncio.gather(*tasks)

asyncio.run(main())
