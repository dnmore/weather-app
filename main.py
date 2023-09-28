from flask import Flask, render_template, request
import requests
import pandas
import datetime
import os

api_key = os.environ["KEY"]

GEO_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"
CURRENT_W_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    data = pandas.read_csv("countries.csv")
    all_states = data.state.to_list()

    today = datetime.date.today()
    if request.method == "POST":
        city_input = request.form.get("city")
        state_input = request.form.get("state")
        location = f"{city_input}, {state_input}"
        geo_parameters = {
            "q": location,
            "limit": 5,
            "appid": api_key
        }

        geo_response = requests.get(GEO_ENDPOINT, params=geo_parameters)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        try:
            latitude = geo_data[0]['lat']
            longitude = geo_data[0]['lon']
        except IndexError:
            return render_template("index.html", all_states=all_states, today=today, city="Invalid Location")
        else:
            current_w_parameters = {
                "lat": latitude,
                "lon": longitude,
                "appid": api_key,
                "units": "metric",
                "exclude": "minutely, hourly, alerts"

            }

            weather_response = requests.get(CURRENT_W_ENDPOINT, params=current_w_parameters)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            description = weather_data['weather'][0]['description']
            temperature = f"{int(weather_data['main']['temp'])}°"
            feels_temp = int(weather_data['main']['feels_like'])
            summary = f"Weather: {description}. Temperature is {temperature} and it feels likes {feels_temp}°."
            return render_template("index.html", all_states=all_states, today=today, city=location,
                                   temperature=temperature, summary=summary)
    else:
        return render_template("index.html", all_states=all_states, today=today, city="Location")


if __name__ == "__main__":
    app.run(debug=True)
