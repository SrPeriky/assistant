import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from utils.traslater import traducir
load_dotenv()

class WeatherModel:
    def __init__(self, lat, lon):
        self.api_key = os.getenv("meteosource")
        self.lat = lat
        self.lon = lon
        try:
            with open('./assets/weather.json', encoding='utf-8') as json_file:
                self.data= json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = self.setJsonData()

    def fetchData(self):
        url = "https://www.meteosource.com/api/v1/free/point"
        params = {
            "lat": self.lat,
            "lon": self.lon,
            "sections": "current,hourly",
            "language": "en",
            "units": "auto",
            "key": self.api_key
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener datos de la API. Código de estado: {response.status_code}")
            return False

    def getWeather(self, user_time):
        if not self.data or not self.isUserTimeInData(str(user_time)):
            self.data = self.setJsonData()
            print("Datos actualizados desde la API.")
        user_datetime = datetime.strptime(str(user_time), "%Y-%m-%dT%H:%M:%S")

        start_index = self.binarySearch(user_datetime)
        if start_index is None:
            return "La hora del usuario no está en la data. Haciendo una nueva solicitud a la API."

        data = self.data[start_index]
        if start_index < len(self.data) - 1:
            next_data = self.data[start_index + 1]
            if not next_data:
                self.data = self.setJsonData()
                self.getWeather(user_time)
                return 0
            if user_datetime >= datetime.strptime(next_data["date"], "%Y-%m-%dT%H:%M:%S") - timedelta(minutes=20):
                data = self.calculateAverageData(data, next_data)

        return self.formatData(data)

    def isUserTimeInData(self, user_time):
        user_datetime = datetime.strptime(user_time, "%Y-%m-%dT%H:%M:%S")
        data_start_time = datetime.strptime(self.data[0]["date"], "%Y-%m-%dT%H:%M:%S")
        data_end_time = datetime.strptime(self.data[-1]["date"], "%Y-%m-%dT%H:%M:%S") + timedelta(minutes=20)
        return data_start_time <= user_datetime < data_end_time

    def formatData(self, data):
        parts = [
            f"Clima: {traducir(str(data['weather']).replace('_', ' '))}",
            f"Temperatura: {data['temperature']}",
            f"Velocidad del viento: {data['wind']['speed']}",
            f"Dirección del viento: {data['wind']['dir']}",
            f"Ángulo del viento: {data['wind']['angle']}",
            f"Cobertura de nubes: {data['cloud_cover']['total']}",
            f"Precipitación total: {data['precipitation']['total']}"
        ]

        return "\n".join(parts)

    def calculateAverageData(self, data1, data2):
        try:
            avg_temperature = (data1["temperature"] + data2["temperature"]) / 2
            avg_wind_speed = (data1["wind"]["speed"] + data2["wind"]["speed"]) / 2
            avg_wind_dir = (data1["wind"]["dir"] + data2["wind"]["dir"]) / 2
            avg_wind_angle = (data1["wind"]["angle"] + data2["wind"]["angle"]) / 2
            avg_cloud_cover = (data1["cloud_cover"]["total"] + data2["cloud_cover"]["total"]) / 2
            avg_precipitation = (data1["precipitation"]["total"] + data2["precipitation"]["total"]) / 2
        except:
            avg_temperature=0
            avg_wind_speed=0
            avg_wind_dir=0
            avg_wind_angle=0
            avg_cloud_cover=0
            avg_precipitation=0


        return {
            "weather": f"{data2['summary']}",
            "temperature": avg_temperature,
            "wind": {
                "speed": avg_wind_speed,
                "dir": avg_wind_dir,
                "angle": avg_wind_angle
            },
            "cloud_cover": {
                "total": avg_cloud_cover
            },
            "precipitation": {
                "total": avg_precipitation
            }
        }

    def binarySearch(self, user_datetime):
        low = 0
        high = len(self.data) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_time = datetime.strptime(self.data[mid]["date"], "%Y-%m-%dT%H:%M:%S")

            if mid_time <= user_datetime < datetime.strptime(self.data[mid + 1]["date"], "%Y-%m-%dT%H:%M:%S"):
                return mid
            elif user_datetime < mid_time:
                high = mid - 1
            else:
                low = mid + 1

        return None

    def setJsonData(self):
        res = self.fetchData()
        if res:
            res = res["hourly"]["data"]
            with open('./assets/weather.json', 'w') as archivo_json:
                json.dump(res, archivo_json, indent=2)
            
            return res
        else:
            return []

