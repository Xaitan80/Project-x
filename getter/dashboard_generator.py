from pathlib import Path
from datetime import datetime, timezone

def generate_landing_html(region_statuses, output_path="docs/index.html"):
    Path("docs").mkdir(exist_ok=True)

    html = [
        "<html><head>",
        '<meta charset="UTF-8">',
        "<title>Cloud Service Dashboard</title>",
        "<style>",
        """
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: #f4f6f8;
            color: #333;
        }
        header {
            background: #1e88e5;
            color: white;
            padding: 20px 40px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        header h1 {
            margin: 0;
            font-size: 28px;
        }
        .container {
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 20px;
        }
        .timestamp {
            font-size: 14px;
            color: #777;
            margin-bottom: 20px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        .region-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        .region-card:hover {
            transform: translateY(-4px);
        }
        .region-card h2 {
            margin: 0 0 10px;
            font-size: 20px;
        }
        .status-icon {
            font-size: 24px;
            margin-right: 10px;
            vertical-align: middle;
        }
        a {
            text-decoration: none;
            color: #1e88e5;
        }
        a:hover {
            text-decoration: underline;
        }
        """,
        "</style>",
        "</head><body>",
        "<header><h1>🌍 Cloud Services Health Overview</h1></header>",
        "<div class='container'>",
        f"<p class='timestamp'><em>Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</em></p>",
        "<div class='grid'>"
    ]

    for region, status in region_statuses.items():
        emoji = "🟢" if status == "healthy" else "🔴"
        
        if region.startswith("aws-"):
            clean_region = region[len("aws-"):]
            label = f"AWS - {clean_region.upper()}"
            link = f"aws-{clean_region}.html"
        elif region.startswith("gcp-"):
            clean_region = region[len("gcp-"):]
            label = f"GCP - {clean_region.upper()}"
            link = f"gcp-{clean_region}.html"
        else:
            clean_region = region
            label = region.upper()
            link = f"{region}.html"

        html.append("<div class='region-card'>")
        html.append(f"<h2><span class='status-icon'>{emoji}</span><a href='{link}'>{label}</a></h2>")
        html.append("</div>")

    html.extend(["</div>", "</div>", "</body></html>"])
    Path(output_path).write_text("\n".join(html), encoding="utf-8")


def generate_region_html(region, dashboard, output_path, provider="AWS"):
    html = [
        "<html><head>",
        '<meta charset="UTF-8">',
        f"<title>{provider} {region} - Service Status</title>",
        "<style>",
        """
        body { font-family: Arial, sans-serif; background: #f2f2f2; padding: 40px; margin: 0; }
        .container { max-width: 900px; margin: auto; }
        h1 { font-size: 32px; color: #222; margin-bottom: 10px; }
        p, a, h2 { color: #333; }
        .timestamp { color: #666; font-size: 14px; margin-bottom: 30px; }
        .back-link { display: inline-block; margin-bottom: 20px; font-size: 16px; color: #0077cc; text-decoration: none; }
        .back-link:hover { text-decoration: underline; }

        .service-card {
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            padding: 20px;
            margin-bottom: 20px;
        }

        .healthy {
            background: #e8f5e9; /* light green */
            border-left: 6px solid #66bb6a;
        }

        .unhealthy {
            background: #ffebee; /* light red */
            border-left: 6px solid #e53935;
        }

        .service-card h2 {
            font-size: 20px;
            margin: 0 0 8px 0;
        }

        .service-card p {
            margin: 5px 0;
        }

        .rss-link {
            display: inline-block;
            margin-top: 10px;
            color: #2e7d32;
            font-weight: bold;
            text-decoration: none;
        }

        .rss-link:hover {
            text-decoration: underline;
        }
        """,
        "</style>",
        "</head><body>",
        "<div class='container'>",
        f"<h1>📍 {provider} Status for {region.upper()}</h1>",
        f"<p class='timestamp'><em>Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</em></p>",
        "<a class='back-link' href='index.html'>&larr; Back to Overview</a>",
    ]

    # Prioritize impacted services at the top while preserving original order for others
    dashboard_sorted = sorted(
        enumerate(dashboard),
        key=lambda item: (0 if item[1].get("classification") == "IMPACT" else 1, item[0])
    )

    for _, service_data in dashboard_sorted:
        emoji = service_data['emoji']
        name = service_data['name']
        title = service_data['title']
        summary = service_data['summary']
        published = service_data['published']
        link = service_data['link']
        feed_url = service_data['feed_url']

        # Determine status based on emoji
        card_class = "unhealthy" if emoji == "🔴" else "healthy"

        html.append(f"<div class='service-card {card_class}'>")
        html.append(f"<h2>{emoji} {name}</h2>")
        if title:
            html.append(f"<strong>{title}</strong><br>")
        if summary:
            html.append(f"<p>{summary}</p>")
        if published:
            html.append(f"<p><em>{published}</em></p>")
        if feed_url:
            html.append(f"<a class='rss-link' href='{feed_url}' target='_blank'>📡 View on Provider</a>")
        html.append("</div>")

    html.append("</div></body></html>")
    Path(output_path).write_text("\n".join(html), encoding="utf-8")
