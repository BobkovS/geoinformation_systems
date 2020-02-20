import os
import pickle
import warnings

import numpy as np
import osmnx as ox
from osgeo import osr, ogr

warnings.filterwarnings('ignore')


def get_data_from_polygon(geometry):
    json = {'type': 'Polygon',
            'coordinates': [list(geometry.exterior.coords)]}

    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)
    target = osr.SpatialReference()
    target.ImportFromEPSG(5243)

    transform = osr.CoordinateTransformation(source, target)
    poly = ogr.CreateGeometryFromJson(str(json).replace('(', '[').replace(')', ']'))
    poly.Transform(transform)
    x1, x2, y1, y2 = poly.GetEnvelope()
    h_len, v_len, area = abs(x2 - x1), abs(y2 - y1), poly.GetArea()
    return area, h_len, v_len


encoder = pickle.load(open(os.path.join('data', 'encoder.pkl'), 'rb'))
model = pickle.load(open(os.path.join('data', 'model.pkl'), 'rb'))

accommodation_buildings = ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'ger', 'hotel',
                           'house', 'houseboat', 'residential', 'semidetached_house', 'static_caravan', 'terrace']
undefined_buildings = ['yes']


def score_people_count(data):
    people_count = 0
    for ix, row in data.iterrows():
        if row['building:levels']:
            people_count += row.area * int(row['building:levels']) / 22
        else:
            people_count += row.area / 22
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
            data["poly_shapes_count"][index], data['building:levels'] = element.geometry.exterior.coords.__len__(), '1'
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

    people_count = score_people_count(data)

    return people_count, accommodation_building_variances


place_for_search = "Пермь Ленинский Район"
p_count, b_variances = score_people_count_script(place_for_search)
print(f"По расчетам в {place_for_search} проживает {round(p_count)} человек\n"
      f"Разновидности жилых зданий в {place_for_search}: {b_variances}")
