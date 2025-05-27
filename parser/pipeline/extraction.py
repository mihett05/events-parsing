import json
import re

from config import get_config
from models import DatesInfoModel, EventInfoModel
from openai import OpenAI

config = get_config()


class OpenAiExtraction:
    """Класс для извлечения структурированной информации о событиях из текста с помощью OpenAI.

        Инкапсулирует логику взаимодействия с OpenAI API, включая парсинг ответов
        и валидацию извлеченных данных.
        """
    def __init__(
        self, init_prompt: dict[str, str], url: str, model: str, key: str
    ):
        """Инициализация клиента OpenAI с настройками для обработки текстовых запросов."""
        self.client = OpenAI(
            base_url=url,
            api_key=key,
        )
        self.model = model
        self.init_prompt = init_prompt

    def extract(self, text: str) -> EventInfoModel:
        """Извлекает данные о единичном событии из неструктурированного текста."""
        completion = self.client.chat.completions.create(
            extra_body={},
            model=self.model,
            messages=[
                {"role": "user", "content": self.init_prompt["single"]},
                {"role": "user", "content": text},
            ],
        )
        response = completion.choices[0].message.content

        return self.parse_response(response)

    def parse_response(self, response: str) -> EventInfoModel:  # noqa
        """Преобразует сырой ответ от OpenAI в валидированную модель события."""

        response_dict = json.loads(
            response.replace("```", "").replace("json", "").strip()
        )
        return EventInfoModel(
            **{
                **response_dict,
                "dates": DatesInfoModel(**response_dict["dates"]),
            }
        )

    def extract_list(self, text: str) -> list[EventInfoModel]:
        """Извлекает список событий из текста, фильтруя некорректные или неполные данные."""

        result = []
        completion = self.client.chat.completions.create(
            extra_body={},
            model=self.model,
            messages=[
                {"role": "user", "content": self.init_prompt["list"] + text},
            ],
        )
        try:
            r = completion.choices[0].message.content
        except TypeError:
            print("Tokens")
            return result
        try:
            response_dict = json.loads(
                r.replace("```", "").replace("json", "").strip()
            )
        except Exception:
            return result
        for item in response_dict:
            try:
                event = EventInfoModel(
                    **{**item, "dates": DatesInfoModel(**item["dates"])}
                )
                if event.location == "null":
                    event.location = None
                pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")
                if (
                    event.dates.start_date is not None
                    and pattern.match(event.dates.start_date)
                    and (
                        event.dates.end_date is None
                        or pattern.match(event.dates.end_date)
                    )
                    and (
                        event.dates.end_registration is None
                        or pattern.match(event.dates.end_registration)
                    )
                ):
                    result.append(event)
            except Exception:
                continue
        return result


def get_prompt() -> dict[str, str]:
    """Загружает шаблоны промтов для OpenAI из файлов (одиночный запрос и список)."""

    result = {}
    with open("./init_prompt.txt", encoding="UTF-8") as f:
        result["single"] = f.read()
    with open("./init_prompt_for_list.txt", encoding="UTF-8") as f:
        result["list"] = f.read()
    return result


api = OpenAiExtraction(
    get_prompt(),
    config.openai_url,
    config.openai_model,
    config.openai_api_key,
)


def extract_features(text: str) -> EventInfoModel:
    """Публичная функция для извлечения данных о событии из текста. Обертка вокруг OpenAiExtraction.extract."""
    return api.extract(text)


def extract_list(text: str) -> list[EventInfoModel]:
    """Публичная функция для извлечения списка событий. Обертка вокруг OpenAiExtraction.extract_list."""
    return api.extract_list(text)
