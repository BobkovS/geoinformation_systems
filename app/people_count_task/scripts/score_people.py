import pickle
import warnings

import numpy as np
import osmnx as ox

from app.people_count_task.utils import get_data_from_polygon, accommodation_buildings, undefined_buildings

warnings.filterwarnings('ignore')

encoder = pickle.load(open('app/people_count_task/data/encoder.pkl', 'rb'))
model = pickle.load(open('app/people_count_task/data/model.pkl', 'rb'))


def score_people_count(data):
    people_count = 0
    for ix, row in data.iterrows():
        people_count += row.area / 24
    return people_count


def score_people_count_script(place_name):
    data = ox.footprints_from_place(place_name)

    data = data[['building', 'building:levels', 'geometry']]
    data = data.reset_index(drop=True)

    data["area"], data["horizontal_len"], data["vertical_len"], data["poly_shapes_count"] = None, None, None, None
    for index, element in data.iterrows():
        try:
            data["area"][index], data["horizontal_len"][index], data["vertical_len"][index] = get_data_from_polygon(
                element.geometry)
            data["poly_shapes_count"][index] = element.geometry.exterior.coords.__len__()
        except Exception:
            pass

    data = data.drop(['geometry'], axis=1)
    data = data.reset_index(drop=True)

    data.poly_shapes_count = data.poly_shapes_count.astype('float')
    data = data[np.isfinite(data['poly_shapes_count'])]

    data = data.fillna(0)
    data_accomodation_buildings = data.loc[data.building.isin(accommodation_buildings)]
    data_undefined_buildings = data.loc[data.building.isin(undefined_buildings)]

    data_undefined_buildings = data_undefined_buildings.drop(['building'], axis=1)
    data_undefined_buildings['building'] = model.predict(data_undefined_buildings)
    data_undefined_buildings.building = encoder.inverse_transform(data_undefined_buildings.building.astype('int'))

    data = data_accomodation_buildings.append(data_undefined_buildings)
    data = data.loc[data.building.isin(accommodation_buildings)]

    accommodation_building_variances = dict(data.building.value_counts())

    print(data['building:levels'].value_counts())
    people_count = score_people_count(data)

    return people_count, accommodation_building_variances

