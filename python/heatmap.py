import os
import pandas as pd
import numpy as np

import folium
from folium import plugins
from IPython.display import display

BASE_DIR = os.path.dirname(os.path.dirname( __file__ ))
DATA_DIR = os.path.join( BASE_DIR, 'data' )

df = pd.read_csv('https://brasil.io/dataset/covid19/caso?format=csv')
#df.city_ibge_code.astype('int64').dtypes

cidades = pd.read_csv(os.path.join(DATA_DIR, 'IBGE.csv'))
cidades = cidades.set_index("codigo_ibge")

cities = df.loc[ df.place_type == 'city' , : ]
cities = cities.join( cidades, on = "city_ibge_code" )

geo_last = cities.loc[cities.is_last == True, ['city', 'latitude', 'longitude', 'state', 'confirmed', 'deaths']]
geo_last = geo_last.dropna()
print(geo_last.head())
print(len(geo_last))
print(geo_last.confirmed.sum())
print(geo_last.state.unique())
print(len(geo_last.state.unique()))

coordenadas = geo_last[['latitude', 'longitude', 'confirmed']].dropna()

baseMap = folium.Map(
    width = "100%",
    height = "100%",
    location = [-15.788497, -47.879873],
    zoom_start = 4
)

baseMap = baseMap.add_child( plugins.HeatMap(coordenadas) )

for i in range(0, len(geo_last)):
    folium.Circle(
        location = [ geo_last.iloc[i]['latitude'], geo_last.iloc[i]['longitude'] ],
        color = '#00FF65',
        fill = '#0099FF',
        tooltip =   '<li><bold> CIDADE: ' + str(geo_last.iloc[i]['city']) + '</li></bold>' +
                    '<li><bold> ESTADO: ' + str(geo_last.iloc[i]['state']) + '</li></bold>' +
                    '<li><bold> CASOS: ' + str(geo_last.iloc[i]['confirmed']) + '</li></bold>' +
                    '<li><bold> MORTES: ' + str(geo_last.iloc[i]['deaths']) + '</li></bold>',
        radius = (geo_last.iloc[i]['confirmed']**1.1)
    ).add_to(baseMap)

baseMap.save('heatmap-cidades.html')