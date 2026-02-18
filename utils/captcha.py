import requests
import time

class RazorCapSolver:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def create_task(self, task_type, params):
        payload = {
            "clientKey": self.api_key,
            "task": {"type": task_type, **params}
        }
        try:
            resp = requests.post(f"{self.base_url}/createTask", json=payload, timeout=12).json()
            if resp.get("errorId") == 0:
                return resp["taskId"]
        except:
            pass
        return None

    def get_result(self, task_id):
        for _ in range(60):
            try:
                r = requests.post(f"{self.base_url}/getTaskResult", json={
                    "clientKey": self.api_key,
                    "taskId": task_id
                }, timeout=10).json()
                if r.get("status") == "ready":
                    return r["solution"]
                if r.get("status") != "processing":
                    break
            except:
                pass
            time.sleep(4)
        return None

    def solve_hcaptcha(self, site_key, page_url, proxy_str=None):
        params = {
            "websiteURL": page_url,
            "websiteKey": site_key,
            "isInvisible": False
        }
        if proxy_str:
            params["proxy"] = proxy_str

        task_id = self.create_task("HCaptchaTaskProxyless", params)
        if not task_id:
            return None

        solution = self.get_result(task_id)
        return solution.get("gRecaptchaResponse") if solution else None
