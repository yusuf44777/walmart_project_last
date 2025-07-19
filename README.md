# 🛒 Walmart Ürün Açıklaması Üreteci

Bu uygulama, Walmart.com için AI destekli ürün açıklaması oluşturan modern bir Streamlit uygulamasıdır.

## ✨ Özellikler

- 🤖 **Ollama (Ücretsiz & Yerel)** ve OpenAI ChatGPT desteği
- 🎯 **Walmart-GPT**: Özel fine-tuned edilmiş model
- 📊 **Fine-tuning veri toplama** ve model eğitimi
- 🏷️ Walmart standartlarına uygun içerik üretimi
- 🔍 SEO uyumlu başlık ve açıklama oluşturma
- 💾 Export özelliği (TXT, JSONL formatları)
- 🎨 Modern ve responsive kullanıcı arayüzü

## 🚀 Kurulum

### Gereksinimler
- Python 3.11+
- Ollama (önerilen - ücretsiz)

### 1. Repository'yi klonlayın
```bash
git clone https://github.com/yusuf44777/walmart_project_last.git
cd walmart_project_last
```

### 2. Sanal ortam oluşturun (önerilen)
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# veya
venv\Scripts\activate     # Windows
```

### 3. Gerekli paketleri yükleyin
```bash
pip install -r requirements.txt
```

### 4. Ollama'yı kurun (ücretsiz seçenek)
```bash
# macOS
brew install ollama

# veya manuel kurulum: https://ollama.ai/download
```

### 5. Ollama'yı başlatın ve model indirin
```bash
ollama serve
ollama pull llama3.1:8b
```

### 6. Uygulamayı çalıştırın
```bash
streamlit run walmart.py
```

## Kullanım

1. Sidebar'dan AI modelinizi seçin (Google Gemini veya OpenAI ChatGPT)
2. İlgili API anahtarınızı girin
3. Ürün adı ve özelliklerini doldurur
4. "Açıklama Oluştur" butonuna tıklayın

## Deploy

Bu uygulama Streamlit Cloud, Heroku veya diğer bulut platformlarında kolayca deploy edilebilir.

### Streamlit Cloud Deploy

1. GitHub'a repository'yi yükleyin
2. [Streamlit Cloud](https://streamlit.io/cloud) hesabınızla GitHub'ı bağlayın
3. Repository'yi seçin ve deploy edin

### Heroku Deploy

1. Heroku hesabınızda yeni bir app oluşturun
2. Git ile kod deposunu Heroku'ya gönderin
3. Environment variables olarak API anahtarlarını ekleyin

## Gereksinimler

- Python 3.11+
- Streamlit
- Google Generative AI
- OpenAI

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
