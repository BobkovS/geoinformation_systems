import traceback

from flask import request, jsonify, make_response

from app import app
from app.people_count_task.scripts.score_people import score_people_count_script


@app.route('/score_people_count', methods=["POST"])
def people_count():
    resp_data = {"building_variances": None,
                 "people_count": None,
                 "errors": None}
    req_json = request.get_json()
    place_name = req_json["place_name"]
    try:
        resp_data['people_count'], resp_data['building_variances'] = score_people_count_script(place_name)
        resp_data['people_count'] = str(resp_data['people_count'])
        resp_data['building_variances'] = str(resp_data['building_variances'])
        return make_response(jsonify(resp_data))
    except Exception:
        resp_data["errors"] = traceback.format_exc()
        return make_response(jsonify(resp_data))
