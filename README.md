# Project-x
Added more AWS sites, and during the event on october 18, i got to see the site work!
Just my dumb stuff  
This should create a dashboard with status information for the largest CSP's.  
Starting with AWS and its europe-north-1 DC and GCP europe-north2 region.

## 🛠️ Customizing Monitored Services

This dashboard is a **proof of concept**. The included RSS feed lists only cover a few AWS services in `eu-north-1` and `eu-central-1`, and GCP europe-north2.

To monitor more services:
1. Go to [AWS Status](https://status.aws.amazon.com/)
2. Find the RSS icon next to the service and region you care about
3. Copy the URL (e.g., `https://status.aws.amazon.com/rss/s3-eu-central-1.rss`)
4. Add it to the appropriate `input/rss-<region>.txt` file

For GCP:
1. Use the JSON data from Google Cloud Service Health or the RSS feed at [https://status.cloud.google.com/en/feed.atom](https://status.cloud.google.com/en/feed.atom)
2. The script currently supports europe-north2 (Stockholm) region data via JSON.
3. You can extend the GCP JSON feed handling or add additional RSS feeds as needed.

💡 The script will pick up any valid RSS or JSON URL you add — no changes needed in code.

## ⚙️ Automation with GitHub Actions

This project uses GitHub Actions to automatically:

- Run the data collection scripts regularly (e.g., daily)
- Generate the updated dashboard HTML files
- Deploy the static site to GitHub Pages

If you want to customize the schedule or trigger manual runs:

- Edit `.github/workflows/deploy.yml` to adjust the cron schedule or workflow triggers.

### To manually trigger:

- Push changes to the `main` branch or
- Use the "Run workflow" button in the Actions tab on GitHub.

## 🕒 Timezone Notes

All timestamps are generated in UTC by default.  
If you want timestamps in your local timezone, you need to:

- Modify the scripts to use your desired timezone, or
- Convert times client-side after page load, or
- Adjust manually in the README/configuration.

---

Feel free to open issues or pull requests if you want to contribute or request features!

---

© 2025 Xaitan
