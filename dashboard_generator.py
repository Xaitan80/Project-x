from pathlib import Path
from datetime import datetime, timezone

def generate_landing_html(region_statuses, output_path="docs/index.html"):
    Path("docs").mkdir(exist_ok=True)  # Ensure docs directory exists

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
        f"<p><em>Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</em></p>",
    ]

    for region, status in region_statuses.items():
        emoji = "🟢" if status == "healthy" else "🔴"
        html.append("<div class='region-card'>")
    
    # Clean prefix and build label and link accordingly
        if region.startswith("aws-"):
            clean_region = region[len("aws-"):]
            label = f"AWS-{clean_region}"
            link = f"aws-{clean_region}.html"
        elif region.startswith("gcp-"):
            clean_region = region[len("gcp-"):]
            label = f"GCP-{clean_region}"
            link = f"gcp-{clean_region}.html"
        else:
            clean_region = region
            label = region
            link = f"{region}.html"
    
        html.append(f"<span class='status-icon'>{emoji}</span><a href='{link}'><h2>{label}</h2></a>")
        html.append("</div>")



    html.append("</body></html>")
    Path(output_path).write_text("\n".join(html), encoding="utf-8")


def generate_region_html(region, dashboard, output_path=None):
    if output_path is None:
        output_path = f"docs/aws-{region}.html"
    Path("docs").mkdir(exist_ok=True)  # Ensure docs directory exists

    html = [
        "<html><head>",
        '<meta charset="UTF-8">',
        f"<title>AWS {region} - Service Status</title>",
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
        f"<h1>📍 AWS Status for {region.upper()}</h1>",
        f"<p><em>Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</em></p>",
        "<div class='services'>"
    ]

    for service_data in dashboard:
        emoji = service_data['emoji']
        name = service_data['name']
        title = service_data['title']
        summary = service_data['summary']
        published = service_data['published']
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
