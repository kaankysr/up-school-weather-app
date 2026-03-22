import streamlit as st
import requests

# Sayfa Ayarları
st.set_page_config(page_title="Hava Durumu Önerici", page_icon="🌤️")

# Başlık ve UP School Notu
st.title("🌤️ Hava Durumuna Göre Aktivite Önerici")
st.write("UP School Ödevi - @kaankysr")

# API Anahtarın (Buraya kendi anahtarını tırnak içine yapıştır)
API_KEY = "BURAYA_KENDI_API_KEYINI_YAZ" 

city = st.text_input("Şehir adını giriniz:", placeholder="Örn: Istanbul")

if city:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=tr"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        main_weather = data['weather'][0]['main']

        st.metric(label=f"{city.capitalize()} Hava Durumu", value=f"{temp} °C", delta=desc)

        # Aktivite Önerileri Mantığı
        st.subheader("💡 Bugün Ne Yapmalı?")
        
        if "Rain" in main_weather or "Drizzle" in main_weather:
            st.info("Hava yağmurlu... En sevdiğin kitabı al ve kahveni yudumla. ☕📚")
        elif temp > 25:
            st.success("Hava harika! Dışarı çıkıp dondurma yiyerek yürüyüş yapabilirsin. 🍦🌳")
            st.balloons()
        elif temp < 10:
            st.warning("Hava biraz soğuk. Sıcak bir çorba içip film izlemek iyi gelebilir. 🍜🎬")
        else:
            st.write("Hava tam kararında! Kısa bir yürüyüş için ideal. 👟")
    else:
        st.error("Şehir bulunamadı veya API anahtarı henüz aktif değil. Lütfen kontrol et.")

# DİKKAT: app.run() gibi Flask komutları Streamlit'te ASLA OLMAMALI.
