import requests
import json
import time
import random
from .captcha import CaptchaSolver
from .fingerprint import generate_x_fingerprint
from .proxy import ProxyManager

class DiscordAPI:
    def __init__(self, config):
        self.config = config
        self.solver = CaptchaSolver(config["captcha"]["api_key"])
        self.proxy_mgr = ProxyManager(config["proxies_file"]) if config["use_proxies"] else None
        self.headers_base = {
            "User-Agent": config["user_agent_template"],
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/register"
        }

    def _get_headers(self, extra=None):
        h = self.headers_base.copy()
        h["X-Fingerprint"] = generate_x_fingerprint()
        h["X-Super-Properties"] = self._get_super_properties()  # implement below
        if extra:
            h.update(extra)
        return h

    def _get_super_properties(self):
        # minimal working in Feb 2026 — update build_number dynamically if possible
        build_number = 999999  # placeholder — scrape from https://discord.com/assets/index-*.js
        props = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": self.config["user_agent_template"],
            "browser_version": "128.0",
            "os_version": "10",
            "referrer": "https://discord.com",
            "client_build_number": build_number,
            "release_channel": "stable",
            "client_event_source": None
        }
        return base64.b64encode(json.dumps(props).encode()).decode()

    def register(self):
        proxy = self.proxy_mgr.get_proxy() if self.proxy_mgr else None
        prox_dict = proxy if proxy else None

        fp = generate_x_fingerprint()
        sitekey = "4c672d35-0701-42b2-88c3-78380b0db560"  # current discord hcaptcha — verify on page
        captcha_key = self.solver.solve_hcaptcha(sitekey, "https://discord.com/register", proxy=proxy)

        if not captcha_key:
            return None, "captcha failed"

        username = f"user{random.randint(10000,999999)}"
        email = self._get_email()  # implement in email.py
        if not email:
            return None, "no email"

        payload = {
            "fingerprint": fp,
            "email": email,
            "username": username,
            "password": self.config["password"],
            "invite": None,
            "consent": True,
            "date_of_birth": self.config["dob"],
            "captcha_key": captcha_key
        }

        try:
            r = requests.post(
                f"{self.config['discord_base_url']}/auth/register",
                json=payload,
                headers=self._get_headers(),
                proxies=prox_dict,
                timeout=15
            )
            data = r.json()
            if r.status_code == 201 and "token" in data:
                token = data["token"]
                return token, None
            else:
                return None, f"register fail {r.status_code} {data}"
        except Exception as e:
            return None, str(e)

    def _get_email(self):
        # placeholder — call your email.py function
        return "tempuser123@gmx.com"  # replace with real logic
