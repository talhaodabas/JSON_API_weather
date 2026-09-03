import requests
from InquirerPy import inquirer


def fetch_weather_data(latitude,longitude):
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": latitude,
		"longitude": longitude,
		"current": "temperature_2m,wind_speed_10m,weather_code,is_day",
		"timezone": "auto"
	}
	response = requests.get(url, params=params)
	return response.json()


def parse_weather_data(data):
	current_data = data["current"]
	return {
		"time": current_data.get("time"),
		"temperature": current_data.get("temperature_2m"),
		"wind_speed": current_data.get("wind_speed_10m"),
		"weather_code": current_data.get("weather_code"),
		"is_day": current_data.get("is_day")
	}


def get_coordinates_city(city_name):
	search_url = "https://geocoding-api.open-meteo.com/v1/search"
	params = {
		"name": city_name,
		"count": 1,
		"language": "tr",
    }
	search_response = requests.get(search_url, params=params).json()
	first_result = search_response["results"][0]
	
	return {
        "latitude": first_result["latitude"],
        "longitude": first_result["longitude"],
    }


def get_temp_category(temp):
	if temp <= 0:
		return "freezing"
	elif temp < 10:
		return "cold"
	elif temp < 20:
		return "mild"
	elif temp < 30:
		return "warm"
	else:
		return "hot"


def get_weather_category(code):
	if code in [0, 1]:
		return "clear"
	elif code in [2, 3]:
		return "cloudy"
	elif code in [45, 48]:
		return "foggy"
	elif code in [51, 53, 55, 61, 63, 65, 66, 67, 80, 81, 82]:
		return "rainy"
	elif code in [71, 73, 75, 77, 85, 86]:
		return "snowy"
	elif code in [95, 96, 99]:
		return "stormy"
	else:
		return "clear"


def get_recommendation(weather):
	time = weather.get("time").replace("T", " ")
	day = weather.get("is_day")
	temp = weather.get("temperature")
	code = weather.get("weather_code")
	wind = weather.get("wind_speed")

	advice = []
	advice.append(time)
	if day==1:
		advice.append("Gün doğdu.")
	elif day==0:
		advice.append("Gün battı.")
	
	advice.append(f"Hava sıcaklığı: {temp} C")

	temp_cat = get_temp_category(temp)
	weather_cat = get_weather_category(code)
	advice.append(WEATHER_MATRIX[temp_cat][weather_cat])

	#	Rüzgara bağlı öneriler.
	if wind <= 19:
		advice.append("Sakin / Hafif Esinti")
	elif wind <= 39:
		advice.append("Orta Rüzgarlı")
	elif wind <=60:
		advice.append("Kuvvetli Rüzgar")
	else:
		advice.append("Çok Kuvvetli Fırtına!")
	return "\n".join(advice)


WEATHER_MATRIX = {
    "freezing": {
        "clear": "Güneş aldatmasın, dondurucu soğuk var. İçlik ve kalın mont giy.",
        "cloudy": "Hava kapalı ve dondurucu soğuk. Kalın kaban, atkı ve eldiven şart.",
        "foggy": "Gizli buzlanma ve dondurucu sis var. Termal içlik ve çok kalın kaban giy.",
        "rainy": "Buzlanma riski olan dondurucu yağmur var. Su geçirmez kalın mont ve bot giy.",
        "snowy": "Dondurucu soğukta kar var. Kaymayan bot ve termal giysiler tercih et.",
        "stormy": "Dondurucu fırtına var! Rüzgar geçirmez kalın mont ve termal giy, dışarı çıkma."
    },
    "cold": {
        "clear": "Soğuk ama açık bir hava. Güneş gözlüğü ve kalın bir mont tercih et.",
        "cloudy": "Serin ve kasvetli bir hava. Mont veya kalın hırka giyebilirsin.",
        "foggy": "Hava soğuk ve sisli. Kalın mont, bere ve atkı tercih et.",
        "rainy": "Soğuk yağmur var. Su geçirmez kaban ve kaymayan bot giy, şemsiye al.",
        "snowy": "Kar yağışlı ve soğuk. Kaymayan bot ve kalın mont giymelisin.",
        "stormy": "Soğuk fırtına var! Rüzgar geçirmez kalın kaban giy ve kapalı alanda kal."
    },
    "mild": {
        "clear": "Tam yürüyüş havası! Hafif bir ceket veya mevsimlik mont yeterli.",
        "cloudy": "Hava ılık ama bulutlu. Yanına hafif bir hırka veya sweatshirt alabilirsin.",
        "foggy": "Ilık ve sisli bir hava. Rüzgarlık veya mevsimlik ceket tercih et.",
        "rainy": "Ilık bir yağmur yağıyor. Yağmurluk giy veya su geçirmez ceket al.",
        "snowy": "Ilık havada sulu kar yağışı var. Su geçirmeyen bot ve ceket giy.",
        "stormy": "Ilık havada fırtına riski var! Rüzgarlık giy ve kapalı mekan tercih et."
    },
    "warm": {
        "clear": "Hava mis gibi ve sıcak. T-shirt ve rahat bir pantolon/şort giy.",
        "cloudy": "Ilık-sıcak arası kapalı bir hava. İnce ve nefes alan kıyafetler tercih et.",
        "foggy": "Nemli ve sıcak bir sis var. İnce keten veya pamuklu kıyafetler giy.",
        "rainy": "Yaz yağmuru havası. İnce giyin ama yanına hafif bir yağmurluk al.",
        "snowy": "Sıcak havada kar olağan dışı! İnce giyin ama tedbiren yanına mont al.",
        "stormy": "Yaz fırtınası var! İnce bir rüzgarlık giy ve hemen kapalı alana geç."
    },
    "hot": {
        "clear": "Aşırı sıcak ve güneşli! İnce/açık renk giyin, şapka tak ve bol su tüket.",
        "cloudy": "Bunaltıcı ve sıcak bir hava. Şort, t-shirt gibi ince ve ferah kıyafetler giy.",
        "foggy": "Yüksek nem ve aşırı sıcak var. En ince ve ferah kıyafetlerini tercih et.",
        "rainy": "Sıcak ve bunaltıcı yağmur var. Çok ince giyin, yanına hafif yağmurluk al.",
        "snowy": "Aşırı sıcakta kar imkansız! İnce giyin ancak ani hava değişimine dikkat et.",
        "stormy": "Aşırı sıcakta fırtına var! İnce rüzgarlık giy ve korunaklı bir alana geç."
    }
}



if __name__ == "__main__":
	cities = {
		"istanbul": {"latitude": 41.00, "longitude": 28.97},
		"ankara": {"latitude": 39.93, "longitude": 32.85}
	}
	while True:
		user_input = input("Şehir ismi girin(Örn: istanbul):	").strip().lower()
		city_coord = get_coordinates_city(user_input)
		latitude, longitude = city_coord["latitude"],city_coord["longitude"]
		coords = {"latitude": float(latitude), "longitude": float(longitude)}
		data = fetch_weather_data(coords["latitude"], coords["longitude"])
		current_weather = parse_weather_data(data)
		recommendation = get_recommendation(current_weather)
		print(recommendation)
		selected_option = inquirer.select(
    		message="Seçim yapın.",
    		choices=[
				"Arama",
				"Çıkış"
				]
		).execute()
		if selected_option == "Çıkış":
			break
		elif selected_option == "Arama":
			continue
