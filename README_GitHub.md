# GitHub Yükleme ve Ayarlar Kılavuzu

Botunuzun GitHub Actions üzerinde her gün otomatik çalışması için şu adımları izleyin:

## 1. Kodları GitHub'a Yükleme
1. [GitHub](https://github.com/) üzerinde yeni bir **Private** (Gizli) repository oluşturun.
2. Bilgisayarınızdaki tüm dosyaları (`bot.py`, `requirements.txt`, `.github` klasörü vb.) bu repository'ye yükleyin.
   > **Önemli:** `.env` dosyasını GitHub'a **YÜKLEMEYİN**. Şifrelerinizi bir sonraki adımda güvenli şekilde ekleyeceğiz.

## 2. Secrets (Gizli Değişkenler) Ayarları
Giriş Bilgilerinizi GitHub'a şu şekilde tanıtın:

1. GitHub Repository sayfanızda üstteki **"Settings"** sekmesine tıklayın.
2. Sol taraftaki menüden **"Secrets and variables"** -> **"Actions"** yolunu izleyin.
3. **"New repository secret"** butonuna tıklayarak aşağıdaki 3 anahtarı tek tek ekleyin:

| Secret Name | Değer (Secret Value) |
| :--- | :--- |
| `OPENAI_API_KEY` | OpenAI API Anahtarınız |
| `INSTAGRAM_USERNAME` | Instagram Kullanıcı Adınız |
| `INSTAGRAM_PASSWORD` | Instagram Şifreniz |

## 3. Çalışma Durumunu Kontrol Etme
1. Üstteki **"Actions"** sekmesine tıklayın.
2. Sol tarafta **"Instagram Bot Daily Post"** isimli workflow'u göreceksiniz.
3. Manuel test etmek için **"Run workflow"** butonuna basarak hemen çalıştırabilirsiniz.
4. Bot her gün saat 15:00'te (TSİ) otomatik olarak tetiklenecektir.

Artık bilgisayarınız kapalı olsa bile Instagram botunuz otonom bir şekilde çalışmaya devam edecek!
