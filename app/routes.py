import osmnx as ox
from flask import request, jsonify, make_response

from app import app


@app.route('/town_buildings_variances', methods=["POST"])
def building_variances():
    resp_data = {"building_variances": None,
                 "errors": None}
    req_json = request.get_json()
    town_name = req_json["town_name"]
    try:
        buildings = ox.footprints_from_place(town_name)
        resp_data["building_variances"] = buildings['building'].value_counts().to_dict()
        return make_response(jsonify(resp_data))
    except Exception:
        resp_data["errors"] = "Не получается найти выбранное место, попробуйте другое"
        return make_response(jsonify(resp_data))

@app.route('/district_amenities')
def district_amenities():
    import osmnx as ox
    town_name = "Пермь Ленинский район"
    Ameneties = ox.pois_from_place(town_name)
