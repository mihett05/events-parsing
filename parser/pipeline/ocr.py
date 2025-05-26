import io
import os
import sys

import cv2
import fitz
import numpy as np
import pytesseract
import requests
from docx import Document
from PIL import Image


def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="rus")
        return text
    except Exception:
        return None


def extract(pdf_url):
    response = requests.get(pdf_url)
    pdf_data = io.BytesIO(response.content)
    file = fitz.open(stream=pdf_data, filetype="pdf")
    full_text = []
    for pageNum, page in enumerate(file.pages(), start=1):
        text = page.get_text()
        full_text.append(f"=== Страница {pageNum} ===\n{text}\n")
    return "\n".join(full_text) if full_text else ""


def pdf_to_text_with_ocr(content: bytes) -> str:
    pdf_data = io.BytesIO(content)
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

    extracted_text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=600)
        img_bytes = pix.tobytes("ppm")
        img = Image.open(io.BytesIO(img_bytes))
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]
        custom_config = r"--oem 3 --psm 6"
        page_text = pytesseract.image_to_string(
            thresh, config=custom_config, lang="eng+rus"
        )
        extracted_text += f"--- Страница {page_num + 1} ---\n{page_text}\n"

    return extracted_text


def extract_text_from_docx(content: bytes):
    try:
        docx_file = io.BytesIO(content)
        doc = Document(docx_file)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception:
        return None


def get_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return "pdf"
    elif ext in (".png", ".jpg", ".jpeg"):
        return "image"
    elif ext == ".docx":
        return "docx"
    else:
        return "unknown"


def process_file(filename: str, content: bytes) -> str | None:
    file_type = get_file_type(filename)
    if file_type == "pdf":
        return pdf_to_text_with_ocr(content)
    elif file_type == "image":
        return pdf_to_text_with_ocr(content)
    elif file_type == "docx":
        return extract_text_from_docx(content)


def process_files(files: dict[str, bytes]) -> dict[str, str]:
    return {
        filename: text
        for filename, content in files.items()
        if (text := process_file(filename, content))
    }


def process_links(files_links: dict[str, str]) -> dict[str, str]:
    output = {}

    for filename, link in files_links.items():
        content = requests.get(link).content
        text = process_file(filename, content)
        if text:
            output[filename] = text

    return output


def process_filenames(filenames: list[str]) -> dict[str, str]:
    output = {}

    for filename in filenames:
        with open(filename, "rb") as f:
            text = process_file(filename, f.read())
            if text:
                output[filename] = text

    return output


if __name__ == "__main__":
    file_list = sys.argv[1:]
    print(process_filenames(file_list))
