from pathlib import Path
from datetime import datetime, timezone

def generate_landing_html(region_statuses, output_path="docs/index.html"):
    Path("docs").mkdir(exist_ok=True)

    all_healthy = region_statuses and all(status == "healthy" for status in region_statuses.values())
    issue_count = sum(1 for status in region_statuses.values() if status != "healthy")
    if all_healthy:
        banner_message = "☕ All is good! You can go back to your coffee."
        banner_class = "ok"
    else:
        banner_message = (
            f"⚠️ {issue_count} region{'s' if issue_count != 1 else ''} reporting issues. "
            "I hope you got your coffiee, it's time to work."
        )
        banner_class = "warn"

    html = [
        "<html><head>",
        '<meta charset="UTF-8">',
        "<title>Cloud Service Dashboard</title>",
        "<style>",
        """
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #edf2fb 0%, #e2f0d9 100%); color: #2f3437; min-height: 100vh; }
        header { background: rgba(30, 136, 229, 0.92); color: white; padding: 30px 40px; box-shadow: 0 12px 24px rgba(30,136,229,0.25); position: sticky; top: 0; backdrop-filter: blur(8px); }
        header h1 { margin: 0; font-size: 32px; letter-spacing: 0.5px; }
        .container { max-width: 1100px; margin: 40px auto 80px; padding: 0 20px 60px; }
        .timestamp { font-size: 14px; color: #455a64; margin-bottom: 20px; }
        .status-banner { border-radius: 14px; padding: 16px 22px; margin-bottom: 30px; font-size: 18px; box-shadow: 0 20px 45px rgba(0,0,0,0.08); display: flex; align-items: center; gap: 12px; }
        .status-banner.ok { background: #e8f5e9; color: #2e7d32; }
        .status-banner.warn { background: #fff3e0; color: #ef6c00; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 24px; }
        .region-card { background: rgba(255,255,255,0.92); border-radius: 16px; padding: 22px; box-shadow: 0 18px 36px rgba(15,23,42,0.12); transition: transform 0.25s ease, box-shadow 0.25s ease; border: 1px solid rgba(255,255,255,0.6); backdrop-filter: blur(6px); }
        .region-card:hover { transform: translateY(-6px); box-shadow: 0 24px 44px rgba(15,23,42,0.16); }
        .region-card h2 { margin: 0 0 10px; font-size: 20px; display: flex; align-items: center; gap: 12px; }
        .status-icon { font-size: 28px; }
        a { text-decoration: none; color: #1565c0; }
        a:hover { text-decoration: underline; }
        """,
        "</style>",
        "</head><body>",
        "<header><h1>🌍 Cloud Services Health Overview</h1></header>",
        "<div class='container'>",
        f"<p class='timestamp'><em>Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</em></p>",
        f"<div class='status-banner {banner_class}'>{banner_message}</div>",
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
    incident_classifications = {"DISRUPTION", "OUTAGE", "IMPACT", "DEGRADED"}
    active_incidents = sum(
        1 for item in dashboard
        if item.get("classification") in incident_classifications or item.get("emoji") in {"🔴", "🟡"}
    )
    total_services = len(dashboard)
    if active_incidents == 0 and total_services:
        hero_message = "☕ Smooth sailing — all services look healthy."
        hero_class = "ok"
    elif total_services == 0:
        hero_message = "No services found for this region."
        hero_class = "neutral"
    else:
        hero_message = f"⚠️ {active_incidents} service{'s' if active_incidents != 1 else ''} reporting notices."
        hero_class = "warn"

    html = [
        "<html><head>",
        '<meta charset="UTF-8">',
        f"<title>{provider} {region} - Service Status</title>",
        "<style>",
        """
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(125deg, #f1f4ff 0%, #f1fff4 100%); margin: 0; padding: 60px 20px; min-height: 100vh; color: #263238; }
        .container { max-width: 960px; margin: auto; background: rgba(255,255,255,0.95); padding: 46px 48px; border-radius: 22px; box-shadow: 0 26px 60px rgba(15,23,42,0.16); backdrop-filter: blur(8px); }
        h1 { font-size: 34px; color: #102027; margin-bottom: 10px; letter-spacing: 0.6px; display: flex; align-items: center; gap: 12px; }
        p, a, h2 { color: #37474f; }
        .subtitle { font-size: 18px; margin-bottom: 28px; color: #546e7a; }
        .timestamp { color: #607d8b; font-size: 15px; margin-bottom: 24px; padding-left: 12px; border-left: 3px solid rgba(33,150,243,0.45); }
        .back-link { display: inline-flex; align-items: center; gap: 6px; margin-bottom: 26px; font-size: 16px; color: #1976d2; text-decoration: none; font-weight: 600; transition: color 0.2s ease; }
        .back-link:hover { color: #0d47a1; }
        .hero-banner { border-radius: 14px; padding: 18px 24px; font-size: 18px; margin-bottom: 30px; box-shadow: inset 0 1px 6px rgba(255,255,255,0.4); display: flex; align-items: center; gap: 12px; }
        .hero-banner.ok { background: #e8f5e9; color: #1b5e20; }
        .hero-banner.warn { background: #fff3e0; color: #e65100; }
        .hero-banner.neutral { background: #eceff1; color: #455a64; }
        .service-card { border-radius: 16px; box-shadow: 0 16px 38px rgba(15,23,42,0.12); padding: 24px 26px; margin-bottom: 26px; position: relative; overflow: hidden; transition: transform 0.25s ease, box-shadow 0.25s ease; border: 1px solid rgba(255,255,255,0.65); backdrop-filter: blur(5px); }
        .service-card::after { content: ""; position: absolute; inset: auto -30px -30px; height: 120px; background: radial-gradient(circle at top left, rgba(255,255,255,0.45), transparent 60%); opacity: 0; transition: opacity 0.35s ease; pointer-events: none; }
        .service-card:hover { transform: translateY(-6px); box-shadow: 0 24px 54px rgba(15,23,42,0.18); }
        .service-card:hover::after { opacity: 1; }
        .healthy { background: linear-gradient(155deg, rgba(232,245,233,0.92) 0%, rgba(232,245,233,0.65) 100%); border-left: 6px solid #43a047; }
        .unhealthy { background: linear-gradient(155deg, rgba(255,235,238,0.92) 0%, rgba(255,205,210,0.62) 100%); border-left: 6px solid #d32f2f; }
        .warning { background: linear-gradient(155deg, rgba(255,248,225,0.92) 0%, rgba(255,236,179,0.62) 100%); border-left: 6px solid #ffa000; }
        .service-card h2 { font-size: 22px; margin: 0 0 10px 0; display: flex; align-items: center; gap: 10px; }
        .service-card p { margin: 6px 0; line-height: 1.5; }
        .rss-link { display: inline-flex; align-items: center; gap: 6px; margin-top: 12px; color: #2e7d32; font-weight: 600; text-decoration: none; background: rgba(255,255,255,0.6); padding: 8px 12px; border-radius: 999px; transition: background 0.2s ease, transform 0.2s ease; }
        .rss-link:hover { text-decoration: none; background: rgba(46,125,50,0.12); transform: translateY(-2px); }
        """,
        "</style>",
        "</head><body>",
        "<div class='container'>",
        f"<h1>📍 {provider} Status for {region.upper()}</h1>",
        "<div class='subtitle'>Live summary of recent incidents and service health.</div>",
        f"<p class='timestamp'><em>Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</em></p>",
        f"<div class='hero-banner {hero_class}'>{hero_message}</div>",
        "<a class='back-link' href='index.html'>&larr; Back to Overview</a>",
    ]

    # Prioritize outage and impact cards while preserving original order within each group
    priority_map = {"DISRUPTION": 0, "OUTAGE": 1, "IMPACT": 2, "DEGRADED": 3}
    dashboard_sorted = sorted(
        enumerate(dashboard),
        key=lambda item: (priority_map.get(item[1].get("classification"), 4), item[0])
    )

    for _, service_data in dashboard_sorted:
        emoji = service_data['emoji']
        name = service_data['name']
        title = service_data['title']
        summary = service_data['summary']
        published = service_data['published']
        link = service_data['link']
        feed_url = service_data['feed_url']

        classification = service_data.get("classification")
        if classification in {"DISRUPTION", "OUTAGE"} or emoji == "🔴":
            card_class = "unhealthy"
        elif classification in {"IMPACT", "DEGRADED"} or emoji == "🟡":
            card_class = "warning"
        else:
            card_class = "healthy"

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
