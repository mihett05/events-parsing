import json
<<<<<<< HEAD
=======
import re
>>>>>>> 734238dad51cb720fbb31b35c5efe9ed046573b5

from config import get_config
from events import DatesInfo, EventInfo
from openai import OpenAI

config = get_config()


class OpenAiExtraction:
    def __init__(
        self, init_prompt: dict[str, str], url: str, model: str, key: str
    ):
        self.client = OpenAI(
            base_url=url,
            api_key=key,
        )
        self.model = model
        self.init_prompt = init_prompt

    def extract(self, text: str) -> EventInfo:
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

    def parse_response(self, response: str) -> EventInfo:  # noqa
        response_dict = json.loads(
            response.replace("```", "").replace("json", "").strip()
        )
        return EventInfo(
            **{**response_dict, "dates": DatesInfo(**response_dict["dates"])}
        )

    def extract_list(self, text: str) -> list[EventInfo]:
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
        except:
            return result
        for item in response_dict:
            try:
                event = EventInfo(
                    **{**item, "dates": DatesInfo(**item["dates"])}
                )
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
                    # print(result[-1])
            except:
                continue
        return result


def get_prompt() -> dict[str, str]:
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


def extract_features(text: str) -> EventInfo:
    return api.extract(text)


def extract_list(text: str) -> list[EventInfo]:
    return api.extract_list(text)
