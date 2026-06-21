import html


def normalize_input(prompt):
    return input(prompt).strip()


def format_list_text(text):
    items = [item.strip() for item in text.replace('\n', ',').split(',') if item.strip()]
    if not items:
        return '<p class="empty">Not provided</p>'
    return '<ul>' + ''.join(f'<li>{html.escape(item)}</li>' for item in items) + '</ul>'


def format_summary_text(text):
    safe_text = html.escape(text.strip())
    return safe_text.replace('\n', '<br>') if safe_text else 'No summary provided.'


def format_link(link):
    if not link:
        return 'Not provided'
    safe_link = html.escape(link.strip())
    if not safe_link.startswith(('http://', 'https://')):
        safe_link = 'https://' + safe_link
    return f'<a href="{safe_link}" target="_blank">{html.escape(link.strip())}</a>'


def safe_filename(name):
    cleaned = ''.join(c if c.isalnum() or c in ' _-' else '_' for c in name).strip()
    return cleaned or 'resume'


name = normalize_input('Type Your Name: ')
designation = normalize_input('Type Your Designation: ')
address = normalize_input('Type Your Address: ')
email = normalize_input('Type Your Email: ')
glink = normalize_input('Type Your Github Link: ')
summaryPara = normalize_input('Type Your Summary / Paragraph: ')
Langs = normalize_input('Type Your Languages (comma-separated): ')
Frams = normalize_input('Type Your Frameworks (comma-separated): ')
Tools = normalize_input('Type Your Tools (comma-separated): ')
Concp = normalize_input('Type Your Concepts (comma-separated): ')
deg = normalize_input('Type Your Degree: ')
degS = normalize_input('Type Your Degree Start Year: ')
degE = normalize_input('Type Your Degree End Year: ')
Uni = normalize_input('Type Your University: ')

contact_email = html.escape(email) if email else 'Not provided'
contact_link = format_link(glink)
summary_html = format_summary_text(summaryPara)

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(name) or 'Resume'}</title>
    <style>
        :root {{
            --bg-color: #ffffff;
            --text-color: #222222;
            --text-muted: #666666;
            --accent-color: #0066cc;
            --border-color: #eeeeee;
            --section-spacing: 2.5rem;
        }}

        [data-theme="dark"] {{
            --bg-color: #121212;
            --text-color: #e0e0e0;
            --text-muted: #a0a0a0;
            --accent-color: #4da3ff;
            --border-color: #2c2c2c;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            transition: background-color 0.3s, color 0.3s;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
        }}

        a {{
            color: var(--accent-color);
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        .theme-toggle-btn {{
            position: fixed;
            top: 1.5rem;
            right: 1.5rem;
            background: none;
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 0.5rem 0.75rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85rem;
            background-color: var(--bg-color);
        }}

        header {{
            margin-bottom: var(--section-spacing);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.5rem;
        }}

        header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            letter-spacing: -0.05em;
            margin-bottom: 0.5rem;
        }}

        .subtitle {{
            font-size: 1.2rem;
            color: var(--text-muted);
            margin-bottom: 1rem;
        }}

        .contact-info {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            font-size: 0.9rem;
            color: var(--text-muted);
        }}

        section {{
            margin-bottom: var(--section-spacing);
        }}

        section h2 {{
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--text-muted);
            margin-bottom: 1.25rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.25rem;
        }}

        .item {{
            margin-bottom: 1.5rem;
        }}

        .item-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            margin-bottom: 0.25rem;
        }}

        .item-title {{
            font-weight: 600;
            font-size: 1.1rem;
        }}

        .item-date {{
            color: var(--text-muted);
            font-size: 0.9rem;
        }}

        .item-subtitle {{
            color: var(--accent-color);
            font-weight: 500;
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
        }}

        .skill-category h3 {{
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }}

        .skill-list {{
            font-size: 0.9rem;
            color: var(--text-color);
        }}

        .skill-list ul {{
            list-style: disc inside;
            margin: 0;
            padding-left: 1rem;
        }}

        .skill-list li {{
            margin-bottom: 0.25rem;
        }}

        .summary-text {{
            font-size: 0.95rem;
            color: var(--text-color);
            white-space: pre-wrap;
        }}

        @media (max-width: 600px) {{
            header h1 {{
                font-size: 2rem;
            }}
            .item-header {{
                flex-direction: column;
            }}
            .item-date {{
                margin-top: 0.1rem;
                margin-bottom: 0.25rem;
            }}
        }}
    </style>
</head>
<body>
    <button class="theme-toggle-btn" id="themeToggle" aria-label="Toggle theme">Dark Mode</button>
    <div class="container">
        <header>
            <h1>{html.escape(name) or 'Your Name'}</h1>
            <div class="subtitle">{html.escape(designation) or 'Your Designation'}</div>
            <div class="contact-info">
                <span>📍 {html.escape(address) or 'Not provided'}</span>
                <span>✉️ {contact_email if email else 'Not provided'}</span>
                <span>💻 {contact_link}</span>
            </div>
        </header>
        <section id="summary">
            <h2>Summary</h2>
            <div class="summary-text">{summary_html}</div>
        </section>
        <section id="skills">
            <h2>Skills</h2>
            <div class="skills-grid">
                <div class="skill-category">
                    <h3>Languages</h3>
                    <div class="skill-list">{format_list_text(Langs)}</div>
                </div>
                <div class="skill-category">
                    <h3>Frameworks</h3>
                    <div class="skill-list">{format_list_text(Frams)}</div>
                </div>
                <div class="skill-category">
                    <h3>Tools</h3>
                    <div class="skill-list">{format_list_text(Tools)}</div>
                </div>
                <div class="skill-category">
                    <h3>Concepts</h3>
                    <div class="skill-list">{format_list_text(Concp)}</div>
                </div>
            </div>
        </section>

        <section id="education">
            <h2>Education</h2>
            <div class="item">
                <div class="item-header">
                    <div class="item-title">{html.escape(deg) or 'Degree'}</div>
                    <div class="item-date">{html.escape(degS) or 'Start Year'} — {html.escape(degE) or 'End Year'}</div>
                </div>
                <div class="item-subtitle">{html.escape(Uni) or 'University'}</div>
            </div>
        </section>
    </div>
    <script>
        const themeToggle = document.getElementById('themeToggle');
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {{
            document.documentElement.setAttribute('data-theme', 'dark');
            themeToggle.textContent = 'Light Mode';
        }} else {{
            document.documentElement.setAttribute('data-theme', 'light');
            themeToggle.textContent = 'Dark Mode';
        }}

        themeToggle.addEventListener('click', () => {{
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            themeToggle.textContent = newTheme === 'dark' ? 'Light Mode' : 'Dark Mode';
        }});
    </script>
</body>
</html>'''

file_name = f"{safe_filename(name)}_Resume.html"
with open(file_name, 'w', encoding='utf-8') as rfile:
    rfile.write(html_content)

print(f'Created resume file: {file_name}')
