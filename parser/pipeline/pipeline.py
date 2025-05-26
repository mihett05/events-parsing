import os
from urllib.parse import urlparse

from models import EventInfoModel, MailModel

from .classification import is_text_relates_to_topics, topic_descriptions
from .extraction import extract_features
from .ocr import process_links


def pipeline(mail: MailModel) -> EventInfoModel | None:
    text = f"Тема письма: {mail.theme}\nОтправитель: {mail.sender}\nДата: {mail.received_date}\n\n{mail.raw_content.decode('utf-8')}"
    links = {
        os.path.basename(urlparse(attachment).path): attachment
        for attachment in mail.attachments
    }
    files = process_links(links)

    if files:
        text += "Приложения:\n\n"

    for filename, content in files.items():
        text += f"{filename}: {content}\n\n"

    if not is_text_relates_to_topics(text, topic_descriptions):
        return None
    event = extract_features(text)
    required_fields = (
        event.dates.start_date,
        event.title,
        event.format,
        event.type,
    )
    if not all(required_fields):
        return None

    return event
