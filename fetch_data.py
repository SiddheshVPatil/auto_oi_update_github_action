import requests
import json
import time

URL = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_data():
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)
    res = session.get(URL, headers=headers)
    data = res.json()

    total_call_oi = 0
    total_put_oi = 0

    for item in data["records"]["data"]:
        if "CE" in item and "PE" in item:
            total_call_oi += item["CE"]["openInterest"]
            total_put_oi += item["PE"]["openInterest"]

    return {
        "time": time.strftime("%H:%M"),
        "call_oi": total_call_oi,
        "put_oi": total_put_oi
    }


# Load old data
try:
    with open("data.json", "r") as f:
        store = json.load(f)
except:
    store = []

# Append new data
new_data = fetch_data()
store.append(new_data)

# Keep last 50 points
store = store[-50:]

# Save
with open("data.json", "w") as f:
    json.dump(store, f)
