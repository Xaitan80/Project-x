import requests
import re

def get_current_build_id():
    MAIN_PAGE = "https://www.bredband2.com/privat/kundservice/driftinformation"
    r = requests.get(MAIN_PAGE)
    r.raise_for_status()
    match = re.search(r'/_next/data/([^/]+)/privat/kundservice/driftinformation.json', r.text)
    if match:
        return match.group(1)
    else:
        return None

def test_fetch_drift_list(build_id):
    url = f"https://www.bredband2.com/_next/data/{build_id}/privat/kundservice/driftinformation.json"
    print(f"Fetching overview JSON from:\n{url}\n")
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    print("Top-level keys:", list(data.keys()))
    page_props = data.get("pageProps")
    print("pageProps keys:", list(page_props.keys()) if page_props else "None")
    drift_list = page_props.get("driftList") if page_props else None
    print("driftList type:", type(drift_list))
    print("driftList length:", len(drift_list) if drift_list else "None")
    if drift_list:
        print("Sample entry:", drift_list[0])

if __name__ == "__main__":
    build_id = get_current_build_id()
    if build_id:
        print("Current build ID found:", build_id)
        test_fetch_drift_list(build_id)
    else:
        print("Could not find build ID!")
