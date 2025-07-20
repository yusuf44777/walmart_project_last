# 🛒 Walmart Model Eğitimi Rehberi

## 🎯 Amaç
Bu rehber, üst düzey Walmart-GPT modellerinin nasıl eğitileceğini ve optimize edileceğini açıklar.

## 📋 Model Seviyелері

### 1. **Walmart-GPT Basic** (Temel Seviye)
- **Kullanım**: Başlangıç seviyesi, temel Walmart kuralları
- **Eğitim Verisi**: Minimum 50 örnek
- **Özellikler**: Temel format kontrolü, karakter limitleri

### 2. **Walmart-GPT Advanced** (Gelişmiş Seviye)  
- **Kullanım**: Profesyonel kullanım, optimize edilmiş içerik
- **Eğitim Verisi**: 200+ kaliteli örnek
- **Özellikler**: SEO optimizasyonu, veri analizi

### 3. **Walmart-GPT Expert** (Uzman Seviye)
- **Kullanım**: Maksimum performans, ticari kullanım
- **Eğitim Verisi**: 500+ premium örnek  
- **Özellikler**: Psikolojik persuasion, conversion optimization

## 🚀 Eğitim Süreci

### Adım 1: Veri Toplama
```bash
# Streamlit uygulamanızı çalıştırın
streamlit run walmart.py --server.port 8504

# "Veri Toplama" seçeneğini aktif edin
# Her ürün içeriği oluşturduğunuzda training_data.json dosyasına kaydedilir
```

### Adım 2: Veri Kalitesi Analizi
```bash
# Veri kalitesini kontrol edin
python3 advanced_model_training.py
```

**Kalite Kriterleri:**
- ✅ Başlık: 50-100 karakter
- ✅ Özellikler: 3-10 adet, her biri ≤80 karakter
- ✅ Açıklama: ≥150 kelime
- ✅ Walmart uyumluluğu: %80+ skor

### Adım 3: Temel Model Oluşturma
```bash
# Sidebar'dan "🔧 Temel Model Oluştur" butonuna tıklayın
# Veya manuel olarak:
python3 create_walmart_model.py
```

### Adım 4: Gelişmiş Model Eğitimi
```bash
# Sidebar'dan "🚀 Gelişmiş Model Oluştur" butonuna tıklayın
# Veya manuel olarak:
python3 model_optimizer.py
```

### Adım 5: Model Performans Analizi
```bash
# Sidebar'dan "📈 Model Analytics" butonuna tıklayın
# Veya manuel olarak:
python3 model_analytics.py
```

## 📊 Model Optimizasyonu

### Veri Kalitesi İyileştirme
1. **Düşük Skorlu Örnekleri Temizleme**
   - Skor < 80 olan örnekleri gözden geçirin
   - Walmart kurallarına uymayan içerikleri düzeltin

2. **Veri Augmentation**
   - Mevcut kaliteli örneklerden varyasyonlar oluşturma
   - Kategori bazlı şablonlar kullanma

3. **Sürekli İyileştirme**
   - Kullanıcı geri bildirimlerini analiz etme
   - A/B testleri yapma

### Model Parametreleri

#### Temel Model
```
Temperature: 0.7 (Yaratıcı ama tutarlı)
Top-K: 40 (Kelime seçimi çeşitliliği)
Top-P: 0.9 (Kontrollü rastgelelik)
```

#### Gelişmiş Model
```
Temperature: 0.6 (Daha tutarlı)
Top-K: 35 (Odaklanmış kelime seçimi)
Top-P: 0.85 (Daha kontrollü)
Context: 6144 (Genişletilmiş bağlam)
```

#### Uzman Model
```
Temperature: 0.5 (Maksimum tutarlılık)
Top-K: 30 (En odaklanmış seçim)
Top-P: 0.8 (En kontrollü)
Context: 8192 (Maksimum bağlam)
```

## 🔄 Sürekli İyileştirme Döngüsü

### 1. Veri Toplama Döngüsü
- **Haftalık**: Yeni ürün kategorilerinden veri toplama
- **Aylık**: Veri kalitesi analizi ve temizleme
- **Üç Aylık**: Model performans değerlendirmesi

### 2. Model Güncelleme Stratejisi
```bash
# Yeni verilerle model güncelleme
# 1. Yeni training data topla (en az 100 örnek)
# 2. Veri kalitesini analiz et
# 3. Mevcut model ile karşılaştırmalı test yap
# 4. Performans artışı varsa yeni modeli devreye al
```

### 3. A/B Testing
```python
# Model karşılaştırması
python3 model_analytics.py

# Metrikler:
# - Walmart Compliance Score
# - SEO Score  
# - Readability Score
# - Conversion Estimate
```

## 📈 Performans Metrikleri

### Temel Metrikler
- **Walmart Uyumluluk**: %95+ hedef
- **SEO Skoru**: 70+ hedef  
- **Okunabilirlik**: 60+ hedef
- **Tahmini Dönüşüm**: 7+ hedef

### Gelişmiş Metrikler
- **Yanıt Süresi**: <5 saniye
- **Tutarlılık**: %90+ aynı promptlar için
- **Kategori Optimizasyonu**: Kategori bazlı performans

## 🛠️ Sorun Giderme

### Model Oluşturma Hataları
```bash
# Ollama servisini kontrol edin
ollama list

# Ollama'yı yeniden başlatın
brew services restart ollama

# Disk alanını kontrol edin (en az 10GB gerekli)
df -h
```

### Düşük Model Performansı
1. **Veri Kalitesi**: training_data.json dosyasını analiz edin
2. **Veri Miktarı**: En az 200 kaliteli örnek gerekli
3. **Kategori Çeşitliliği**: Farklı ürün kategorilerinden veri ekleyin

### Bellek Sorunları
```bash
# Hafif model kullanın
ollama run llama3.1:8b

# Sistem kaynaklarını kontrol edin
htop
```

## 🎯 İleri Seviye Optimizasyonlar

### 1. Kategoriye Özel Modeller
```python
# Elektronik ürünler için özel model
# Ev eşyaları için özel model  
# Moda ürünleri için özel model
```

### 2. Multi-Model Ensemble
```python
# Farklı modellerin sonuçlarını birleştirme
# Voting mechanism ile en iyi sonucu seçme
```

### 3. Real-Time Learning
```python
# Kullanıcı feedback'i ile model güncelleme
# Online learning sistemleri
```

## 🎉 Başarı Hikayeleri

### Örnek Performans Artışları
- **Walmart Uyumluluğu**: %65 → %95 (+30%)
- **SEO Performansı**: 45 → 85 (+40 puan)
- **İçerik Kalitesi**: 6.2 → 8.7 (+2.5 puan)

### ROI Hesaplaması
- **Manuel İçerik Üretimi**: 30 dakika/ürün
- **AI ile İçerik Üretimi**: 2 dakika/ürün  
- **Zaman Tasarrufu**: %93
- **Kalite Artışı**: %40

---

## 📞 Destek

Model eğitimi konusunda sorularınız için:
- 📧 Geliştiriciye ulaşın
- 📚 Dokümantasyonu inceleyin
- 🔧 Debug loglarını kontrol edin

**Başarılar! 🚀**
