# AIQRMenu - Yapay Zeka Destekli Akıllı QR Menü Sistemi

🌐 **Dil**

[🇬🇧 English](README.md) | 🇹🇷 Türkçe

---

AIQRMenu, klasik restoran menülerini dijitalleştirerek interaktif bir deneyime dönüştüren, tam teşekküllü (Full-Stack) bir web uygulamasıdır. Müşteriler, masalarındaki QR kodu okutarak sadece ürünleri görmekle kalmaz, aynı zamanda menüye entegre edilmiş yapay zeka asistanı sayesinde kişiselleştirilmiş yemek önerileri alabilirler.

## Projenin Amacı

Geleneksel restoran menülerinde müşterilerin ürün içeriklerini, kalorilerini veya vegan/vejetaryen seçenekleri bulması zaman alır. Bu proje, müşterilerin aradıkları lezzeti saniyeler içinde filtreleyebilmesini ve kararsız kaldıklarında akıllı bir asistana danışabilmesini sağlamak amacıyla geliştirilmiştir.

## Temel Özellikler

* **Entegre Yapay Zeka Garsonu:** Groq API altyapısı ile çalışan akıllı asistan; müşterinin ruh haline, bütçesine veya diyet tercihlerine göre anında menüden ürün önerileri sunar.
* **Dinamik ve Hızlı Filtreleme:** Sayfa yenilenmesine gerek kalmadan (Asynchronous) çalışan kategori butonları ile anında ürün listeleme.
* **Premium UI/UX Tasarımı:** Kullanıcı dostu, modern, mobil öncelikli (mobile-first) ve estetik animasyonlara sahip ön yüz.
* **Tam Otomatik QR Sistemi:** Python tabanlı yerleşik algoritma ile canlı sunucu linkini (Ngrok) anında fiziksel masalara koyulabilecek bir QR koda dönüştürme.

## Kullanılan Teknolojiler ve Mimari

Bu proje, modern web geliştirme standartlarına uygun olarak tasarlanmıştır:

* **Backend:** Python, FastAPI (Yüksek performanslı asenkron API yönetimi), Uvicorn (Sunucu)
* **Yapay Zeka:** Groq API (Gecikmesiz, anlık dil modeli yanıtları)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (Harici kütüphane bağımlılığı olmadan saf ve hızlı tasarım)
* **DevOps & Araçlar:** Ngrok (Yerel sunucuyu internete açma tüneli), qrcode (Dinamik barkod üretimi)

## Yerelde Kurulum ve Çalıştırma Rehberi

Projeyi kendi ortamınızda test etmek için sırasıyla şu adımları uygulayabilirsiniz:

**1. Projeyi Klonlayın**
```bash
git clone https://github.com/Slhcnats/AIQRMenu.git
cd AIQRMenu
```
**2. Sanal Ortam Oluşturun ve Gereksinimleri Yükleyin**
```bash
pip install fastapi uvicorn groq qrcode[pil]
```
**3. API Yapılandırması**
```text
antigravity.py dosyasını açın ve ilgili satıra kendi Groq API anahtarınızı ekleyin.
```
**4. Sunucuyu Başlatın**
```bash
uvicorn antigravity:app --reload
Sunucu başlatıldıktan sonra tarayıcınızda http://localhost:8000 adresinden veya Ngrok tüneli açarak mobil cihazınızdan projeyi görüntüleyebilirsiniz.
```

Geliştirici: Salih Can Ateş | Fırat Üniversitesi - Bilgisayar Mühendisliği
