import json
import sys
import requests
import redis
import pprint
from flask import Flask
from functools import wraps
from time import time

app = Flask(__name__)


def time_it(my_func):
    @wraps(my_func)
    def timed(*args, **kw):

        tstart = time()
        output = my_func(*args, **kw)
        tend = time()

        print(f"{my_func.__name__} took {(tend - tstart) * 1000} ms to execute")

        return output

    return timed


def redis_connect():
    try:
        client = redis.Redis(
            host="localhost",
            port=6379,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.ConnectionError:
        print("ConnectionError")
        sys.exit(1)
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)


client = redis_connect()

BASE_URL = "http://api.weatherbit.io/v2.0"
API_TOKEN = "YOUR-TOKEN"


def get_current_weather(city, country):

    response = requests.get(
        f"{BASE_URL}/current?city={city}&country={country}&key={API_TOKEN}"
    )

    if response.status_code != 200:
        return {}

    data = response.json()["data"][0]
    data_to_return = {
        "temperature": data["temp"],
        "wind_speed": data["wind_spd"],
        "wind_direction": data["wind_cdir"],
        "description": data["weather"]["description"],
    }
    return data_to_return


def get_forecast(city, country):
    response = requests.get(
        f"{BASE_URL}/forecast/hourly?city={city}&country={country}&hours=5&key={API_TOKEN}"
    )
    data = response.json()["data"]

    data_to_return = {"forecast": []}
    for forecast in data:
        hourly_forecast = {
            "time": forecast["timestamp_local"],
            "temperature": forecast["temp"],
            "wind_speed": forecast["wind_spd"],
            "wind_direction": forecast["wind_cdir"],
            "description": forecast["weather"]["description"],
        }
        data_to_return["forecast"].append(hourly_forecast)
    return data_to_return


def get_data_from_cache(key):

    return client.get(key)


def set_data_to_cache(key, value, is_forecast):

    if is_forecast:
        expiration_time = 60 * 60
    else:
        expiration_time = 60 * 15

    set_data = client.setex(
        key,
        expiration_time,
        value=value,
    )
    return set_data


@time_it
def get_weather_optima(city, country):

    current_weather_data = get_data_from_cache(key=f"current:{city}:{country}")

    if current_weather_data is not None:
        data_to_return = json.loads(current_weather_data)
        data_to_return["from_cache"] = True
        return data_to_return

    else:
        data = get_current_weather(city, country)
        if data:
            data["from_cache"] = False
            data = json.dumps(data)
            state = set_data_to_cache(
                key=f"current:{city}:{country}", value=data, is_forecast=False
            )

            if state is True:
                return json.loads(data)
        return data


@time_it
def get_forecast_optima(city, country):

    current_forecast_data = get_data_from_cache(key=f"forecast:{city}:{country}")

    if current_forecast_data is not None:
        data_to_return = json.loads(current_forecast_data)
        data_to_return["from_cache"] = True
        return data_to_return

    else:
        data = get_forecast(city, country)
        if data:
            data["from_cache"] = False
            data = json.dumps(data)
            state = set_data_to_cache(
                key=f"forecast:{city}:{country}", value=data, is_forecast=False
            )

            if state is True:
                return json.loads(data)
        return data


def main():
    return {
        "weather": get_weather_optima("thessaloniki", "gr"),
        "forecast": get_forecast_optima("thessaloniki", "gr"),
    }


@app.route("/weather/<country>/<city>")
def fetch_weather(country, city):
    return {
        "weather": get_weather_optima(city, country),
        "forecast": get_forecast_optima(city, country),
    }


if __name__ == "__main__":
    app.run(debug=True)
