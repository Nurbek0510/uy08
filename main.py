import os
from urllib.parse import urlparse, unquote
import requests

ruxsat_etilgan_formatlar = [
    ".mp3", ".mp4", ".pdf", ".png", ".jpg", ".jpeg", ".webp"
]

url = input("Fayl havolasini kiriting: ").strip()

manzil = urlparse(url)
fayl_nomi = unquote(os.path.basename(manzil.path))
kengaytma = os.path.splitext(fayl_nomi)[1].lower()

if kengaytma not in ruxsat_etilgan_formatlar:
    print("Xatolik: Bu fayl formati qo‘llab-quvvatlanmaydi!")
    print("Ruxsat etilgan formatlar: mp3, mp4, pdf, png, jpg, jpeg, webp")

elif not fayl_nomi:
    print("Faylni yuklab bo‘lmadi!")
    print("URL manzilni tekshiring yoki fayl mavjud emas.")

else:
    print(f"Fayl turi: {kengaytma[1:].upper()}")
    print("Yuklab olinmoqda...")

    try:
        javob = requests.get(url, stream=True, timeout=30)
        javob.raise_for_status()

        os.makedirs("downloads", exist_ok=True)

        fayl_yoli = os.path.join("downloads", fayl_nomi)

        with open(fayl_yoli, "wb") as fayl:
            for bolak in javob.iter_content(chunk_size=8192):
                if bolak:
                    fayl.write(bolak)

        print("Fayl muvaffaqiyatli yuklandi!")
        print(f"Saqlangan fayl: {fayl_yoli}")

    except requests.exceptions.RequestException:
        print("Faylni yuklab bo‘lmadi!")
        print("URL manzilni tekshiring yoki fayl mavjud emas.")