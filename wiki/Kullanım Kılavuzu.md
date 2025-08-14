# 📚 Kullanım Kılavuzu

> **Adım Adım Rehber** - Walmart AI Content Generator'ün tüm özelliklerini öğrenin

## 🎯 Bu Kılavuz Kimlere Uygun?

- ✅ **İçerik Editörleri** - Ürün açıklamaları yazanlar
- ✅ **E-ticaret Yöneticileri** - Marketplace içerik yönetimi
- ✅ **Pazarlama Uzmanları** - SEO ve conversion optimization
- ✅ **Girişimciler** - Küçük işletme sahipleri

## 🚀 Uygulama Arayüzü

### Ana Ekran Layout
```
┌─────────────────────────────────────────────────────────┐
│  🛒 Walmart Ürün Açıklaması Üreteci                     │
├─────────────────┬───────────────────────────────────────┤
│  📋 Sidebar     │  📝 Ana İçerik Alanı                   │
│                 │                                       │
│ • Model Seçimi  │ • Ürün Bilgileri Formu                │
│ • API Settings  │ • Sonuç Görüntüleme                    │
│ • Veri Toplama  │ • Export Butonları                     │
│ • Model Yönetimi│                                       │
│                 │                                       │
└─────────────────┴───────────────────────────────────────┘
```

## 📝 Temel Kullanım

### 1. AI Model Seçimi

#### Ollama (Ücretsiz) 🟢
```yaml
Avantajları:
  - Tamamen ücretsiz
  - Gizlilik (yerel işlem)
  - İnternet kesintisinde çalışır
  - Sınırsız kullanım

Dezavantajları:
  - Kurulum gerekli
  - Donanım kaynak kullanımı
  - Biraz daha yavaş
```

#### OpenAI GPT (Ücretli) 🔵
```yaml
Avantajları:
  - Yüksek kalite
  - Hızlı yanıt
  - Kurulum gerektirmez
  - Sürekli güncellenen model

Dezavantajları:
  - Ücretli (token başına)
  - İnternet bağlantısı gerekli
  - API key gerekli
```

### 2. Ürün Bilgileri Girişi

#### Ürün Adı
```
Örnek: Samsung Galaxy S24 Ultra
İpucu: Marka + Model + Varyant formatında
Kural: 10-100 karakter arası
```

#### Ürün Özellikleri
```
Format: Her satıra bir özellik
Örnek:
6.8 inç Dynamic AMOLED 2X ekran
200MP ana kamera, 12MP ultra geniş
5000mAh batarya, 45W hızlı şarj
12GB RAM, 256GB/512GB/1TB depolama
S Pen dahil
```

#### Kategori (Opsiyonel)
```
Örnekler:
- Elektronik > Cep Telefonu
- Ev & Yaşam > Mutfak
- Moda > Kadın Giyim
- Spor > Fitness Ekipmanları
```

### 3. İçerik Üretimi Süreci

#### Adım Adım
1. **Model Seçin** - Sidebar'dan AI modelinizi belirleyin
2. **API Key Girin** - (Sadece OpenAI için)
3. **Ürün Bilgilerini Doldurun** - Form alanlarını tamamlayın
4. **"Açıklama Oluştur"** - Butona tıklayın
5. **Bekleyin** - 5-15 saniye işlem süresi
6. **Sonuçları İnceleyin** - Üretilen içeriği kontrol edin
7. **Export Edin** - İstediğiniz formatta kaydedin

## 📊 Sonuç Analizi

### Üretilen İçerik Bileşenleri

#### 1. Başlık (Title)
```
Örnek: "Samsung Galaxy S24 Ultra - 200MP Kamerayla 
        Profesyonel Fotoğrafçılık Deneyimi"

Kriterler:
✅ 50-100 karakter
✅ Anahtar kelimeler dahil
✅ Çekici ve bilgilendirici
✅ Walmart standartlarına uygun
```

#### 2. Özellik Listesi (Features)
```
Format: Madde işaretli liste
Örnek:
• 6.8" Dynamic AMOLED 2X Infinity-O Display
• 200MP Ana Kamera + 12MP Ultra Geniş + 10MP Telefoto
• 5000mAh Batarya ile Tüm Gün Kullanım
• 12GB RAM + 256GB Dahili Hafıza
• S Pen ile Gelişmiş Verimlilik

Kriterler:
✅ 3-8 özellik
✅ Her madde 80 karakter altı
✅ En önemli özellikler önce
```

#### 3. Detaylı Açıklama (Description)
```
Yapısı:
- Giriş paragrafı (Hook)
- Ana özellikler detayı
- Kullanım senaryoları
- Satın alma motivasyonu
- Sonuç/Call-to-action

Kriterler:
✅ 150+ kelime
✅ HTML formatında
✅ SEO anahtar kelimeleri
✅ Paragraf yapısı
✅ Walmart tone-of-voice
```

## 🎛️ Gelişmiş Özellikler

### Veri Toplama Modu
```
Amaç: Model eğitimi için veri biriktirme
Konum: Sidebar > "📊 Veri Toplama"

Nasıl Çalışır:
1. Özelliği aktif edin
2. Normal içerik üretimi yapın
3. Her üretim training_data.json'a kaydedilir
4. Veriler model eğitiminde kullanılır

Fayda: Zamanla daha iyi sonuçlar
```

### Model Yönetimi
```
Konum: Sidebar > "🔧 Model Yönetimi"

Özellikler:
- Walmart-GPT Basic oluşturma
- Model performans analizi
- Veri kalitesi kontrolü
- Model güncelleme

Gereksinimler:
- 50+ training data
- Ollama kurulu
- Yeterli disk alanı
```

### Export Seçenekleri

#### TXT Format
```
Kullanım: Basit metin editörü
İçerik: Sadece düz metin
Boyut: En küçük dosya
Uyumluluk: Tüm platformlar
```

#### JSONL Format
```
Kullanım: Teknik analiz
İçerik: Yapılandırılmış veri
Boyut: Orta
Uyumluluk: Programlama araçları
```

## 🔍 Kalite Kontrolü

### İyi İçerik Örnekleri

#### Başarılı Başlık
```
❌ Kötü: "Telefon"
❌ Orta: "Samsung telefon"
✅ İyi: "Samsung Galaxy S24 Ultra - 200MP Kamerayla Profesyonel Fotoğrafçılık"

Neden İyi:
- Marka ve model belirtilmiş
- Ana özellik vurgulanmış
- Fayda odaklı
- SEO dostu
```

#### Başarılı Özellik Listesi
```
❌ Kötü: 
- Kamera var
- Batarya var

✅ İyi:
- 200MP Triple Kamera Sistemi
- 5000mAh Batarya + 45W Hızlı Şarj
- 6.8" Dynamic AMOLED 2X Ekran
- 12GB RAM + 256GB Depolama

Neden İyi:
- Spesifik sayısal değerler
- Teknik terimler doğru
- Fayda odaklı açıklama
```

### Yaygın Hatalar ve Çözümleri

#### Hata 1: Çok Genel Bilgiler
```
❌ Problem: "Bu ürün çok kaliteli ve kullanışlıdır"
✅ Çözüm: "A17 Pro çip ile %15 daha hızlı performans"

İpucu: Sayısal veriler ve spesifik özellikler kullanın
```

#### Hata 2: Çok Uzun Açıklama
```
❌ Problem: 500+ kelimelik makale tarzı
✅ Çözüm: 150-250 kelime, öz ve net

İpucu: Her paragraf bir ana noktayı vurgulasın
```

#### Hata 3: SEO Dostu Olmayan İçerik
```
❌ Problem: Anahtar kelime eksikliği
✅ Çözüm: Ürün adı, kategori, marka kelimelerini dahil edin

İpucu: "Samsung smartphone", "Galaxy S24", "200MP camera" gibi
```

## 🎯 Kullanım Senaryoları

### Senaryo 1: Toplu Ürün İçeriği
```
Durum: 100 ürün için içerik gerekli
Strateji:
1. Veri toplama modunu açın
2. İlk 10 ürünü manuel yapın
3. Model eğitimi gerçekleştirin
4. Kalan 90 ürünü otomatik yapın
5. Son kontrol ve düzenleme

Süre: 2-3 gün (manuel) → 4-6 saat (otomatik)
```

### Senaryo 2: A/B Test İçeriği
```
Durum: Conversion rate optimizasyonu
Strateji:
1. Aynı ürün için 3 farklı başlık üretin
2. Farklı feature vurguları deneyin
3. Sonuçları test edin
4. En başarılıyı seçin

Fayda: %10-30 conversion artışı
```

### Senaryo 3: Çok Dilli İçerik
```
Durum: Farklı ülke marketleri
Strateji:
1. İngilizce master içerik oluşturun
2. Prompta dil belirtmesi ekleyin
3. Her dil için customize edin
4. Yerel kültürel uyumlamalar yapın

Desteklenen Diller: TR, EN, ES, FR, DE, IT
```

## 📱 Mobil Kullanım

### Responsive Design
```
Telefon (320-768px):
- Tek sütun layout
- Büyük butonlar
- Kolay dokunma
- Hızlı yükleme

Tablet (768-1024px):
- İki sütun layout
- Sidebar genişletebilir
- Optimized forms

Desktop (1024px+):
- Tam feature set
- Multiple windows
- Keyboard shortcuts
```

### Mobil İpuçları
```
✅ Portrait modda kullanın
✅ Wifi bağlantısını tercih edin
✅ Büyük ürün listelerinde batch işlem yapın
✅ Regular olarak sync edin
```

## ⚙️ Performans Optimizasyonu

### Hızlandırma İpuçları

#### Model Seçimi
```
En Hızlı: OpenAI GPT-3.5 (2-5 saniye)
Orta: Ollama llama3.1:8b (5-10 saniye)
En Kaliteli: OpenAI GPT-4 (8-15 saniye)
```

#### Prompt Optimizasyonu
```
❌ Verimsiz: Çok detaylı özellik listesi
✅ Etkili: 3-5 ana özellik, net format

❌ Verimsiz: "Mükemmel ürün açıklaması yaz"
✅ Etkili: "50 kelimelik e-ticaret açıklaması yaz"
```

#### Cache Kullanımı
```
Benzer ürünler için:
1. Önceki sonuçları referans alın
2. Template yaklaşımı kullanın
3. Batch processing yapın
```

## 🔧 Troubleshooting

### Yaygın Problemler

#### "Model Bulunamadı" Hatası
```
Neden: Ollama modeli indirilmemiş
Çözüm:
ollama pull llama3.1:8b
ollama list  # kontrol

Alternatif: OpenAI'ya geçin
```

#### "API Key Geçersiz" Hatası
```
Neden: Yanlış/eski OpenAI API key
Çözüm:
1. platform.openai.com'da yeni key oluşturun
2. Billing aktif mi kontrol edin
3. Key'i doğru kopyalayın (boşluk yok)
```

#### "Bağlantı Zaman Aşımı"
```
Neden: Ağ problemi veya model yavaş
Çözüm:
1. İnternet bağlantısını kontrol edin
2. Daha küçük model kullanın
3. Prompt'u kısaltın
```

#### "Kalitesiz Sonuç"
```
Neden: Yetersiz input bilgisi
Çözüm:
1. Daha detaylı özellik listesi
2. Kategori bilgisi ekleyin
3. Örnekler verin
4. Farklı model deneyin
```

## 📈 İleri Düzey Kullanım

### Custom Prompt Engineering
```python
# Gelişmiş prompt şablonu
prompt_template = """
Ürün: {product_name}
Kategori: {category}
Hedef Kitle: {target_audience}
Ton: {tone} (Profesyonel/Samimi/Teknik)
Uzunluk: {length} kelime
SEO Keywords: {keywords}

Format:
1. Başlık (60 karakter)
2. Özellikler (5 madde)
3. Açıklama ({length} kelime)
"""
```

### API Integration
```python
# Kendi uygulamanızda kullanım
import requests

def generate_walmart_content(product_data):
    response = requests.post(
        "http://localhost:8501/api/generate",
        json=product_data
    )
    return response.json()
```

### Batch Processing
```python
# Toplu işlem için script
products = [
    {"name": "iPhone 15", "features": [...]},
    {"name": "Galaxy S24", "features": [...]},
    # ...
]

for product in products:
    content = generate_content(product)
    save_to_database(content)
```

## 📊 Analytics ve Raporlama

### Kullanım İstatistikleri
```
Dashboard Metrikleri:
- Günlük içerik üretim sayısı
- Model başarı oranları
- Ortalama yanıt süreleri
- Kullanıcı memnuniyeti
- Error rate
```

### Kalite Metrikleri
```
İçerik Kalite Skorları:
- Başlık uygunluğu (0-100)
- Özellik completeness (0-100)
- Açıklama kalitesi (0-100)
- SEO skoru (0-100)
- Walmart uyumluluğu (0-100)
```

---

## 🎉 Artık Uzman Kullanıcısınız!

Bu kılavuzu tamamladıktan sonra:

- ✅ **Profesyonel içerik** üretebilirsiniz
- ✅ **Optimizasyon teknikleri** uygulayabilirsiniz  
- ✅ **Sorunları** hızla çözebilirsiniz
- ✅ **Gelişmiş özellikler** kullanabilirsiniz

### Sonraki Seviye
- [[Model Eğitimi]] - Kendi özel modelinizi oluşturun
- [[API Dokümantasyonu]] - Programmatic erişim
- [[Proje Yönetimi]] - Takım çalışması rehberleri

---

*📖 Kılavuz versiyon: 3.0 | 👥 Hedef kullanıcı: Tüm seviyeler | ⏱️ Okuma süresi: 25 dk | 📞 Destek: [[SSS]]*
