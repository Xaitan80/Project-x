import os
from pathlib import Path
from common.feed_utils import (
    load_rss_urls,
    parse_feed,
    extract_service_name,
    classify_status
)

def get_status_dashboard(rss_urls, provider="AWS", region="eu-north-1"):
    dashboard = {provider: {region: {}}}

    for url in rss_urls:
        latest_status = parse_feed(url)
        service_name = extract_service_name(url)

        if latest_status:
            classification, emoji = classify_status(latest_status["title"], latest_status["summary"])
        else:
            # No data = treat as OK (green)
            classification, emoji = "OK", "🟢"
            latest_status = {
                "title": "No incidents reported",
                "summary": "All systems operational.",
                "published": "",
                "link": "#"
            }

        latest_status["classification"] = classification
        latest_status["emoji"] = emoji
        dashboard[provider][region][service_name] = latest_status

    return dashboard


def generate_html(dashboard, rss_urls_map, output_path):
    html = [
        "<html><head>",
        "<meta charset=UTF-8>",
        "<title>Service Status Dashboard</title>",
        "<style>",
        """
        body { font-family: Arial, sans-serif; background: #f9f9f9; padding: 20px; }
        .service-card { background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; padding: 15px; }
        .service-card h2 { margin-top: 0; }
        a.rss-link { text-decoration: none; font-weight: bold; color: #ff6600; }
        a.rss-link:hover { text-decoration: underline; }
        """,
        "</style>",
        "</head><body>",
        "<h1>🟢 RSS FEEDS AWS ZONE EUROPE</h1>",
        "<div class='services'>"
    ]

    for provider, regions in dashboard.items():
        for region, services in regions.items():
            for service, status in services.items():
                title = status.get("title", "No data")
                summary = status.get("summary", "")
                emoji = status.get("emoji", "❓")

                # Get the feed URL from map, fallback to '#'
                feed_url = rss_urls_map.get(service, "#")

                html.append(f"""
                <div class='service-card'>
                    <h2>{emoji} {service}</h2>
                    <p><strong>{title}</strong></p>
                    <p>{summary}</p>
                    <a href="{feed_url}" target="_blank" rel="noopener noreferrer" class="rss-link">📡 View on Provider</a>
                </div>
                """)

    html.append("</div></body></html>")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n".join(html), encoding="utf-8")


if __name__ == "__main__":
    rss_file = os.path.join("input", "rss-eu-north-1.txt")
    rss_urls = load_rss_urls(rss_file)

    # Build mapping service_name -> feed URL
    rss_urls_map = {}
    for url in rss_urls:
        service_name = extract_service_name(url)
        rss_urls_map[service_name] = url

    print("Loaded RSS URLs:")
    for url in rss_urls:
        print(" -", url)

    dashboard = get_status_dashboard(rss_urls)
    output_file = os.path.join("dashboards", "services-status.html")
    generate_html(dashboard, rss_urls_map, output_file)
    print(f"Status dashboard generated at: {output_file}")
