import os
import re

def slug_to_title(slug, lang='en'):
    # Remove extension
    slug = re.sub(r'\.html$', '', slug)
    slug = re.sub(r'/$', '', slug)
    
    # Replace dashes and underscores with spaces
    title = slug.replace('-', ' ').replace('_', ' ')
    
    # Capitalize first letter of each word
    title = title.title()
    
    # Common replacements (can be expanded)
    title = title.replace('Pno', 'PNG').replace('Jpg', 'JPG').replace('Webp', 'WebP').replace('Gf', 'GIF')
    
    return title

def generate_backlinks():
    input_file = r'd:\resizer\all_urls.txt'
    output_file = r'd:\eldhopaulose.github.io\backlinks_list.html'
    
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    # Categorize by language
    langs = {
        'en': 'English',
        'es': 'Spanish (Español)',
        'fr': 'French (Français)',
        'pt': 'Portuguese (Português)',
        'de': 'German (Deutsch)',
        'id': 'Indonesian (Bahasa Indonesia)',
        'ar': 'Arabic (العربية)'
    }
    
    categorized = {l: [] for l in langs}
    
    for url in urls:
        # Detect language
        match = re.search(r'resizo\.in/([a-z]{2})/', url)
        lang_code = match.group(1) if match else 'en'
        
        if lang_code in categorized:
            categorized[lang_code].append(url)
        else:
            categorized['en'].append(url)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resizo Backlink Hub - All Tools & Blog Posts</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --primary: #06b6d4;
            --primary-hover: #22d3ee;
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --accent: #6366f1;
            --glass-border: rgba(255, 255, 255, 0.05);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(6, 182, 212, 0.1) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.1) 0px, transparent 50%);
            color: var(--text-main);
            line-height: 1.6;
            min-height: 100vh;
            padding: 4rem 1rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 4rem;
        }

        h1 {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(to right, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            letter-spacing: -0.025em;
        }

        .subtitle {
            font-size: 1.125rem;
            color: var(--text-dim);
            max-width: 600px;
            margin: 0 auto;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }

        .stat-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            padding: 1.5rem;
            border-radius: 1rem;
            text-align: center;
            transition: transform 0.3s ease;
        }

        .stat-card:hover { transform: translateY(-5px); border-color: var(--primary); }
        .stat-card .val { font-size: 2rem; font-weight: 700; color: var(--primary); display: block; }
        .stat-card .lab { font-size: 0.875rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.05em; }

        .search-box {
            position: sticky;
            top: 2rem;
            z-index: 100;
            margin-bottom: 3rem;
        }

        #searchInput {
            width: 100%;
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            padding: 1.25rem 1.5rem;
            border-radius: 1rem;
            color: white;
            font-size: 1rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            outline: none;
            transition: all 0.3s;
        }

        #searchInput:focus { border-color: var(--primary); box-shadow: 0 0 20px rgba(6, 182, 212, 0.2); }

        .lang-section {
            margin-bottom: 4rem;
        }

        .lang-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--glass-border);
        }

        .lang-header h2 { font-size: 1.5rem; font-weight: 700; color: var(--text-main); }
        .lang-header .badge {
            background: rgba(6, 182, 212, 0.1);
            color: var(--primary);
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .links-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1rem;
        }

        .link-card {
            background: var(--card-bg);
            border: 1px solid var(--glass-border);
            padding: 1.25rem;
            border-radius: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
            group: hover;
        }

        .link-card:hover { background: rgba(30, 41, 59, 0.9); border-color: var(--primary); }

        .link-info {
            flex: 1;
            overflow: hidden;
            margin-right: 1rem;
        }

        .link-info .title {
            display: block;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 0.25rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-decoration: none;
            transition: color 0.2s;
        }

        .link-info .title:hover { color: var(--primary); }

        .link-info .url {
            display: block;
            font-size: 0.75rem;
            color: var(--text-dim);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .copy-btn {
            background: rgba(255, 255, 255, 0.05);
            border: none;
            color: var(--text-dim);
            padding: 0.5rem;
            border-radius: 0.5rem;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .copy-btn:hover { background: var(--primary); color: white; }
        .copy-btn svg { width: 1.25rem; height: 1.25rem; }

        footer {
            text-align: center;
            margin-top: 6rem;
            padding: 2rem;
            color: var(--text-dim);
            font-size: 0.875rem;
            border-top: 1px solid var(--glass-border);
        }

        /* Success toast simple version */
        #toast {
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            background: var(--primary);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 999px;
            font-weight: 600;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);
            display: none;
            z-index: 1000;
            animation: slideUp 0.3s ease;
        }

        @keyframes slideUp { from { bottom: 0; opacity: 0; } to { bottom: 2rem; opacity: 1; } }

        @media (max-width: 768px) {
            h1 { font-size: 2rem; }
            .links-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Resizo Link Hub</h1>
            <p class="subtitle">Complete directory of SEO-optimized tools and articles for internal linking and backlinking campaigns.</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <span class="val">{TOTAL_COUNT}</span>
                <span class="lab">Total URLs</span>
            </div>
            <div class="stat-card">
                <span class="val">7</span>
                <span class="lab">Languages</span>
            </div>
            <div class="stat-card">
                <span class="val">100%</span>
                <span class="lab">Privacy-First</span>
            </div>
        </div>

        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search by tool name, language, or URL...">
        </div>
        
        <main id="content">
"""

    total_count = len(urls)
    html_content = html_content.replace('{TOTAL_COUNT}', str(total_count))

    for code, name in langs.items():
        links = categorized[code]
        if not links:
            continue
            
        html_content += f'\n        <section class="lang-section" data-lang="{name.lower()}">\n'
        html_content += f'            <div class="lang-header">\n'
        html_content += f'                <h2>{name}</h2>\n'
        html_content += f'                <span class="badge">{len(links)} Links</span>\n'
        html_content += f'            </div>\n'
        html_content += '            <div class="links-grid">\n'
        
        for url in links:
            # Extract slug
            parts = [p for p in url.split('/') if p]
            if len(parts) <= 2: # Domain or Lang Home
                if len(parts) == 1: # resizo.in
                   title = "Resizo Home"
                else: # resizo.in/es
                   title = f"Resizo Home ({name})"
            else:
                slug = parts[-1]
                title = slug_to_title(slug, code)
                
            html_content += f"""                <div class="link-card" data-title="{title.lower()}">
                    <div class="link-info">
                        <a href="{url}" target="_blank" class="title">{title}</a>
                        <span class="url">{url}</span>
                    </div>
                    <button class="copy-btn" onclick="copyUrl('{url}')" title="Copy URL">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path></svg>
                    </button>
                </div>\n"""
            
        html_content += '            </div>\n        </section>\n'

    html_content += """
        </main>

        <footer>
            <p>&copy; 2026 Resizo - Privacy-First Image Suite. Optimized by Antigravity AI.</p>
        </footer>
    </div>

    <div id="toast">URL Copied!</div>

    <script>
        function copyUrl(url) {
            navigator.clipboard.writeText(url).then(() => {
                const toast = document.getElementById('toast');
                toast.style.display = 'block';
                setTimeout(() => {
                    toast.style.display = 'none';
                }, 2000);
            });
        }

        const searchInput = document.getElementById('searchInput');
        const sections = document.querySelectorAll('.lang-section');
        const cards = document.querySelectorAll('.link-card');

        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            
            sections.forEach(section => {
                let sectionVisible = false;
                const sectionCards = section.querySelectorAll('.link-card');
                
                sectionCards.forEach(card => {
                    const title = card.getAttribute('data-title');
                    const url = card.querySelector('.url').textContent.toLowerCase();
                    
                    if (title.includes(term) || url.includes(term)) {
                        card.style.display = 'flex';
                        sectionVisible = true;
                    } else {
                        card.style.display = 'none';
                    }
                });

                section.style.display = sectionVisible ? 'block' : 'none';
            });
        });
    </script>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated {output_file} successfully.")

if __name__ == "__main__":
    generate_backlinks()
