import os
import feedparser

# Path to your file
RSS_FILE_PATH = os.path.join("input", "rss-eu-north-1.txt")

def load_rss_urls(filepath):
    """Load RSS URLs from the given file."""
    with open(filepath, "r") as file:
        return [line.strip() for line in file if line.strip()]

def parse_feed(url):
    """Parse a single RSS feed and return latest entry."""
    feed = feedparser.parse(url)
    if not feed.entries:
        return None
    latest = feed.entries[0]
    return {
        "title": latest.title,
        "summary": latest.summary,
        "published": latest.published,
        "link": latest.link,
    }

def extract_service_name(url):
    """Extract the AWS service name from the RSS URL."""
    filename = url.split("/")[-1]
    name_part = filename.replace("-eu-north-1.rss", "").replace(".rss", "")
    return name_part.upper()

def get_status_dashboard(rss_urls):
    """Build a status dictionary from all RSS feeds."""
    dashboard = {}
    for url in rss_urls:
        service_name = extract_service_name(url)
        latest_status = parse_feed(url)
        dashboard[service_name] = latest_status
    return dashboard

def print_dashboard(dashboard):
    """Display the dashboard in terminal."""
    print("=" * 50)
    print("AWS Service Status — eu-north-1")
    print("=" * 50)
    for service, status in dashboard.items():
        print(f"\n[{service}]")
        if status:
            print(f"{status['published']}: {status['title']}")
        else:
            print("No recent updates or failed to fetch.")
    print("\n")

if __name__ == "__main__":
    rss_urls = load_rss_urls(RSS_FILE_PATH)
    dashboard = get_status_dashboard(rss_urls)
    print_dashboard(dashboard)
