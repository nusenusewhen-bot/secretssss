import requests
import time

class RazorCap:
    def __init__(self, api_key, base_url):
        self.key = api_key
        self.base = base_url

    def create_task(self, params):
        payload = {"clientKey": self.key, "task": params}
        try:
            r = requests.post(f"{self.base}/createTask", json=payload, timeout=12).json()
            if r.get("errorId") == 0:
                return r["taskId"]
        except Exception as e:
            print("Create error:", e)
        return None

    def get_result(self, task_id):
        for _ in range(60):
            try:
                r = requests.post(f"{self.base}/getTaskResult", json={
                    "clientKey": self.key,
                    "taskId": task_id
                }, timeout=10).json()
                if r.get("status") == "ready":
                    return r["solution"]
                if r.get("status") in ["failed", "timeout"]:
                    print("Solve failed:", r)
                    return None
            except:
                pass
            time.sleep(4.5)
        print("Timeout")
        return None

    def solve_hcaptcha(self, site_key, url, proxy_str=None):
        params = {
            "type": "HCaptchaTaskProxyless",
            "websiteURL": url,
            "websiteKey": site_key,
            "isInvisible": False
        }
        if proxy_str:
            params["type"] = "HCaptchaTask"
            params["proxy"] = proxy_str

        task_id = self.create_task(params)
        if not task_id:
            return None

        sol = self.get_result(task_id)
        return sol.get("gRecaptchaResponse") if sol else None
