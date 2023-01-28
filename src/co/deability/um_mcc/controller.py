from http import HTTPStatus
from typing import Final

from flask import Blueprint, jsonify, make_response, request

from co.deability.um_mcc import person_finder

mcc_blueprint: Final[Blueprint] = Blueprint("um_mcc", __name__, url_prefix="/um_mcc/")


@mcc_blueprint.get("/")
def health_check():
    return make_response(jsonify({"status": "OK"}), HTTPStatus.OK)


@mcc_blueprint.get("/find")
def find_staff():
    return make_response(
        jsonify(person_finder.find(args=request.args.to_dict())), HTTPStatus.OK
    )
