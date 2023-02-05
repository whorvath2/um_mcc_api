from http import HTTPStatus
from typing import Dict, Final

from flask import Blueprint, jsonify, make_response, request

from co.deability.um_mcc import cost_calculator, person_finder

mcc_blueprint: Final[Blueprint] = Blueprint("um_mcc", __name__, url_prefix="/um_mcc/")

ACCESS_CONTROL_HEADER: Final[Dict[str, str]] = {"Access-Control-Allow-Origin": "*"}


@mcc_blueprint.get("/")
def health_check():
    return make_response(
        jsonify({"status": "OK"}),
        HTTPStatus.OK,
        ACCESS_CONTROL_HEADER,
    )


@mcc_blueprint.get("/find")
def find_staff():
    return make_response(
        jsonify(person_finder.find(args=request.args.to_dict())),
        HTTPStatus.OK,
        ACCESS_CONTROL_HEADER,
    )


@mcc_blueprint.post("/cost/<int:meeting_length_minutes>")
def calculate_meeting_cost(meeting_length_minutes):
    return (
        make_response(
            jsonify(
                cost_calculator.calc_meeting_cost_from_attendees(
                    attendees=request.json, minutes=meeting_length_minutes
                )
            ),
            HTTPStatus.OK,
        )
        if request.json
        else make_response(
            jsonify(
                {
                    "error": "The request body must contain a JSON-formatted list of employees"
                }
            ),
            HTTPStatus.BAD_REQUEST,
            ACCESS_CONTROL_HEADER,
        )
    )
