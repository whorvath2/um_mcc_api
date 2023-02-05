from flask import Flask

from co.deability.um_mcc import init_app

app: Flask = init_app()


def run_app():
    app.run(host="0.0.0.0", port=8662)


if __name__ == "__main__":
    run_app()
