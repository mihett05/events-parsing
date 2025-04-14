import json
import re
from dataclasses import asdict
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from events import Event

URL = "https://www.хакатоны.рф/"
MONTH_NUM = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12",
}


def clear_date(date_str: str):
    date_str = date_str.lower().replace("до", "").replace("г.", "")
    date_str = date_str.replace("с", "").replace("по", "-")
    date_str = re.sub(r"[—–]", "-", date_str)
    date_str = date_str.replace(" - ", "-").strip()
    return date_str


def parse_date(date_str: str, year: str):
    date_str = clear_date(date_str)
    if "-" in date_str:
        start_part, end_part = date_str.split("-")
        if not re.search(r"[а-я]{3,}", start_part):
            start_part = f"{start_part} {end_part.split()[1]}"
        if not re.search(r"\d{4}", end_part):
            end_part = f"{end_part} {year}"
        if not re.search(r"\d{4}", start_part):
            start_part = "{0} {1}".format(
                start_part, re.search(r"\d{4}", end_part).group(1)
            )
        start_part = parse_date_part(start_part)
        end_part = parse_date_part(end_part)
        return start_part, end_part
    else:
        if not re.search(r"\d{4}", date_str):
            date_str = f"{date_str} {year}"
        return parse_date_part(date_str)


def parse_date_part(date_str: str):
    day, month, year = date_str.split()
    month = MONTH_NUM.get(month, "01")
    return datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y")


def parser(url: str = URL) -> list[Event]:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    for item in soup.select("div.t776__textwrapper"):
        title = item.select_one(".t776__title").text.strip()

        description = item.select_one(".t776__descr")
        for br in description.select("br"):
            br.replace_with("\n")
        description = description.text.strip()

        dates_match = re.search(r"Хакатон:\s*(.*?)\n", description)
        if not dates_match:
            continue
        try:
            dates = parse_date(dates_match.group(1).strip(), "2024")
            if isinstance(dates, tuple):
                start_date, end_date = dates
            else:
                start_date = end_date = dates

            registration_match = re.search(
                r"Регистрация:\s*до\s*(.*?)\n", description
            )
            end_registration = parse_date(
                registration_match.group(1).strip(), "2024"
            )
        except:
            continue
        events.append(
            Event(
                title=title,
                start_date=start_date,
                end_date=end_date,
                end_registration=end_registration,
                description=description,
                type="collect cotton",
                format="nigger",
            )
        )

    return events


def write(data: list[Event]):
    with open("output.json", "w", encoding="utf8") as file:
        events = list(map(asdict, data))
        for event in events:
            event["start_date"] = event["start_date"].strftime("%d-%m-%Y")
            event["end_date"] = event["end_date"].strftime("%d-%m-%Y")
            event["end_registration"] = event["end_registration"].strftime(
                "%d-%m-%Y"
            )
        json.dump(events, file, ensure_ascii=False, indent=4)
