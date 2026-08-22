import re
import json

HTML_PATH = r"c:\googleebook\website\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update <head> tags
# Define JSON-LD Schemas
website_schema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Iconic Vintage Pulp Fiction",
    "url": "https://pdf.softcoverbooks.co.za/",
    "description": "Discover 500+ iconic vintage pulp fiction adventure, mystery, and sci-fi eBooks across 40 classic series.",
    "potentialAction": {
        "@type": "SearchAction",
        "target": {
            "@type": "EntryPoint",
            "urlTemplate": "https://pdf.softcoverbooks.co.za/?q={search_term_string}"
        },
        "query-input": "required name=search_term_string"
    }
}

person_schema = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Pieter Haasbroek",
    "url": "https://pdf.softcoverbooks.co.za/",
    "description": "Retired scientist, passionate book collector, and digital archivist of classic South African pulp fiction and adventure eBooks.",
    "sameAs": [
        "https://panther-ebooks.com",
        "https://www.softcoverbooks.co.za"
    ]
}

series_list = [
    {"name": "Sahara Avontuur Reeks", "id": "sahara-avontuur-reeks", "lang": "af", "books": 41},
    {"name": "Sahara Adventure Series", "id": "sahara-adventure-series", "lang": "en", "books": 41},
    {"name": "Serie Aventure Sahara (French)", "id": "serie-aventure-sahara-french", "lang": "fr", "books": 1},
    {"name": "Serie Avventure Sahara (Italian)", "id": "serie-avventure-sahara-italian", "lang": "it", "books": 1},
    {"name": "Sahara Abenteuer Reine (German)", "id": "sahara-abenteuer-reine-german", "lang": "de", "books": 1},
    {"name": "Serie Aventure Sahara (Spanish)", "id": "serie-aventure-sahara-spanish", "lang": "es", "books": 1},
    {"name": "Die Buiter Reeks", "id": "die-buiter-reeks", "lang": "af", "books": 10},
    {"name": "The Masked Robber Series", "id": "the-masked-robber-series", "lang": "en", "books": 10},
    {"name": "Die Swart Luiperd Reeks", "id": "die-swart-luiperd-reeks", "lang": "af", "books": 71},
    {"name": "The Black Leopard Series", "id": "the-black-leopard-series", "lang": "en", "books": 9},
    {"name": "Oloff die Seerower Reeks", "id": "oloff-die-seerower-reeks", "lang": "af", "books": 25},
    {"name": "Oloff the Pirate Series", "id": "oloff-the-pirate-series", "lang": "en", "books": 25},
    {"name": "Woeste Laeveld Reeks", "id": "woeste-laeveld-reeks", "lang": "af", "books": 8},
    {"name": "Untamed Lowveld Series", "id": "wild-lowveld-series", "lang": "en", "books": 8},
    {"name": "Oerwoudvalk Reeks", "id": "oerwoudvalk-reeks", "lang": "af", "books": 8},
    {"name": "Jungle Hawk Series", "id": "jungle-hawk-series", "lang": "en", "books": 8},
    {"name": "SA Polisie Reeks", "id": "sa-polisie-reeks", "lang": "af", "books": 30},
    {"name": "SA Police Series", "id": "sa-police-series", "lang": "en", "books": 12},
    {"name": "Sahara Reeks", "id": "sahara-reeks", "lang": "af", "books": 13},
    {"name": "Sahara Series", "id": "sahara-series", "lang": "en", "books": 13},
    {"name": "Maagd van die See Reeks", "id": "maagd-van-die-see-reeks", "lang": "af", "books": 10},
    {"name": "Red Ruby Series", "id": "red-ruby-series", "lang": "en", "books": 10},
    {"name": "Tamar Reeks", "id": "tamar-reeks", "lang": "af", "books": 2},
    {"name": "Tamar Series", "id": "tamar-series", "lang": "en", "books": 2},
    {"name": "Swerwer Speurder Reeks", "id": "swerwer-speurder-reeks", "lang": "af", "books": 16},
    {"name": "Wanderer Detective Series", "id": "wanderer-detective-series", "lang": "en", "books": 9},
    {"name": "Ryk Schoonraad Reeks", "id": "ryk-schoonraad-reeks", "lang": "af", "books": 4},
    {"name": "Ryk Schoonraad Series", "id": "ryk-schoonraad-series", "lang": "en", "books": 4},
    {"name": "Jaap Zeeman Reeks", "id": "jaap-zeeman-reeks", "lang": "af", "books": 6},
    {"name": "Ruimte Reeks", "id": "ruimte-reeks", "lang": "af", "books": 5},
    {"name": "Henk Human Reeks", "id": "henk-human-reeks", "lang": "af", "books": 6},
    {"name": "Simon Rand Reeks", "id": "simon-rand-reeks", "lang": "af", "books": 7},
    {"name": "Spioenasie Reeks", "id": "spioenasie-reeks", "lang": "af", "books": 6},
    {"name": "Temmers van die Woestyn Reeks", "id": "temmers-van-die-woestyn-reeks", "lang": "af", "books": 39},
    {"name": "AI Stories", "id": "ai-stories", "lang": "en", "books": 3},
    {"name": "Enkel Stories", "id": "enkel-stories", "lang": "af", "books": 11},
    {"name": "Single Stories", "id": "single-stories", "lang": "en", "books": 9},
    {"name": "Pieter Haasbroek Stories", "id": "pieter-haasbroek-stories", "lang": "en", "books": 7},
    {"name": "Christo Malan Stories", "id": "other", "lang": "af", "books": 1},
    {"name": "Social Media", "id": "social-media", "lang": "en", "books": 24}
]

item_list_schema = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "Vintage Pulp Fiction Book Series Collection",
    "numberOfItems": len(series_list),
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": idx + 1,
            "name": s["name"],
            "item": {
                "@type": "BookSeries",
                "name": s["name"],
                "inLanguage": s["lang"],
                "@id": f"https://pdf.softcoverbooks.co.za/#{s['id']}"
            }
        }
        for idx, s in enumerate(series_list)
    ]
}

new_head_meta = f"""<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9JCF3S70W7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-9JCF3S70W7');
</script>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>🔥 Iconic Vintage Pulp Fiction | 500+ Classic Adventure eBooks</title>
<meta name="description" content="Discover 500+ iconic vintage pulp fiction adventure, mystery, and sci-fi eBooks across 40 classic series."/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>
<link rel="canonical" href="https://pdf.softcoverbooks.co.za/"/>
<link href="/favicon.svg" rel="icon" type="image/svg+xml"/>

<!-- Preconnect & Asynchronous Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&amp;display=swap" rel="stylesheet"/>

<!-- Open Graph / Facebook / WhatsApp -->
<meta property="og:type" content="website"/>
<meta property="og:url" content="https://pdf.softcoverbooks.co.za/"/>
<meta property="og:title" content="🔥 Iconic Vintage Pulp Fiction | 500+ Classic Adventure eBooks"/>
<meta property="og:description" content="Discover 500+ iconic vintage pulp fiction adventure, mystery, and sci-fi eBooks across 40 classic series."/>
<meta property="og:image" content="https://pdf.softcoverbooks.co.za/images/covers/cover_14.jpg"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:image:alt" content="Iconic Vintage Pulp Fiction eBook Collection"/>
<meta property="og:site_name" content="Iconic Vintage Pulp Fiction"/>
<meta property="og:locale" content="en_US"/>

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:url" content="https://pdf.softcoverbooks.co.za/"/>
<meta name="twitter:title" content="🔥 Iconic Vintage Pulp Fiction | 500+ Classic Adventure eBooks"/>
<meta name="twitter:description" content="Discover 500+ iconic vintage pulp fiction adventure, mystery, and sci-fi eBooks across 40 classic series."/>
<meta name="twitter:image" content="https://pdf.softcoverbooks.co.za/images/covers/cover_14.jpg"/>

<!-- JSON-LD Structured Data -->
<script type="application/ld+json">
{json.dumps(website_schema, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(person_schema, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(item_list_schema, indent=2)}
</script>

<link href="/style.css" rel="stylesheet"/>
</head>"""

# Replace <head>...</head>
html = re.sub(r'<head>.*?</head>', new_head_meta, html, flags=re.DOTALL)

# 2. Replace all dead anchor links with semantic anchor targets:
# data-target="X" href="#" -> data-target="X" href="#X"
def replace_href(m):
    full = m.group(0)
    # Check if has data-target
    dt_match = re.search(r'data-target="([^"]+)"', full)
    if dt_match:
        target = dt_match.group(1)
        # replace href="#" with href="#{target}"
        full = re.sub(r'href="#"', f'href="#{target}"', full)
    return full

html = re.sub(r'<a\s+[^>]*href="#"[^>]*>', replace_href, html)
html = re.sub(r'<a\s+[^>]*data-target="[^"]+"[^>]*>', replace_href, html)

# 3. Fix heading hierarchy in Genre cards: <h4> -> <h3>
def fix_genre_h4(m):
    content = m.group(0)
    content = content.replace('<h4>', '<h3>').replace('</h4>', '</h3>')
    return content

html = re.sub(r'<div class="genre-info">.*?</div>', fix_genre_h4, html, flags=re.DOTALL)

# 4. Add lang attributes to sections based on series language mapping
series_lang_map = {s['id']: s['lang'] for s in series_list}

def add_section_lang(m):
    sec_tag = m.group(0)
    id_match = re.search(r'id="([^"]+)"', sec_tag)
    if id_match:
        sec_id = id_match.group(1)
        lang = series_lang_map.get(sec_id)
        if lang and 'lang=' not in sec_tag:
            sec_tag = sec_tag.replace('>', f' lang="{lang}">')
    return sec_tag

html = re.sub(r'<section\s+class="view"[^>]*>', add_section_lang, html)

# 5. Enhance book cards with image width/height/decoding and aria-labels on CTA buttons
def enhance_book_card(m):
    card = m.group(0)
    
    # Extract title
    title_match = re.search(r'<h3>(.*?)</h3>', card)
    title = title_match.group(1).strip() if title_match else "Book"
    clean_title = re.sub(r'[<>&"\']', '', title)
    
    # Enhance <img>: add width="300" height="450" decoding="async" if not present
    def enhance_img(img_m):
        img_tag = img_m.group(0)
        if 'width=' not in img_tag:
            img_tag = img_tag.replace('<img ', '<img width="300" height="450" decoding="async" ')
        return img_tag
    card = re.sub(r'<img\s+[^>]+>', enhance_img, card)
    
    # Enhance <a class="btn btn-primary" ...>: add aria-label
    def enhance_link(link_m):
        link_tag = link_m.group(0)
        if 'aria-label=' not in link_tag:
            link_tag = link_tag.replace('<a ', f'<a aria-label="View {clean_title} on store" ')
        return link_tag
    card = re.sub(r'<a\s+class="btn\s+btn-primary"[^>]+>', enhance_link, card)
    
    return card

html = re.sub(r'<article class="book-card">.*?</article>', enhance_book_card, html, flags=re.DOTALL)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Applied SEO enhancements to website/index.html successfully!")
