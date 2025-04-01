from classification import is_text_relates_to_topics, topic_descriptions
from events import EventInfo
from extraction import extract_features


def pipeline(text: str) -> EventInfo | None:
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
