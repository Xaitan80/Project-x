import requests
from bs4 import BeautifulSoup

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

def generate_markdown_and_html(status_list):
    markdown = "\n\n".join(status_list)
    html = f"""<!DOCTYPE html>
<html>
<head><title>Status Dashboard</title></head>
<body>
<pre>{markdown}</pre>
</body>
</html>"""
    with open("status.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Dashboard updated: status.html")

if __name__ == "__main__":
    status = fetch_bredband2_incidents()
    generate_markdown_and_html([status])
