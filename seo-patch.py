#!/usr/bin/env python3
"""Patch all a290.wiki pages with SEO improvements."""
import os
import re
import json
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

# Page metadata: (path, meta_description, og_title)
PAGES = {
    "index.html": {
        "desc": "The unofficial Alpine A290 knowledge base. Owner tips, charging guides, troubleshooting, specs, accessories and community links.",
        "og_title": "Alpine A290 Knowledge Base",
        "path": "/",
        "fr_path": "/fr/",
    },
    "prospective-owner/index.html": {
        "desc": "Everything you need to know before buying an Alpine A290. Pricing, model differences (GT vs GTS), real world range, and honest first impressions from owners.",
        "og_title": "Things a Prospective Owner Should Know – Alpine A290",
        "path": "/prospective-owner/",
        "fr_path": "/fr/prospective-owner/",
    },
    "new-owner/index.html": {
        "desc": "Just got your Alpine A290? Delivery checks, app setup, charging tips and first week essentials from experienced owners.",
        "og_title": "New Owner Guide – Alpine A290",
        "path": "/new-owner/",
        "fr_path": "/fr/new-owner/",
    },
    "how-to/index.html": {
        "desc": "Alpine A290 how-to guides: charge efficiently, maximise range, unlock hidden features and customise your dashboard.",
        "og_title": "How To Guides – Alpine A290",
        "path": "/how-to/",
        "fr_path": "/fr/how-to/",
    },
    "troubleshooting/index.html": {
        "desc": "Fix common Alpine A290 problems: charging failures, app issues, electrical glitches, mechanical faults and paint concerns.",
        "og_title": "Troubleshooting – Alpine A290",
        "path": "/troubleshooting/",
        "fr_path": "/fr/troubleshooting/",
    },
    "reference/index.html": {
        "desc": "Alpine A290 specifications, charging curve data, real world running costs, service intervals and MY26 changes.",
        "og_title": "Reference & Specs – Alpine A290",
        "path": "/reference/",
        "fr_path": "/fr/reference/",
    },
    "accessories/index.html": {
        "desc": "Best Alpine A290 accessories and mods: home chargers, dashcams, cup holders, wheels, styling parts and compatible suppliers.",
        "og_title": "Accessories & Mods – Alpine A290",
        "path": "/accessories/",
        "fr_path": "/fr/accessories/",
    },
    "communities/index.html": {
        "desc": "Alpine A290 owner communities: Facebook groups, forums, PistonHeads threads and social media channels.",
        "og_title": "Communities – Alpine A290",
        "path": "/communities/",
        "fr_path": "/fr/communities/",
    },
}

# French pages
FR_PAGES = {
    "fr/index.html": {
        "desc": "La base de connaissances non officielle de l'Alpine A290. Conseils, guides de recharge, dépannage, spécifications et accessoires.",
        "og_title": "Base de connaissances Alpine A290",
        "path": "/fr/",
        "en_path": "/",
    },
    "fr/prospective-owner/index.html": {
        "desc": "Tout ce qu'il faut savoir avant d'acheter une Alpine A290. Prix, différences entre modèles, autonomie réelle et premières impressions.",
        "og_title": "Futur propriétaire – Alpine A290",
        "path": "/fr/prospective-owner/",
        "en_path": "/prospective-owner/",
    },
    "fr/new-owner/index.html": {
        "desc": "Vous venez de recevoir votre Alpine A290 ? Vérifications à la livraison, configuration de l'app et conseils pour la première semaine.",
        "og_title": "Nouveau propriétaire – Alpine A290",
        "path": "/fr/new-owner/",
        "en_path": "/new-owner/",
    },
    "fr/how-to/index.html": {
        "desc": "Guides pratiques Alpine A290 : charger efficacement, maximiser l'autonomie, fonctions cachées et personnalisation du tableau de bord.",
        "og_title": "Guides pratiques – Alpine A290",
        "path": "/fr/how-to/",
        "en_path": "/how-to/",
    },
    "fr/troubleshooting/index.html": {
        "desc": "Résoudre les problèmes courants de l'Alpine A290 : recharge, application, électrique, mécanique et carrosserie.",
        "og_title": "Dépannage – Alpine A290",
        "path": "/fr/troubleshooting/",
        "en_path": "/troubleshooting/",
    },
    "fr/reference/index.html": {
        "desc": "Spécifications Alpine A290, courbe de recharge, coûts réels, entretien et changements MY26.",
        "og_title": "Référence & Spécifications – Alpine A290",
        "path": "/fr/reference/",
        "en_path": "/reference/",
    },
    "fr/accessories/index.html": {
        "desc": "Accessoires et modifications Alpine A290 : chargeurs, dashcams, porte-gobelets, jantes et fournisseurs compatibles.",
        "og_title": "Accessoires & Modifications – Alpine A290",
        "path": "/fr/accessories/",
        "en_path": "/accessories/",
    },
    "fr/communities/index.html": {
        "desc": "Communautés de propriétaires Alpine A290 : groupes Facebook, forums et réseaux sociaux.",
        "og_title": "Communautés – Alpine A290",
        "path": "/fr/communities/",
        "en_path": "/communities/",
    },
}

OG_IMAGE = "https://a290.wiki/images/a290-hero.png"
SITE_NAME = "a290.wiki"
TODAY = datetime.now().strftime("%Y-%m-%d")


def build_seo_tags(meta, lang="en"):
    """Build the SEO meta tags to inject after the og:description line."""
    url = f"https://a290.wiki{meta['path']}"
    tags = []
    
    # Standard meta description
    tags.append(f'<meta name="description" content="{meta["desc"]}" />')
    
    # Complete Open Graph
    tags.append(f'<meta property="og:title" content="{meta["og_title"]}" />')
    tags.append(f'<meta property="og:type" content="website" />')
    tags.append(f'<meta property="og:url" content="{url}" />')
    tags.append(f'<meta property="og:image" content="{OG_IMAGE}" />')
    tags.append(f'<meta property="og:site_name" content="{SITE_NAME}" />')
    
    # Twitter Card
    tags.append(f'<meta name="twitter:card" content="summary_large_image" />')
    tags.append(f'<meta name="twitter:title" content="{meta["og_title"]}" />')
    tags.append(f'<meta name="twitter:description" content="{meta["desc"]}" />')
    tags.append(f'<meta name="twitter:image" content="{OG_IMAGE}" />')
    
    # Canonical
    tags.append(f'<link rel="canonical" href="{url}" />')
    
    # Hreflang
    if lang == "en":
        en_url = url
        fr_url = f"https://a290.wiki{meta['fr_path']}"
    else:
        en_url = f"https://a290.wiki{meta['en_path']}"
        fr_url = url
    
    tags.append(f'<link rel="alternate" hreflang="en" href="{en_url}" />')
    tags.append(f'<link rel="alternate" hreflang="fr" href="{fr_url}" />')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{en_url}" />')
    
    return "".join(tags)


def build_website_jsonld():
    """JSON-LD for the homepage."""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Alpine A290 Knowledge Base",
        "url": "https://a290.wiki",
        "description": "The unofficial Alpine A290 knowledge base. Owner tips, charging guides, troubleshooting, specs and accessories.",
        "inLanguage": ["en", "fr"],
    }, separators=(',', ':'))


def build_faq_jsonld(page_path):
    """Build FAQPage JSON-LD from the troubleshooting page content."""
    filepath = os.path.join(BASE, page_path)
    with open(filepath, 'r') as f:
        html = f.read()
    
    faqs = []
    # Extract Q&A pairs from bold text patterns
    # Pattern: <strong>Question:</strong> Answer text
    pattern = r'<p><strong>(.*?)</strong>\s*(.*?)</p>'
    matches = re.findall(pattern, html)
    
    for q, a in matches:
        # Clean HTML tags from answer
        q_clean = re.sub(r'<[^>]+>', '', q).strip().rstrip(':')
        a_clean = re.sub(r'<[^>]+>', '', a).strip()
        if a_clean and len(q_clean) > 10:
            faqs.append({
                "@type": "Question",
                "name": q_clean,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a_clean
                }
            })
    
    if not faqs:
        return None
    
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faqs[:10]  # Cap at 10 for readability
    }, separators=(',', ':'))


def patch_page(filepath, meta, lang="en", jsonld=None):
    """Inject SEO tags into a page."""
    with open(filepath, 'r') as f:
        html = f.read()
    
    seo_tags = build_seo_tags(meta, lang)
    
    # Insert after the og:description meta tag
    og_pattern = r'(<meta content="[^"]*" property="og:description" />)'
    match = re.search(og_pattern, html)
    if not match:
        print(f"  ⚠️  No og:description found in {filepath}")
        return False
    
    # Check if already patched
    if '<meta name="description"' in html:
        print(f"  ⏭️  Already patched: {filepath}")
        return False
    
    insert_point = match.end()
    new_html = html[:insert_point] + seo_tags + html[insert_point:]
    
    # Add JSON-LD before </body>
    if jsonld:
        jsonld_tag = f'<script type="application/ld+json">{jsonld}</script>'
        new_html = new_html.replace('</body>', f'{jsonld_tag}</body>')
    
    with open(filepath, 'w') as f:
        f.write(new_html)
    
    print(f"  ✅ Patched: {filepath}")
    return True


def update_sitemap():
    """Add lastmod to sitemap entries."""
    sitemap_path = os.path.join(BASE, 'sitemap.xml')
    with open(sitemap_path, 'r') as f:
        content = f.read()
    
    # Add lastmod after each priority tag
    content = re.sub(
        r'(</priority>)',
        f'\\1<lastmod>{TODAY}</lastmod>',
        content
    )
    
    with open(sitemap_path, 'w') as f:
        f.write(content)
    
    print(f"  ✅ Sitemap updated with lastmod={TODAY}")


def main():
    print("🔧 A290 Wiki SEO Patch\n")
    
    # Patch EN pages
    print("English pages:")
    for page, meta in PAGES.items():
        filepath = os.path.join(BASE, page)
        jsonld = None
        if page == "index.html":
            jsonld = build_website_jsonld()
        elif page == "troubleshooting/index.html":
            jsonld = build_faq_jsonld(page)
        elif page == "how-to/index.html":
            jsonld = build_faq_jsonld(page)
        patch_page(filepath, meta, "en", jsonld)
    
    # Patch FR pages
    print("\nFrench pages:")
    for page, meta in FR_PAGES.items():
        filepath = os.path.join(BASE, page)
        patch_page(filepath, meta, "fr")
    
    # Update sitemap
    print("\nSitemap:")
    update_sitemap()
    
    print("\n✅ Done! Review changes with: cd ~/Projects/a290/website-v2 && git diff")


if __name__ == "__main__":
    main()
