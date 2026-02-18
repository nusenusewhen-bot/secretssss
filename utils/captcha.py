import requests
import time
import json

class CaptchaSolver:
    def __init__(self, api_key="44b5a90f-182f-4c67-b219-ef8dfd33d7a1"):
        self.api_key = api_key
        self.base_url = "https://api.razorcap.cc"

    def create_task(self, task_type, params):
        payload = {
            "clientKey": self.api_key,
            "task": {
                "type": task_type,
                **params
            }
        }
        try:
            resp = requests.post(f"{self.base_url}/createTask", json=payload, timeout=12).json()
            if resp.get("errorId") == 0:
                return resp.get("taskId")
            else:
                print(f"RazorCap create error: {resp}")
                return None
        except Exception as e:
            print(f"RazorCap request failed: {e}")
            return None

    def get_result(self, task_id, max_polls=40, poll_delay=5):
        for _ in range(max_polls):
            try:
                r = requests.post(
                    f"{self.base_url}/getTaskResult",
                    json={"clientKey": self.api_key, "taskId": task_id},
                    timeout=10
                ).json()
                
                status = r.get("status")
                if status == "ready":
                    return r.get("solution")
                elif status == "processing":
                    time.sleep(poll_delay)
                    continue
                else:
                    print(f"RazorCap status: {status} - {r}")
                    return None
            except Exception as e:
                print(f"Poll error: {e}")
                time.sleep(poll_delay)
        print("RazorCap timeout")
        return None

    def solve_hcaptcha(self, site_key, page_url, invisible=False, data=None, proxy=None):
        params = {
            "websiteURL": page_url,
            "websiteKey": site_key,
            "isInvisible": invisible,
        }
        if data:  # for enterprise / custom data
            params["enterprisePayload"] = data
        
        # optional proxy support (RazorCap allows passing proxy per task)
        if proxy:
            # format: http://user:pass@ip:port or socks5://...
            params["proxy"] = proxy  # RazorCap supports this field

        task_id = self.create_task("HCaptchaTaskProxyless", params)  # or "HCaptchaTask" if using your own proxy
        if not task_id:
            return None

        solution = self.get_result(task_id)
        if solution:
            return solution.get("gRecaptchaResponse") or solution.get("code")
        return None

    def get_balance(self):
        try:
            r = requests.post(f"{self.base_url}/getBalance", json={"clientKey": self.api_key}).json()
            return r.get("balance", 0)
        except:
            return 0
