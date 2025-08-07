# Project-x
Just my dumb stuff
This should create a dashboard with satus information for the largest CSP's.
Starting with AWS and it's europe-north-1 DC

## 🛠️ Customizing Monitored Services

This dashboard is a **proof of concept**. The included RSS feed lists only cover a few AWS services in `eu-north-1` and `eu-central-1`.

To monitor more services:
1. Go to [AWS Status](https://status.aws.amazon.com/)
2. Find the RSS icon next to the service and region you care about
3. Copy the URL (e.g., `https://status.aws.amazon.com/rss/s3-eu-central-1.rss`)
4. Add it to the appropriate `input/rss-<region>.txt` file

💡 The script will pick up any valid RSS URL you add — no changes needed in code.

