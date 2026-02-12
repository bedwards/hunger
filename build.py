#!/usr/bin/env python3
"""Extract chapters from hunger.html and generate site pages."""

import re
import os

with open('hunger.html', 'r') as f:
    lines = f.readlines()

os.makedirs('docs', exist_ok=True)

# Chapter boundaries (1-based line numbers from the source, converted to 0-based)
chapters = [
    {'num': 1, 'title': 'Part I', 'start': 6, 'end': 1585},
    {'num': 2, 'title': 'Part II', 'start': 1588, 'end': 2860},
    {'num': 3, 'title': 'Part III', 'start': 2862, 'end': 4670},
    {'num': 4, 'title': 'Part IV', 'start': 4672, 'end': 5909},
]

roman = ['I', 'II', 'III', 'IV']

EXTRA_TITLES = [
    'The Invention of the Interior',
    'Christiania: A City of Ghosts',
    'The Theater of Starvation',
    'After Hunger',
]

def nav_html(num):
    parts = []
    parts.append('<nav class="chapter-nav">')
    left = f'<a href="part-{num-1}.html">\u2190 Part {roman[num-2]}</a>' if num > 1 else '<span></span>'
    right = f'<a href="part-{num+1}.html">Part {roman[num]} \u2192</a>' if num < 4 else '<span></span>'
    parts.append(f'  {left}')
    parts.append(f'  <a href="index.html">Home</a>')
    parts.append(f'  {right}')
    parts.append('</nav>')
    parts.append('<nav class="extra-nav">')
    parts.append(f'  <a href="extra-{num}.html">Companion essay: {EXTRA_TITLES[num-1]} \u2192</a>')
    parts.append('</nav>')
    return '\n'.join(parts)

for ch in chapters:
    # 0-based indexing: line N in editor = index N-1
    content_lines = lines[ch['start']:ch['end']]
    content = ''.join(content_lines)

    # Remove the <h2 class="spaced"> heading since we add our own
    content = re.sub(r'<h2 class="spaced">.*?</h2>\s*', '', content)
    # Remove chapter div wrappers
    content = content.replace('<div class="chapter">', '').replace('</div><!--end chapter-->', '')
    # Clean up pginternal footnote links for Part IV
    content = content.replace('class="pginternal"', '')
    content = content.strip()

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hunger \u2014 {ch['title']}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <a href="index.html" class="home-link">Hunger</a>
    </header>
    <main data-type="novel" data-chapter="{ch['num']}">
        <h1>{ch['title']}</h1>
{content}
    </main>
{nav_html(ch['num'])}
    <script src="app.js"></script>
</body>
</html>'''

    path = f'docs/part-{ch["num"]}.html'
    with open(path, 'w') as f:
        f.write(html)
    print(f'Generated {path} ({len(content_lines)} lines)')

print('Done.')
