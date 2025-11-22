from pdf2image import convert_from_bytes
from pathlib import Path

def render_pdf_to_images(pdf_bytes: bytes, outdir: Path):
    images = convert_from_bytes(pdf_bytes, dpi=300)
    paths = []
    for idx, img in enumerate(images, start=1):
        p = outdir / f"page_{idx:04d}.png"
        img.save(p)
        paths.append(p)
    return paths
