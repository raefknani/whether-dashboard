from flask import Flask, render_template, request
from weather_api import get_weather_data

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            data = get_weather_data(city)
            if "error" in data:
                error_message = data["error"]
            else:
                weather_data = data
                print("Weather Data:", weather_data)  # Debugging line
        else:
            error_message = "Please enter a city name."

    return render_template("dashboard.html", weather_data=weather_data, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
