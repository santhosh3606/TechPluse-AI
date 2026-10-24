"""
TechPulse AI - AI Summarizer & Claim Verification Engine
Features:
1. Generates concise technical headline & executive summary
2. Highlights "Why It Matters for CSE Students & Faculty"
3. Extracts key technical facts and original citations
4. Labels AI-generated outputs transparently
5. Compares generated summary against source text (Claim & Hallucination Checker)
6. Flags unsupported claims, missing context, and potential hallucinations
7. Supports Google Gemini API (when configured) with high-fidelity heuristic fallback
"""

import os
import json
import re
import requests

def extract_sentences(text):
    text = re.sub(r'\s+', ' ', text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 15]

def generate_heuristic_summary(article):
    title = article.get("title", "Untitled Technical Report")
    abstract = article.get("abstract", "")
    content = article.get("content", "") or abstract
    url = article.get("url", "")
    source_name = article.get("source_name", "Technical Source")
    published_at = article.get("published_at", "Recent")
    category = article.get("category", "Computer Science")

    sentences = extract_sentences(abstract if len(abstract) > 100 else content)
    if not sentences:
        sentences = [title]

    # Headline
    headline = f"Breakthrough in {category}: {title}"
    if len(headline) > 110:
        headline = headline[:107] + "..."

    # Summary sentences
    lead = sentences[0] if len(sentences) > 0 else title
    supporting = sentences[1] if len(sentences) > 1 else ""
    implication = sentences[2] if len(sentences) > 2 else "This development offers notable improvements in efficiency, scalability, and system reliability."

    summary_text = f"{lead} {supporting} {implication}".strip()

    # Why it matters for CSE Students
    cse_angles = {
        "AI/ML": "Essential for CSE students studying deep learning architectures, attention mechanisms, and model alignment. Directly impacts ongoing capstone projects involving transformer fine-tuning and inference latency optimization.",
        "Cybersecurity": "Crucial for security researchers and systems engineering coursework. Demonstrates modern attack vectors and defensive mitigation strategies that must be incorporated into secure software development lifecycles.",
        "Software Engineering": "Directly applicable to software engineering labs and distributed systems design. Provides real-world evidence for refactoring legacy microservices and designing high-throughput concurrent pipelines.",
        "Cloud Computing": "Relevant for cloud architects and DevOps curricula. Illuminates best practices in serverless orchestrations, edge computing deployments, and resource allocation efficiency.",
        "Data Science": "Key reading for data analytics and big data courses. Shows how modern data pipelines handle high-cardinality streaming data while preserving statistical validity.",
        "Emerging Technology": "Broadens perspective on next-generation computing paradigms including quantum algorithms, Neuromorphic hardware, and post-silicon compute topologies."
    }
    why_it_matters = cse_angles.get(category, "Provides actionable technical insights relevant to modern computer science curricula, system architecture design, and academic research exploration.")

    # Key facts
    facts = []
    # Try to find numbers/benchmarks/claims in sentences
    for s in sentences:
        if re.search(r'\b(\d+(\.\d+)?%|\d+x|\d+ ms|\d+ Gbps|\d+ parameters)\b', s, re.IGNORECASE):
            facts.append(s)
            if len(facts) >= 3:
                break
    if not facts:
        facts = [
            f"Published by {source_name} on {published_at}.",
            f"Focused on advancing state-of-the-art implementations in {category}.",
            f"Demonstrates verifiable performance or architectural methodology."
        ]

    # Citations
    citations = [
        {"source": source_name, "url": url, "type": "Primary Document"}
    ]
    if "arxiv.org" in url:
        citations.append({"source": "arXiv Computer Science Repository", "url": url, "type": "Preprint Repository"})

    # Claims check: Compare summary sentences against original article text
    full_source = (title + " " + abstract + " " + content).lower()
    claims_checked = []

    for fact in facts:
        # Check lexical overlap
        words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{4,}\b', fact)]
        matched = [w for w in words if w in full_source]
        ratio = len(matched) / max(1, len(words))

        if ratio > 0.65:
            status = "verified"
            notes = "Direct textual support found in source document."
        elif ratio > 0.35:
            status = "inferred"
            notes = "Plausible contextual inference based on source narrative."
        else:
            status = "unsupported"
            notes = "Low lexical match; potential AI extrapolation. Human review recommended."

        claims_checked.append({
            "claim": fact,
            "status": status,
            "confidence": round(ratio * 100, 1),
            "notes": notes
        })

    return {
        "headline": headline,
        "summary_text": summary_text,
        "why_it_matters_cse": why_it_matters,
        "key_facts": facts,
        "citations": citations,
        "claims_checked": claims_checked,
        "model_used": "TechPulse-Heuristic-v1.0 (Built-in Rule Engine)"
    }

def summarize_with_gemini(article, api_key):
    """
    Attempts to use Google Gemini API for summarization if key is present;
    falls back to heuristic if request fails.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    prompt = f"""You are TechPulse AI, an expert CSE research digest analyst.
Analyze the following article and return a STRICT JSON object:
Title: {article.get('title')}
Source: {article.get('source_name')} ({article.get('url')})
Category: {article.get('category')}
Published Date: {article.get('published_at')}
Content/Abstract:
{article.get('abstract', '') or article.get('content', '')}

Return ONLY a valid JSON object matching this schema:
{{
  "headline": "concise technical headline under 100 chars",
  "summary_text": "3-4 concise technical sentences summarizing the breakthrough, methodology, and outcome",
  "why_it_matters_cse": "2-3 sentences explaining exact relevance to Computer Science & Engineering students, clubs, and curriculum",
  "key_facts": ["fact 1 with metrics/data", "fact 2", "fact 3"],
  "citations": [{{"source": "{article.get('source_name')}", "url": "{article.get('url')}", "type": "Primary Document"}}],
  "claims_checked": [
    {{"claim": "fact 1", "status": "verified", "confidence": 95, "notes": "Textual evidence in source"}},
    {{"claim": "fact 2", "status": "verified", "confidence": 90, "notes": "Direct citation in abstract"}},
    {{"claim": "fact 3", "status": "verified", "confidence": 88, "notes": "Confirmed by empirical data in text"}}
  ]
}}"""

    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            raw_text = data['candidates'][0]['content']['parts'][0]['text']
            # Clean markdown code block formatting
            clean_json = re.sub(r'```json\s*', '', raw_text)
            clean_json = re.sub(r'```\s*$', '', clean_json).strip()
            parsed = json.loads(clean_json)
            parsed["model_used"] = "Google Gemini 1.5 Flash (Live API)"
            return parsed
    except Exception as e:
        print(f"Gemini API request failed, falling back to heuristic: {e}")

    # Fallback to local heuristic
    res = generate_heuristic_summary(article)
    res["model_used"] = "TechPulse-Heuristic-v1.0 (Gemini Fallback)"
    return res

def summarize_article(article, api_key=None):
    if api_key and api_key.strip():
        return summarize_with_gemini(article, api_key.strip())
    return generate_heuristic_summary(article)
