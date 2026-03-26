from instagrapi import Client

username = "orumcekcik" # Kendi kullanıcı adını yaz
password = "Orum1453"       # Kendi şifreni yaz

print("Instagram'a bağlanılıyor...")
cl = Client()
cl.login(username, password)
cl.dump_settings("session.json")
print("Harika! session.json dosyası başarıyla oluşturuldu!")