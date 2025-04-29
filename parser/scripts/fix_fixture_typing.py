import os
from pathlib import Path

comment = "# --------------------------------------------------------------------------"


def fix_typing(filename):
    with open(filename, "r") as f:
        data = f.read()

    return data.replace("Callable[[...]", "Callable[[]")


def main():
    relative = "main_service/infrastructure/tests/integration_tests"
    path = Path(__file__).parent.parent.parent.resolve() / relative

    for root, _, files in os.walk(path):
        root = Path(root)
        for file in files:
            if not file.endswith(".py"):
                continue
            print(root / file)
            result = fix_typing(root / file)
            with open(root / file, "w", encoding="utf8") as f:
                f.write(result)


if __name__ == "__main__":
    main()
