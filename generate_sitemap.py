import re
from datetime import datetime

BASE_URL = "https://pdf.softcoverbooks.co.za"

with open(r"c:\googleebook\website\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Extract all data-target section IDs from the sidebar
section_matches = re.findall(r'data-target="([^"]+)"', html)
seen = set()
sections = []
for s in section_matches:
    if s not in seen and s != "home":
        seen.add(s)
        sections.append(s)

# Extract book cards
card_blocks = re.findall(r'<article class="book-card">(.*?)</article>', html, re.DOTALL)
books = []

for block in card_blocks:
    img_match = re.search(r'<img[^>]+src="([^"]+)"', block)
    alt_match = re.search(r'<img[^>]+alt="([^"]*)"', block)
    title_match = re.search(r'<h3>(.*?)</h3>', block)
    author_match = re.search(r'<p class="author">By (.*?)</p>', block)
    
    img_src = img_match.group(1) if img_match else ""
    alt_text = alt_match.group(1) if alt_match else ""
    title = title_match.group(1) if title_match else ""
    author = author_match.group(1) if author_match else "Pieter Haasbroek"
    
    if title:
        books.append({
            "img": img_src,
            "alt": alt_text,
            "title": title,
            "author": author
        })

print(f"Found {len(sections)} sections and {len(books)} books.")

now_date = datetime.now().strftime("%Y-%m-%d")

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
    '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    '  <!-- Main Homepage & Full Library -->',
    '  <url>',
    f'    <loc>{BASE_URL}/</loc>',
    f'    <lastmod>{now_date}</lastmod>',
    '    <changefreq>weekly</changefreq>',
    '    <priority>1.0</priority>'
]

def escape_xml(s):
    return re.sub(r'[<>&"\']', lambda m: {'<':'&lt;', '>':'&gt;', '&':'&amp;', '"':'&quot;', "'":'&apos;'}[m.group(0)], s)

for b in books:
    if not b["img"]:
        continue
    img_src = b["img"]
    full_img_url = f"{BASE_URL}{img_src}" if img_src.startswith("/") else f"{BASE_URL}/{img_src}"
    clean_title = escape_xml(b["title"].strip())
    clean_author = escape_xml(b["author"].strip())
    clean_alt = escape_xml(b["alt"].strip()) or clean_title

    xml_lines.append('    <image:image>')
    xml_lines.append(f'      <image:loc>{full_img_url}</image:loc>')
    xml_lines.append(f'      <image:title>{clean_title} - By {clean_author}</image:title>')
    xml_lines.append(f'      <image:caption>{clean_alt}</image:caption>')
    xml_lines.append('    </image:image>')

xml_lines.append('  </url>')

# Category sections
for sec in sections:
    xml_lines.append('  <url>')
    xml_lines.append(f'    <loc>{BASE_URL}/#{sec}</loc>')
    xml_lines.append(f'    <lastmod>{now_date}</lastmod>')
    xml_lines.append('    <changefreq>monthly</changefreq>')
    xml_lines.append('    <priority>0.8</priority>')
    xml_lines.append('  </url>')

xml_lines.append('</urlset>')

sitemap_content = "\n".join(xml_lines)

with open(r"c:\googleebook\website\public\sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)

print(f"Generated website/public/sitemap.xml ({len(sitemap_content):,} bytes, {len(books)} book images indexed)")

# Robots.txt
robots_content = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""

with open(r"c:\googleebook\website\public\robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_content)

print("Generated website/public/robots.txt")
