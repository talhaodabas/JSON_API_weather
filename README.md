#       Open-Meteo Weather Forecast And Recommendation

Bu uygulama, Open-Meteo API kullanarak anlık hava durumu verilerini çeker, şehir adına göre koordinat bulur ve hava koşullarına uygun giyim/yaşam tavsiyeleri sunar.

---

## 🛠️ Kurulum

Projenin çalışması için tek harici kütüphane `requests`'tir. Terminalden şu komutla yükleyebilirsiniz:

```bash
pip install requests
```

## Fonksiyonlar

* `fetch_weather_data(latitude,longitude)`: Koordinat verilerini kullanarak Open-Meteo API'sinden anlık hava durumu verisini çeker.
* `parse_weather_data(data)`: API'den gelen veri içerisinden zaman, sıcaklık, rüzgar hızı, hava kodu ve gündüz/gece bilgisini ayıklar.
* `get_coordinates_city(city_name)`: Girilen şehir ismini Open-Meteo Geocoding API ile aratarak `latitude` ve `longitude` koordinat değerlerini döndürür.
* `get_temp_category(temp)`: Sıcaklık değerini kategorize eder.
* `get_weather_category(code)`: Dünya Meteoroloji Örgütü hava durumu kodunu kategorize eder.
* `get_recommendation(weather)`: Sıcaklık ve hava durumunu karar matrisinde eşleştirerek tavsiye metnini oluşturur.