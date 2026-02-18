import requests
import re
import base64
import json

def get_current_build_number_and_super_props(proxy=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
        r = requests.get("https://discord.com/login", headers=headers, proxies=proxy, timeout=10)
        if r.status_code != 200:
            r = requests.get("https://discord.com/assets/index-*.js", allow_redirects=True)  # fallback

        # extract build number - most reliable patterns right now
        build_match = re.search(r'"build_number"\s*:\s*(\d+)', r.text) or \
                      re.search(r'build_number\D*?(\d{6,8})', r.text)
        
        build_number = int(build_match.group(1)) if build_match else 999999  # fallback safe-ish value

        # construct minimal X-Super-Properties that passes in 2026
        super_props = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": headers["User-Agent"],
            "browser_version": "128.0",
            "os_version": "10",
            "referrer": "https://discord.com",
            "client_build_number": build_number,
            "release_channel": "stable",
            "client_event_source": None,
            "client_version": f"1.0.{build_number // 1000}",
        }
        x_super = base64.b64encode(json.dumps(super_props, separators=(',', ':')).encode()).decode()
        
        return build_number, x_super
    except Exception as e:
        print(f"Scraper failed: {e}")
        return 999999, "eyJvc0ZhbGxiYWNrIjoib3NfZmFsbGJhY2sifQ=="  # garbage fallback
