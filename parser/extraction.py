import json

from openai import OpenAI

from config import get_config
from events import DatesInfo, EventInfo

config = get_config()


class OpenAiExtraction:
    def __init__(self, init_prompt: str, url: str, model: str, key: str):
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
                {"role": "user", "content": self.init_prompt},
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
                {"role": "user", "content": self.init_prompt + text},
            ],
        )
        # print(completion)
        try:
            r = completion.choices[0].message.content
        except TypeError:
            print(completion)
            return result
        try:
            response_dict = json.loads(
                r.replace("```", "").replace("json", "").strip()
            )
        except:
            return result
        for item in response_dict:
            try:
                result.append(
                    EventInfo(**{**item, "dates": DatesInfo(**item["dates"])})
                )
                # print(result[-1])
            except:
                continue
        return result


def get_prompt():
    with open("./init_prompt.txt", encoding="UTF-8") as f:
        return f.read()


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
