#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import datetime

def fetch_bredband2_incidents():
    url = "https://www.bredband2.com/privat/kundservice/driftinformation"
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # Adjust this selector if needed
    incidents = []
    for div in soup.select("div.drift-card__text"):
        text = div.get_text(strip=True)
        if text:
            incidents.append(text)

    if incidents:
        return "Bredband2 Incidents:\n" + "\n".join(f"- {inc}" for inc in incidents)
    else:
        return "Bredband2: No incidents found"

def fetch_bredband2_incidents_js():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.bredband2.com/privat/kundservice/driftinformation")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "entry-content"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    incidents = []
    danger_classes = [
        "alert-bar--status-danger",
        "alert-notification--status-danger",
        "tag__status--danger",
        "ticket-record__status--danger",
        "u-color-danger"
    ]
    for class_name in danger_classes:
        for el in soup.find_all(class_=class_name):
            text = el.get_text(strip=True)
            if text:
                incidents.append(text)
    if incidents:
        return "Bredband2 Incidents:\n" + "\n".join(f"- {inc}" for inc in incidents)
    else:
        return "Bredband2: No incidents found"

def generate_markdown_and_html(status_list):
    markdown = "\n\n".join(status_list)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""<!DOCTYPE html>
<html>
<head><title>Status Dashboard</title></head>
<body>
<pre>{markdown}</pre>
<p><em>Last updated: {timestamp}</em></p>
</body>
</html>"""
    with open("status.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Dashboard updated: status.html")

if __name__ == "__main__":
    status = fetch_bredband2_incidents_js()
    generate_markdown_and_html([status])
