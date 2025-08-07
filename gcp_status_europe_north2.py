import requests
from datetime import datetime, timezone

REGION = "europe-north2"
FEED_URL = "https://status.cloud.google.com/regional/europe"
STATUS_JSON_URL = "https://status.cloud.google.com/incidents.json"

# Known service product IDs with friendly names
KNOWN_PRODUCTS = {
    "compute": "Compute Engine",
    "cloud-storage": "Cloud Storage",
    "cloud-sql": "Cloud SQL",
    "cloud-functions": "Cloud Functions",
    "cloud-pubsub": "Cloud Pub/Sub",
    "kubernetes-engine": "Google Kubernetes Engine",
    "bigquery": "BigQuery",
    "cloud-run": "Cloud Run",
}


def collect_gcp_dashboard():
    try:
        response = requests.get(STATUS_JSON_URL)
        response.raise_for_status()
        incidents = response.json()
    except Exception as e:
        print(f"Failed to fetch GCP status data: {e}")
        return [], "issues"

    affected_products = {}

    for incident in incidents:
        # Check if this incident affects europe-north2
        for impact in incident.get("external_impact_regions", []):
            if REGION in impact.get("region_ids", []):
                for product in impact.get("affected_products", []):
                    product_id = product.get("id")
                    if product_id in KNOWN_PRODUCTS:
                        # Use most recent update if available
                        update = incident.get("most_recent_update", {}).get("text", "")
                        affected_products[product_id] = {
                            "title": incident.get("external_desc", "Incident reported"),
                            "summary": update,
                            "published": incident.get("begin", ""),
                            "link": incident.get("public_url", ""),
                        }

    dashboard = []
    all_healthy = True

    for product_id, product_name in KNOWN_PRODUCTS.items():
        if product_id in affected_products:
            all_healthy = False
            incident = affected_products[product_id]
            dashboard.append({
                "name": product_name,
                "emoji": "🔴",
                "title": incident["title"],
                "summary": incident["summary"],
                "published": incident["published"],
                "link": incident["link"],
                "feed_url": FEED_URL
            })
        else:
            dashboard.append({
                "name": product_name,
                "emoji": "🟢",
                "title": "No incidents reported",
                "summary": "All systems operational.",
                "published": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                "link": "",
                "feed_url": FEED_URL
            })

    return dashboard, "healthy" if all_healthy else "issues"


# Optional test entry point
if __name__ == "__main__":
    dashboard, status = collect_gcp_dashboard()
    print(f"Status: {status}")
    for service in dashboard:
        print(f"{service['emoji']} {service['name']}: {service['title']}")
