import pandas as pd

# Загрузка CSV
df = pd.read_csv("events.csv")


def esc(val):
    if pd.isna(val):
        return "NULL"
    return "'{}'".format(str(val).replace("'", "''"))


with open("events.sql", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        values = [
            str(int(row["id"])),
            esc(row["created_at"]),
            esc(row["title"]),
            esc(row["description"]),
            "TRUE" if row["is_visible"] else "FALSE",
            esc(row["end_date"]),
            esc(row["start_date"]),
            esc(row["end_registration"]),
            esc(row["type"]),
            esc(row["format"]),
            esc(row["location"]),
        ]
        f.write(
            "INSERT INTO events (id, created_at, title, description, is_visible, end_date, start_date, end_registration, type, format, location)\n"
        )
        f.write(f"VALUES ({', '.join(values)});\n\n")
