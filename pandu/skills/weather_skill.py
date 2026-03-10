import requests
from skills.base_skill import BaseSkill
from utils.config import config
from utils.logger import logger

class WeatherSkill(BaseSkill):
    @property
    def intent_name(self) -> str:
        return "weather"

    def execute(self, entities: dict) -> str:
        city = entities.get("location")
        weather_config = config.get("skills", {}).get("weather", {})
        
        if not city:
            city = weather_config.get("default_city", "London")
            
        api_key = weather_config.get("api_key")
        
        if not api_key or api_key == "YOUR_OPENWEATHERMAP_API_KEY_HERE":
            logger.warning("OpenWeatherMap API key is not configured.")
            return f"I don't have an API key configured for the weather, but it usually rains in {city} anyway."
            
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                temp = round(data["main"]["temp"])
                desc = data["weather"][0]["description"]
                return f"The current temperature in {city} is {temp} degrees Celsius with {desc}."
            elif response.status_code == 404:
                return f"I couldn't find weather information for {city}."
            else:
                logger.error(f"Weather API returned status code {response.status_code}")
                return "I'm having trouble connecting to the weather service right now."
                
        except Exception as e:
            logger.error(f"Error fetching weather: {e}")
            return "Sorry, I couldn't get the weather data at the moment."
