import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import uuid
import threading

from utils.pdf_utils import render_pdf_to_images
from deepseek_ocr import ocr_image_to_markdown
from ir_utils import build_document_ir, export_markdown, export_html_from_markdown

app = FastAPI()

WORKDIR = Path("server_jobs")
WORKDIR.mkdir(exist_ok=True)

def process_job(job_id: str, pdf_bytes: bytes):
    job_dir = WORKDIR / job_id
    input_dir = job_dir / "input"
    pages_dir = job_dir / "pages"
    ocr_dir = job_dir / "ocr_raw"
    ir_dir = job_dir / "ir"
    export_dir = job_dir / "exports"

    for d in [input_dir, pages_dir, ocr_dir, ir_dir, export_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Save PDF
    pdf_path = input_dir / "input.pdf"
    pdf_path.write_bytes(pdf_bytes)

    # Render pages
    images = render_pdf_to_images(pdf_bytes, pages_dir)
    markdown_pages = []

    for idx, img in enumerate(images, start=1):
        md = ocr_image_to_markdown(img)
        out = ocr_dir / f"page_{idx:04d}.md"
        out.write_text(md)
        markdown_pages.append(md)

    # Build IR
    doc_ir = build_document_ir(markdown_pages)
    (ir_dir / "document_ir.json").write_text(json.dumps(doc_ir, indent=2))

    # Exports
    md_full = export_markdown(doc_ir)
    html_full = export_html_from_markdown(md_full)

    (export_dir / "document.md").write_text(md_full)
    (export_dir / "document.html").write_text(html_full)

@app.post("/jobs")
async def create_job(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    pdf_bytes = await file.read()
    t = threading.Thread(target=process_job, args=(job_id, pdf_bytes))
    t.start()
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job_dir = WORKDIR / job_id
    if not job_dir.exists():
        return JSONResponse({"error": "job not found"}, status_code=404)
    return {"status": "completed", "job_id": job_id}
