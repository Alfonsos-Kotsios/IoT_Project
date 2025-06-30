from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import requests
import time
from retry_requests import retry
from send_email import (send_alert_email, user_settings, last_alert_times)
import requests

CHANNEL_ID = "2945205"
READ_API_KEY = "GV1LOU25EOX27SW2"
THING_SPEAK_URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json?api_key={READ_API_KEY}"

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add this line if not already present


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global user_settings
    if request.method == 'POST':
        user_settings['email'] = request.form['email']
        user_settings['LIGHT_THRESHOLD'] = float(request.form['LIGHT_THRESHOLD'])
        user_settings['TEMP_THRESHOLD'] = float(request.form['TEMP_THRESHOLD'])
        user_settings['HUMIDITY_THRESHOLD'] = float(request.form['HUMIDITY_THRESHOLD'])
        user_settings['LIGHT_LOW_THRESHOLD'] = float(request.form['LIGHT_LOW_THRESHOLD'])
        user_settings['TEMP_LOW_THRESHOLD'] = float(request.form['TEMP_LOW_THRESHOLD'])
        user_settings['HUMIDITY_LOW_THRESHOLD'] = float(request.form['HUMIDITY_LOW_THRESHOLD'])
        user_settings['COOLDOWN_SECONDS'] = int(request.form['COOLDOWN_SECONDS'])
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('settings'))
    return render_template('settings.html', settings=user_settings)

def get_weather_data():
    API_KEY = 'b4cbf658a1c946e7a1f144613251605'
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q=Athens&aqi=no"
    try:
        response = requests.get(url)
        data = response.json()
        return {
            "city": data['location']['name'],
            "temp_c": data['current']['temp_c'],
            "uv": data['current']['uv'],
            "humidity": data['current']['humidity']
        }
    except Exception as e:
        return {"error": str(e)}


def get_sensor_data():
    try:
        response = requests.get(THING_SPEAK_URL)
        response.raise_for_status()
        data = response.json()
        light = data.get("field1")
        temperature = data.get("field2")
        humidity = data.get("field3")

        light_val = float(light) if light else None
        temp_val = 32 #float(temperature) if temperature else None
        humidity_val = float(humidity) if humidity else None

        now = time.time()

        # Έλεγχος φωτός
        if light_val and light_val > user_settings["LIGHT_THRESHOLD"]:
            if now - last_alert_times["light"] > user_settings["COOLDOWN_SECONDS"]:
                send_alert_email("Light Alert", f"Light level is too high: {light_val} maybe is time to close the curtains!!☀️")
                last_alert_times["light"] = now

        # Έλεγχος θερμοκρασίας
        if temp_val and temp_val > user_settings["TEMP_THRESHOLD"]:
            if now - last_alert_times["temperature"] > user_settings["COOLDOWN_SECONDS"]:
                send_alert_email("Temperature Alert", f"Temperature is too high: {temp_val}°C maybe is time to turn on the AC!!❄️")
                last_alert_times["temperature"] = now

        # Έλεγχος υγρασίας
        if humidity_val and humidity_val > user_settings["HUMIDITY_THRESHOLD"]:
            if now - last_alert_times["humidity"] > user_settings["COOLDOWN_SECONDS"]:
                send_alert_email("Humidity Alert", f"Humidity is too high: {humidity_val}% maybe is time to turn on the dehumidifier!!💧")
                last_alert_times["humidity"] = now

        # Έλεγχος χαμηλού φωτός
        if light_val and light_val < user_settings["LIGHT_LOW_THRESHOLD"]:
            if now - last_alert_times.get("light_low", 0) > user_settings["COOLDOWN_SECONDS"]:
                send_alert_email("Low Light Alert", f"Light level is too low: {light_val} maybe is time to open the curtains! 🌑")
                last_alert_times["light_low"] = now

        # Έλεγχος χαμηλής θερμοκρασίας
        if temp_val and temp_val < user_settings["TEMP_LOW_THRESHOLD"]:
            if now - last_alert_times.get("temperature_low", 0) > user_settings["COOLDOWN_SECONDS"]:
                send_alert_email("Low Temperature Alert", f"Temperature is too low: {temp_val}°C maybe is time to turn off the AC! 🥶")
                last_alert_times["temperature_low"] = now

        # Έλεγχος χαμηλής υγρασίας
        if humidity_val and humidity_val < user_settings["HUMIDITY_LOW_THRESHOLD"]:
            if now - last_alert_times.get("humidity_low", 0) > user_settings["COOLDOWN_SECONDS"]:
                send_alert_email("Low Humidity Alert", f"Humidity is too low: {humidity_val}% maybe is time to use a humidifier! 💨")
                last_alert_times["humidity_low"] = now

        return {
            "light": f"{light_val:.1f}" if light_val else None,
            "temperature": f"{temp_val:.1f}" if temp_val else None,
            "humidity": f"{humidity_val:.1f}" if humidity_val else None
        }
    except requests.RequestException as e:
        return {"error": str(e)}


@app.route('/')
def index():
    sensor_data = get_sensor_data()
    weather_data = get_weather_data()
    return render_template('index.html', sensor_data=sensor_data, weather_data=weather_data)

@app.route('/data')
def data():
    return jsonify(get_sensor_data())

if __name__ == '__main__':
    app.run(debug=True)

