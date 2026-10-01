"""
app.py
------
Flask REST API for the AI Resume Analyzer.
Exposes a single POST /api/analyze endpoint.
"""

import os
import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# ensure backend package is importable when run from any cwd
sys.path.insert(0, os.path.dirname(__file__))

from resume_parser import parse_resume, extract_contact_info, extract_sections
from nlp_analyzer  import analyze_resume

# ── app setup ─────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt"}
MAX_CONTENT_MB     = 5
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_MB * 1024 * 1024


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ── routes ────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "AI Resume Analyzer API is running."})


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Accepts a multipart/form-data POST with:
      - file  : the resume file (PDF / DOCX / TXT)
      - job   : (optional) target job role string

    Returns a JSON analysis report.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part in request."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        }), 415

    filename   = secure_filename(file.filename)
    file_bytes = file.read()

    try:
        # 1. parse raw text
        parsed  = parse_resume(file_bytes, filename)

        # 2. extract contact & sections
        contact  = extract_contact_info(parsed["raw_text"])
        sections = extract_sections(parsed["raw_text"])

        # 3. full NLP analysis
        result = analyze_resume(parsed, contact, sections)

        # 4. attach metadata
        result["filename"]     = filename
        result["contact_info"] = contact
        result["sections"]     = {k: v[:300] for k, v in sections.items()}  # truncate for payload

        return jsonify({"success": True, "data": result})

    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        app.logger.exception("Unexpected error during analysis")
        return jsonify({"error": "Internal server error.", "detail": str(e)}), 500


@app.route("/api/skills", methods=["GET"])
def list_skills():
    """Return the full skills taxonomy (useful for the frontend tag cloud)."""
    from skills_data import SKILLS_DB
    return jsonify({"skills": sorted(SKILLS_DB)})


@app.route("/api/roles", methods=["GET"])
def list_roles():
    """Return all supported job roles."""
    from skills_data import JOB_ROLES
    return jsonify({"roles": list(JOB_ROLES.keys())})


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
