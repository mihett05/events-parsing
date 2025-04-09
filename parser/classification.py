import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("punkt_tab")

topic_descriptions = {
    "hackathon": "Мероприятие, где участники работают в командах над решением технических задач в ограниченное время.",
    "conference": "Мероприятие, где люди собираются, чтобы обсудить и обменяться идеями по определенной теме.",
    "programming contest": "Соревнование или олимпиада, где участники решают алгоритмические задачи по программированию чаще всего самостоятельно и соревнуются друг с другом.",
}


def is_text_relates_to_topics(
    text: str, descriptions: dict[str, str], threshhold: float = 0.3
) -> bool:
    text = preprocess_text(text)
    text_emb = model.encode([text])

    topic_scores = []
    for topic, description in descriptions.items():
        description_emb = model.encode([description])
        similarity = util.cos_sim(text_emb, description_emb)[0][0]
        topic_scores.append((topic, similarity))

    topic, score = max(topic_scores, key=lambda x: x[1])

    # примитивная проверка, что на вход поступает не общая статья, а конкретное событие
    event_detected = any(
        date_str in text.lower()
        for date_str in [
            "года",
            "января",
            "февраля",
            "марта",
            "апреля",
            "мая",
            "июня",
            "июля",
            "августа",
            "сентября",
            "октября",
            "ноября",
            "декабря",
        ]
    )

    return score < threshhold


def preprocess_text(text: str):
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens]

    stop_words = set(stopwords.words("russian"))
    tokens = [token for token in tokens if token not in stop_words]

    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]

    return " ".join(tokens)
