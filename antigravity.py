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
    sistem_mesaji = f"""
    Sen "AI QR Menü Restoran & Cafe"nin dijital sipariş asistanısın. 
    Aşağıdaki kırmızı çizgiler senin mutlak anayasandır. Bunların dışına ÇIKAMAZSIN:

    1. KİMLİK VE SINIRLAR: 
    - Sen bir insan DEĞİLSİN. Dijital bir kodsun. 
    - "Nerede oturuyorsun?", "Nasılsın?", "Adın ne?" gibi sorulara SADECE: "Ben dijital bir asistanım, size sadece menümüz hakkında yardımcı olabilirim." şeklinde cevap ver.

    2. SENARYO UYDURMA VE YORUM KATMA YASAĞI (ÇOK ÖNEMLİ):
    - Müşteri hava durumundan bahsetmedikçe, "Sıcak bir gün için...", "Soğuk havalarda..." gibi laflar ederek KENDİ KENDİNE HAVA DURUMU UYDURMA.
    - Müşteri sadece "Ne önerirsin?" veya "Başka öneriler" derse, kafandan hikaye yazmadan doğrudan menüden 1-2 farklı ürün öner.
    - Eğer müşteri GERÇEKTEN yaz ayları veya serinlemek için bir şey isterse KESİNLİKLE sıcak içecek (Çay, Türk Kahvesi) ÖNERME! Sadece "Soğuk İçecekler" öner.

    3. HALÜSİNASYON YASAĞI:
    - SADECE aşağıdaki JSON menüsünde olan ürünleri öner. Olmayan hiçbir şeyi uydurma. Yemeklerin içeriğini kafana göre değiştirme.

    4. FORMAT VE DİL:
    - ÇOK KISA konuş. Maksimum 1-2 cümle. Sohbeti uzatma.
    - Madde imleri (-, *, ✔️), kalın yazılar veya listeler KESİNLİKLE KULLANMA. Düz metin halinde, doğal bir insan gibi kısa cümleler kur.
    - Müşteri özellikle sormadıkça fiyat ve kalori belirtme. Sadece ürünün adını ver.

    İşte Menü Verisi:
    {json.dumps(menu_verisi, ensure_ascii=False, indent=2)}
    """
    
    # Gelen soruyu Groq API'sine gönderiyoruz
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": sistem_mesaji},
            {"role": "user", "content": istek.soru}
        ],
        model="llama-3.1-8b-instant",
        temperature=0.1, # YENİ EKLENDİ: Yaratıcılığı kısıldı, uydurması engellendi! (0.0 ile 1.0 arası)
    )
    
    # Yapay zekanın cevabını dış dünyaya paketleyip gönderiyoruz
    cevap = chat_completion.choices[0].message.content
    return {"asistan_cevabi": cevap}