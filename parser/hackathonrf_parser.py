import json
from dataclasses import asdict
from typing import Iterator

import requests
from bs4 import BeautifulSoup
from events import EventInfo
from extraction import extract_list

URL = "https://www.хакатоны.рф/"


def parser(url: str = URL, stop_year: int = 2020) -> Iterator[EventInfo]:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.find_all(
        "div", attrs={"data-record-type": lambda x: x in ["396", "776"]}
    )
    year = "2025"
    text = "---\n"
    for item in items:
        if item.get("data-record-type") == "396":
            year = item.text.strip()
            if year == str(stop_year):
                events = extract_list(text)
                yield from events
                # write(events)
                break
            print(year)
        else:
            for event in item.select("div.t776__textwrapper"):
                for br in item.select("br"):
                    br.replace_with("\n")
                add_part = str(year) + " год\n" + event.text.strip() + "\n---\n"
                if len(text + add_part) > 6400:
                    events = extract_list(text)
                    # write(events)
                    text = add_part
                    yield from events
                else:
                    text += add_part


def write(data: list[EventInfo]):
    with open("output.json", "w", encoding="utf8") as file:
        events = list(map(asdict, data))
        json.dump(events, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    for i in parser():
        print(i)
