import os
import warnings

import osmnx as ox
import pandas as pd

from app.people_count_task.utils import get_data_from_polygon

warnings.filterwarnings('ignore')

places = ["Пермь", "Екатеринбург", "Челябинск", "Омск", "Самара", "Санкт-Петербург", "Москва"]

result_dataframe = pd.DataFrame(
    columns=["building", "building:levels", "area", "horizontal_len", "vertical_len", "poly_shapes_count"])

for place in places:
    print(place)
    data = ox.footprints_from_place(place)
    data = data[['building', 'building:levels', 'geometry']]
    data = data.reset_index(drop=True)

    idx_for_drop = []
    data["area"], data["horizontal_len"], data["vertical_len"], data["poly_shapes_count"] = None, None, None, None
    for index, element in data.iterrows():
        try:
            data["area"][index], data["horizontal_len"][index], data["vertical_len"][index] = get_data_from_polygon(
                element.geometry)
            data["poly_shapes_count"][index] = element.geometry.exterior.coords.__len__()
        except Exception:
            pass
    data = data.drop(['geometry'], axis=1)
    result_dataframe = result_dataframe.append(data)
    result_dataframe = result_dataframe.reset_index(drop=True)
    result_dataframe.to_csv(os.path.join('app', 'people_count_task', 'data', 'data.csv'), index=False)
