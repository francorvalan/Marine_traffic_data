import requests
import json

url = "https://www.marinetraffic.com/getData/get_data_json_4/z:7/X:21/Y:38/station:0"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    with open("marinetraffic_data.json", "w") as outfile:
        json.dump(data, outfile)
