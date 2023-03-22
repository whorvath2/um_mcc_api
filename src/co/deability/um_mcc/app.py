import logging

from flask import Flask

from co.deability.um_mcc import init_app


logging.getLogger().info("Starting UM_MCC API...")
app: Flask = init_app()

if __name__ == "__main__":
    if app.config["DEBUG"]:
        logging.getLogger().info("Running flask in debug mode on port 8000")
        app.run(port=8000)
    else:
        logging.getLogger().info(
            "Running flask in production mode using the default port"
        )
        app.run()
