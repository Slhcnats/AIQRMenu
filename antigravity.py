import json
import os
from dotenv import load_dotenv
from groq import Groq
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

# 1. API Anahtarı ve Groq Kurulumu
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 2. FastAPI Uygulamasını Başlatıyoruz
app = FastAPI(title="Antigravity API", description="AI Destekli QR Menü Asistanı")

# 3. Menüyü Yüklüyoruz
def menuyu_yukle(dosya_yolu):
    with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
        return json.load(dosya)

menu_verisi = menuyu_yukle('menu.json')
print("⚡ Web Sunucusu ve Yapay Zeka Motoru Hazır!")

# 4. Veri Modeli: Dışarıdan (telefondan/siteden) gelecek verinin şeklini belirliyoruz
class MusteriSorusu(BaseModel):
    soru: str

# Ana sayfaya girildiğinde HTML arayüzümüzü göster
@app.get("/")
def ana_sayfa():
    return FileResponse("index.html")

# EKSİK OLAN KISIM EKLENDİ: Arayüzün menüyü okumasını sağlayan uç nokta
@app.get("/api/menu")
def menuyu_getir():
    return menu_verisi

# 5. API Uç Noktası (POST İsteği Dinleyicisi)
@app.post("/sor")
def asistana_sor(istek: MusteriSorusu):
    # Sistem mesajımızı hazırlıyoruz
    sistem_mesaji = f"""
    Sen Antigravity Cafe'nin akıllı dijital asistanısın. 
    Müşterilere SADECE aşağıdaki JSON menü verisine göre cevap ver. 
    Menüde olmayan hiçbir şeyi önerme. Müşterinin alerjilerine ve isteklerine dikkat et.

    Menü Verisi:
    {json.dumps(menu_verisi, ensure_ascii=False, indent=2)}
    """
    
    # Gelen soruyu Groq API'sine gönderiyoruz
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": sistem_mesaji},
            {"role": "user", "content": istek.soru}
        ],
        model="llama-3.1-8b-instant",
    )
    
    # Yapay zekanın cevabını dış dünyaya paketleyip gönderiyoruz
    cevap = chat_completion.choices[0].message.content
    return {"asistan_cevabi": cevap}