import feedparser

def load_rss_urls(filepath):
    """Load RSS feed URLs from a text file, one per line, ignoring empty lines and comments."""
    urls = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls

def parse_feed(url):
    """Parse the RSS feed URL and return the latest entry as a dict or None if no entries."""
    feed = feedparser.parse(url)
    if feed.bozo:
        # Error parsing feed
        return None
    if not feed.entries:
        return None

    latest_entry = feed.entries[0]
    return {
        "title": latest_entry.get("title", ""),
        "summary": latest_entry.get("summary", ""),
        "published": latest_entry.get("published", ""),
        "link": latest_entry.get("link", "")
    }

def extract_service_name(url):
    """Extract a simple service name from the RSS feed URL."""
    # Example: parse the last path component or use some known mapping
    # For example, if the URL ends with something like 'ec2.rss' -> 'EC2'
    import os
    base = os.path.basename(url)
    name = base.split(".")[0].upper()
    return name

def classify_status(title, summary):
    """
    Basic classification of status based on title or summary keywords.
    Returns (classification, emoji).
    """
    lower_title = title.lower()
    lower_summary = summary.lower()
    if ("service is operating normally" in lower_title or
            "service is operating normally" in lower_summary or
            "no incidents reported" in lower_title or
            "no incidents reported" in lower_summary):
        return ("OK", "🟢")
    if "service disruption" in lower_title or "service disruption" in lower_summary:
        return ("DISRUPTION", "🔴")
    if "service impact" in lower_title or "service impact" in lower_summary:
        return ("IMPACT", "🟡")

    if "operational" in lower_title or "operational" in lower_summary:
        return ("OK", "🟢")
    elif "degraded" in lower_title or "degraded" in lower_summary:
        return ("DEGRADED", "🟡")
    elif "outage" in lower_title or "outage" in lower_summary or "issue" in lower_title or "issue" in lower_summary:
        return ("OUTAGE", "🔴")
    else:
        return ("UNKNOWN", "⚪")
