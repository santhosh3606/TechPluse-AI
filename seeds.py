"""
TechPulse AI - Database Seed Script
Populates:
1. >= 10 Trusted Sources with credibility rationale & trust score
2. 4 Sample Weekly Digest Editions (distinct dates, articles, summaries)
3. Sample articles across categories (AI/ML, Cybersecurity, Software Eng, Cloud, Data Science, Emerging Tech)
4. Verification checklist checks for seeded articles
5. Structured summaries with 'Why it matters for CSE' and claim verifications
6. 7 Prompt templates in the Prompt Library
"""

import json
from database import get_db, init_db

TRUSTED_SOURCES = [
    {
        "name": "arXiv Computer Science",
        "type": "Academic Preprint Archive",
        "official_url": "https://arxiv.org/archive/cs",
        "credibility_rationale": "World's foremost open-access scientific repository for computer science research, managed by Cornell University with rigorous automated moderation and institutional submissions.",
        "trust_score": 98,
        "verification_status": "verified"
    },
    {
        "name": "IEEE Spectrum & Computer Society",
        "type": "Professional Engineering Organization",
        "official_url": "https://spectrum.ieee.org",
        "credibility_rationale": "Flagship publication of the Institute of Electrical and Electronics Engineers, peer-reviewed engineering reporting by certified researchers and industry leaders.",
        "trust_score": 96,
        "verification_status": "verified"
    },
    {
        "name": "MIT Technology Review",
        "type": "Academic Tech Publication",
        "official_url": "https://www.technologyreview.com",
        "credibility_rationale": "Founded at the Massachusetts Institute of Technology in 1899; authoritative, journalistically independent analysis of emerging tech with strict editorial standards.",
        "trust_score": 95,
        "verification_status": "verified"
    },
    {
        "name": "Communications of the ACM",
        "type": "Academic Computing Society",
        "official_url": "https://cacm.acm.org",
        "credibility_rationale": "Premier monthly magazine for computing professionals by the Association for Computing Machinery; peer-reviewed viewpoints, milestone research papers, and ethics reviews.",
        "trust_score": 97,
        "verification_status": "verified"
    },
    {
        "name": "Google Research & DeepMind Blog",
        "type": "Official Corporate Research Lab",
        "official_url": "https://research.google/blog/",
        "credibility_rationale": "Direct publications from primary research scientists developing frontier models, algorithms, and tensor hardware architectures.",
        "trust_score": 95,
        "verification_status": "verified"
    },
    {
        "name": "OpenAI Research",
        "type": "Official AI Research Lab",
        "official_url": "https://openai.com/research",
        "credibility_rationale": "Primary releases and technical documentation for frontier generative models, alignment methodologies, and safety evals.",
        "trust_score": 94,
        "verification_status": "verified"
    },
    {
        "name": "AWS Architecture & Cloud Blog",
        "type": "Official Cloud Vendor Blog",
        "official_url": "https://aws.amazon.com/blogs/architecture/",
        "credibility_rationale": "Industry-standard reference for distributed systems design, fault tolerance patterns, and hyperscale cloud infrastructure.",
        "trust_score": 92,
        "verification_status": "verified"
    },
    {
        "name": "GitHub Engineering Blog",
        "type": "Official Tech Engineering Blog",
        "official_url": "https://github.blog/category/engineering/",
        "credibility_rationale": "Detailed post-mortems, scalable database architectures, and developer tooling insights directly from engineers maintaining the largest git host.",
        "trust_score": 94,
        "verification_status": "verified"
    },
    {
        "name": "CISA / US-CERT Cybersecurity Advisories",
        "type": "National Cybersecurity Agency",
        "official_url": "https://www.cisa.gov/news-events/cybersecurity-advisories",
        "credibility_rationale": "Official United States federal agency providing verified vulnerability disclosures, threat intelligence, and zero-day alert catalog.",
        "trust_score": 99,
        "verification_status": "verified"
    },
    {
        "name": "Nature Machine Intelligence",
        "type": "Peer-Reviewed Academic Journal",
        "official_url": "https://www.nature.com/natmachintell/",
        "credibility_rationale": "Top-tier peer-reviewed journal from Nature Publishing Group covering high-impact AI, robotics, and computational cognitive systems.",
        "trust_score": 98,
        "verification_status": "verified"
    },
    {
        "name": "Cloud Native Computing Foundation (CNCF)",
        "type": "Open Source Standards Body",
        "official_url": "https://www.cncf.io/blog/",
        "credibility_rationale": "Linux Foundation entity governing Kubernetes, Envoy, Prometheus, and vendor-neutral cloud native standards.",
        "trust_score": 95,
        "verification_status": "verified"
    },
    {
        "name": "Hacker News (Top Verified Tech)",
        "type": "Peer-Curated Tech Community",
        "official_url": "https://news.ycombinator.com",
        "credibility_rationale": "High-signal algorithmic curation by senior systems engineers and founders; community cross-checks claims in real time.",
        "trust_score": 88,
        "verification_status": "verified"
    }
]

SAMPLE_ARTICLES = [
    # Edition 42 Articles (Week of Oct 20-24, 2026)
    {
        "title": "Autonomous Multi-Agent Orchestration via Asynchronous State Trees",
        "abstract": "We present AST-Agent, a novel decentralized orchestration protocol allowing heterogeneous AI agents to coordinate complex software engineering workflows without central token bottlenecking. Evaluated across 500 GitHub repos, AST-Agent reduces task latency by 41% and eliminates circular agent deadlocks.",
        "url": "https://arxiv.org/abs/2610.08412",
        "source_name": "arXiv Computer Science",
        "authors": "Dr. Elena Rostova, Marcus Chen, et al.",
        "category": "AI/ML",
        "published_at": "2026-10-22",
        "is_saved": 1,
        "is_digest_candidate": 1,
        "is_live_retrieved": 0,
        "verification_status": "verified",
        "edition_issue": 42,
        "display_order": 1,
        "why_it_matters_cse": "Provides CSE students working on LLM capstones with a resilient, non-blocking agent architecture pattern. Directly replaces simplistic single-agent ReAct loops in distributed coding tasks.",
        "facts": [
            "Reduces multi-agent task execution latency by 41% on complex benchmark tasks.",
            "Eliminates circular lock-in states using asynchronous state tree pruning.",
            "Tested on 500 open-source repositories with 92.4% successful patch synthesis."
        ]
    },
    {
        "title": "Hardware-Accelerated Memory Safety: Deploying CHERI in Operating System Kernels",
        "abstract": "Memory safety violations continue to represent over 65% of critical CVEs. This paper details the port of FreeBSD and Linux microkernel components to CHERI hardware capabilities, demonstrating spatial and temporal memory protection with under 3.2% performance overhead.",
        "url": "https://spectrum.ieee.org/cheri-memory-safety-os-kernel",
        "source_name": "IEEE Spectrum & Computer Society",
        "authors": "Robert Watson, Simon Moore, Peter Sewell",
        "category": "Cybersecurity",
        "published_at": "2026-10-21",
        "is_saved": 1,
        "is_digest_candidate": 1,
        "is_live_retrieved": 0,
        "verification_status": "verified",
        "edition_issue": 42,
        "display_order": 2,
        "why_it_matters_cse": "Vital reading for Operating Systems and Computer Architecture students. Illustrates how hardware-enforced pointer bounds replace fragile runtime bounds checks in C/C++ systems programming.",
        "facts": [
            "Guarantees hardware-enforced spatial and temporal pointer bounds protection.",
            "Benchmarked with less than 3.2% CPU cycle overhead on RISC-V CHERI silicon.",
            "Directly mitigates buffer overflows, use-after-free, and pointer forgery vulnerabilities."
        ]
    },
    {
        "title": "Scaling Distributed Key-Value Stores to 100 Million IOPS with eBPF and NVMe-oF",
        "abstract": "We describe the design of FlashMesh, an in-kernel high-performance caching layer built on eBPF bypass paths and NVMe over Fabrics. By sidestepping traditional kernel socket overheads, FlashMesh delivers sub-15 microsecond tail latency at 100M IOPS.",
        "url": "https://github.blog/2026-10-20-flashmesh-ebpf-nvme-distributed-store/",
        "source_name": "GitHub Engineering Blog",
        "authors": "GitHub Infrastructure & Storage Team",
        "category": "Cloud Computing",
        "published_at": "2026-10-20",
        "is_saved": 1,
        "is_digest_candidate": 1,
        "is_live_retrieved": 0,
        "verification_status": "verified",
        "edition_issue": 42,
        "display_order": 3,
        "why_it_matters_cse": "Exceptional case study for Cloud Computing and Distributed Systems courses. Shows how eBPF kernel probes can safely bypass context switching bottlenecks in hyperscale database tiers.",
        "facts": [
            "Achieves sub-15 microsecond p99 tail latency across 64-node clusters.",
            "Eliminates user-space to kernel-space buffer copies via eBPF XDP hook points.",
            "Surpasses traditional Redis/Memcached throughput by 5.4x per server rack."
        ]
    },

    # Edition 41 Articles (Week of Oct 13-17, 2026)
    {
        "title": "Post-Quantum Cryptography in Production: Migrating TLS to Kyber-1024 and Dilithium",
        "abstract": "With NIST standardizing ML-KEM (Kyber) and ML-DSA (Dilithium), enterprise engineering teams are facing latency and packet fragmentation challenges. This paper details lessons learned migrating 4 billion daily TLS handshakes to hybrid quantum-resistant key exchange.",
        "url": "https://cacm.acm.org/practice/post-quantum-tls-kyber-dilithium-production/",
        "source_name": "Communications of the ACM",
        "authors": "Tanja Lange, Douglas Stebila, Cloudflare Cryptography Group",
        "category": "Cybersecurity",
        "published_at": "2026-10-15",
        "is_saved": 1,
        "is_digest_candidate": 1,
        "is_live_retrieved": 0,
        "verification_status": "verified",
        "edition_issue": 41,
        "display_order": 1,
        "why_it_matters_cse": "Imperative for network security and cryptography students. Explains the pragmatic network packet MTU limitations when transitioning from elliptic curves (ECDH) to lattice-based polynomial cryptosystems.",
        "facts": [
            "Measures real-world packet fragmentation rates on Kyber-1024 handshakes.",
            "Analyzes CPU cryptographic accelerator instructions on ARMv9 and x86 AVX-512.",
            "Prevents future 'Harvest Now, Decrypt Later' adversaries against encrypted traffic."
        ]
    },
    {
        "title": "Formal Verification of Concurrent Rust Kernels using Automated SMT Solvers",
        "abstract": "Concurrent lock-free algorithms are notorious for subtle race conditions. We present VeriRust, a framework translating Rust MIR into Z3 SMT constraints to formally prove memory safety and deadlock freedom without manual invariants.",
        "url": "https://arxiv.org/abs/2610.05201",
        "source_name": "arXiv Computer Science",
        "authors": "Vikram Patel, Sophie Becker, MIT CSAIL",
        "category": "Software Engineering",
        "published_at": "2026-10-14",
        "is_saved": 1,
        "is_digest_candidate": 1,
        "is_live_retrieved": 0,
        "verification_status": "verified",
        "edition_issue": 41,
        "display_order": 2,
        "why_it_matters_cse": "Shows CSE students how formal methods and SMT theorem provers are bridging the gap from theoretical verification to practical systems programming in Rust.",
        "facts": [
            "Automatically synthesizes invariant proofs for cross-thread channel primitives.",
            "Verifies over 20,000 lines of unsafe concurrent Rust kernel code with 0 false negatives.",
            "Reduces formal specification time from weeks of Coq proof scripts to minutes."
        ]
    },
    {
        "title": "Streaming Vector Indexing on Billions of High-Dimensional Embeddings",
        "abstract": "We introduce HNSW-Stream, an incremental approximate nearest neighbor index supporting concurrent insertions, deletions, and queries at 80,000 queries per second on single NVMe nodes with 99.1% recall.",
        "url": "https://research.google/blog/hnsw-stream-vector-database-indexing/",
        "source_name": "Google Research & DeepMind Blog",
        "authors": "Google Brain Systems Team",
        "category": "Data Science",
        "published_at": "2026-10-13",
        "is_saved": 1,
        "is_digest_candidate": 1,
        "is_live_retrieved": 0,
        "verification_status": "verified",
        "edition_issue": 41,
        "display_order": 3,
        "why_it_matters_cse": "Directly benefits students developing RAG (Retrieval-Augmented Generation) systems and recommendation engines that require dynamic vector updating without long re-indexing downtime.",
        "facts": [
            "Sustains 80k vector queries/sec while maintaining live concurrent graph updates.",
            "Maintains 99.1% top-k recall relative to brute-force Euclidean distance.",
            "Compresses 1536-dimensional vectors using product quantization with 75% RAM savings."
        ]
    },

    # Edition 40 Articles (Week of Oct 06-10, 2026)
    {
        "title": "WebAssembly in Serverless: Cold-Start Reduction from 300ms to 800 Microseconds",
        "abstract": "Traditional containerized serverless functions suffer from high virtualization and container startup penalties. This paper benchmarks native WASI runtimes (Wasmtime, Wasmer) deployed on edge nodes, achieving sub-millisecond cold starts and 10x higher density per compute node.",
        "url": "https://www.cncf.io/blog/2026/10/08/wasm-serverless-submillisecond-coldstart/",
        "source_name": "Cloud Native Computing Foundation (CNCF)",
        "authors": "CNCF Wasm Working Group",
        "category": "Cloud Computing",
        "published_at": "2026-10-08",
        "is_saved": 1,
        "is_digest_candidate": 1,
        "is_live_retrieved": 0,
        "verification_status": "verified",
        "edition_issue": 40,
        "display_order": 1,
        "why_it_matters_cse": "Critical for students designing microservice architectures. Demonstrates how sandboxed WebAssembly bytecode replaces heavy Linux container images for lightweight edge computing.",
        "facts": [
            "Reduces function cold-start latency from 300ms (Docker) to 820 microseconds.",
            "Increases tenant execution density by 10.4x on identical bare-metal hardware.",
            "Implements capability-based security isolation via WebAssembly System Interface (WASI)."
        ]
    },
    {
        "title": "Quantum Error Correction Thresholds Surpassed in 1000-Qubit Topological Lattice",
        "abstract": "We present experimental results from a 1,024-qubit superconducting quantum processor demonstrating physical error rates below the fault-tolerant surface code threshold. Logical qubit fidelity exceeds physical fidelity by a factor of 12.",
        "url": "https://www.nature.com/natmachintell/quantum-error-correction-topological-1000",
        "source_name": "Nature Machine Intelligence",
        "authors": "Dr. Sarah Lindqvist, Quantum Hardware Consortium",
        "category": "Emerging Technology",
        "published_at": "2026-10-07",
        "is_saved": 1,
        "is_digest_candidate": 1,
        "is_live_retrieved": 0,
        "verification_status": "verified",
        "edition_issue": 40,
        "display_order": 2,
        "why_it_matters_cse": "Inspires students interested in Quantum Information Theory and physics-informed computing. Proves that fault-tolerant logical qubits are mathematically viable at scale.",
        "facts": [
            "Demonstrates 12x improvement in logical qubit coherence over physical qubits.",
            "Operates across a 1,024 superconducting transmon array at 15 millikelvin.",
            "Confirms fault-tolerant threshold theorem in real physical quantum processors."
        ]
    },

    # Edition 39 Articles (Week of Sep 29-Oct 03, 2026)
    {
        "title": "Speculative Decoding with Small Specialized Drafter Models: 3.8x Speedup",
        "abstract": "We investigate speculative decoding where a compact 1B parameter drafter generates token candidates verified in parallel by a 70B parameter target model. By optimizing acceptance probability through speculative tree search, we achieve 3.8x inference speedup without any quality degradation.",
        "url": "https://arxiv.org/abs/2609.11029",
        "source_name": "arXiv Computer Science",
        "authors": "Alexandre Moreau, Priya Sundaram, et al.",
        "category": "AI/ML",
        "published_at": "2026-10-01",
        "is_saved": 1,
        "is_digest_candidate": 1,
        "is_live_retrieved": 0,
        "verification_status": "verified",
        "edition_issue": 39,
        "display_order": 1,
        "why_it_matters_cse": "Essential practical optimization for students building LLM-powered applications. Teaches how memory bandwidth bottlenecks can be overcome with parallel verification trees.",
        "facts": [
            "Delivers 3.8x real-world token generation throughput on standard NVIDIA H100 GPUs.",
            "Zero degradation in output distribution; mathematically identical to greedy decoding.",
            "Drafter model footprint fits within 2GB of VRAM."
        ]
    },
    {
        "title": "Zero-Knowledge Proofs for Verifiable Machine Learning Inference (zkML)",
        "abstract": "We present zk-Tensor, a zero-knowledge proof circuit compiler that generates non-interactive proofs of neural network inferences under 2 seconds for ResNet and BERT architectures, allowing verifiable privacy-preserving AI audits.",
        "url": "https://www.technologyreview.com/2026/09/30/zkml-verifiable-ai-inference/",
        "source_name": "MIT Technology Review",
        "authors": "Eileen Vance, Applied Cryptography Lab",
        "category": "Cybersecurity",
        "published_at": "2026-09-30",
        "is_saved": 1,
        "is_digest_candidate": 1,
        "is_live_retrieved": 0,
        "verification_status": "verified",
        "edition_issue": 39,
        "display_order": 2,
        "why_it_matters_cse": "Convergence of cryptography and machine learning. Shows students how SNARKs and STARKs can verify that an AI model actually executed an inference without exposing proprietary weights or private user inputs.",
        "facts": [
            "Generates cryptographic proof of model inference in under 1.8 seconds.",
            "Proof verification takes 12ms on consumer hardware (mobile/web browser).",
            "Protects both model weights and input privacy in regulatory compliance audits."
        ]
    }
]

SAMPLE_EDITIONS = [
    {
        "issue_number": 42,
        "title": "Frontier AI Agents, Hardware-Enforced OS Kernels, & Distributed Flash Storage",
        "theme": "Autonomous Systems, CHERI Memory Safety, and Low-Latency Cloud Runtimes",
        "week_date": "Week of October 20 - 24, 2026",
        "status": "approved",
        "draft_email_subject": "TechPulse AI Digest #42: Multi-Agent Orchestration & CHERI Kernel Safety",
        "draft_email_body": """Dear CSE Students, Researchers, and Faculty,

Welcome to Edition #42 of the TechPulse AI Digest! Our automated verification engine reviewed 48 research preprints and engineering bulletins this week. Here are the top vetted breakthroughs for computing education:

1. [AI/ML] Autonomous Multi-Agent Orchestration via Asynchronous State Trees
   - Source: arXiv Computer Science (cs.AI) | Oct 22, 2026
   - Breakthrough: Eliminates circular deadlocks and achieves 41% latency reduction across 500 open-source testbeds.
   - Why it matters for CSE: Perfect architecture template for capstone projects building distributed coding assistants.

2. [Cybersecurity] Hardware-Accelerated Memory Safety: CHERI in OS Kernels
   - Source: IEEE Spectrum | Oct 21, 2026
   - Breakthrough: Hardware-enforced spatial and temporal pointer bounds with under 3.2% overhead.
   - Why it matters for CSE: Demonstrates the future of systems security replacing runtime sanitizers.

3. [Cloud Computing] FlashMesh: 100M IOPS with eBPF & NVMe-oF
   - Source: GitHub Engineering | Oct 20, 2026
   - Breakthrough: In-kernel eBPF socket bypass delivers sub-15 microsecond tail latency.
   - Why it matters for CSE: Practical blueprint for high-throughput distributed database architecture.

Read the full interactive digest, verify evidence checklists, or listen to the podcast summary on our dashboard!

Warm regards,
The TechPulse AI Editorial Engine
Dept. of Computer Science & Engineering""",
        "audio_script": "Welcome to TechPulse AI Audio Digest, Issue 42. In this week's highlights: First, researchers on arXiv introduce AST-Agent, a decentralized multi-agent orchestration model reducing execution latency by 41 percent. In systems security, IEEE Spectrum highlights the port of operating system kernels to CHERI hardware capabilities, eliminating buffer overflows with under four percent overhead. Finally, GitHub Engineering details FlashMesh, achieving 100 million IOPS using eBPF and NVMe over Fabrics. For full citations and verified checklists, visit the TechPulse AI portal."
    },
    {
        "issue_number": 41,
        "title": "Post-Quantum Cryptography in Production, Formally Verified Rust, & Vector Databases",
        "theme": "Lattice-Based Encryption, SMT Theorem Provers, and High-Throughput RAG Indexing",
        "week_date": "Week of October 13 - 17, 2026",
        "status": "approved",
        "draft_email_subject": "TechPulse AI Digest #41: Migrating to Post-Quantum TLS & Formal Rust Verification",
        "draft_email_body": """Dear CSE Students, Researchers, and Faculty,

Welcome to Edition #41 of TechPulse AI Digest! Highlights curated and verified for the week of October 13-17:

1. [Cybersecurity] Post-Quantum Cryptography in Production: Kyber-1024 & Dilithium
   - Source: Communications of the ACM | Oct 15, 2026
   - Mitigating quantum decrypt-later risks across 4 billion daily TLS handshakes.

2. [Software Engineering] VeriRust: Formal Verification of Concurrent Rust with SMT
   - Source: arXiv Computer Science | Oct 14, 2026
   - Automated SMT constraint proofs for 20,000 lines of concurrent unsafe Rust code.

3. [Data Science] HNSW-Stream: Live Streaming Vector Indexing at 80k QPS
   - Source: Google Research | Oct 13, 2026
   - Eliminates re-indexing downtime for dynamic RAG and embedding retrieval engines.

Access verified source checklists and summary comparisons on the web portal.

The TechPulse AI Editorial Engine""",
        "audio_script": "This is TechPulse AI Audio Digest, Issue 41. Cryptography teams report on migrating four billion TLS connections to NIST post-quantum algorithms Kyber and Dilithium. In software engineering, MIT researchers unveil VeriRust, translating concurrent Rust code into Z3 SMT constraints for automated formal verification. And Google Research shares HNSW-Stream, sustaining 80 thousand vector queries per second with live graph updates. Stay curious, and keep building."
    },
    {
        "issue_number": 40,
        "title": "Sub-Millisecond WebAssembly Microservices & 1000-Qubit Topological Error Correction",
        "theme": "Next-Gen Edge Compute Topologies and Fault-Tolerant Quantum Silicon",
        "week_date": "Week of October 06 - 10, 2026",
        "status": "published",
        "draft_email_subject": "TechPulse AI Digest #40: WASM Microservices & Topological Quantum Milestones",
        "draft_email_body": """Dear CSE Community,

Edition #40 of TechPulse AI Digest is now published. Key technical developments:

1. [Cloud Computing] WebAssembly in Serverless: 800 Microsecond Cold Starts
   - CNCF Blog: Sandboxed WASI bytecode outperforms containers by 10x compute density.
2. [Emerging Technology] 1000-Qubit Topological Lattice Breaks Error Correction Threshold
   - Nature Machine Intelligence: 12x coherence multiplication over physical superconducting transmons.

Explore the full breakdown on the TechPulse dashboard!""",
        "audio_script": "Welcome to TechPulse Audio Digest #40. The Cloud Native Computing Foundation benchmarks WebAssembly edge functions, demonstrating cold starts under 800 microseconds. Meanwhile in quantum computing, Nature reports a 1000-qubit topological lattice surpassing physical fault-tolerant error thresholds. Thanks for tuning into TechPulse AI."
    },
    {
        "issue_number": 39,
        "title": "Speculative Decoding for 3.8x LLM Speedups & Zero-Knowledge Machine Learning",
        "theme": "Transformer Acceleration Techniques and Cryptographic Model Auditing",
        "week_date": "Week of September 29 - October 03, 2026",
        "status": "published",
        "draft_email_subject": "TechPulse AI Digest #39: Speculative Decoding & zkML Audits",
        "draft_email_body": """Dear CSE Students and Faculty,

Here is Edition #39 of TechPulse AI Digest:

1. [AI/ML] Speculative Decoding with 1B Drafter Models
   - arXiv cs.AI: 3.8x inference speedup on NVIDIA H100 GPUs with zero quality loss.
2. [Cybersecurity] zkML: Zero-Knowledge Proofs for Verifiable AI Inferences
   - MIT Technology Review: Sub-2 second SNARK proofs verifying model computation without leaking weights.

Happy hacking!
TechPulse AI Team""",
        "audio_script": "TechPulse AI Digest Issue 39 audio briefing: Speculative decoding achieves 3.8 times higher token generation throughput by pairing lightweight drafter models with frontier LLMs. In cryptographic AI, zkML enables sub-two-second zero-knowledge verification of deep neural network inferences. Tune in next week for more verified tech research."
    }
]

PROMPTS_DATA = [
    {
        "category": "Technology Research",
        "title": "ArXiv Research Discovery & Filter Prompt",
        "description": "Formulates targeted academic search queries for preprint servers, prioritizing high-impact empirical methodologies and novelty.",
        "tags": "arXiv, research, search, literature review",
        "template_text": """You are an academic research assistant for Computer Science & Engineering.
Task: Evaluate the following technological topic: {{topic}}
1. Identify the primary IEEE/ACM taxonomy subdisciplines (e.g. cs.AI, cs.CR, cs.DC).
2. Generate 5 precise boolean search queries suitable for arXiv API and Google Scholar.
3. List 3 key inclusion criteria (e.g. empirical benchmarks, reproducible GitHub repository, baseline ablation) and 2 exclusion criteria (e.g. speculative whitepapers, unsubstantiated vendor claims).
4. Outline the key research questions a CSE senior capstone team should investigate."""
    },
    {
        "category": "Article Summarization",
        "title": "CSE Student & Faculty Targeted Summarizer",
        "description": "Transforms dense technical papers into structured, actionable digests focusing on systems architecture, mathematical findings, and lab applications.",
        "tags": "summarization, cse, pedagogy, technical digest",
        "template_text": """You are TechPulse AI, a technical digest editor for Computer Science students and faculty.
Analyze the source paper below and synthesize a structured briefing:
Title: {{article_title}}
Source: {{source_name}} | Published: {{published_at}}
Full Text/Abstract:
{{article_content}}

Formatting Constraints:
- Headline: Catchy yet technically rigorous (under 100 characters).
- Executive Summary: Exactly 3 sentences explaining the core engineering problem, the novel methodology, and the measured outcome.
- Why It Matters for CSE: Detail why an undergraduate or graduate computer science student should care (e.g. algorithms, compilers, security lab relevance).
- Key Facts: 3 bullet points with concrete metrics, benchmark numbers, or mathematical theorems.
- Citations: Preserve the exact canonical URL and primary author attribution.
- Transparency: Clearly indicate this is an AI-assisted synthesis."""
    },
    {
        "category": "Source Verification",
        "title": "7-Point Source Credibility Audit Prompt",
        "description": "Rigorous verification framework checking publisher pedigree, institutional attribution, empirical backing, and canonical links.",
        "tags": "credibility, verification, fact-checking, provenance",
        "template_text": """Act as an independent scientific fact-checker and source credibility auditor.
Review the candidate technical article:
Title: {{article_title}}
URL: {{article_url}}
Publisher: {{publisher_name}}
Content: {{article_content}}

Evaluate each of the following 7 dimensions:
1. Publisher Authenticity: Is the domain an accredited academic repository, peer-reviewed journal, or verified corporate engineering blog?
2. Author Attribution: Are individual researchers or recognized labs named?
3. Publication Date Recency: Is the date valid? Is the research fresh or outdated?
4. Supporting Evidence: Are there links to GitHub repositories, datasets, DOIs, or mathematical appendices?
5. Original Source Link: Is there an accessible canonical link without deceptive paywalls?
6. Duplicate Content: Is this original reporting or syndicated press release copy?
7. Deprecated Technology: Does the text recommend obsolete APIs or cryptographically broken primitives (e.g., Python 2, SHA-1, CentOS 8)?

Provide a confidence score (0-100) and explicit evidentiary justification for each item."""
    },
    {
        "category": "Hallucination Detection",
        "title": "Sentence-Level Claim Cross-Examiner",
        "description": "Compares every sentence in a generated summary against the raw source text to identify hallucinations and ungrounded extrapolations.",
        "tags": "hallucination, grounding, claim check, nlp",
        "template_text": """You are a rigorous Hallucination & Grounding Detection Engine.
Compare the generated AI summary against the original source document:
--- ORIGINAL SOURCE ---
{{source_text}}
--- GENERATED SUMMARY ---
{{generated_summary}}

Instructions:
1. Break down the generated summary into individual atomic factual claims.
2. For each claim, classify status as:
   - [VERIFIED]: Directly confirmed by verbatim or synonymous phrasing in source.
   - [INFERRED]: Contextually plausible extrapolation, but not explicitly stated.
   - [UNSUPPORTED / HALLUCINATION]: Contradicts source or introduces ungrounded metrics/names.
3. Calculate Grounding Score = (Verified Claims / Total Claims) * 100%.
4. Highlight any ungrounded claim and rewrite it to match source truth strictly."""
    },
    {
        "category": "Outdated Information Detection",
        "title": "Deprecated Frameworks & Obsolete Tech Detector",
        "description": "Scans technical articles for discontinued libraries, end-of-life operating systems, superseded protocols, and insecure algorithms.",
        "tags": "outdated tech, deprecation, security hygiene, cse curriculum",
        "template_text": """Inspect the following computer science article for obsolete or deprecated recommendations:
Text: {{article_text}}

Audit Criteria:
- Deprecated Languages/Runtimes: Python 2, AngularJS 1.x, Java 8 legacy practices.
- Deprecated Cryptography: MD5, SHA-1, RC4, single DES, TLS 1.0/1.1.
- Superseded Machine Learning Frameworks: Caffe, Theano, TensorFlow 1.x graph mode.
- EOL Operating Systems: CentOS 8, Ubuntu 18.04, Windows 7/8.
- Superseded Cloud APIs or Hardware architectures.

Output:
- Identified Outdated Terms (if any)
- Severity (Critical, Warning, Informational)
- Recommended Modern Replacement (e.g., PyTorch / JAX instead of TF 1.x)."""
    },
    {
        "category": "Weekly Digest Generation",
        "title": "Weekly Curated Issue Synthesizer",
        "description": "Synthesizes multiple approved articles into an engaging, cohesive weekly newsletter with an editorial theme and takeaway summary.",
        "tags": "weekly digest, newsletter, editorial, cse club",
        "template_text": """You are the Senior Editor of TechPulse AI Weekly Digest for the Computer Science & Engineering department.
Input: {{approved_articles_json}}
Issue Number: {{issue_number}}
Week Date: {{week_date}}

Produce:
1. Editorial Theme & Title for the issue.
2. 150-word Opening Remarks connecting this week's breakthroughs to broader trends in computing.
3. Categorized Article Sections (AI/ML, Cybersecurity, Cloud, Software Engineering, Data Science).
4. Quick Study Challenge: 2 multiple-choice conceptual questions based on the papers for CSE students.
5. Formatted Draft Email ready for broadcast to the student body."""
    },
    {
        "category": "Audio Script Generation",
        "title": "Conversational Tech Podcast Script Generator",
        "description": "Adapts technical digests into natural, rhythmic spoken scripts suitable for podcast broadcasts or automated text-to-speech engines.",
        "tags": "audio, podcast, elevenlabs, speech synthesis",
        "template_text": """Convert the following approved weekly digest into an engaging 2-minute podcast script:
Digest Theme: {{digest_theme}}
Articles:
{{articles_summary}}

Script Guidelines:
- Host Persona: Knowledgeable, energetic senior engineering mentor speaking directly to CSE students.
- Tone: Clear, conversational, accessible, avoiding visual cues (do not say 'as seen in table 1').
- Pronunciation cues: Spell out acronyms where appropriate (e.g., e-B-P-F, C-H-E-R-I).
- Duration target: 250-300 words (approx. 2 minutes at 140 WPM).
- Sign-off: 'Stay curious, keep your code clean, and we'll see you next week on TechPulse AI.'"""
    }
]

def seed_database():
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    # 1. Insert Trusted Sources
    print("Seeding trusted sources...")
    source_id_map = {}
    for s in TRUSTED_SOURCES:
        cursor.execute("""
        INSERT OR IGNORE INTO sources (name, type, official_url, credibility_rationale, trust_score, verification_status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (s["name"], s["type"], s["official_url"], s["credibility_rationale"], s["trust_score"], s["verification_status"]))
        
        cursor.execute("SELECT id FROM sources WHERE name = ?", (s["name"],))
        row = cursor.fetchone()
        if row:
            source_id_map[s["name"]] = row["id"]

    # 2. Insert Sample Weekly Digest Editions
    print("Seeding weekly digest editions...")
    edition_id_map = {}
    for ed in SAMPLE_EDITIONS:
        cursor.execute("""
        INSERT OR REPLACE INTO digest_editions (issue_number, title, theme, week_date, status, draft_email_subject, draft_email_body, audio_script)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ed["issue_number"],
            ed["title"],
            ed["theme"],
            ed["week_date"],
            ed["status"],
            ed["draft_email_subject"],
            ed["draft_email_body"],
            ed["audio_script"]
        ))
        cursor.execute("SELECT id FROM digest_editions WHERE issue_number = ?", (ed["issue_number"],))
        edition_id_map[ed["issue_number"]] = cursor.fetchone()["id"]

    # 3. Insert Sample Articles, Verification Checks, Summaries, and Digest Associations
    print("Seeding articles, verification checks, and summaries...")
    from verifier import verify_article

    for art in SAMPLE_ARTICLES:
        source_id = source_id_map.get(art["source_name"], 1)
        cursor.execute("""
        INSERT OR IGNORE INTO articles (title, abstract, content, url, source_id, source_name, authors, category, published_at, is_saved, is_digest_candidate, is_live_retrieved, verification_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            art["title"],
            art["abstract"],
            art["abstract"],
            art["url"],
            source_id,
            art["source_name"],
            art["authors"],
            art["category"],
            art["published_at"],
            art["is_saved"],
            art["is_digest_candidate"],
            art["is_live_retrieved"],
            art["verification_status"]
        ))

        cursor.execute("SELECT id FROM articles WHERE url = ?", (art["url"],))
        art_id = cursor.fetchone()["id"]

        # Verification check
        v_res = verify_article(art)
        cursor.execute("""
        INSERT OR REPLACE INTO verification_checks 
        (article_id, publisher_score, author_score, date_score, evidence_score, source_link_score, duplicate_score, outdated_score, overall_score, overall_status, checklist_json, evidence_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            art_id,
            v_res["publisher_score"],
            v_res["author_score"],
            v_res["date_score"],
            v_res["evidence_score"],
            v_res["source_link_score"],
            v_res["duplicate_score"],
            v_res["outdated_score"],
            v_res["overall_score"],
            v_res["overall_status"],
            json.dumps(v_res["checklist"]),
            v_res["evidence_notes"]
        ))

        # Structured summary
        headline = f"{art['category']} Digest: {art['title']}"[:95]
        summary_text = art["abstract"]
        why_it_matters = art["why_it_matters_cse"]
        facts = art["facts"]
        citations = [{"source": art["source_name"], "url": art["url"], "type": "Peer Source"}]
        claims = [
            {"claim": f, "status": "verified", "confidence": 96.0, "notes": "Corroborated by primary publication."}
            for f in facts
        ]

        cursor.execute("""
        INSERT OR REPLACE INTO summaries
        (article_id, headline, summary_text, why_it_matters_cse, key_facts_json, citations_json, claims_checked_json, is_approved, edited_by_user, model_used)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            art_id,
            headline,
            summary_text,
            why_it_matters,
            json.dumps(facts),
            json.dumps(citations),
            json.dumps(claims),
            1,
            0,
            "TechPulse-Curator-v1.0 (Expert Seeded)"
        ))

        # Associate with digest edition
        ed_issue = art.get("edition_issue")
        if ed_issue and ed_issue in edition_id_map:
            digest_id = edition_id_map[ed_issue]
            cursor.execute("""
            INSERT OR REPLACE INTO digest_articles (digest_id, article_id, display_order, custom_notes)
            VALUES (?, ?, ?, ?)
            """, (digest_id, art_id, art.get("display_order", 1), f"Featured in Issue #{ed_issue}"))

    # 4. Insert Prompts
    print("Seeding prompt library...")
    for p in PROMPTS_DATA:
        cursor.execute("""
        INSERT OR IGNORE INTO prompts (category, title, template_text, description, tags)
        VALUES (?, ?, ?, ?, ?)
        """, (p["category"], p["title"], p["template_text"], p["description"], p["tags"]))

    # 5. Insert User Settings
    print("Seeding default user settings...")
    defaults = {
        "gemini_api_key": "",
        "elevenlabs_api_key": "",
        "scheduled_runs_enabled": "true",
        "schedule_cron": "0 9 * * 1",  # Every Monday at 9:00 AM
        "digest_recipients": "cse-students@university.edu, cse-faculty@university.edu",
        "minimum_verification_score": "80",
        "auto_email_draft": "true"
    }
    for k, v in defaults.items():
        cursor.execute("INSERT OR REPLACE INTO user_settings (key, value) VALUES (?, ?)", (k, v))

    conn.commit()
    conn.close()
    print("Seeding complete! Database ready with 12 sources, 4 editions, seeded articles, and 7 prompts.")

if __name__ == "__main__":
    seed_database()
