import time, urllib.request, json, urllib.error

time.sleep(2)
url = "http://127.0.0.1:8001/api/auth/login"
payload = json.dumps({"email": "admin@ecosphere.org", "password": "Admin@123456"}).encode()
req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
try:
    with urllib.request.urlopen(req, timeout=5) as r:
        resp = json.loads(r.read())
        print("Keys:", list(resp.keys()))
        user_val = resp.get("user")
        print("user type:", type(user_val))
        print("user value:", repr(user_val)[:300])
        print("token:", str(resp.get("access_token", ""))[:40])
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code, e.read().decode())
except Exception as e:
    print("Error:", type(e).__name__, e)
