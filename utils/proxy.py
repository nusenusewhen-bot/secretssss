import random

class ProxyManager:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.proxies = [l.strip() for l in f if l.strip() and not l.startswith('#')]

    def get_proxy(self):
        if not self.proxies:
            return None
        raw = random.choice(self.proxies)
        if raw.startswith(('http://', 'https://', 'socks')):
            return {"http": raw, "https": raw}
        parts = raw.split(':')
        if len(parts) == 4:
            p = f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
            return {"http": p, "https": p}
        return None

    def get_proxy_str(self):
        p = self.get_proxy()
        return p["http"] if p else None
