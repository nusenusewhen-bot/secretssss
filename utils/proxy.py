import random

class ProxyManager:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        self.proxies = []
        for line in lines:
            if line.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
                self.proxies.append(line)
            else:
                parts = line.split(':')
                if len(parts) == 4:
                    self.proxies.append(f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}")

    def get_proxy(self):
        if not self.proxies:
            return None
        p = random.choice(self.proxies)
        return {"http": p, "https": p}

    def get_proxy_str(self):
        p = self.get_proxy()
        return p["http"] if p else None
