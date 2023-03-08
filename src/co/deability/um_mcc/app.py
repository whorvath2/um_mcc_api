import logging

from flask import Flask

from co.deability.um_mcc import init_app


logging.getLogger().info("Starting UM_MCC API...")
app: Flask = init_app()

if __name__ == "__main__":
    app.run(port=8000)
