import requests
import json
from datetime import datetime
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def descargar_procesar_convertir(url_list):
    # Descargar datos web
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    fecha_actual = datetime.now()
    counter = 0
    dfs = pd.DataFrame()
    for url in url_list:
        
        df = pd.DataFrame()
        respuesta = requests.get(url, headers=headers)
        print(respuesta)
        # Verificar si la solicitud fue exitosa
        if respuesta.status_code == 200:
            counter += 1
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
            
            df =pd.concat([pd.DataFrame(datos_filtrados),df])
            
            print(df.head())
        # Unir df
        dfs = pd.concat([dfs, df])
        print(dfs.head())
    if counter>0:
    # Convertir a GeoDataFrame
        geometry = [Point(lon, lat) for lon, lat in zip(dfs['LON'], dfs['LAT'])]
        gdf = gpd.GeoDataFrame(dfs, geometry=geometry, crs="EPSG:4326")
        print(gdf)
        # Escribir el GeoDataFrame en un archivo con nombre dependiente de la fecha
        gdf_outputdir = "./01_Data/01_Prince_Ruport_Area/01_Shapefiles"
        if not os.path.exists(gdf_outputdir): os.makedirs(gdf_outputdir)
        output_file = f"{gdf_outputdir}/{fecha_actual.strftime('%Y%m%d_%H%M%S')}_{counter}-18.shp"
        gdf.to_file(output_file)
        
        geojson_outputdir = "./01_Data/01_Prince_Ruport_Area/02_Geojsons"
        if not os.path.exists(geojson_outputdir): os.makedirs(geojson_outputdir)
        with open(f"{geojson_outputdir}/{fecha_actual.strftime('%Y%m%d_%H%M%S')}_{counter}-18.geojson" , 'w') as file:
            file.write(gdf.to_json())
# urls = [
#         'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1128/Y:2622/station:0',
#     'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1128/Y:2620/station:0',
#     'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1128/Y:2619/station:0',
#     'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1128/Y:2618/station:0',
#     'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1128/Y:2617/station:0',
#     'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1128/Y:2621/station:0',
#     'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1129/Y:2618/station:0',
#     'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1129/Y:2617/station:0',
#     'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1129/Y:2621/station:0'
#     ]

urls = [
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1130/Y:2617/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1131/Y:2618/station:0',
        'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1129/Y:2618/station:0',
        'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1129/Y:2618/station:0',
        'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1131/Y:2617/station:0',
        'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1129/Y:2617/station:0',
        'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1130/Y:2617/station:0'
        'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1130/Y:2617/station:0',
        'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1128/Y:2622/station:0',
    
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1128/Y:2620/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1128/Y:2619/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1128/Y:2618/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1128/Y:2617/station:0',

'https://www.marinetraffic.com/getData/get_data_json_4/z:7/X:21/Y:38/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1128/Y:2621/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1129/Y:2618/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1129/Y:2617/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1129/Y:2621/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1129/Y:2620/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1129/Y:2619/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1129/Y:2622/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1130/Y:2617/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1130/Y:2619/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1130/Y:2621/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1130/Y:2620/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1130/Y:2622/station:0',
    'https://www.marinetraffic.com/getData/get_data_json_4/z:14/X:1130/Y:2618/station:0'
    ]
descargar_procesar_convertir(urls)
