import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

# Sayfa Ayarları
st.set_page_config(page_title="Hava Durumu Önerici", page_icon="🌤️", layout="wide")

# Cafcaflı stil
st.markdown(
    """
    <style>
    /* Ana arka plan gradient */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 50%, #e94560 100%);
        background-attachment: fixed;
    }

    /* Başlık alanı */
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffd700, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0;
        text-shadow: 0 0 40px rgba(255,215,0,0.3);
        font-family: 'Segoe UI', sans-serif;
    }

    .subtitle-text {
        text-align: center;
        color: rgba(255,255,255,0.8);
        font-size: 1.1rem;
        margin-top: 0;
        margin-bottom: 2rem;
    }

    /* UP School badge - sağ üst */
    #up-school-note {
        position: fixed;
        top: 15px;
        right: 25px;
        background: linear-gradient(135deg, #ffd700, #ff8c00);
        padding: 10px 22px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 14px;
        color: #1a1a2e !important;
        z-index: 9999;
        box-shadow: 0 4px 20px rgba(255,215,0,0.5);
        border: 2px solid rgba(255,255,255,0.5);
        letter-spacing: 1px;
    }

    /* Input container */
    .input-card {
        background: rgba(255,255,255,0.12);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    /* Hava durumu kartı */
    .weather-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.2), rgba(255,255,255,0.05));
        backdrop-filter: blur(15px);
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.25);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        text-align: center;
    }

    .temp-display {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(180deg, #fff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }

    .city-name {
        font-size: 1.8rem;
        color: #ffd700;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    /* Öneri kutuları - özel stiller */
    .recommend-rain {
        background: linear-gradient(135deg, #2d3436, #636e72);
        color: #dfe6e9 !important;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        border-left: 5px solid #74b9ff;
        font-size: 1.2rem;
        font-weight: 500;
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
        margin: 1rem 0;
    }

    .recommend-sun {
        background: linear-gradient(135deg, #fdcb6e, #e17055);
        color: #2d3436 !important;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        border-left: 5px solid #ffeaa7;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 8px 30px rgba(225,112,85,0.4);
        margin: 1rem 0;
    }

    .recommend-cold {
        background: linear-gradient(135deg, #0984e3, #74b9ff);
        color: #fff !important;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        border-left: 5px solid #a29bfe;
        font-size: 1.2rem;
        font-weight: 500;
        box-shadow: 0 8px 30px rgba(9,132,227,0.4);
        margin: 1rem 0;
    }

    .recommend-mild {
        background: linear-gradient(135deg, #00b894, #55efc4);
        color: #2d3436 !important;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        border-left: 5px solid #81ecec;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 8px 30px rgba(0,184,148,0.4);
        margin: 1rem 0;
    }

    /* Input alanı stilleri - yazı okunabilir olsun */
    .stTextInput input, .stTextInput > div > div > input {
        background: rgba(255,255,255,0.95) !important;
        border: 2px solid rgba(255,215,0,0.6) !important;
        border-radius: 12px !important;
        color: #1a1a2e !important;
        -webkit-text-fill-color: #1a1a2e !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }

    .stTextInput input::placeholder {
        color: #6b7280 !important;
        -webkit-text-fill-color: #6b7280 !important;
    }

    /* Öneri başlığı */
    .suggestion-title {
        font-size: 1.5rem;
        color: #ffd700;
        font-weight: 700;
        margin: 1.5rem 0 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Gizle streamlit varsayılan elemanlar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    <div id="up-school-note">✨ UP School Ödevi</div>
    """,
    unsafe_allow_html=True
)

# Başlık
st.markdown('<p class="main-title">🌤️ Hava Durumuna Göre Aktivite Önerici</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">@kaankysr · Şehir adını gir, bugün ne yapacağını keşfet 🚀</p>', unsafe_allow_html=True)

# API Anahtarı (.env dosyasından veya ortam değişkeninden)
API_KEY = "da5e68fb21b2a08958925c135b57217b"

# Input alanı - ortalı ve şık
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    city = st.text_input(
        "📍 Şehir adını girin",
        placeholder="Örn: Istanbul, Ankara, İzmir...",
        label_visibility="collapsed"
    )

if city:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=tr"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        main_weather = data['weather'][0]['main']

        # Hava durumu ikonu
        weather_icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Fog": "🌫️",
        }
        icon = weather_icons.get(main_weather, "🌤️")

        # Hava durumu kartı
        st.markdown(
            f"""
            <div class="weather-card">
                <p class="city-name">{icon} {city.capitalize()}</p>
                <p class="temp-display">{temp:.1f} °C</p>
                <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">{desc.capitalize()}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Aktivite Önerisi
        st.markdown('<p class="suggestion-title">💡 Bugün Ne Yapmalı?</p>', unsafe_allow_html=True)

        if "Rain" in main_weather or "Drizzle" in main_weather:
            st.markdown(
                '<div class="recommend-rain">📚 En sevdiğin kitabı al ve kahveni yudumla... ☕</div>',
                unsafe_allow_html=True
            )
        elif temp > 25:
            st.markdown(
                '<div class="recommend-sun">🍦 Hava harika! Dondurma yiyerek sahilde yürüyüş yap! 🌴</div>',
                unsafe_allow_html=True
            )
            st.balloons()
        elif temp < 10:
            st.markdown(
                '<div class="recommend-cold">🍜 Sıcak bir çorba iç ve battaniye altında film izle! 🎬</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="recommend-mild">👟 Hava tam kararında! Kısa bir açık hava yürüyüşü için ideal. 🌳</div>',
                unsafe_allow_html=True
            )
    else:
        st.error("Şehir bulunamadı veya API anahtarı henüz aktif değil. Lütfen kontrol et.")
