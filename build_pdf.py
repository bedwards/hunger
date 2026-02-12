#!/usr/bin/env python3
"""Generate PDF downloads from the site HTML files using WeasyPrint CLI."""

import re
import os
import subprocess
import tempfile

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs')

PRINT_CSS = '''
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500&display=swap');

@page {
    size: A5;
    margin: 2cm 1.8cm;
    @bottom-center {
        content: counter(page);
        font-family: 'Lexend', sans-serif;
        font-size: 8pt;
        color: #999;
    }
}

@page :first {
    @bottom-center { content: none; }
}

body {
    font-family: 'Lexend', sans-serif;
    font-weight: 300;
    font-size: 10.5pt;
    line-height: 1.75;
    color: #1a1a1a;
    background: #fff;
}

h1 {
    font-weight: 400;
    font-size: 18pt;
    text-align: center;
    margin: 2em 0 1.5em;
    color: #333;
    letter-spacing: 0.05em;
    page-break-before: always;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    font-weight: 400;
    font-size: 12pt;
    color: #444;
    margin-top: 1.8em;
    margin-bottom: 0.8em;
    letter-spacing: 0.03em;
}

h3 {
    font-weight: 400;
    font-size: 10.5pt;
    color: #666;
    font-style: italic;
    margin-top: 1.5em;
    margin-bottom: 0.6em;
}

p {
    margin-bottom: 0.6em;
    text-indent: 1.2em;
    orphans: 3;
    widows: 3;
}

h1 + p, h2 + p, h3 + p, hr + p, blockquote + p {
    text-indent: 0;
}

hr {
    border: none;
    border-top: 0.5pt solid #ccc;
    margin: 1.5em auto;
    width: 3em;
}

em { font-style: italic; }
strong { font-weight: 500; }

blockquote {
    border-left: 1.5pt solid #ccc;
    padding-left: 1em;
    margin: 1em 0;
    color: #555;
    font-style: italic;
}

blockquote p { text-indent: 0; }

.footnote {
    font-size: 9pt;
    color: #666;
    text-indent: 0 !important;
    line-height: 1.5;
}

.pdf-title-page {
    text-align: center;
    padding-top: 35%;
}

.pdf-title-page h1 {
    font-size: 28pt;
    margin-bottom: 0.3em;
    page-break-before: avoid;
}

.pdf-title-page .author {
    font-size: 13pt;
    color: #666;
    margin-bottom: 0.2em;
}

.pdf-title-page .translator {
    font-size: 10pt;
    color: #888;
    font-style: italic;
}
'''


def extract_main_content(filepath):
    """Extract content from <main> tags."""
    with open(filepath, 'r') as f:
        html = f.read()
    match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    return match.group(1).strip() if match else ''


def generate_pdf(html_content, output_path):
    """Write HTML to temp file, run weasyprint CLI."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        tmp_html = f.name

    css_path = tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False)
    css_path.write(PRINT_CSS)
    css_path.close()

    try:
        subprocess.run(
            ['weasyprint', tmp_html, output_path, '-s', css_path.name],
            check=True, capture_output=True, text=True
        )
        print(f'Generated {output_path}')
    except subprocess.CalledProcessError as e:
        print(f'Error: {e.stderr}')
        raise
    finally:
        os.unlink(tmp_html)
        os.unlink(css_path.name)


def build_novel_pdf():
    parts = []
    for i in range(1, 5):
        parts.append(extract_main_content(os.path.join(DOCS, f'part-{i}.html')))

    html = f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"></head>
<body>
<div class="pdf-title-page">
    <h1>Hunger</h1>
    <p class="author">Knut Hamsun</p>
    <p class="translator">Translated by George Egerton</p>
</div>
{''.join(parts)}
</body>
</html>'''

    generate_pdf(html, os.path.join(DOCS, 'hunger-novel.pdf'))


def build_companion_pdf():
    sections = []

    essay_path = os.path.join(DOCS, 'essay.html')
    if os.path.exists(essay_path):
        sections.append(extract_main_content(essay_path))

    for i in range(1, 5):
        for prefix in ['extra', 'companion']:
            path = os.path.join(DOCS, f'{prefix}-{i}.html')
            if os.path.exists(path):
                sections.append(extract_main_content(path))

    if not sections:
        print('No companion texts found yet — skipping companion PDF.')
        return

    html = f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"></head>
<body>
<div class="pdf-title-page">
    <h1>Hunger</h1>
    <p class="author">Companion Texts</p>
    <p class="translator">A reading companion to Knut Hamsun's novel</p>
</div>
{''.join(sections)}
</body>
</html>'''

    generate_pdf(html, os.path.join(DOCS, 'hunger-companion.pdf'))


if __name__ == '__main__':
    print('Building novel PDF...')
    build_novel_pdf()
    print('Building companion PDF...')
    build_companion_pdf()
    print('Done.')
