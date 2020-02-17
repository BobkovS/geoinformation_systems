from osgeo import osr, ogr

accommodation_buildings = ['apartments', 'bungalow', 'cabin', 'detached', 'dormitory', 'farm', 'ger', 'hotel', 'hotel',
                           'house',
                           'houseboat', 'residential', 'semidetached_house', 'static_caravan', 'terrace']
undefined_buildings = ['yes']


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
