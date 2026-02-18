import requests
import time

class CaptchaSolver:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base = "https://api.razorcap.cc"

    def create_task(self, task_type, params):
        payload = {"clientKey": self.api_key, "task": {"type": task_type, **params}}
        try:
            r = requests.post(f"{self.base}/createTask", json=payload, timeout=10).json()
            if r.get("errorId") == 0:
                return r["taskId"]
        except:
            pass
        return None

    def get_result(self, task_id):
        for _ in range(45):
            try:
                r = requests.post(f"{self.base}/getTaskResult", json={
                    "clientKey": self.api_key, "taskId": task_id
                }, timeout=10).json()
                if r.get("status") == "ready":
                    return r["solution"]
                if r.get("status") != "processing":
                    return None
            except:
                pass
            time.sleep(4.5)
        return None

    def solve_hcaptcha(self, site_key, url, proxy=None):
        params = {
            "websiteURL": url,
            "websiteKey": site_key,
            "isInvisible": False
        }
        if proxy:
            params["proxy"] = proxy.get("http") if proxy else None

        task_id = self.create_task("HCaptchaTaskProxyless", params)
        if not task_id:
            return None

        sol = self.get_result(task_id)
        return sol.get("gRecaptchaResponse") if sol else None
