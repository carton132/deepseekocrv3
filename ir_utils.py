import re
from markdown import markdown

def build_document_ir(pages):
    blocks = []
    for p in pages:
        lines = p.splitlines()
        for line in lines:
            if line.startswith("#"):
                level = len(line) - len(line.lstrip("#"))
                blocks.append({"type": "heading", "level": level, "text": line.lstrip("# ").strip()})
            else:
                blocks.append({"type": "paragraph", "text": line})
    return {"blocks": blocks}

def export_markdown(ir):
    out = []
    for b in ir["blocks"]:
        if b["type"] == "heading":
            out.append("#"*b["level"] + " " + b["text"])
        else:
            out.append(b["text"])
    return "\n\n".join(out)

def export_html_from_markdown(md):
    return "<html><body>" + markdown(md) + "</body></html>"
