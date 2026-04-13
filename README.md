# LLM Content Intelligence Pipeline

> Automated content summarisation pipeline using OpenAI GPT — demonstrating production LLM integration patterns: prompt engineering, token budget management, structured output, and batch file processing.

[![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI_GPT-412991?style=flat&logo=openai&logoColor=white)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## Overview

This project implements a production-ready LLM content processing pipeline demonstrating core patterns essential to enterprise AI systems:

- **Token budget management** — precise control over input/output token windows using `tiktoken`
- **Prompt engineering** — instruction-tuned summarisation with configurable style and length constraints
- **Batch processing** — stateless, idempotent pipeline over a directory of Markdown documents
- **Structured output injection** — marker-based content insertion for CMS and static site generators

These are the same patterns used in production RAG and agentic systems, applied to a self-contained, runnable use case.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  PIPELINE FLOW                       │
│                                                     │
│  Blog Directory                                     │
│       │                                             │
│       ▼                                             │
│  Document Loader ──→ HTML/Markdown Parser           │
│       │               (BeautifulSoup)               │
│       ▼                                             │
│  Token Counter ──→ Content Truncation               │
│  (tiktoken)         (respects model context window) │
│       │                                             │
│       ▼                                             │
│  Prompt Assembly ──→ OpenAI GPT API Call            │
│  (instruction +       (configurable model/tokens)   │
│   content)            │                             │
│                       ▼                             │
│               Summary Extraction                    │
│                       │                             │
│                       ▼                             │
│               Marker-Based Injection ──→ Updated    │
│               (<!-- Insert Summary Here -->)  File  │
└─────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| LLM | OpenAI GPT (configurable) | Summarisation inference |
| Token counting | `tiktoken` | Precise context window management |
| HTML parsing | `BeautifulSoup4` | Clean content extraction |
| File I/O | Python `os` + `pathlib` | Idempotent batch processing |

---

## Key Engineering Patterns

### 1. Token Budget Management
```python
def num_tokens_in_content(content: str, model_name: str) -> int:
    """
    Count tokens BEFORE making the API call.
    Critical for: cost control, avoiding 4096/8192 context limit errors,
    and ensuring prompt + response fits within the model window.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(content))
```

### 2. Idempotent Batch Processing
```python
# Marker-based injection is idempotent — safe to re-run on already-processed files
# The insertion marker acts as a state flag: present = unprocessed, absent = done
INSERTION_MARKER = "<!-- Insert Summary Here -->"

if INSERTION_MARKER in content:
    summary = generate_blog_summary(content, MODEL_NAME, MAX_RESPONSE_TOKENS)
    updated = content.replace(INSERTION_MARKER, summary)
    write_file(path, updated)
```

### 3. Configurable Prompt Template
```python
# Prompt engineering: explicit instruction + length constraint + tone guidance
prompt = f"""
Summarise the following blog article in {MAX_RESPONSE_TOKENS} tokens or fewer.
Write for a technical audience. Lead with the key insight.
Be precise — avoid filler phrases.

Article:
{content}
"""
```

---

## Configuration

```python
# config.py — all tuneable parameters in one place
OPENAI_API_KEY   = "YOUR_API_KEY"
BLOG_DIR         = "./content/posts"
BLOG_FILE_EXT    = ".markdown"
MODEL_NAME       = "gpt-4o"               # Swap to gpt-3.5-turbo for cost reduction
MAX_RESPONSE_TOKENS = 150                  # Controls summary length
INSERTION_MARKER = "<!-- Insert Summary Here -->"
BLOG_OFFSET      = 11                     # Lines to skip (frontmatter)
```

---

## Quickstart

```bash
git clone https://github.com/codebygarrysingh/blog-summarizer-app
cd blog-summarizer-app
pip install openai tiktoken beautifulsoup4

# Configure
cp config.example.py config.py
# Edit config.py: set OPENAI_API_KEY and BLOG_DIR

# Run
python main.py
```

---

## Extending This Pattern

This pipeline is intentionally minimal to be a clear foundation for extension:

| Extension | How |
|---|---|
| Swap to Claude / Gemini | Replace OpenAI client with `anthropic` / `google-generativeai` |
| Add RAG context | Inject retrieved docs into prompt before summarisation |
| Stream responses | Use `stream=True` for real-time output |
| Async batch processing | Wrap API calls in `asyncio.gather()` for 10× throughput |
| Quality evaluation | Add ROUGE/BERTScore to measure summary quality |

---

## Related Work

- [production-rag-pipeline](https://github.com/codebygarrysingh/production-rag-pipeline) — advanced LLM pipeline with hybrid retrieval and evaluation
- [llmops-reference-architecture](https://github.com/codebygarrysingh/llmops-reference-architecture) — production deployment, versioning, and drift monitoring

---

## Author

**Garry Singh** — Principal AI & Data Engineer · MSc Oxford

[Portfolio](https://garrysingh.dev) · [LinkedIn](https://linkedin.com/in/singhgarry) · [Book a Consultation](https://calendly.com/garry-singh2902)
