import markdown

def generate_markdown_and_html(statuses):
    # Markdown output
    md_text = "# 🇸🇪 ISP Status Dashboard\n\n"
    md_text += "_Last updated manually_\n\n"
    for status in statuses:
        md_text += f"## {status}\n\n"

    # Write markdown file
    with open("dashboard.md", "w", encoding="utf-8") as f:
        f.write(md_text)

    # Convert to HTML and write HTML file
    html_body = markdown.markdown(md_text)
    full_html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>ISP Status Dashboard</title>
        <style>
            body {{
                font-family: sans-serif;
                margin: 2em;
            }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; }}
            p, li {{ font-size: 1.1em; }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("✅ dashboard.html generated from dashboard.md")
