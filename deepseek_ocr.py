from transformers import AutoTokenizer, AutoModel
from pathlib import Path
import torch
from PIL import Image

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-OCR", trust_remote_code=True)
model = AutoModel.from_pretrained("deepseek-ai/DeepSeek-OCR", trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()

def ocr_image_to_markdown(image_path: Path) -> str:
    img = Image.open(image_path).convert("RGB")
    prompt = "Please extract all text from this page in clean markdown with structure."
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    with torch.no_grad():
        response = model.chat(image=img, tokenizer=tokenizer, **inputs)
    return response
