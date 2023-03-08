import html
import logging
import os
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Final, Generator, Iterator, List

from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix


__version__: str = "1.1.1"


def init_app() -> Flask:
    app: Flask = Flask("um_mcc")
    # Remove the next line in production if the API is exposed to the internet
    CORS(app)
    app.url_map.strict_slashes = False
    _register_blueprints(app)
    return app


def _register_blueprints(app: Flask):
    from co.deability.um_mcc.resources import mcc_blueprint

    app.register_blueprint(mcc_blueprint)


def _add_proxy_fix(app: Flask):
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


class EmployeeProperties(str, Enum):
    KEY = "key"
    NAME = "name"
    TITLE = "title"
    DEPARTMENT = "department"
    SALARY = "salary"


def _key_generator() -> Generator[int, None, None]:
    current_key: int = 1
    while True:
        yield current_key
        current_key += 1


def _find_salary_file() -> Path:
    salary_file_name: str = "salary-disclosure-2022.csv"
    um_mcc_dir: Any = os.getenv("UM_MCC_DIR")
    current_dir: Path = (
        Path(um_mcc_dir) if um_mcc_dir else Path(__file__).parent.resolve()
    )
    salary_file_path_maker: () = lambda curr_dir: Path(
        curr_dir, salary_file_name
    ).absolute()

    salary_file_path = salary_file_path_maker(current_dir)
    while not salary_file_path.exists() and current_dir != Path(current_dir.root):
        current_dir = current_dir.parent
        salary_file_path = salary_file_path_maker(current_dir)
    print(f"salary_file_path = {salary_file_path}")
    return salary_file_path


def _read_file() -> Iterator[Dict]:
    filepath: Path = _find_salary_file()
    if not filepath.exists():
        logging.getLogger().critical(f"The salary file cannot be found at {filepath}")
        exit(1)
    key_maker = _key_generator()
    with filepath.open(mode="r", buffering=1) as salaryfile:
        salaryfile.readline()  # ignore header line
        line = salaryfile.readline()
        while line:
            yield _parse_line(line=html.unescape(line), key=next(key_maker))
            line = salaryfile.readline()


def _parse_line(line: str, key: int):
    words: List[str] = line.split("|")
    assert len(words) == 8
    name: str = ", ".join(words[1].split(sep=",", maxsplit=1))
    return {
        EmployeeProperties.KEY: key,
        EmployeeProperties.NAME: name.upper(),
        EmployeeProperties.TITLE: words[2].upper(),
        EmployeeProperties.DEPARTMENT: words[3].upper(),
        EmployeeProperties.SALARY: Decimal("".join(words[4].split(","))),
    }


SALARY_DATA: Final[List[Dict[str, Any]]] = list(_read_file())
