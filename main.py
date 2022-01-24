from crypt import methods
from flask import Flask, request
import requests
from pydantic import BaseModel
from flask_pydantic import validate
from loguru import logger
from cachetools import TTLCache

cache = TTLCache(maxsize=4096, ttl=86400)

cache.clear()

logger.add("logs/app.log", rotation="1 MB") 

class City(BaseModel):
    name: str
    country: str

class Weather(BaseModel):
    min: float
    max: float
    avg: float
    feels_like: float
    city: City
    

app = Flask(__name__)


api_key = "a8142e63a3fa212da2fdfb04d74edfca"

cached_data = []

base_weather_url = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/temperature/<city>", methods=["GET"])
@validate()
def get_temperature_by_city(city: str):

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    request = requests.get(base_weather_url, params=params)

    if request.status_code != 200:
        return "no data founded", 503 

    returned_data = request.json()

    city_record = City(
        name=returned_data["name"],
        country=returned_data["sys"]["country"],
    )

    weather = Weather(
        min=returned_data["main"]["temp_min"],
        max=returned_data["main"]["temp_max"],
        avg=returned_data["main"]["temp"],
        feels_like=returned_data["main"]["feels_like"],
        city=city_record,
    )


    extract_data = cache.get("weather")

    insert_new_data = False    
    
    if extract_data != None:
        for item in extract_data:
            if item["city"]["name"] == city_record.name:
                extract_data.remove(item)
                extract_data.append(weather.dict())
                cache["weather"] = extract_data
                logger.info(f"{city_record.name} is already in cache")
                return weather
            else:
                insert_new_data = True
                
        if insert_new_data:
            extract_data.append(weather.dict())
    else:
        extract_data = [weather.dict()]

    
    cache["weather"] = extract_data

    return weather

@app.route("/temperature", methods=["GET"])
@validate()
def get_temperature_by_city_from_cache():

    max_number = request.args.get('max')

    extract_data = cache.get("weather")
    logger.info(extract_data)

    if extract_data == None or max_number == None:
        cache["weather"] = extract_data
        return "No data founded", 503

    
    cache["weather"] = extract_data
    reversed_data = extract_data[::-1]

    return {"data": reversed_data[0:int(max_number)]}

@app.route("/cache/clear", methods=["GET"])
@validate()
def cache_clear():

    cache.clear()

    return {"status": "success"}