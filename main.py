import asyncio
from utils import proxy, captcha, email, humanizer, discord_api

async def create_one():
    prox = proxy.get_proxy()
    fp = discord_api.generate_fp()
    captcha_key = captcha.solve(sitekey="your_hcaptcha_sitekey")
    email_addr = email.get_temp_email()
    # build payload
    payload = {"fingerprint": fp, "email": email_addr, ...}
    resp = requests.post("https://discord.com/api/v9/auth/register", json=payload, proxies=prox)
    if "token" in resp.json():
        token = resp.json()["token"]
        # humanize immediately
        if config["humanize"]:
            humanizer.do_humanize(token, prox)
        save_token(token)

async def main():
    tasks = [create_one() for _ in range(config["threads"])]
    await asyncio.gather(*tasks)

asyncio.run(main())
