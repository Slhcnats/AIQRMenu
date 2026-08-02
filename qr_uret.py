import qrcode

# Kendi Ngrok linkini buraya yapıştır
link = "https://woozy-domestic-decade.ngrok-free.dev"

# QR kod tasarımı
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(link)
qr.make(fit=True)

# Görsel olarak kaydet
resim = qr.make_image(fill_color="#2c3e50", back_color="#fcfaf8")
resim.save("Masa_1_QR.png")

print("✅ QR Kod başarıyla oluşturuldu! Soldaki dosyalar arasında Masa_1_QR.png resmini görebilirsin.")