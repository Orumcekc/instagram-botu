# PythonAnywhere Kurulum Rehberi

Botunuzu PythonAnywhere üzerinde her gün otomatik çalışacak şekilde ayarlamak için şu adımları izleyin:

## 1. Dosyaların Yüklenmesi
1. PythonAnywhere paneline giriş yapın.
2. **"Files"** sekmesine gidin.
3. Yeni bir klasör oluşturun (örneğin: `instagram_bot`).
4. Klasörün içine şu dosyaları yükleyin:
   - `bot.py`
   - `.env`
   - `requirements.txt`

## 2. Bağımlılıkların Kurulması
1. PythonAnywhere panelinden **"Consoles"** sekmesine gidin.
2. Bir **"Bash"** konsolu açın.
3. Şu komutu yazarak kütüphaneleri kurun:
   ```bash
   pip3 install --user -r /home/KULLANICI_ADINIZ/instagram_bot/requirements.txt
   ```
   *(Not: `KULLANICI_ADINIZ` kısmını kendi kullanıcı adınızla, `instagram_bot` kısmını da oluşturduğunuz klasör adıyla değiştirin.)*

## 3. Otomatik Görev (Task) Ayarlama
1. Panelden **"Tasks"** sekmesine gidin.
2. **"Description"** kısmına isteğe bağlı bir isim yazın (örn: Instagram Bot).
3. **"Command"** kısmına tam olarak şu komutu yazın:
   ```bash
   python3 /home/KULLANICI_ADINIZ/instagram_bot/bot.py
   ```
4. **"Time"** kısmından botun her gün çalışmasını istediğiniz saati (UTC formatında) ayarlayın.
5. **"Create"** butonuna tıklayın.

Artık botunuz her gün belirttiğiniz saatte otomatik olarak çalışacak, gönderisini atacak ve kapanacaktır.
