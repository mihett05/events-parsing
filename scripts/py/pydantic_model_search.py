import os
from pathlib import Path

comment = "# --------------------------------------------------------------------------"


def try_find_model(filename):
    with open(filename, "r") as f:
        data = f.read()
    if "CamelModel" in data:
        results = []
        current = ""
        for line in data.split("\n"):
            if "CamelModel" in line and not line.startswith("from"):
                current += line
            elif current != "":
                current += f"\n{line}"
                if line.strip() == "":
                    results.append(current)
                    current = ""
        return "\n\n\n".join(results)


def main():
    path = Path(__file__).parent.parent.parent.resolve() / "main_service"
    content = ""
    for root, _, files in os.walk(path):
        root = Path(root)
        for file in files:
            if not file.endswith(".py"):
                continue
            print(root / file)
            if result := try_find_model(root / file):
                content += f"{result}\n\n{comment}\n\n"

    with open("content.py", "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()
