import json
from dataclasses import asdict

import requests
from bs4 import BeautifulSoup
from events import EventInfo
from extraction import extract_list

URL = "https://www.хакатоны.рф/"

def parser(url: str = URL) -> list[EventInfo]:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    items = soup.find_all('div', attrs={'data-record-type': lambda x: x in ['396', '776']})
    year = "2025"
    text = ""
    for item in items:
        if item.get('data-record-type') == '396':
            year = item.text.strip()
        else:
            for event in item.select("div.t776__textwrapper"):
                add_part = str(year) + " год\n" + event.text.strip() + "\n" + "-"*3 + "\n"
                if len(text + add_part) > 5000:
                    events += (extract_list(text))
                    text = add_part
                else:
                    text += add_part
    return events


def write(data: list[EventInfo]):
    with open("output.json", "w", encoding="utf8") as file:
        events = list(map(asdict, data))
        json.dump(events, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    write(parser())
