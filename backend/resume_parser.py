"""
resume_parser.py
----------------
Extracts raw text from PDF and DOCX resume files,
then tokenizes and cleans it for downstream NLP.
"""

import re
import io
from pdfminer.high_level import extract_text as pdf_extract
from docx import Document
from skills_data import STOP_WORDS


# ── helpers ───────────────────────────────────────────────────────────────────

def _clean(text: str) -> str:
    """Lower-case, collapse whitespace, remove non-ASCII junk."""
    text = text.lower()
    text = re.sub(r"[^\x00-\x7F]+", " ", text)      # strip non-ASCII
    text = re.sub(r"[\r\n\t]+", " ", text)            # flatten newlines
    text = re.sub(r"[^\w\s\.\+\#\/\-]", " ", text)   # keep useful punctuation
    text = re.sub(r"\s{2,}", " ", text)               # collapse spaces
    return text.strip()


def _tokenize(text: str) -> list[str]:
    """Simple whitespace tokenizer that strips short/stop tokens."""
    tokens = text.split()
    return [t for t in tokens if len(t) > 1 and t not in STOP_WORDS]


# ── public API ────────────────────────────────────────────────────────────────

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Return raw text extracted from a PDF byte stream."""
    return pdf_extract(io.BytesIO(file_bytes))


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Return raw text extracted from a DOCX byte stream."""
    doc = Document(io.BytesIO(file_bytes))
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)


def parse_resume(file_bytes: bytes, filename: str) -> dict:
    """
    Master entry point.

    Returns
    -------
    {
        "raw_text"  : str,   full original text
        "clean_text": str,   normalised text
        "tokens"    : list   token list
    }
    """
    ext = filename.rsplit(".", 1)[-1].lower()

    if ext == "pdf":
        raw = extract_text_from_pdf(file_bytes)
    elif ext in ("doc", "docx"):
        raw = extract_text_from_docx(file_bytes)
    elif ext == "txt":
        raw = file_bytes.decode("utf-8", errors="replace")
    else:
        raise ValueError(f"Unsupported file format: .{ext}")

    clean = _clean(raw)
    tokens = _tokenize(clean)

    return {
        "raw_text":   raw,
        "clean_text": clean,
        "tokens":     tokens,
    }


# ── section extractor ─────────────────────────────────────────────────────────

_SECTION_PATTERNS = {
    "contact":    re.compile(r"(contact|email|phone|mobile|address|linkedin|github)", re.I),
    "education":  re.compile(r"(education|academic|qualification|degree|university|college)", re.I),
    "experience": re.compile(r"(experience|work|employment|career|position|internship)", re.I),
    "skills":     re.compile(r"(skill|technology|tool|language|framework|competenc)", re.I),
    "projects":   re.compile(r"(project|portfolio|build|develop)", re.I),
    "summary":    re.compile(r"(summary|objective|profile|about me|overview)", re.I),
    "certifications": re.compile(r"(certif|licens|award|achievement)", re.I),
}


def extract_sections(raw_text: str) -> dict[str, str]:
    """
    Rough section splitter.  Returns a dict of section_name → text snippet.
    Not guaranteed to be perfect for all resume layouts.
    """
    lines = raw_text.splitlines()
    sections: dict[str, list] = {k: [] for k in _SECTION_PATTERNS}
    current = "summary"

    for line in lines:
        matched = False
        for name, pat in _SECTION_PATTERNS.items():
            if pat.search(line) and len(line.strip()) < 60:   # likely a heading
                current = name
                matched = True
                break
        if not matched:
            sections[current].append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items()}


def extract_contact_info(raw_text: str) -> dict:
    """Pull email, phone, LinkedIn, and GitHub from raw text."""
    email_pat   = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
    phone_pat   = re.compile(r"(\+?\d[\d\s\-\(\)]{7,}\d)")
    linkedin    = re.compile(r"linkedin\.com/in/[\w\-]+", re.I)
    github      = re.compile(r"github\.com/[\w\-]+", re.I)

    return {
        "email":    (email_pat.findall(raw_text) or [None])[0],
        "phone":    (phone_pat.findall(raw_text) or [None])[0],
        "linkedin": (linkedin.findall(raw_text) or [None])[0],
        "github":   (github.findall(raw_text) or [None])[0],
    }
