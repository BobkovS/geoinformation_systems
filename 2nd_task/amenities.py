import osmnx as ox

sustenance_amenities = ['bar', 'bbq', 'biergarten', 'cafe', 'fast_food', 'food_court', 'ice_cream', 'pub', 'restaurant']


def find_amenities(place_name):
    area = ox.gdf_from_place(place_name)
    graph = ox.graph_from_place(place_name)
    nodes, edges = ox.graph_to_gdfs(graph)
    buildings = ox.footprints_from_place(place_name)
    amenities = ox.pois_from_place(place_name, amenities=sustenance_amenities)

    ax = area.plot(facecolor='white')
    ax = edges.plot(ax=ax, linewidth=1, edgecolor='#BC8F8F', alpha=0.2)
    ax = buildings.plot(ax=ax, facecolor='blue', alpha=1)
    ax = amenities.plot(ax=ax, color='green', alpha=1, markersize=10)
    ax.figure.savefig('amenities.png')

    sustenance_amenities_variances = dict(amenities.amenity.value_counts())

    wrong_dict_keys = []
    for key in sustenance_amenities_variances.keys():
        if key not in sustenance_amenities:
            wrong_dict_keys.append(key)
    for key in wrong_dict_keys:
        del sustenance_amenities_variances[key]

    return sustenance_amenities_variances


place_for_search = "Пермь Ленинский Район"
print(f"Разновидности общепита в {place_for_search}: {find_amenities(place_for_search)}")
