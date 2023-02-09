import logging
from flask import Flask

from co.deability.um_mcc import init_app


def create_app():
    logging.getLogger().info("Starting UM_MCC API...")
    app: Flask = init_app()
    return app


if __name__ == "__main__":
    app: Flask = create_app()
    app.run()
