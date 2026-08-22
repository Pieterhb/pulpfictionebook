import re
import json
import xml.etree.ElementTree as ET
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = r"c:\googleebook\website\index.html"
SITEMAP_FILE = r"c:\googleebook\website\public\sitemap.xml"
ROBOTS_FILE = r"c:\googleebook\website\public\robots.txt"
CSS_FILE = r"c:\googleebook\website\style.css"
JS_FILE = r"c:\googleebook\website\main.js"

print("="*60)
print("RUNNING TECHNICAL SEO VERIFICATION AUDIT")
print("="*60)

with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Check Font Loading & Preconnects
assert '<link rel="preconnect" href="https://fonts.googleapis.com"/>' in html, "Missing font preconnect"
assert '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>' in html, "Missing font gstatic preconnect"
assert 'fonts.googleapis.com/css2?family=Outfit' in html, "Missing Outfit font stylesheet in head"
print("✅ 1. Asynchronous Google Fonts & Preconnects: PASSED")

# 2. Check CSS @import removal
with open(CSS_FILE, "r", encoding="utf-8") as f:
    css = f.read()
assert '@import url' not in css, "Render-blocking @import found in style.css"
print("✅ 2. CSS Render-Blocking @import Elimination: PASSED")

# 3. Check Meta Tags (Robots, Canonical, OG, Twitter)
assert '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>' in html, "Missing robots directive"
assert '<link rel="canonical" href="https://pdf.softcoverbooks.co.za/"/>' in html, "Missing canonical URL"
assert '<meta property="og:image" content="https://pdf.softcoverbooks.co.za/images/covers/cover_14.jpg"/>' in html, "Missing og:image"
assert '<meta property="og:image:width" content="1200"/>' in html, "Missing og:image:width"
assert '<meta property="og:image:height" content="630"/>' in html, "Missing og:image:height"
assert '<meta name="twitter:card" content="summary_large_image"/>' in html, "Missing twitter:card"
assert '<meta name="twitter:image" content="https://pdf.softcoverbooks.co.za/images/covers/cover_14.jpg"/>' in html, "Missing twitter:image"
print("✅ 3. Robots, Canonical, OpenGraph & Twitter Meta: PASSED")

# 4. Check JSON-LD Structured Data
json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
assert len(json_ld_matches) == 3, f"Expected 3 JSON-LD blocks, found {len(json_ld_matches)}"

schemas = [json.loads(j.strip()) for j in json_ld_matches]
types = [s.get("@type") for s in schemas]
assert "WebSite" in types, "Missing WebSite Schema"
assert "Person" in types, "Missing Person Schema"
assert "ItemList" in types, "Missing ItemList Schema"

# Verify SearchAction in WebSite Schema
ws = next(s for s in schemas if s.get("@type") == "WebSite")
assert "potentialAction" in ws and ws["potentialAction"]["@type"] == "SearchAction", "Missing SearchAction"

# Verify ItemList has 40 series and uses semantic @id (no page-level hash fragment URLs)
il = next(s for s in schemas if s.get("@type") == "ItemList")
assert len(il["itemListElement"]) == 40, f"Expected 40 series in ItemList, found {len(il['itemListElement'])}"
for el in il["itemListElement"]:
    assert "url" not in el, f"Found URL property on ListItem {el} which causes Googlebot fragment discovery errors"
    assert "item" in el and "@id" in el["item"], f"Missing semantic item @id in {el}"
print("✅ 4. Structured Data (JSON-LD WebSite, Person, ItemList x40 with clean semantic @id): PASSED")

# 5. Check Dead Anchors (href="#")
dead_links = re.findall(r'<a\s+[^>]*href="#"[^>]*>', html)
assert len(dead_links) == 0, f"Found {len(dead_links)} dead href='#' links"
print("✅ 5. Internal Link Crawlability (Zero dead href='#' links): PASSED")

# 6. Check Heading Hierarchy in Genre Cards (no h4 skip)
genre_h4 = re.findall(r'<div class="genre-info">\s*<h4>', html)
assert len(genre_h4) == 0, f"Found {len(genre_h4)} h4 tags inside genre-info"
genre_h3 = re.findall(r'<div class="genre-info">\s*<h3>', html)
assert len(genre_h3) == 6, f"Expected 6 h3 genre cards, found {len(genre_h3)}"
print("✅ 6. Semantic Heading Hierarchy (h2 -> h3): PASSED")

# 7. Check Image Dimensions & Loading Attributes
cards = re.findall(r'<article class="book-card".*?>(.*?)</article>', html, re.DOTALL)
assert len(cards) > 500, f"Expected >500 book cards, found {len(cards)}"

missing_dim = 0
missing_aria = 0
for c in cards:
    if 'width="300"' not in c or 'height="450"' not in c:
        missing_dim += 1
    if 'aria-label="View' not in c:
        missing_aria += 1

assert missing_dim == 0, f"Found {missing_dim} images missing explicit dimensions"
assert missing_aria == 0, f"Found {missing_aria} links missing aria-label"
print(f"✅ 7. Image CLS Prevention (width/height on all {len(cards)} covers) & Descriptive Anchor Context: PASSED")

# 8. Check Language Attributes on Sections
sections_with_lang = re.findall(r'<section class="view"[^>]*lang="([a-z]{2})"', html)
assert len(sections_with_lang) >= 38, f"Expected >=38 localized sections, found {len(sections_with_lang)}"
print(f"✅ 8. Internationalization Markup ({len(sections_with_lang)} sections tagged with language codes): PASSED")

# 9. Check Sitemap.xml
tree = ET.parse(SITEMAP_FILE)
root = tree.getroot()
urls = root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
assert len(urls) == 1, f"Expected 1 canonical URL entry in sitemap, found {len(urls)}"

loc = urls[0].find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
assert loc == "https://pdf.softcoverbooks.co.za/", f"Unexpected sitemap loc: {loc}"
assert "#" not in loc, "Hash fragment found in sitemap URL!"

images = urls[0].findall("{http://www.google.com/schemas/sitemap-image/1.1}image")
assert len(images) > 500, f"Expected >500 indexed images in sitemap, found {len(images)}"
print(f"✅ 9. XML Sitemap Google 0.9 & Image 1.1 Specification ({len(images)} images indexed, 0 fragments): PASSED")

# 10. Check Robots.txt
with open(ROBOTS_FILE, "r", encoding="utf-8") as f:
    robots = f.read()
assert "User-agent: *" in robots, "Missing User-agent"
assert "Sitemap: https://pdf.softcoverbooks.co.za/sitemap.xml" in robots, "Missing Sitemap declaration"
print("✅ 10. Robots.txt Syntax & Sitemap Reference: PASSED")

# 11. Check main.js router
with open(JS_FILE, "r", encoding="utf-8") as f:
    js = f.read()
assert "history.pushState" in js, "Missing history.pushState in main.js"
assert "popstate" in js, "Missing popstate listener in main.js"
assert "checkInitialHash" in js, "Missing initial hash deep-linking in main.js"
print("✅ 11. Client-Side Router Deep-Linking & History API: PASSED")

print("="*60)
print("ALL 11 TECHNICAL SEO AUDIT CHECKS PASSED WITH 100% SUCCESS!")
print("="*60)
