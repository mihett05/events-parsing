from models import EventInfo, MailModel

from .classification import is_text_relates_to_topics, topic_descriptions
from .extraction import extract_features


def pipeline(mail: MailModel) -> EventInfo | None:
    text = f"Тема письма: {mail.theme}\nОтправитель: {mail.sender}\nДата: {mail.received_date}\n\n{mail.raw_content.decode('utf-8')}"
    # TODO: добавить текст из документов

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
