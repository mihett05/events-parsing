import os
import pytesseract
from PIL import Image
from docx import Document
import fitz
import io
import cv2
import numpy as np

# Тут по идее надо его поставить
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='rus')
        return text
    except Exception as e:
        print(f"Ошибка при обработке изображения {image_path}: {str(e)}")
        return ""


# круто работает если pdf приведенный
def extract(pdf_path):
    file = fitz.open(pdf_path)
    full_text = []
    for pageNum, page in enumerate(file.pages(), start=1):
        text = page.get_text()
        full_text.append(f"=== Страница {pageNum} ===\n{text}\n")
    return "\n".join(full_text) if full_text else ""


# сканы
def pdf_to_text_with_ocr(pdf_path, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_txt_path = os.path.join(output_dir, f"{base_name}_ocr.txt")
    pdf_document = fitz.open(pdf_path)
    extracted_text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=600)
        img_bytes = pix.tobytes("ppm")
        img = Image.open(io.BytesIO(img_bytes))
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        custom_config = r'--oem 3 --psm 6'
        page_text = pytesseract.image_to_string(
            thresh,
            config=custom_config,
            lang='eng+rus'
        )
        extracted_text += f"--- Страница {page_num + 1} ---\n{page_text}\n"

    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

    return output_txt_path


def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Ошибка при обработке DOCX {docx_path}: {str(e)}")
        return ""


def get_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return 'pdf'
    elif ext in ('.png', '.jpg', '.jpeg'):
        return 'image'
    elif ext == '.docx':
        return 'docx'
    else:
        return 'unknown'


def process_file(file_path):
    file_type = get_file_type(file_path)
    if file_type == 'pdf':
        return pdf_to_text_with_ocr(file_path)
    elif file_type == 'image':
        return pdf_to_text_with_ocr(file_path)
    elif file_type == 'docx':
        return extract_text_from_docx(file_path)
    else:
        print(f"Формат не поддерживается: {file_path}")
        return ""


def process_files(file_list, output_dir="output_texts"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for file_path in file_list:
        if not os.path.exists(file_path):
            print(f"Файл не найден: {file_path}")
            continue

        text = process_file(file_path)
        filename = os.path.splitext(os.path.basename(file_path))[0] + ".txt"
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Результат сохранён: {output_path}\n")
