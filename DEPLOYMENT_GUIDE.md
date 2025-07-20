# Deployment Environment Configuration

## 🚀 Environment Detection & Configuration

Bu uygulama artık **akıllı environment detection** ile çalışıyor!

### 🏠 **Yerel Ortam (Local)**
- ✅ Ollama modelleri kullanılabilir
- ✅ OpenAI ChatGPT kullanılabilir  
- ✅ Model eğitimi yapılabilir
- ✅ Analytics çalıştırılabilir
- ✅ Tam özellik desteği

### ☁️ **Deploy Ortamı (Cloud)**
- ❌ Ollama modelleri kullanılamaz
- ✅ OpenAI ChatGPT kullanılabilir
- ❌ Model eğitimi yapılamaz
- ❌ Analytics çalıştırılamaz
- ✅ Veri export yapılabilir

---

## 🔧 Deployment Rehberi

### **1. Streamlit Cloud**
```bash
# secrets.toml dosyasında
[secrets]
OPENAI_API_KEY = "your-api-key-here"
```

### **2. Heroku**
```bash
# Environment variables
heroku config:set OPENAI_API_KEY=your-api-key-here
heroku config:set HEROKU_APP_NAME=your-app-name
```

### **3. Railway**
```bash
# Environment variables
OPENAI_API_KEY=your-api-key-here
RAILWAY_ENVIRONMENT=production
```

### **4. Docker**
```dockerfile
ENV OPENAI_API_KEY=your-api-key-here
ENV STREAMLIT_CLOUD_ENV=true
```

---

## 🛠️ Sorun Giderme

### **Ollama "Çalışmıyor" Hatası**
- **Yerel ortamda**: `brew services start ollama` çalıştırın
- **Deploy ortamında**: Bu normal, OpenAI kullanın

### **API Key Hatası**  
- OpenAI API anahtarınızı environment variables'a ekleyin
- Streamlit Cloud'da secrets.toml kullanın

### **Model Eğitimi Çalışmıyor**
- Model eğitimi sadece yerel ortamda çalışır
- Deploy edilmiş uygulamada bu özellik devre dışıdır

---

## 💡 İpuçları

1. **Development**: Yerel ortamda Ollama + OpenAI
2. **Production**: Deploy ortamında sadece OpenAI
3. **Data Collection**: Her iki ortamda da çalışır
4. **Export**: JSONL/CSV export her yerde kullanılabilir

Bu şekilde uygulamanız hem yerel hem de deploy edilmiş ortamda sorunsuz çalışır! 🎉
