import requests
import json
from datetime import datetime

def guardar_como_json(url):
    fecha_actual = datetime.now()
    nombre_archivo = f"datos_{fecha_actual.day}_{fecha_actual.month}_{fecha_actual.year}.json"

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    respuesta = requests.get(url, headers=headers)
    
    # Verificar si la solicitud fue exitosa
    if respuesta.status_code == 200:
        # Obtener el contenido JSON
        datos_json = respuesta.json()
        
        # Guardar los datos JSON en un archivo
        with open(nombre_archivo, 'w') as archivo:
            json.dump(datos_json, archivo, indent=4)
            
        print(f"Los datos se han guardado correctamente en '{nombre_archivo}'.")
    else:
        print(f"Error al obtener los datos. Código de estado: {respuesta.status_code}")

if __name__ == "__main__":
    url = "https://www.marinetraffic.com/getData/get_data_json_4/z:7/X:21/Y:38/station:0"
    guardar_como_json(url)