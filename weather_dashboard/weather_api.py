import requests

def get_weather_data(city):
    """
    Fetch weather data for the specified city, including current weather and hourly forecast.
    """
    # OpenWeatherMap API Key and Base URL
    API_KEY = "27a9368d6a0ab3c50445d90e7bd3a2f1"
    BASE_URL = "http://api.openweathermap.org/data/2.5/"

    try:
        # Current weather endpoint
        current_url = f"{BASE_URL}weather?q={city}&units=metric&appid={API_KEY}"
        # Hourly forecast endpoint (every 1 hour for the next 48 hours)
        forecast_url = f"{BASE_URL}forecast?q={city}&units=metric&appid={API_KEY}"

        # Fetch current weather and forecast data
        current_response = requests.get(current_url).json()
        forecast_response = requests.get(forecast_url).json()

        # Handle city not found or invalid input
        if "cod" in current_response and current_response["cod"] != 200:
            return {"error": f"City not found or invalid input: {city}"}

        # Extract current weather data
        current_weather = {
            "city": current_response.get("name"),
            "temperature": round(current_response["main"]["temp"]),
            "pressure": current_response["main"]["pressure"],
            "wind_speed": round(current_response["wind"]["speed"], 1),  # Round wind speed to 1 decimal
            "wind_direction": current_response["wind"]["deg"],
            "uv_index": requests.get(
                f"{BASE_URL}uvi?lat={current_response['coord']['lat']}&lon={current_response['coord']['lon']}&appid={API_KEY}"
            ).json().get("value", "N/A"),  # Fetch UV index with a fallback
        }

        # Extract hourly forecast (next 24 hours)
        hourly_forecast = []
        for forecast in forecast_response.get("list", [])[:24]:  # Limit to the next 24 data points (1 hour intervals)
            # Format time to 12-hour format
            time_24hr = forecast["dt_txt"][11:16]  # Extract time (HH:MM)
            time_12hr = convert_to_12_hour(time_24hr)  # Helper function defined below

            # Append to hourly forecast
            hourly_forecast.append({
                "time": time_12hr,
                "temp": round(forecast["main"]["temp"]),
                "icon_url": f"http://openweathermap.org/img/wn/{forecast['weather'][0]['icon']}@2x.png",
                "rain": forecast.get("rain", {}).get("1h", 0),  # Default rain to 0mm if missing
            })

        # Combine current weather and hourly forecast
        weather_data = {**current_weather, "hourly_forecast": hourly_forecast}

        return weather_data

    except requests.exceptions.RequestException:
        return {"error": "An error occurred while connecting to the weather API."}

# Helper function to convert 24-hour time to 12-hour format
def convert_to_12_hour(time_24hr):
    """Convert 24-hour time (HH:MM) to 12-hour format with AM/PM."""
    hour, minute = map(int, time_24hr.split(":"))
    period = "AM" if hour < 12 else "PM"
    hour = hour if 1 <= hour <= 12 else abs(hour - 12) or 12
    return f"{hour}:{minute:02d} {period}"
