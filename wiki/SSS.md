# ❓ SSS - Sık Sorulan Sorular

> **Hızlı Yanıtlar** - En çok sorulan sorular ve çözümleri

## 🎯 Genel Sorular

### Q: Bu uygulama ücretsiz mi?
**A:** Evet! Uygulama tamamen ücretsizdir. Ollama ile yerel olarak kullanabilirsiniz. Sadece OpenAI kullanımında API maliyeti vardır.

### Q: Hangi dillerde içerik üretebilirim?
**A:** Türkçe, İngilizce, İspanyolca, Fransızca, Almanca, İtalyanca desteklenir. Prompt'a dil belirtmesi eklemeniz yeterli.

### Q: Üretilen içerik telif hakkı sorunu oluşturur mu?
**A:** AI tarafından üretilen orijinal içerikler telif sorunu oluşturmaz. Ancak ürün bilgileri doğru ve orijinal olmalıdır.

### Q: Offline kullanabilir miyim?
**A:** Evet! Ollama ile tamamen offline çalışabilir. Sadece ilk kurulum için internet gerekli.

## 🔧 Kurulum Sorunları

### Q: Python 3.11 bulamıyorum, daha eski versiyon kullanabilir miyim?
**A:** Minimum Python 3.9 desteklenir ancak 3.11+ önerilir. Performans ve güvenlik açısından güncel sürümü kullanın.

### Q: "pip install" hatası alıyorum
**A:** 
```bash
# Pip'i güncelleyin
python -m pip install --upgrade pip

# Sanal ortam kullanın
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows

# Sonra requirements'ı yükleyin
pip install -r requirements.txt
```

### Q: Ollama kurulumu nasıl yapılır?
**A:**
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# https://ollama.ai/download adresinden exe indirin

# Model indirme
ollama pull llama3.1:8b
```

### Q: "ModuleNotFoundError: No module named 'streamlit'" hatası
**A:** Sanal ortamı aktif ettiğinizden ve requirements.txt'i yüklediğinizden emin olun:
```bash
source venv/bin/activate
pip install streamlit
```

## 🤖 AI Model Sorunları

### Q: Ollama "connection refused" hatası veriyor
**A:**
```bash
# Ollama servisini başlatın
ollama serve

# Arka planda çalışıyor mu kontrol edin
ps aux | grep ollama

# Model indirildi mi kontrol edin
ollama list
```

### Q: OpenAI API key nereden alırım?
**A:** 
1. [platform.openai.com](https://platform.openai.com) hesap açın
2. Billing bilgilerini ekleyin
3. API Keys bölümünden yeni key oluşturun
4. Güvenli yerde saklayın

### Q: "Rate limit exceeded" hatası alıyorum
**A:** OpenAI API limitleriniz dolmuş. Çözümler:
- Ücretli planı aktif edin
- Daha yavaş request gönderin
- Ollama'ya geçin (limitsiz)

### Q: Model yanıtları çok yavaş
**A:**
- **Ollama**: Daha küçük model kullanın (llama3.1:8b yerine 7b)
- **Donanım**: RAM ve CPU'yu kontrol edin
- **İnternet**: Stabil bağlantı sağlayın
- **Prompt**: Daha kısa ve net prompt yazın

## 📝 İçerik Kalitesi

### Q: Üretilen içerik kalitesiz, nasıl iyileştirebilirim?
**A:**
1. **Daha detaylı input**: Ürün özelliklerini tam yazın
2. **Kategori belirtin**: Electronics > Smartphone gibi
3. **Örnekler verin**: "iPhone 15 benzeri akıllı telefon"
4. **Model değiştirin**: GPT-4 daha kaliteli

### Q: Walmart standartlarına uygun mu?
**A:** Evet, özel olarak Walmart marketplace formatına göre eğitilmiştir:
- 50-100 karakter başlık
- Madde işaretli özellikler
- SEO uyumlu açıklama
- HTML formatı

### Q: Başlık çok uzun/kısa çıkıyor
**A:** Model'e daha spesifik talimat verin:
```
"60 karakter başlık oluştur"
"Kısa ve net başlık yaz"
"SEO uyumlu title oluştur"
```

### Q: Aynı ürün için farklı içerikler üretebilir miyim?
**A:** Evet! Her seferinde farklı sonuç üretir. A/B test için mükemmel.

## 💾 Veri ve Export

### Q: Verilerim güvende mi?
**A:** 
- **Ollama**: Tüm işlemler local, hiçbir veri dışarı gönderilmez
- **OpenAI**: Sadece API çağrısı, training'de kullanılmaz (opt-out)
- **Uygulama**: Veriler sadece yerel training_data.json'da

### Q: Export edilen dosyalar nerede?
**A:** Browser'ın download klasörüne kaydedilir:
- **TXT**: Düz metin format
- **JSONL**: Yapılandırılmış JSON data

### Q: Training data nasıl silinir?
**A:**
```bash
# Training verisini temizle
rm training_data.json

# Veya içeriği sıfırla
echo "[]" > training_data.json
```

### Q: Export dosyası açılmıyor
**A:**
- **TXT**: Notepad, VS Code, Word ile açın
- **JSONL**: VS Code, JSON viewer araçları
- **Encoding**: UTF-8 olduğundan emin olun

## 🚀 Performans ve Optimizasyon

### Q: Uygulama çok RAM kullanıyor
**A:**
1. **Model boyutu**: Küçük model kullanın (7b yerine 8b)
2. **Browser**: Gereksiz tabları kapatın
3. **System**: Diğer uygulamaları kapatın
4. **Restart**: Ollama'yı yeniden başlatın

### Q: CPU %100 kullanımda
**A:**
- Normal davranış (AI model processing)
- Büyük modeller daha çok CPU kullanır
- İşlem bitince normale döner
- Arka planda başka ağır işlem yoksa sorun değil

### Q: Disk alanı yetersiz hatası
**A:**
```bash
# Model boyutlarını kontrol edin
ollama list

# Kullanmadığınız modelleri silin
ollama rm model_name

# Training data boyutunu kontrol edin
ls -lah training_data.json
```

## 🌐 Network ve Bağlantı

### Q: İnternet olmadan çalışır mı?
**A:**
- **Ollama**: Tamamen offline çalışır
- **OpenAI**: İnternet gerekli
- **İlk kurulum**: Model indirme için internet gerekli

### Q: Şirket firewall'unda çalışır mı?
**A:**
- **Ollama**: Port 11434, local trafiği engellenmez
- **OpenAI**: Port 443 (HTTPS) açık olmalı
- **Streamlit**: Port 8501, internal network

### Q: Mobil hotspot ile kullanabilir miyim?
**A:**
- **Ollama**: Sadece ilk indirme için data kullanır
- **OpenAI**: Her request veri kullanır (~1-5KB/request)
- **Uygulama**: Minimal data kullanımı

## 🔐 Güvenlik

### Q: API key'imi nasıl güvende tutarım?
**A:**
1. **Environment variable**: OS seviyesinde sakla
2. **Asla paylaşma**: GitHub, email, chat'te paylaşma
3. **Düzenli değiştir**: Aylık yenile
4. **Minimize erişim**: Sadece gerekli permissions

### Q: Şirket bilgileri güvenli mi?
**A:**
- **Ollama**: Tüm veriler local
- **OpenAI**: API policy'ye göre training'de kullanılmaz
- **Uygulama**: Hiçbir external service'e veri gönderme

### Q: GDPR uyumlu mu?
**A:** Evet:
- Kişisel veri toplamaz
- User consent mekanizması var
- Veri silme hakkı mevcut
- Data portability desteklenir

## 🛠️ Geliştirici Sorunları

### Q: Kaynak koda nasıl katkıda bulunabilirim?
**A:**
1. Repository'yi fork edin
2. Feature branch oluşturun
3. Değişikliklerinizi yapın
4. Test edin
5. Pull request gönderin

### Q: Custom model nasıl oluştururum?
**A:** [[Model Eğitimi]] sayfasına bakın:
1. 50+ kaliteli örnek toplayın
2. `create_walmart_model.py` çalıştırın
3. Model test edin
4. Production'da kullanın

### Q: API endpoint var mı?
**A:** Şu anda web UI only. Gelecek versiyonlarda REST API eklenecek.

### Q: Docker container olarak çalıştırabilir miyim?
**A:**
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "walmart.py"]
```

## 📱 Platform Desteği

### Q: Windows'ta çalışır mı?
**A:** Evet, tüm Windows 10+ versiyonlarında test edilmiştir.

### Q: macOS M1/M2 chip desteği var mı?
**A:** Evet, Ollama ARM64 desteği ile optimize edilmiştir.

### Q: Linux dağıtımları?
**A:** Ubuntu 18.04+, CentOS 7+, Debian 10+ desteklenir.

### Q: Mobile browser'da çalışır mı?
**A:** Evet, responsive design ile mobile-friendly'dir.

## 💡 İpuçları ve Püf Noktaları

### Q: En iyi sonuçları nasıl alırım?
**A:**
1. **Detaylı input**: Tüm önemli özellikleri yazın
2. **Consistent format**: Benzer ürünler için benzer format
3. **Multiple attempts**: Farklı sonuçlar için tekrar deneyin
4. **Quality model**: Kritik projeler için GPT-4 kullanın

### Q: Toplu içerik üretimi için en iyi strateji?
**A:**
1. **Template hazırlayın**: Benzer ürünler için şablon
2. **Batch processing**: 10-20 ürünlük gruplar halinde
3. **Quality control**: Her 10 üründe bir kontrol edin
4. **Version control**: Değişiklikleri track edin

### Q: SEO optimizasyonu için öneriler?
**A:**
- **Keywords**: Ürün adı, marka, kategori
- **Long-tail**: "iPhone 15 Pro Max 256GB mavi"
- **Local SEO**: "İstanbul teslimat" gibi
- **Semantic**: İlgili kelimeler ekleyin

---

## 🆘 Hala Sorun mu Var?

### Destek Kanalları
1. **GitHub Issues**: Teknik problemler
2. **Wiki Sayfaları**: Detaylı rehberler
3. **Community Forum**: Kullanıcı deneyimleri
4. **Developer Chat**: Real-time destek

### Hızlı Tanılama
```bash
# System check
python --version
pip list | grep streamlit
ollama list

# Connection test
curl http://localhost:11434/api/version
curl -I https://api.openai.com/v1/models

# App test
streamlit hello
```

### Log Kontrolü
```bash
# Streamlit logs
streamlit run walmart.py --logger.level debug

# Ollama logs
ollama logs

# System logs
tail -f /var/log/system.log  # macOS
journalctl -f               # Linux
```

---

*❓ SSS versiyon: 2.5 | 📅 Son güncelleme: 14 Ağustos 2025 | 🔄 Güncelleme sıklığı: Haftalık | 📞 Yeni soru eklemek için: GitHub Issues*
