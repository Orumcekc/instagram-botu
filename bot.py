import os
import sys
import time
import random
import json
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# .env dosyasını bulunduğu dizinden güvenli şekilde yükle
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env')
load_dotenv(env_path)

# API Anahtarları ve E-posta Bilgileri
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# OpenAI İstemcisi
client_ai = OpenAI(api_key=OPENAI_API_KEY)

# Sistem Talimatı (Karakter ve Tarz)
SYSTEM_INSTRUCTION = """Sen profesyonel bir sosyal medya uzmanısın. Tüm yanıtlarını mükemmel bir Türkçe ile, imla ve yazım kurallarına titizlikle uyarak vermelisin. İçeriklerin yaratıcı, ilgi çekici ve viral potansiyeli yüksek olmalı.
ÖNEMLİ: İçerik üretirken sosyal medyadaki 'Mustafa Şen' (@mustafasenc) profilinin dilini, tarzını ve kurgu yapısını uygula.
ÜSLUP: Ağabey dili, derinlikli analiz, teknofeodalizm eleştirisi, tarih şuuru, meydan okuyan tavır ("Artık yemiyoruz", "Hadi oradan").
KİMLİK: Sosyal ve Dini Yorumcu, Değerlerin Savunucusu, Modern Çağ Eleştirmeni, Jeopolitik Analist, Tarih ve Hafıza Bekçisi.
KONULAR: Gelenek ve Gelecek, Anadolu İrfanı, Gençlik ve Kimlik, Şehir Estetiği, Dijital Kölelik, Medeniyet Tasavvuru."""

def generate_content(is_carousel=False):
    topics = [
        "Gelenek ve Gelecek Bağlantısı", 
        "Anadolu İrfanı ve Modern Dünya", 
        "Cemil Meriç ve Kültür Şuurumuz", 
        "Gençliğin Kimlik İnşası", 
        "Şehir, Mimari ve Ruh",
        "Tarih Bilinci ve Yarınlar",
        "Maneviyat ve Meta-fizik",
        "Küresel Oyunlar ve Jeopolitik",
        "Dijital Çağda İnsan Kalmak",
        "Medeniyet Tasavvurumuz"
    ]
    selected_topic = random.choice(topics)
    
    try:
        if is_carousel:
            prompt = (
                f"Lütfen '{selected_topic}' konusu üzerine bir Instagram Carousel (3'lü kaydırmalı post) içeriği üret:\n"
                f"1. Instagram açıklaması (caption): Derinlikli, 'Mustafa Şen' tarzında.\n"
                f"2. 3 adet Görsel Metni (punchy_texts): Her görsel için birer adet, kısa ve sarsıcı cümle.\n"
                f"Yanıtını sadece JSON formatında ver: {{\"caption\": \"...\", \"punchy_texts\": [\"...\", \"...\", \"...\"]}}"
            )
        else:
            prompt = (
                f"Lütfen '{selected_topic}' konusu üzerine tek bir Instagram postu üret:\n"
                f"1. Instagram açıklaması (caption): Derinlikli, 'Mustafa Şen' tarzında.\n"
                f"2. Görsel Metni (punchy_text): Görselin ortasına yazılacak çok vuruşu bir cümle.\n"
                f"Yanıtını sadece JSON formatında ver: {{\"caption\": \"...\", \"punchy_text\": \"...\"}}"
            )
        
        response = client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" },
            temperature=0.7
        )
        
        result = json.loads(response.choices[0].message.content)
        return result, selected_topic
    except Exception as e:
        print(f"İçerik üretim hatası: {e}")
        return None, None

def generate_image(prompt_text, filename):
    try:
        response = client_ai.images.generate(
            model="dall-e-3",
            prompt=f"Cinematic, professional, high-end photography about: {prompt_text}. Style: Moody, dark tones, minimalist. No text in image.",
            size="1024x1024",
            quality="standard",
            n=1
        )
        img_url = response.data[0].url
        img_data = requests.get(img_url).content
        with open(filename, "wb") as f:
            f.write(img_data)
        return True
    except Exception as e:
        print(f"Görsel üretim hatası ({filename}): {e}")
        return False

def add_text_to_image(image_path, text, output_path):
    try:
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        font_paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "C:/Windows/Fonts/SegoeUI-Bold.ttf", "Arial"]
        font = None
        for p in font_paths:
            try:
                font = ImageFont.truetype(p, 60)
                break
            except: continue
        if not font: font = ImageFont.load_default()

        # Metni sarma ve yazdırma (Basitleştirilmiş)
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if draw.textbbox((0, 0), test_line, font=font)[2] < width * 0.8:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        line_height = draw.textbbox((0, 0), "Ay", font=font)[3] + 10
        total_height = len(lines) * line_height
        y = (height - total_height) / 2

        # Siyah bant
        draw.rectangle([0, y - 20, width, y + total_height + 20], fill=(0, 0, 0, 160))
        
        for line in lines:
            w = draw.textbbox((0, 0), line, font=font)[2]
            draw.text(((width - w) / 2, y), line, font=font, fill=(255, 255, 255, 255))
            y += line_height

        img = Image.alpha_composite(img, overlay).convert("RGB")
        img.save(output_path, quality=95)
        return True
    except Exception as e:
        print(f"Metin ekleme hatası: {e}")
        return False

def send_email(subject, body, image_paths):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        for path in image_paths:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    img_data = f.read()
                    image = MIMEImage(img_data, name=os.path.basename(path))
                    msg.attach(image)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"E-posta gönderim hatası: {e}")
        return False

def main():
    print("Otonom Bot Yeni Mimari Başlatıldı...")
    is_carousel = random.random() < 0.30
    content, topic = generate_content(is_carousel)
    
    if not content: return

    image_paths = []
    if is_carousel:
        print(f"Carousel Post Üretiliyor: {topic}")
        for i, punchy in enumerate(content['punchy_texts']):
            raw_img = f"carousel_{i}_raw.jpg"
            final_img = f"carousel_{i}_ready.jpg"
            if generate_image(f"{topic}: {punchy}", raw_img):
                add_text_to_image(raw_img, punchy, final_img)
                image_paths.append(final_img)
    else:
        print(f"Single Post Üretiliyor: {topic}")
        raw_img = "single_raw.jpg"
        final_img = "single_ready.jpg"
        if generate_image(f"{topic}: {content['punchy_text']}", raw_img):
            add_text_to_image(raw_img, content['punchy_text'], final_img)
            image_paths.append(final_img)

    if image_paths:
        subject = f"Instagram İçeriği: {topic} ({'Carousel' if is_carousel else 'Tekli'})"
        body = f"Konu: {topic}\n\nİçerik Metni:\n\n{content['caption']}\n\n---\nBu içerik otonom bot tarafından üretilmiştir."
        if send_email(subject, body, image_paths):
            print("İçerik başarıyla e-posta ile gönderildi!")
        else:
            print("E-posta gönderilemedi.")
    
    print("İşlem tamamlandı.")
    sys.exit(0)

if __name__ == "__main__":
    main()
# Bu bir senkronizasyon testidir