import random

class ProxyManager:
    def __init__(self, file_path="data/proxies.txt"):
        with open(file_path, "r") as f:
            lines = [l.strip() for l in f if l.strip()]
        self.proxies = []
        for line in lines:
            if "http" in line or "socks" in line:
                self.proxies.append(line)
            else:  # ip:port:user:pass format
                parts = line.split(":")
                if len(parts) == 4:
                    self.proxies.append(f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}")

    def get_proxy(self):
        if not self.proxies:
            return None
        p = random.choice(self.proxies)
        return {"http": p, "https": p}

    def test_proxy(self, proxy, timeout=8):
        try:
            import requests
            r = requests.get("https://discord.com", proxies={"http": proxy, "https": proxy}, timeout=timeout)
            return r.status_code == 200
        except:
            return False
