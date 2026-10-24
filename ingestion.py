"""
TechPulse AI - Ingestion & Normalizer Engine
Supports:
1. Live arXiv API search (e.g. cs.AI, cs.CR, cs.SE, cs.DC)
2. Live RSS feeds (Hacker News, MIT Tech Review, TechCrunch, ArXiv CS)
3. Content normalization and title/URL deduplication
4. Clearly tags live-retrieved articles (is_live_retrieved = 1) vs sample data
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import feedparser
import re
from datetime import datetime

ARXIV_API_BASE = "http://export.arxiv.org/api/query"

DEFAULT_RSS_FEEDS = [
    {
        "name": "Hacker News Top Tech",
        "url": "https://news.ycombinator.com/rss",
        "category": "Software Engineering",
        "type": "Community News"
    },
    {
        "name": "arXiv Computer Science (cs.AI)",
        "url": "https://rss.arxiv.org/rss/cs.AI",
        "category": "AI/ML",
        "type": "Academic Preprint"
    },
    {
        "name": "arXiv Cryptography & Security (cs.CR)",
        "url": "https://rss.arxiv.org/rss/cs.CR",
        "category": "Cybersecurity",
        "type": "Academic Preprint"
    }
]

def clean_html(raw_html):
    if not raw_html:
        return ""
    clean = re.sub(r'<.*?>', '', raw_html)
    return ' '.join(clean.split())

def fetch_arxiv_papers(query="cat:cs.AI OR cat:cs.CR OR cat:cs.SE", max_results=10):
    """
    Fetches real live research papers directly from arXiv's public API.
    """
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    url = f"{ARXIV_API_BASE}?{urllib.parse.urlencode(params)}"
    articles = []

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'TechPulseAI/1.0 (academic-digest-bot)'})
        with urllib.request.urlopen(req, timeout=12) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        # Atom namespace
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text
            title = ' '.join(title.split()) if title else "Untitled arXiv Paper"

            summary = entry.find('atom:summary', ns).text
            summary = ' '.join(summary.split()) if summary else ""

            id_elem = entry.find('atom:id', ns)
            paper_url = id_elem.text if id_elem is not None else ""

            published = entry.find('atom:published', ns)
            published_at = published.text[:10] if published is not None else datetime.now().strftime("%Y-%m-%d")

            authors_list = []
            for author in entry.findall('atom:author', ns):
                name = author.find('atom:name', ns)
                if name is not None and name.text:
                    authors_list.append(name.text)
            authors = ", ".join(authors_list[:3])
            if len(authors_list) > 3:
                authors += " et al."

            # Category inference
            category = "AI/ML"
            summary_lower = (title + " " + summary).lower()
            if any(k in summary_lower for k in ["security", "cryptograph", "attack", "vulnerability", "malware"]):
                category = "Cybersecurity"
            elif any(k in summary_lower for k in ["software", "compiler", "debugging", "testing", "refactor"]):
                category = "Software Engineering"
            elif any(k in summary_lower for k in ["cloud", "distributed", "serverless", "kubernetes", "rpc"]):
                category = "Cloud Computing"
            elif any(k in summary_lower for k in ["dataset", "clustering", "database", "analytics", "graph"]):
                category = "Data Science"
            elif any(k in summary_lower for k in ["quantum", "photonic", "neuromorphic", "robotics"]):
                category = "Emerging Technology"

            articles.append({
                "title": title,
                "abstract": summary,
                "content": summary,
                "url": paper_url,
                "source_name": "arXiv.org",
                "authors": authors or "arXiv Researcher",
                "category": category,
                "published_at": published_at,
                "is_live_retrieved": 1
            })
    except Exception as e:
        print(f"Error fetching from arXiv API: {e}")

    return articles

def fetch_rss_feed(feed_url, feed_name="RSS Tech Feed", category="Software Engineering", max_items=8):
    """
    Parses a live RSS feed and normalizes items into TechPulse articles.
    """
    articles = []
    try:
        parsed = feedparser.parse(feed_url)
        for entry in parsed.entries[:max_items]:
            title = entry.get('title', 'Untitled News')
            link = entry.get('link', '')
            summary = clean_html(entry.get('summary', '') or entry.get('description', ''))
            published = entry.get('published', '') or datetime.now().strftime("%Y-%m-%d")
            # Try to format date
            try:
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
            except Exception:
                pass

            author = entry.get('author', feed_name)

            articles.append({
                "title": title,
                "abstract": summary[:600] if summary else f"Reported by {feed_name}.",
                "content": summary,
                "url": link,
                "source_name": feed_name,
                "authors": author,
                "category": category,
                "published_at": str(published)[:10],
                "is_live_retrieved": 1
            })
    except Exception as e:
        print(f"Error parsing RSS feed {feed_url}: {e}")

    return articles
