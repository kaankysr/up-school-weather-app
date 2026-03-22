"""
Hava Durumuna Göre Aktivite Önerisi - UP School Ödevi
"""
from flask import Flask, render_template, request

app = Flask(__name__)


def get_activity_recommendation(temperature: float, weather: str) -> str:
    """
    Sıcaklık ve hava durumuna göre aktivite önerisi.
    
    - Sıcaklık > 25 ve hava 'Clear' ise: Dondurma ye ve sahilde yürüyüş yap 🍦
    - Hava 'Rain' ise: En sevdiğin kitabı al ve kahveni yudumla ☕
    - Sıcaklık < 10 ise: Sıcak bir çorba iç ve battaniye altında film izle 🍿
    - Diğer durumlar için genel açık hava aktivitesi
    """
    weather = (weather or "").strip()
    temp = float(temperature) if temperature is not None else 15

    # Öncelik: Yağmur
    if weather.lower() == "rain":
        return "En sevdiğin kitabı al ve kahveni yudumla ☕"

    # Öncelik: Sıcak ve güneşli
    if temp > 25 and weather.lower() == "clear":
        return "Dondurma ye ve sahilde yürüyüş yap 🍦"

    # Öncelik: Soğuk
    if temp < 10:
        return "Sıcak bir çorba iç ve battaniye altında film izle 🍿"

    # Diğer durumlar
    return "Parkta yürüyüş yap veya açık havada spor yap 🏃‍♂️"


@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = None
    temp = None
    weather = None

    if request.method == "POST":
        try:
            temp = request.form.get("temperature")
            weather = request.form.get("weather", "").strip()
            if temp:
                recommendation = get_activity_recommendation(float(temp), weather)
        except (ValueError, TypeError):
            recommendation = "Geçerli bir sıcaklık girin."

    return render_template(
        "index.html",
        recommendation=recommendation,
        temperature=temp,
        weather=weather,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
