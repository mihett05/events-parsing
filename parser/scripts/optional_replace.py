import os
from pathlib import Path


def fix_typing_optional(filename):
    with open(filename, "r") as f:
        data = f.read()
    result = ""
    for line in data.split("\n"):
        if "Optional[" not in line:
            result += line
        else:
            line_ = line.split('Optional[')
            prefix = line_[0]
            type_ = line_[1].split("]")[0]
            suffix = line_[1].split("]")[1]
            result += f"{prefix}{type_} | None{suffix}"

    return result


def main():
    relative = "main_service/infrastructure/tests/integration_tests"
    path = Path(__file__).parent.parent.parent.resolve() / relative

    for root, _, files in os.walk(path):
        root = Path(root)
        for file in files:
            if not file.endswith(".py"):
                continue
            print(root / file)
            result = fix_typing_optional(root / file)
            with open(root / file, "w", encoding="utf8") as f:
                f.write(result)


if __name__ == "__main__":
    main()
