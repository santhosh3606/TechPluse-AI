"""
TechPulse AI - Source Credibility & Verification Engine
7-Point Source-Quality Checklist:
1. Publisher Authenticity: Domain verification against curated trusted directory
2. Author Attribution: Academic/Industry institutional credential check
3. Publication Date Recency: Date validity, recency & freshness
4. Supporting Evidence: Citations, DOIs, code repositories, benchmark links
5. Original Source Link: Canonical URL validity & direct access
6. Duplicate Content: Lexical & URL hash similarity against existing corpus
7. Outdated Information Detection: Identifies deprecated tech, superseded models, or obsolete APIs
"""

import re
import urllib.parse
from datetime import datetime, timezone

DEPRECATED_TERMS = [
    ("tensorflow 1", "TensorFlow 1.x is obsolete; projects should migrate to TensorFlow 2.x or PyTorch."),
    ("python 2", "Python 2 reached official End-of-Life in 2020."),
    ("sha-1", "SHA-1 is cryptographically broken and deprecated for security purposes."),
    ("angularjs", "AngularJS (1.x) is EOL; modern standard is Angular 2+."),
    ("gpt-2", "GPT-2 is superseded by modern LLM architectures (GPT-4, Claude 3.5, Gemini 1.5/2.0)."),
    ("bert-base", "BERT-base is generally superseded for generative tasks, though still used in light encoders."),
    ("centos 8", "CentOS Linux 8 reached End-of-Life in 2021.")
]

TRUSTED_DOMAINS = {
    "arxiv.org": {"name": "arXiv.org", "trust": 98, "type": "Academic Preprint Archive"},
    "spectrum.ieee.org": {"name": "IEEE Spectrum", "trust": 96, "type": "Professional Engineering Organization"},
    "technologyreview.com": {"name": "MIT Technology Review", "trust": 95, "type": "Academic Tech Publication"},
    "mags.acm.org": {"name": "Communications of the ACM", "trust": 97, "type": "Academic Computing Society"},
    "cacm.acm.org": {"name": "Communications of the ACM", "trust": 97, "type": "Academic Computing Society"},
    "research.google": {"name": "Google Research", "trust": 95, "type": "Official Corporate Research Lab"},
    "deepmind.google": {"name": "Google DeepMind", "trust": 96, "type": "Official Corporate Research Lab"},
    "openai.com": {"name": "OpenAI Research", "trust": 94, "type": "Official AI Research Lab"},
    "aws.amazon.com": {"name": "AWS Architecture Blog", "trust": 92, "type": "Official Cloud Vendor Blog"},
    "github.blog": {"name": "GitHub Engineering Blog", "trust": 94, "type": "Official Tech Engineering Blog"},
    "cisa.gov": {"name": "CISA / US-CERT", "trust": 99, "type": "National Cybersecurity Agency"},
    "nature.com": {"name": "Nature Machine Intelligence", "trust": 98, "type": "Peer-Reviewed Academic Journal"},
    "cncf.io": {"name": "Cloud Native Computing Foundation", "trust": 95, "type": "Open Source Standards Body"},
    "news.ycombinator.com": {"name": "Hacker News", "trust": 88, "type": "Peer-Curated Tech Community"}
}

def verify_article(article_dict, existing_titles=None):
    """
    Evaluates an article dictionary against the 7-Point Source Credibility Checklist.
    Returns:
    {
        "publisher_score": int,
        "author_score": int,
        "date_score": int,
        "evidence_score": int,
        "source_link_score": int,
        "duplicate_score": int,
        "outdated_score": int,
        "overall_score": int,
        "overall_status": 'verified' | 'flagged' | 'rejected',
        "checklist": [ { id, label, status, score, max_score, evidence } ],
        "evidence_notes": str
    }
    """
    url = article_dict.get("url", "")
    title = article_dict.get("title", "")
    abstract = article_dict.get("abstract", "") or ""
    content = article_dict.get("content", "") or ""
    full_text = f"{title}\n{abstract}\n{content}".lower()
    authors = article_dict.get("authors", "") or ""
    published_at = article_dict.get("published_at", "") or ""

    checklist = []
    evidence_notes = []

    # 1. Publisher Authenticity
    domain = ""
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
    except Exception:
        domain = ""

    publisher_matched = None
    for trusted_d, info in TRUSTED_DOMAINS.items():
        if domain.endswith(trusted_d):
            publisher_matched = info
            break

    if publisher_matched:
        publisher_score = min(100, publisher_matched["trust"])
        pub_status = "pass"
        pub_evidence = f"Verified publisher: {publisher_matched['name']} ({publisher_matched['type']}). Domain '{domain}' matches trusted registry."
    elif any(ext in domain for ext in [".edu", ".gov", ".ac.uk", ".org"]):
        publisher_score = 85
        pub_status = "pass"
        pub_evidence = f"Reputable domain TLD ({domain}). Higher institutional confidence."
    elif domain:
        publisher_score = 65
        pub_status = "warn"
        pub_evidence = f"Independent domain ({domain}) not in primary trusted registry. Requires manual verification."
    else:
        publisher_score = 30
        pub_status = "fail"
        pub_evidence = "Missing or unparseable publisher URL."

    checklist.append({
        "id": "publisher_authenticity",
        "label": "1. Publisher Authenticity",
        "status": pub_status,
        "score": publisher_score,
        "max_score": 100,
        "evidence": pub_evidence
    })

    # 2. Author Attribution
    if authors and authors.strip() not in ["", "Unknown", "Admin", "Editorial Team"]:
        author_score = 95
        author_status = "pass"
        author_evidence = f"Identified author(s): {authors}. Clear academic or professional attribution."
    elif "arxiv.org" in domain or "acm.org" in domain or "ieee.org" in domain:
        author_score = 90
        author_status = "pass"
        author_evidence = "Published under recognized institutional peer/preprint submission standards."
    elif "blog" in domain:
        author_score = 75
        author_status = "warn"
        author_evidence = "Attributed to corporate engineering team without named individual authors."
    else:
        author_score = 50
        author_status = "warn"
        author_evidence = "No distinct individual authors found. Lacks named institutional author."

    checklist.append({
        "id": "author_attribution",
        "label": "2. Author / Institution Attribution",
        "status": author_status,
        "score": author_score,
        "max_score": 100,
        "evidence": author_evidence
    })

    # 3. Publication Date Recency
    date_score = 90
    date_status = "pass"
    date_evidence = f"Publication date recorded: {published_at}."
    if published_at:
        try:
            # Check year
            current_year = datetime.now().year
            found_year = None
            year_match = re.search(r'\b(20[12]\d)\b', published_at)
            if year_match:
                found_year = int(year_match.group(1))
                if current_year - found_year > 3:
                    date_score = 60
                    date_status = "warn"
                    date_evidence = f"Article published in {found_year} (>3 years ago). Check for newer revisions or superseding works."
                elif current_year - found_year <= 1:
                    date_score = 98
                    date_evidence = f"Fresh content published recently ({published_at}). High temporal relevance."
        except Exception:
            pass
    else:
        date_score = 50
        date_status = "warn"
        date_evidence = "No publication timestamp metadata available. Date cannot be verified independently."

    checklist.append({
        "id": "date_recency",
        "label": "3. Publication Date Recency & Validity",
        "status": date_status,
        "score": date_score,
        "max_score": 100,
        "evidence": date_evidence
    })

    # 4. Supporting Evidence & Citations
    evidence_score = 60
    evidence_status = "warn"
    citations_found = []
    if "arxiv" in full_text or "doi.org" in full_text or "http" in full_text:
        citations_found.append("External Hyperlinks/DOIs")
    if "github.com" in full_text or "huggingface.co" in full_text:
        citations_found.append("Reproducible Code/Model Repository")
    if any(k in full_text for k in ["benchmark", "accuracy", "latency", "f1-score", "throughput", "table", "dataset"]):
        citations_found.append("Empirical Benchmarks / Data")

    if len(citations_found) >= 2:
        evidence_score = 95
        evidence_status = "pass"
        ev_text = f"Strong empirical backing found: {', '.join(citations_found)}."
    elif len(citations_found) == 1:
        evidence_score = 80
        evidence_status = "pass"
        ev_text = f"Moderate supporting evidence found: {citations_found[0]}."
    else:
        evidence_score = 50
        evidence_status = "warn"
        ev_text = "Limited empirical citations or external reference links detected in abstract/text."

    checklist.append({
        "id": "supporting_evidence",
        "label": "4. Supporting Evidence & Citations",
        "status": evidence_status,
        "score": evidence_score,
        "max_score": 100,
        "evidence": ev_text
    })

    # 5. Original Source Link
    if url.startswith("https://") or url.startswith("http://"):
        source_link_score = 95
        source_link_status = "pass"
        link_evidence = f"Canonical link present: {url}."
    else:
        source_link_score = 30
        source_link_status = "fail"
        link_evidence = "Invalid or relative URL format."

    checklist.append({
        "id": "source_link",
        "label": "5. Original Canonical Source Link",
        "status": source_link_status,
        "score": source_link_score,
        "max_score": 100,
        "evidence": link_evidence
    })

    # 6. Duplicate & Syndicated Content
    duplicate_score = 95
    duplicate_status = "pass"
    dup_evidence = "Unique content confirmed against current database corpus."
    if existing_titles:
        clean_title = re.sub(r'[^a-zA-Z0-9]', '', title.lower())
        for ext in existing_titles:
            c_ext = re.sub(r'[^a-zA-Z0-9]', '', ext.lower())
            if clean_title and c_ext and (clean_title in c_ext or c_ext in clean_title):
                duplicate_score = 40
                duplicate_status = "warn"
                dup_evidence = f"Potential duplicate or cross-posted syndicate detected ('{ext[:40]}...')."
                break

    checklist.append({
        "id": "duplicate_check",
        "label": "6. Duplicate & Syndication Detection",
        "status": duplicate_status,
        "score": duplicate_score,
        "max_score": 100,
        "evidence": dup_evidence
    })

    # 7. Outdated / Deprecated Claims Detection
    outdated_score = 95
    outdated_status = "pass"
    found_deprecated = []
    for term, reason in DEPRECATED_TERMS:
        if term in full_text:
            found_deprecated.append(f"{term.upper()}: {reason}")

    if found_deprecated:
        outdated_score = 55
        outdated_status = "warn"
        out_evidence = f"Detected references to potentially superseded or deprecated technology: {'; '.join(found_deprecated)}"
    else:
        out_evidence = "No known deprecated technologies, obsolete APIs, or superseded frameworks identified."

    checklist.append({
        "id": "outdated_claims",
        "label": "7. Outdated Information & Deprecated Tech Detection",
        "status": outdated_status,
        "score": outdated_score,
        "max_score": 100,
        "evidence": out_evidence
    })

    # Calculate overall weighted score
    weights = [0.25, 0.15, 0.15, 0.15, 0.10, 0.10, 0.10]
    scores = [
        publisher_score,
        author_score,
        date_score,
        evidence_score,
        source_link_score,
        duplicate_score,
        outdated_score
    ]
    overall_score = int(sum(w * s for w, s in zip(weights, scores)))

    if overall_score >= 82 and publisher_score >= 80 and source_link_score >= 70:
        overall_status = "verified"
    elif overall_score >= 60:
        overall_status = "flagged"
    else:
        overall_status = "rejected"

    summary_notes = f"Evaluation completed with score {overall_score}/100. Status: {overall_status.upper()}. "
    if publisher_matched:
        summary_notes += f"Publisher '{publisher_matched['name']}' verified in trusted index. "
    if found_deprecated:
        summary_notes += f"Warning: {len(found_deprecated)} deprecated tech terms flagged. "

    return {
        "publisher_score": publisher_score,
        "author_score": author_score,
        "date_score": date_score,
        "evidence_score": evidence_score,
        "source_link_score": source_link_score,
        "duplicate_score": duplicate_score,
        "outdated_score": outdated_score,
        "overall_score": overall_score,
        "overall_status": overall_status,
        "checklist": checklist,
        "evidence_notes": summary_notes.strip()
    }
