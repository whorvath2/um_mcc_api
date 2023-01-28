from flask import Flask

from co.deability.um_mcc import init_app

app: Flask = init_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8662)
