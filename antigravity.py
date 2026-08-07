import json
import os
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

# 1. API Anahtarı ve Kurulum
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

app = FastAPI(title="AI QR Menü", description="AI Destekli QR Menü ve Çağrı Sistemi")

# --- YENİ: ÇAĞRILARI TUTACAĞIMIZ RAM LİSTESİ ---
aktif_cagrilar = []
cagri_id_sayaci = 1

# Menü Yükleme
def menuyu_yukle(dosya_yolu):
    with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
        return json.load(dosya)

menu_verisi = menuyu_yukle('menu.json')
print("⚡ Web Sunucusu, Yapay Zeka ve Çağrı Merkezi Hazır!")

# --- VERİ MODELLERİ ---
class MusteriSorusu(BaseModel):
    soru: str

class CagriIstegi(BaseModel):
    masa_no: str
    talep: str

# --- SAYFALAR (FRONTEND) ---
@app.get("/")
def ana_sayfa():
    return FileResponse("index.html")

@app.get("/admin")
def admin_sayfasi():
    return FileResponse("admin.html")

# --- API UÇ NOKTALARI ---
@app.get("/api/menu")
def menuyu_getir():
    return menu_verisi

# YENİ: Admin panelinden gelen güncellenmiş menüyü kaydetme
@app.post("/api/menu/guncelle")
def menuyu_guncelle(yeni_menu: dict):
    global menu_verisi # RAM'deki veriyi kullan
    
    try:
        # 1. Yeni menüyü menu.json dosyasına yazıp kalıcı hale getiriyoruz
        with open('menu.json', 'w', encoding='utf-8') as dosya:
            json.dump(yeni_menu, dosya, ensure_ascii=False, indent=2)
            
        # 2. Sistemdeki aktif menüyü güncelliyoruz (Böylece AI da yeni menüyü öğrenmiş oluyor)
        menu_verisi = yeni_menu
        
        return {"durum": "basarili", "mesaj": "Menü başarıyla güncellendi"}
    except Exception as e:
        return {"durum": "hata", "mesaj": str(e)}

# YENİ: Müşteriden gelen çağrıyı kaydet
@app.post("/api/cagri")
def cagri_olustur(istek: CagriIstegi):
    global cagri_id_sayaci
    yeni_cagri = {
        "id": cagri_id_sayaci,
        "masa_no": istek.masa_no,
        "talep": istek.talep,
        "zaman": datetime.now().strftime("%H:%M")
    }
    aktif_cagrilar.append(yeni_cagri)
    cagri_id_sayaci += 1
    return {"durum": "basarili"}

# YENİ: Kasa (Admin) ekranına aktif çağrıları gönder
@app.get("/api/cagrilar")
def cagrilar_getir():
    return aktif_cagrilar

# YENİ: Kasa çağrıyı onaylayınca listeden sil
@app.delete("/api/cagri/{cagri_id}")
def cagri_tamamla(cagri_id: int):
    global aktif_cagrilar
    aktif_cagrilar = [c for c in aktif_cagrilar if c["id"] != cagri_id]
    return {"durum": "basarili"}

# --- YAPAY ZEKA ---
@app.post("/sor")
def asistana_sor(istek: MusteriSorusu):
    sistem_mesaji = f"""
    Sen, "AI QR Menü Restoran & Cafe" mekanının yapay zeka destekli akıllı garsonusun. Adın "Maison".
    Aşağıdaki kurallar senin mutlak anayasandır:

    1. İNSANİ İLİŞKİLER VE SELAMLAŞMA (ÇOK ÖNEMLİ):
    - Müşteri sana "Merhaba", "Selam", "Nasılsın" derse, asla "Ben dijital bir asistanım" gibi robotik duvarlar örüp kestirip atma. 
    - Önce insani bir refleksle selamını al ve hal hatır sor (Örn: "Merhaba, çok teşekkür ederim iyiyim. Hoş geldiniz, bugün size nasıl yardımcı olabilirim?").
    - Müşteri "Nerede oturuyorsun?" veya "Yaşın kaç?" gibi kişisel/fiziksel hayatınla ilgili şeyler sorarsa o zaman kibarca mekanın asistanı olduğunu belirt.

    2. SENARYO UYDURMA VE HAVA DURUMU YASAĞI:
    - Müşteri sormadıkça veya hava durumundan bahsetmedikçe kendi kendine senaryo uydurma.
    - Sadece müşterinin sorduğu soruya odaklan ve menüden doğrudan 1-2 ürün önerip kısa kes.
    - Yaz aylarında veya serinletmek için bir şey istendiğinde asla sıcak içecek önerme.

    3. HALÜSİNASYON YASAĞI:
    - SADECE aşağıdaki JSON menüsünde olan ürünleri öner. Asla menüde olmayan bir şeyi uydurma.

    4. FORMAT VE DİL:
    - ÇOK KISA konuş. Maksimum 1-2 cümle. Sohbeti uzatma.
    - Madde imleri (-, *, ✔️), kalın yazılar veya listeler KESİNLİKLE KULLANMA. Düz metin halinde, doğal bir garson gibi konuş.
    - Müşteri özellikle sormadıkça fiyat ve kalori belirtme. Sadece ürünün adını ver.

    İşte Menü Verisi:
    {json.dumps(menu_verisi, ensure_ascii=False, indent=2)}
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": sistem_mesaji},
            {"role": "user", "content": istek.soru}
        ],
        model="llama-3.1-8b-instant",
        temperature=0.1, 
    )
    
    cevap = chat_completion.choices[0].message.content
    return {"asistan_cevabi": cevap}