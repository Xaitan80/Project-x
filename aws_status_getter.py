from common.feed_utils import (
    load_rss_urls,
    parse_feed,
    extract_service_name,
    classify_status
)
from gcp_status_europe_north2 import collect_gcp_dashboard
from pathlib import Path
from datetime import datetime, timezone

def generate_landing_html(region_statuses, output_path):
    html = [
        "<html><head>",
        '<meta charset="UTF-8">',
        "<title>Cloud Service Dashboard</title>",
        "<style>",
        """
        body { font-family: Arial, sans-serif; padding: 20px; background: #f2f2f2; }
        .region-card { background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .region-card h2 { margin: 0; display: inline; }
        .status-icon { font-size: 24px; margin-right: 10px; vertical-align: middle; }
        a { text-decoration: none; color: #0077cc; font-size: 18px; }
        a:hover { text-decoration: underline; }
        """,
        "</style>",
        "</head><body>",
        "<h1>🌍 Cloud Services Health Overview</h1>"
    ]

    for region, status in region_statuses.items():
        emoji = "🟢" if status == "healthy" else "🔴"
        html.append("<div class='region-card'>")
        html.append(f"<span class='status-icon'>{emoji}</span><a href='{region}.html'><h2>{region}</h2></a>")
        html.append("</div>")

    html.append("</body></html>")
    Path(output_path).write_text("\n".join(html), encoding="utf-8")


def generate_region_html(region, dashboard, output_path):
    html = [
        "<html><head>",
        '<meta charset="UTF-8">',
        f"<title>{region} - Service Status</title>",
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
        f"<h1>📍 Status for {region}</h1>",
        f"<p><em>Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</em></p>",
        "<div class='services'>"
    ]

    for service_data in dashboard:
        emoji = service_data['emoji']
        name = service_data['name']
        title = service_data['title']
        summary = service_data['summary']
        published = service_data['published']
        link = service_data['link']
        feed_url = service_data['feed_url']

        html.append("<div class='service-card'>")
        html.append(f"<h2>{emoji} {name}</h2>")
        if title:
            html.append(f"<strong>{title}</strong><br>")
        if summary:
            html.append(f"<p>{summary}</p>")
        if published:
            html.append(f"<p><em>{published}</em></p>")
        html.append(f"<a class='rss-link' href='{feed_url}' target='_blank'>📡 View on Provider</a>")
        html.append("</div>")

    html.append("</div></body></html>")
    Path(output_path).write_text("\n".join(html), encoding="utf-8")


def collect_aws_dashboard(feed_file_path):
    rss_urls = load_rss_urls(feed_file_path)
    dashboard = []
    healthy = True

    for url in rss_urls:
        entry = parse_feed(url)
        service_name = extract_service_name(url)

        if entry:
            classification, emoji = classify_status(entry['title'], entry['summary'])
            if classification == "down":
                healthy = False
            dashboard.append({
                "name": service_name,
                "emoji": emoji,
                "title": entry['title'],
                "summary": entry['summary'],
                "published": entry['published'],
                "link": entry['link'],
                "feed_url": url
            })
        else:
            dashboard.append({
                "name": service_name,
                "emoji": "🟢",
                "title": "No incidents reported",
                "summary": "All systems operational.",
                "published": "",
                "link": "",
                "feed_url": url
            })

    return dashboard, ("healthy" if healthy else "issues")


if __name__ == "__main__":
    input_files = {
        "AWS-eu-north-1": "input/rss-eu-north-1.txt",
        "AWS-eu-central-1": "input/rss-eu-central-1.txt"
    }

    region_dashboards = {}
    region_statuses = {}

    # Collect AWS data
    for region, filepath in input_files.items():
        dashboard, status = collect_aws_dashboard(filepath)
        region_dashboards[region] = dashboard
        region_statuses[region] = status

    # Collect GCP data
    gcp_dashboard, gcp_status = collect_gcp_dashboard()
    region_dashboards["GCP-europe-north2"] = gcp_dashboard
    region_statuses["GCP-europe-north2"] = gcp_status

    # Generate landing page
    generate_landing_html(region_statuses, "dashboards/services-status.html")

    # Generate one page per region
    for region, dashboard in region_dashboards.items():
        region_file = f"dashboards/{region}.html"
        generate_region_html(region, dashboard, region_file)

    print("✅ All dashboards generated.")
