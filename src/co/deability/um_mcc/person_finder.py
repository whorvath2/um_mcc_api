import html
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Final, Iterator, List


def _read_file() -> Iterator[Dict]:
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
        "title": words[2].upper(),
        "department": words[3].upper(),
        "salary": Decimal("".join(words[4].split(","))),
    }


SALARY_DATA: Final[List[Dict[str, Any]]] = list(_read_file())


def find_by_name(name: str) -> Iterator[Dict[str, Any]]:
    assert name
    name_uc: str = name.upper()
    return filter(lambda item: name_uc in item["name"], SALARY_DATA)


def find_by_name_dept(name: str, dept: str) -> List[Dict[str, Any]]:
    possible_matches: List[Dict[str, Any]] = list(find_by_name(name=name))
    if not possible_matches:
        return []
    dept_uc: str = dept.upper()
    if len(possible_matches) == 1 and dept == possible_matches[0]["department"]:
        return [possible_matches[0]]
    else:
        assert len(possible_matches) > 1
        return list(
            filter(lambda item: dept_uc in item["department"], possible_matches)
        )


def find_by_name_dept_title(name: str, dept: str, title: str) -> List[Dict[str, Any]]:
    possible_matches: List[Dict[str, Any]] = list(
        find_by_name_dept(name=name, dept=dept)
    )
    title_uc = title.upper()
    if len(possible_matches) == 1 and title_uc == possible_matches[0]["title"]:
        return [possible_matches[0]]
    else:
        assert len(possible_matches) > 1
        return list(filter(lambda item: title_uc in item["title"], possible_matches))
