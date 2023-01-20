import html
from pathlib import Path
from typing import Any, Dict, Final, Iterator, List
from decimal import Decimal


def read_file() -> Iterator[Dict]:
    filedir: Path = Path(__file__).parent
    filepath: Path = Path(filedir, "resources", "salary-disclosure-2022.csv")
    with filepath.open(mode="r", buffering=1) as salaryfile:
        salaryfile.readline()  # ignore header line
        line = salaryfile.readline()
        while line:
            yield parse_line(html.unescape(line))
            line = salaryfile.readline()


def parse_line(line: str):
    words: List[str] = line.split("|")
    assert len(words) == 8
    return {
        "name": words[1].upper(),
        "title": words[2].title(),
        "department": words[3].title(),
        "salary": Decimal("".join(words[4].split(","))),
    }


SALARY_DATA: Final[List[Dict[str, Any]]] = list(read_file())


def find_by_name(name: str) -> Iterator[Dict[str, Any]]:
    assert name
    name_uc = name.upper()
    return filter(lambda item: name_uc in item["name"], SALARY_DATA)
