#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def fetch_telia_status():
    url = "https://www.telia.se/privat/driftinformation"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Simple example: grab page title or some known class
    status_summary = soup.find("h1")  # placeholder
    if status_summary:
        return f"Telia: {status_summary.text.strip()}"
    return "Telia: Unable to fetch status"

def fetch_telenor_status():
    url = "https://www.telenor.se/kundservice/driftinformation/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # You’ll need to inspect the HTML structure to improve this
    issues = soup.find_all("li")  # placeholder
    return f"Telenor: Found {len(issues)} items on status page"

def generate_markdown(statuses):
    with open("dashboard.md", "w", encoding="utf-8") as f:
        f.write("# 🇸🇪 ISP Status Dashboard\n\n")
        f.write("_Last updated manually_\n\n")
        for status in statuses:
            f.write(f"## {status}\n\n")

if __name__ == "__main__":
    statuses = [
        fetch_telia_status(),
        fetch_telenor_status()
        # Add more ISPs here
    ]
    generate_markdown(statuses)
    print("✅ Dashboard generated as `dashboard.md`")
