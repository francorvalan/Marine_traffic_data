import requests
import json
from datetime import datetime
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def descargar_procesar_convertir(url_list):
    output_dir = "01_Request_data/01_Prince_Ruport_Area"
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    # Descargar datos web
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    # Lista para almacenar los DataFrames de cada URL
    dfs = []
    # Lista para almacenar los datos filtrados de cada URL
    datos_filtrados_list = []
    fecha_actual = datetime.now()
    for url in url_list:

        respuesta = requests.get(url, headers=headers)
        # Verificar si la solicitud fue exitosa
        if respuesta.status_code == 200:
            datos_json = respuesta.json()
            
            
            # Procesar JSON
            datos_filtrados = datos_json['data']['rows']
            for fila in datos_filtrados:
                for clave, valor in fila.items():
                    if valor is None:
                        fila[clave] = "_"

            
            # Agregar la fecha a cada fila en datos_filtrados
            for fila in datos_filtrados:
                fila['fecha_consulta'] = str(fecha_actual.strftime('%Y%m%d_%H%M%S'))
            datos_filtrados_list.extend(datos_filtrados)
    # Convertir a DataFrame 
    df = pd.DataFrame(datos_filtrados_list)

    # Convertir a GeoDataFrame
    geometry = [Point(lon, lat) for lon, lat in zip(df['LON'], df['LAT'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    # Escribir el GeoDataFrame en un archivo con nombre dependiente de la fecha
    output_file = f"{output_dir}/{fecha_actual.strftime('%Y%m%d_%H%M%S')}.shp"
    gdf.to_file(output_file)
    #return gdf

urls = ['https://www.marinetraffic.com/getData/get_data_json_4/z:11/X:141/Y:327/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:11/X:141/Y:326/station:0'

    #'https://www.marinetraffic.com/getData/get_data_json_4/z:11/X:140/Y:327/station:0',

    #'https://www.marinetraffic.com/getData/get_data_json_4/z:11/X:142/Y:327/station:0',

    #'https://www.marinetraffic.com/getData#/get_data_json_4/z:11/X:141/Y:328/station:0',

    #'https://www.marinetraffic.com/getData/get_data_json_4/z:11/X:140/Y:326/station:0',

    #'https://www.marinetraffic.com/getData/get_data_json_4/z:11/X:142/Y:326/station:0',

    #'https://www.marinetraffic.com/getData/get_data_json_4/z:11/X:140/Y:328/station:0',

    #'https://www.marinetraffic.com/getData/get_data_json_4/z:11/X:142/Y:328/station:0'

]
gdf = descargar_procesar_convertir(urls)