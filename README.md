# Walmart Ürün Açıklaması Üreteci

Bu uygulama, Walmart.com için AI destekli ürün açıklaması oluşturan bir Streamlit uygulamasıdır.

## Özellikler

- Google Gemini AI ve OpenAI ChatGPT desteği
- Walmart standartlarına uygun içerik üretimi
- SEO uyumlu başlık ve açıklama oluşturma
- Kullanıcı dostu arayüz

## Kurulum

1. Repository'yi klonlayın
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Uygulamayı çalıştırın:
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
