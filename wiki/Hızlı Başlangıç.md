# ⚡ Hızlı Başlangıç

> **5 dakikada** Walmart AI Content Generator'ü çalıştırın!

## 🎯 Bu Rehber Kimlere Uygun?

- ✅ **İlk kez kullananlar** - Hiç deneyim gerektirmez
- ✅ **Hızlı test etmek isteyenler** - Dakikalar içinde sonuç
- ✅ **Kurumsal kullanıcılar** - Basit kurulum süreci

## 📋 Ön Gereksinimler

### Sistem Gereksinimleri
| Bileşen | Minimum | Önerilen |
|---------|---------|----------|
| **İşletim Sistemi** | Windows 10, macOS 10.15, Ubuntu 18.04 | Latest |
| **Python** | 3.11+ | 3.11.5 |
| **RAM** | 2GB | 8GB |
| **Disk Alanı** | 1GB | 5GB |
| **İnternet** | Gerekli | Stabil bağlantı |

### Yazılım Gereksinimleri
```bash
# Python versiyonunu kontrol edin
python --version
# Python 3.11.0 veya üzeri olmalı

# pip versiyonunu kontrol edin  
pip --version
```

## 🚀 Kurulum Adımları

### Adım 1: Repository'yi İndirin
```bash
# Git ile klonlama (önerilen)
git clone https://github.com/yusuf44777/walmart_project_last.git
cd walmart_project_last

# Veya ZIP olarak indirip çıkarın
# https://github.com/yusuf44777/walmart_project_last/archive/main.zip
```

### Adım 2: Sanal Ortam Oluşturun (Önerilen)
```bash
# Sanal ortam oluştur
python -m venv walmart_env

# Sanal ortamı aktif et
# macOS/Linux:
source walmart_env/bin/activate

# Windows:
walmart_env\Scripts\activate

# Sanal ortam aktifse (walmart_env) prefix görünür
```

### Adım 3: Bağımlılıkları Yükleyin
```bash
# Tüm gerekli paketleri yükle
pip install -r requirements.txt

# Alternatif: Temel paketleri tek tek yükle
pip install streamlit openai requests pandas
```

### Adım 4: Uygulamayı Başlatın
```bash
# Streamlit uygulamasını çalıştır
streamlit run walmart.py

# Uygulama şu adreste açılır:
# http://localhost:8501
```

## 🎮 İlk Kullanım

### AI Model Seçimi
1. **Sol sidebar**'ı açın
2. **AI Model** seçin:
   - 🟢 **Ollama (Önerilen)**: Ücretsiz, yerel
   - 🔵 **OpenAI GPT**: Ücretli, cloud-based

### Ollama Kurulumu (Ücretsiz Seçenek)
```bash
# macOS için Homebrew ile:
brew install ollama

# Manuel kurulum:
# https://ollama.ai/download adresinden indirin

# Ollama'yı başlatın
ollama serve

# Temel model indirin (4GB)
ollama pull llama3.1:8b
```

### OpenAI Kurulumu (Ücretli Seçenek)
1. [OpenAI Dashboard](https://platform.openai.com/api-keys)'da API key oluşturun
2. Sidebar'da **OpenAI API Key** alanına yapıştırın
3. Model: **gpt-3.5-turbo** veya **gpt-4** seçin

## 📝 İlk İçerik Üretimi

### Örnek Ürün Bilgileri
```
Ürün Adı: Samsung Galaxy S24 Ultra
Kategori: Elektronik > Cep Telefonu
Özellikler: 
- 6.8 inç Dynamic AMOLED ekran
- 200MP ana kamera
- 5000mAh batarya
- 12GB RAM, 256GB depolama
```

### Adımlar
1. **Ürün Adı** girin
2. **Özellikler** listeleyin (satır satır)
3. **"Açıklama Oluştur"** butonuna tıklayın
4. **5-10 saniye** bekleyin
5. **Sonuçları** inceleyin ve **Export** edin

## ✅ Kurulum Testi

### Test Senaryosu
```python
# Test için minimal örnek
Ürün: "Apple iPhone 15"
Özellikler: "128GB, Gece Mavisi, A17 çip"
```

### Beklenen Çıktı
- ✅ Başlık: 50-100 karakter
- ✅ Özellikler: 3-8 madde halinde
- ✅ Açıklama: 150+ kelime, HTML formatında
- ✅ Export butonları aktif

## 🔧 Sorun Giderme

### Yaygın Problemler

#### "ModuleNotFoundError" Hatası
```bash
# Çözüm: Gereksinimler eksik
pip install -r requirements.txt
```

#### Port Zaten Kullanımda
```bash
# Çözüm: Farklı port kullan
streamlit run walmart.py --server.port 8502
```

#### Ollama Bağlantı Hatası
```bash
# Çözüm: Ollama servisini başlat
ollama serve

# Arka planda çalışıyor mu kontrol et
ps aux | grep ollama
```

#### OpenAI API Hatası
- ✅ API key doğru kopyalandı mı?
- ✅ Hesapta yeterli kredi var mı?
- ✅ API key aktif mi?

## 📱 Mobil Kullanım

Streamlit uygulaması **responsive**'dir:
- **Telefon**: Tam özellik desteği
- **Tablet**: Optimized layout
- **Desktop**: En iyi deneyim

### Mobil Erişim
```
# Local network üzerinden erişim
streamlit run walmart.py --server.address 0.0.0.0

# Mobil cihazınızdan:
http://[BİLGİSAYAR_IP]:8501
```

## 🎯 Sonraki Adımlar

Temel kurulum tamamlandı! Şimdi şunları keşfedebilirsiniz:

| Gelişmiş Özellik | Rehber | Süre |
|------------------|---------|------|
| **Custom Model** | [[Model Eğitimi]] | 30 dk |
| **Toplu İşleme** | [[API Dokümantasyonu]] | 15 dk |
| **Cloud Deploy** | [[Deployment]] | 45 dk |
| **Veri Analizi** | [[Performans]] | 20 dk |

---

## 💡 Pro İpuçları

### Performans Optimizasyonu
- 🚀 **SSD kullanın** - Model yükleme hızı
- 🧠 **8GB+ RAM** - Büyük modeller için
- 🌐 **Stabil internet** - Cloud API'ler için

### Güvenlik
- 🔐 **API keyleri** asla paylaşmayın
- 🔒 **Environment variables** kullanın
- 🛡️ **Rate limiting** uygulayın

### Kalite Artırma
- 📝 **Detaylı ürün bilgisi** verin
- 🎯 **Spesifik özellikler** ekleyin
- 🔄 **Farklı modeller** deneyin

---

*⏱️ Ortalama kurulum süresi: 5-10 dakika | 🎯 Başarı oranı: %95 | 📞 Destek: [[SSS]]*
