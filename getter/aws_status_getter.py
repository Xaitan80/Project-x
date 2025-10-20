# aws_status_getter.py
from common.feed_utils import load_rss_urls, parse_feed, extract_service_name, classify_status

def collect_aws_dashboard(feed_file_path):
    rss_urls = load_rss_urls(feed_file_path)
    dashboard = []
    healthy = True

    for url in rss_urls:
        entry = parse_feed(url)
        service_name = extract_service_name(url)

        if entry:
            classification, emoji = classify_status(entry['title'], entry['summary'])
            if classification in {"OUTAGE", "IMPACT", "DISRUPTION", "DEGRADED"}:
                healthy = False
            dashboard.append({
                "name": service_name,
                "emoji": emoji,
                "classification": classification,
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
                "classification": "NO_DATA",
                "title": "No incidents reported",
                "summary": "All systems operational.",
                "published": "",
                "link": "",
                "feed_url": url
            })

    return dashboard, ("healthy" if healthy else "issues")
