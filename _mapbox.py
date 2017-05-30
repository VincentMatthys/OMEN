import folium

"""
custom = folium.Map(location=[45.5236, -122.6750], tiles='Mapbox', API_key='pk.eyJ1IjoidmluY2VudG1hdHRoeXMiLCJhIjoiY2ozYm5xZzdoMDA3aDJ3bzluenppMWxuOSJ9.-r2ksAZeuF0F_m8pgCHcOQ')
custom.save('test.html')
"""

"""
map_osm = folium.Map(location=[45.5236, -122.6750])
map_osm.save('osm.html')
"""

stamen = folium.Map(location=[45.5236, -122.6750], tiles='Stamen Toner',
                    zoom_start=13)
stamen.save('stamen_toner.html')
