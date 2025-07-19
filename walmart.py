import streamlit as st
import openai
import os
import json
import requests
from datetime import datetime
import pandas as pd

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Walmart Ürün Açıklaması Üreteci",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bootstrap CSS
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
""", unsafe_allow_html=True)

# Ana header
st.markdown("""
<div class="container-fluid bg-primary text-white py-5 mb-4">
    <div class="container text-center">
        <h1 class="display-4 fw-bold mb-3">
            🛒 Walmart Ürün Açıklaması Üreteci
        </h1>
        <p class="lead">AI ile profesyonel ürün içerikleri oluşturun</p>
        <div class="row justify-content-center mt-4">
            <div class="col-md-3">
                <div class="card bg-light border-0 h-100">
                    <div class="card-body text-primary text-center">
                        <h5 class="card-title">🤖 AI Powered</h5>
                        <h2 class="text-primary">99%</h2>
                        <small class="text-muted">Doğruluk Oranı</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card bg-light border-0 h-100">
                    <div class="card-body text-success text-center">
                        <h5 class="card-title">🎯 SEO Optimized</h5>
                        <h2 class="text-success">100%</h2>
                        <small class="text-muted">Uyumluluk</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card bg-light border-0 h-100">
                    <div class="card-body text-warning text-center">
                        <h5 class="card-title">⚡ Hızlı Üretim</h5>
                        <h2 class="text-warning">10s</h2>
                        <small class="text-muted">Ortalama Süre</small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar with Bootstrap design
st.sidebar.markdown("""
<div class="card bg-primary text-white mb-3">
    <div class="card-body text-center">
        <h4 class="card-title mb-3">🔧 Ayarlar</h4>
    </div>
</div>
""", unsafe_allow_html=True)

# Model selection with enhanced styling
selected_model = st.sidebar.selectbox(
    "🤖 AI Model Seçin:",
    ["OpenAI ChatGPT", "Ollama (Yerel - Ücretsiz)"],
    index=1,  # Ollama'yı varsayılan yap
    help="Kullanmak istediğiniz AI modelini seçin - Ollama tamamen ücretsiz!"
)

# API Key section
st.sidebar.markdown("""
<div class="card bg-light mb-3">
    <div class="card-body">
        <h5 class="card-title text-primary">🔑 API Anahtarı</h5>
        <p class="card-text text-muted small">Güvenli ve şifreli bağlantı</p>
    </div>
</div>
""", unsafe_allow_html=True)

if selected_model == "OpenAI ChatGPT":
    api_key = st.sidebar.text_input(
        "🔍 OpenAI API Key:",
        type="password",
        help="OpenAI Platform'dan API anahtarınızı alın"
    )
    
    if api_key:
        st.sidebar.markdown("""
        <div class="alert alert-success" role="alert">
            <strong>✅ OpenAI ChatGPT hazır!</strong>
        </div>
        """, unsafe_allow_html=True)

elif selected_model == "Ollama (Yerel - Ücretsiz)":
    st.sidebar.markdown("""
    <div class="alert alert-success" role="alert">
        <strong>✅ Ollama Hazır!</strong> (Tamamen Ücretsiz)<br>
        <small>🏠 Yerel sunucunuzda çalışıyor</small>
    </div>
    """, unsafe_allow_html=True)
    
    ollama_model = st.sidebar.selectbox(
        "🦙 Ollama Model:",
        ["llama3.1:8b", "walmart-gpt", "llama3.1:70b", "mistral:7b", "codellama:7b", "qwen2.5:7b"],
        index=0,
        help="Kullanılacak Ollama modelini seçin - walmart-gpt özel eğitilmiş model"
    )
    
    # Model durumunu kontrol et
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            
            if ollama_model in model_names:
                # Model bilgisini bul
                model_info = next((m for m in models if m["name"] == ollama_model), None)
                model_size = model_info.get('size', 'N/A') if model_info else 'N/A'
                
                # Özel Walmart modeli kontrolü
                if ollama_model == "walmart-gpt":
                    st.sidebar.markdown(f"""
                    <div class="alert alert-success" role="alert">
                        <strong>🎯 Walmart-GPT Hazır!</strong> (Özel Model)<br>
                        <small>🏷️ Walmart için fine-tuned edilmiş</small><br>
                        <small>📦 Model boyutu: ~{model_size}</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.sidebar.markdown(f"""
                    <div class="alert alert-success" role="alert">
                        <strong>🎯 {ollama_model} hazır!</strong><br>
                        <small>Model boyutu: ~{model_size}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                if ollama_model == "walmart-gpt":
                    st.sidebar.markdown(f"""
                    <div class="alert alert-warning" role="alert">
                        <strong>⚠️ Walmart-GPT henüz oluşturulmadı</strong><br>
                        <small>👆 "Walmart Modeli Oluştur" butonuna tıklayın</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.sidebar.markdown(f"""
                    <div class="alert alert-warning" role="alert">
                        <strong>⚠️ {ollama_model} yüklü değil</strong><br>
                        <small>Komutu çalıştırın: ollama pull {ollama_model}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown("""
            <div class="alert alert-danger" role="alert">
                <strong>❌ Ollama servisine bağlanamıyor</strong>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.sidebar.markdown("""
        <div class="alert alert-danger" role="alert">
            <strong>❌ Ollama çalışmıyor</strong><br>
            <small>Başlatın: brew services start ollama</small>
        </div>
        """, unsafe_allow_html=True)
    
    api_key = "ollama_local"

# Enhanced help section
st.sidebar.markdown("""
<div class="card bg-success text-white mt-4">
    <div class="card-header">
        <h5 class="mb-0">🎯 Ollama - Tamamen Ücretsiz!</h5>
    </div>
    <div class="card-body">
        <h6 class="card-title">✅ Avantajları:</h6>
        <ul class="list-unstyled">
            <li>🆓 Tamamen ücretsiz</li>
            <li>🏠 Yerel çalışır (gizlilik)</li>
            <li>⚡ Çok hızlı</li>
            <li>🔒 Veri güvenliği</li>
        </ul>
        <hr class="border-light">
        <h6 class="card-title">💸 Ücretli Alternatif:</h6>
        <a href="https://platform.openai.com/api-keys" target="_blank" class="text-light">
            📍 OpenAI API
        </a>
        <hr class="border-light">
        <small>🚀 Ollama önerilen seçenek!</small>
    </div>
</div>
""", unsafe_allow_html=True)

# Fine-tuning data collection
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="card bg-info text-white">
    <div class="card-body">
        <h6 class="card-title">🎯 Fine-Tuning Veri Toplama</h6>
        <p class="card-text small mb-0">Her başarılı içerik üretimi Walmart modeli için eğitim verisi olarak kaydedilir.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Data collection toggle
collect_data = st.sidebar.checkbox("📊 Veri Toplama", value=True, help="Kendi modelinizi eğitmek için veri toplar")
collect_data = st.sidebar.checkbox("📊 Veri Toplama", value=True, help="Kendi modelinizi eğitmek için veri toplar")

# Fine-tuning Management
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="card bg-warning text-dark">
    <div class="card-body">
        <h6 class="card-title">🔧 Model Eğitimi</h6>
        <p class="card-text small mb-0">Toplanan veriyi model eğitimi için hazırla</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Training data stats
if os.path.exists("training_data.json"):
    try:
        with open("training_data.json", "r", encoding="utf-8") as f:
            training_data = json.load(f)
        
        st.sidebar.markdown(f"""
        <div class="card bg-light">
            <div class="card-body">
                <h6 class="card-title text-success">📊 Veri İstatistikleri</h6>
                <p class="card-text small">
                    • Toplam örnek: <strong>{len(training_data)}</strong><br>
                    • En fazla kullanılan model: <strong>{max(set([item['model_used'] for item in training_data]), key=[item['model_used'] for item in training_data].count) if training_data else 'Yok'}</strong>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Export buttons bölümünü geçici olarak kaldırıyoruz
        # Model eğitimi butonları ekleyelim
        st.sidebar.markdown("### 🏋️ Model Eğitimi")
        
        col_train1, col_train2 = st.sidebar.columns(2)
        
        with col_train1:
            if st.button("🔧 Walmart Modeli Oluştur", help="Training data ile özel Walmart modeli oluştur"):
                with st.spinner("Walmart modeli oluşturuluyor..."):
                    # Model oluşturma scripti çalıştır
                    import subprocess
                    result = subprocess.run(
                        ["python3", "create_walmart_model.py"],
                        cwd="/Users/mahiracan/Desktop/walmart_project_last",
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        st.sidebar.success("✅ Walmart modeli oluşturuldu!")
                        st.sidebar.info("🔄 Sayfayı yenileyin ve 'walmart-gpt' modelini seçin")
                    else:
                        st.sidebar.error(f"❌ Hata: {result.stderr}")
        
        with col_train2:
            if st.button("📊 Export JSONL", help="OpenAI fine-tuning formatında export et"):
                export_file = export_training_data_for_finetuning("jsonl")
                if export_file:
                    st.sidebar.success(f"✅ {export_file} oluşturuldu!")
                    
                    # Download link oluştur
                    with open(export_file, "r", encoding="utf-8") as f:
                        data = f.read()
                    
                    st.sidebar.download_button(
                        "💾 JSONL İndir",
                        data=data,
                        file_name=export_file,
                        mime="application/jsonl",
                        help="OpenAI fine-tuning için kullanın"
                    )
        
        # Training data clear button
        if st.sidebar.button("🗑️ Veriyi Temizle", help="Tüm training data'yı sil"):
            if os.path.exists("training_data.json"):
                os.remove("training_data.json")
                st.sidebar.success("✅ Training data temizlendi!")
                st.rerun()
    except Exception as e:
        st.sidebar.error(f"Veri okuma hatası: {str(e)}")
else:
    st.sidebar.markdown("""
    <div style="background: #f5f5f5; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <p style="color: #666; font-size: 0.9rem; margin: 0;">
            Henüz training data yok. İçerik üretmeye başlayın!
        </p>
    </div>
    """, unsafe_allow_html=True)

# AI Model Functions
def call_ollama_api(prompt, model="llama3.1:8b"):
    """Ollama API çağrısı - Geliştirilmiş versiyon"""
    try:
        # Model'e göre parametreleri optimize et
        if model == "walmart-gpt":
            options = {
                "temperature": 0.3,  # Daha tutarlı sonuçlar için düşük
                "num_ctx": 4096,
                "top_k": 20,
                "top_p": 0.8,
                "repeat_penalty": 1.2,
                "num_predict": 1000  # Daha uzun yanıtlar için
            }
        else:
            options = {
                "temperature": 0.5,  # Daha düşük temperature
                "num_ctx": 4096,
                "top_k": 30,
                "top_p": 0.85,
                "repeat_penalty": 1.15,
                "num_predict": 1000
            }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": options
            },
            timeout=180  # Daha uzun timeout
        )
        
        if response.status_code == 200:
            result = response.json()["response"]
            
            # Debug için yanıt bilgileri
            st.info(f"✅ Ollama yanıtı alındı ({len(result)} karakter)")
            
            return result
        else:
            st.error(f"Ollama API hatası: {response.status_code}")
            if response.text:
                st.code(response.text)
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Ollama servisine bağlanamıyor!")
        st.info("🔧 Çözüm: `brew services start ollama` komutu ile Ollama'yı başlatın")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Ollama yanıt verme süresi aşıldı")
        st.info("💡 Daha küçük bir model deneyin veya prompt'u kısaltın")
        return None
    except Exception as e:
        st.error(f"Ollama bağlantı hatası: {str(e)}")
        return None

def get_ai_response(prompt, selected_model, api_key):
    """AI modellerinden yanıt al - Ollama odaklı"""
    if selected_model == "OpenAI ChatGPT":
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional content writer for Walmart.com product listings."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"OpenAI ChatGPT hatası: {str(e)}")
            return None
    elif selected_model == "Ollama (Yerel - Ücretsiz)":
        return call_ollama_api(prompt, ollama_model)
    else:
        st.error("Desteklenmeyen model")
        return None

def export_training_data_for_finetuning(format_type="jsonl"):
    """Training data'yı fine-tuning formatına çevir"""
    try:
        if not os.path.exists("training_data.json"):
            st.warning("Henüz training data yok!")
            return None
            
        with open("training_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if format_type == "jsonl":
            # OpenAI fine-tuning formatı
            formatted_data = []
            for item in data:
                # System message + user input + assistant response formatı
                formatted_item = {
                    "messages": [
                        {"role": "system", "content": "Sen Walmart.com için profesyonel ürün açıklaması yazan bir içerik uzmanısın. Türkçe olarak etkili, SEO dostu ve satış odaklı ürün açıklamaları oluşturuyorsun."},
                        {"role": "user", "content": f"Bu ürün için Walmart.com'a uygun bir ürün açıklaması oluştur:\n\nÜrün Adı: {item['input']['product_name']}\nÜrün Özellikleri: {item['input']['product_features']}"},
                        {"role": "assistant", "content": f"Başlık: {item['output']['title']}\n\nAnahtar Özellikler: {item['output']['key_features']}\n\nÜrün Açıklaması: {item['output']['description']}"}
                    ]
                }
                formatted_data.append(formatted_item)
            
            # JSONL formatında kaydet
            with open("walmart_finetuning_data.jsonl", "w", encoding="utf-8") as f:
                for item in formatted_data:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
                    
            return "walmart_finetuning_data.jsonl"
            
        elif format_type == "csv":
            # CSV formatında kaydet
            csv_data = []
            for item in data:
                csv_row = {
                    "timestamp": item["timestamp"],
                    "product_name": item["input"]["product_name"],
                    "product_features": item["input"]["product_features"],
                    "title": item["output"]["title"],
                    "key_features": item["output"]["key_features"],
                    "description": item["output"]["description"],
                    "model_used": item["model_used"]
                }
                csv_data.append(csv_row)
            
            df = pd.DataFrame(csv_data)
            df.to_csv("walmart_training_data.csv", index=False, encoding="utf-8")
            return "walmart_training_data.csv"
            
    except Exception as e:
        st.error(f"Export işlemi sırasında hata: {str(e)}")
        return None

def save_training_data(product_name, product_features, title, key_features, description, model_used):
    """Fine-tuning için veri kaydet"""
    if not collect_data:
        return
    
    training_sample = {
        "timestamp": datetime.now().isoformat(),
        "input": {
            "product_name": product_name,
            "product_features": product_features
        },
        "output": {
            "title": title,
            "key_features": key_features,
            "description": description
        },
        "model_used": model_used,
        "prompt_template": "walmart_product_content"
    }
    
    # JSON dosyasına kaydet
    try:
        # Dosya varsa oku, yoksa yeni liste oluştur
        try:
            with open("training_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        
        # Yeni veriyi ekle
        data.append(training_sample)
        
        # Dosyaya yaz
        with open("training_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        # Kullanıcıya bilgi ver
        st.success(f"✅ Training data kaydedildi! Toplam {len(data)} örnek")
        
    except Exception as e:
        st.error(f"Training data kaydedilirken hata: {str(e)}")

# Ana içerik
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div class="card h-100">
        <div class="card-header bg-primary text-white text-center">
            <h5 class="mb-0">📝 Ürün Bilgileri</h5>
        </div>
        <div class="card-body">
    """, unsafe_allow_html=True)
    
    # Enhanced form with Bootstrap
    with st.form("product_form"):
        st.markdown("""
        <div class="mb-4">
            <h6 class="text-primary mb-2">🏷️ Ürün Adı</h6>
            <p class="text-muted small mb-3">Ürününüzün tam adını girin</p>
        </div>
        """, unsafe_allow_html=True)
        
        product_name = st.text_input(
            "Ürün adını girin:",
            placeholder="Örn: Sony WH-1000XM4 Wireless Bluetooth Headphones",
            label_visibility="collapsed"
        )
        
        st.markdown("""
        <div class="mb-4 mt-4">
            <h6 class="text-primary mb-2">🔧 Ürün Özellikleri</h6>
            <p class="text-muted small mb-3">Detaylı özellikler ve faydaları yazın</p>
        </div>
        """, unsafe_allow_html=True)
        
        product_features = st.text_area(
            "Ürün özelliklerini girin:",
            placeholder="Ürününüzün tüm özelliklerini detaylı bir şekilde yazın...\n\n✅ Marka ve model bilgisi\n✅ Teknik özellikler\n✅ Avantajlar ve faydalar\n✅ Hedef kitle\n✅ Kullanım alanları\n✅ Boyut ve ağırlık\n✅ Garanti bilgisi",
            height=250,
            help="Minimum 100 karakter yazmanızı öneririz",
            label_visibility="collapsed"
        )
        
        # Enhanced submit button
        st.markdown('<div class="mt-4"></div>', unsafe_allow_html=True)
        submit_button = st.form_submit_button(
            "🚀 Profesyonel İçerik Oluştur", 
            use_container_width=True
        )
    
    st.markdown('</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card h-100">
        <div class="card-header bg-success text-white text-center">
            <h5 class="mb-0">✨ Oluşturulan İçerik</h5>
        </div>
        <div class="card-body">
    """, unsafe_allow_html=True)
    
    if submit_button and api_key and product_name and product_features:
        # Bootstrap loading spinner
        st.markdown("""
        <div class="text-center my-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-primary mt-3">🤖 AI içerik oluşturuyor... Lütfen bekleyin</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Progress simulation
            progress_bar = st.progress(0)
            
            # Simulate progress steps
            import time
            for i in range(0, 101, 20):
                progress_bar.progress(i)
                time.sleep(0.3)
            
            # Geliştirilmiş prompt oluşturma
            prompt = f"""You are a professional content writer for Walmart.com. Create product content in the exact format specified below.

Product Name: {product_name}
Product Features: {product_features}

Create content using this EXACT format:

TITLE: [Write a compelling, SEO-optimized product title for Walmart.com. Include brand, product name, and key selling points. Maximum 150 characters.]

KEY_FEATURES: [List 5-8 key product features. Each feature should be on a new line starting with "•". Focus on benefits that matter to customers.]

DESCRIPTION: [Write a comprehensive product description for Walmart.com. Minimum 100 words. Include benefits, use cases, and why customers should buy this product. Use professional, persuasive language.]

Example format:
TITLE: Sony WH-1000XM4 Wireless Bluetooth Headphones with Noise Cancellation, 30H Battery & Quick Charge

KEY_FEATURES: • Industry-leading Active Noise Cancellation technology
• 30-hour battery life with quick charge capability
• Premium sound quality with LDAC codec support
• Touch sensor controls and voice assistant compatibility
• Comfortable over-ear design perfect for travel

DESCRIPTION: Experience exceptional audio quality with these premium wireless headphones featuring Sony's industry-leading noise cancellation technology. The 30-hour battery life ensures all-day listening, while quick charge provides 5 hours of playback with just 10 minutes of charging. Advanced LDAC codec delivers superior sound quality, and intuitive touch controls make operation effortless. Compatible with voice assistants and featuring a comfortable over-ear design, these headphones are perfect for travel, work, or everyday listening. The foldable design and included carrying case make them ideal for on-the-go use.

Now create content for the product above using this exact format. Make sure to include all three sections: TITLE, KEY_FEATURES, and DESCRIPTION."""
            
            # AI'dan yanıt al
            content = get_ai_response(prompt, selected_model, api_key)
            
            if content is None:
                st.error("AI model yanıt veremiyor. Lütfen ayarları kontrol edin.")
                st.stop()
            
            # Debug için ham yanıtı göster (geliştirme aşamasında)
            with st.expander("🔍 Debug: Ham AI Yanıtı", expanded=False):
                st.code(content, language="text")
                st.info(f"Yanıt uzunluğu: {len(content)} karakter")
                st.info(f"Kullanılan model: {selected_model}")
                if selected_model == "Ollama (Yerel - Ücretsiz)":
                    st.info(f"Ollama modeli: {ollama_model}")
            
            # İçeriği parse et - Geliştirilmiş versiyon
            title = ""
            key_features = ""
            description = ""
            
            # Yanıtı satırlara böl
            lines = content.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                
                # Boş satırları atla
                if not line:
                    continue
                
                # Bölüm başlıklarını kontrol et
                if line.startswith('TITLE:'):
                    current_section = 'title'
                    title = line.replace('TITLE:', '').strip()
                    continue
                elif line.startswith('KEY_FEATURES:'):
                    current_section = 'key_features'
                    # Eğer aynı satırda içerik varsa al
                    if len(line.replace('KEY_FEATURES:', '').strip()) > 0:
                        key_features = line.replace('KEY_FEATURES:', '').strip()
                    continue
                elif line.startswith('DESCRIPTION:'):
                    current_section = 'description'
                    # Eğer aynı satırda içerik varsa al
                    if len(line.replace('DESCRIPTION:', '').strip()) > 0:
                        description = line.replace('DESCRIPTION:', '').strip()
                    continue
                
                # İçeriği ilgili bölüme ekle
                if current_section == 'title' and not title:
                    title = line
                elif current_section == 'key_features':
                    if key_features:
                        key_features += '\n' + line
                    else:
                        key_features = line
                elif current_section == 'description':
                    if description:
                        description += ' ' + line
                    else:
                        description = line
            
            # Eğer parse edilemiyorsa alternatif yöntem dene
            if not title or not key_features or not description:
                # Daha basit parse yöntemi
                sections = content.split('\n\n')
                for section in sections:
                    if 'TITLE:' in section and not title:
                        title = section.split('TITLE:')[-1].strip()
                    elif 'KEY_FEATURES:' in section and not key_features:
                        key_features = section.split('KEY_FEATURES:')[-1].strip()
                    elif 'DESCRIPTION:' in section and not description:
                        description = section.split('DESCRIPTION:')[-1].strip()
            
            # Son kontrol - eğer hala boşsa uyarı ver ve alternatif çözüm sun
            if not title:
                title = "Başlık oluşturulamadı - AI yanıtını kontrol edin"
                st.warning("⚠️ Başlık parse edilemedi. Ham yanıtı kontrol edin.")
            if not key_features:
                key_features = "• Özellikler oluşturulamadı\n• AI yanıtını kontrol edin"
                st.warning("⚠️ Özellikler parse edilemedi. Ham yanıtı kontrol edin.")
            if not description:
                description = "Ürün açıklaması oluşturulamadı. AI yanıtını kontrol edin."
                st.warning("⚠️ Açıklama parse edilemedi. Ham yanıtı kontrol edin.")
            
            # Başarısız parse durumunda alternatif çözüm öner
            if (title == "Başlık oluşturulamadı - AI yanıtını kontrol edin" or 
                "oluşturulamadı" in key_features or 
                "oluşturulamadı" in description):
                
                st.error("🚨 İçerik parse edilemedi!")
                st.info("💡 Çözüm önerileri:")
                st.info("1. Farklı bir Ollama modeli deneyin (örn: llama3.1:70b)")
                st.info("2. OpenAI ChatGPT'yi deneyin")
                st.info("3. Ürün özelliklerini daha kısa ve net yazın")
                
                # Manuel düzenleme seçeneği sun
                st.markdown("### ✏️ Manuel Düzenleme")
                manual_title = st.text_input("Başlık:", value=title if title != "Başlık oluşturulamadı - AI yanıtını kontrol edin" else "")
                manual_features = st.text_area("Özellikler:", value=key_features if "oluşturulamadı" not in key_features else "", height=100)
                manual_description = st.text_area("Açıklama:", value=description if "oluşturulamadı" not in description else "", height=150)
                
                if st.button("💾 Manuel İçeriği Kaydet"):
                    if manual_title and manual_features and manual_description:
                        title = manual_title
                        key_features = manual_features
                        description = manual_description
                        save_training_data(product_name, product_features, title, key_features, description, f"{selected_model} (Manuel)")
                        st.success("✅ Manuel içerik kaydedildi!")
                        st.rerun()
            
            # Clear loading
            st.markdown("""
            <script>
                document.getElementById('loading-container').style.display = 'none';
            </script>
            """, unsafe_allow_html=True)
            
            # Success animation
            st.balloons()
            
            # Training data'yı kaydet
            save_training_data(product_name, product_features, title, key_features, description, selected_model)
            
            # Success message with Bootstrap
            st.markdown("""
            <div class="alert alert-success text-center" role="alert">
                <h4 class="alert-heading">🎉 İçerik Başarıyla Oluşturuldu!</h4>
                <p class="mb-0">AI tarafından Walmart standartlarına uygun profesyonel içerik hazırlandı</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced results display with Bootstrap
            st.markdown("""
            <div class="card border-primary mb-3">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0">📍 Ürün Başlığı</h6>
                </div>
                <div class="card-body">
                    <p class="card-text">{}</p>
                    <small class="text-muted">📏 {} karakter</small>
                </div>
            </div>
            """.format(title if title else "Başlık oluşturulamadı", len(title) if title else 0), unsafe_allow_html=True)
            
            # Key Features with Bootstrap
            st.markdown("""
            <div class="card border-warning mb-3">
                <div class="card-header bg-warning text-dark">
                    <h6 class="mb-0">⭐ Önemli Özellikler</h6>
                </div>
                <div class="card-body">
                    <pre class="card-text mb-0" style="white-space: pre-line; font-family: inherit;">{}</pre>
                    <small class="text-muted">📋 {} özellik</small>
                </div>
            </div>
            """.format(key_features if key_features else "Özellikler oluşturulamadı", len(key_features.split('\n')) if key_features else 0), unsafe_allow_html=True)
            
            # Description with Bootstrap
            st.markdown("""
            <div class="card border-success mb-3">
                <div class="card-header bg-success text-white">
                    <h6 class="mb-0">📄 Detaylı Açıklama</h6>
                </div>
                <div class="card-body">
                    <p class="card-text text-justify">{}</p>
                    <small class="text-muted">📝 {} kelime</small>
                </div>
            </div>
            """.format(description if description else "Açıklama oluşturulamadı", len(description.split()) if description else 0), unsafe_allow_html=True)
            
            # Bootstrap action buttons
            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("📋 Tümünü Görüntüle", use_container_width=True, type="secondary"):
                    full_content = f"TITLE:\n{title}\n\nKEY FEATURES:\n{key_features}\n\nDESCRIPTION:\n{description}"
                    st.markdown("""
                    <div class="card bg-light mt-3">
                        <div class="card-header">
                            <h6 class="mb-0">📄 Tam İçerik</h6>
                        </div>
                        <div class="card-body">
                            <pre class="bg-white p-3 rounded" style="overflow-x: auto; font-size: 0.9rem;">{}</pre>
                        </div>
                    </div>
                    """.format(full_content), unsafe_allow_html=True)
            
            with col_b:
                if title:
                    st.download_button(
                        "💾 İndir (.txt)",
                        data=f"TITLE:\n{title}\n\nKEY FEATURES:\n{key_features}\n\nDESCRIPTION:\n{description}",
                        file_name=f"{product_name.replace(' ', '_')}_walmart_content.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            
            with col_c:
                if st.button("🔄 Yeniden Oluştur", use_container_width=True, type="primary"):
                    st.rerun()
            
        except Exception as e:
            st.markdown(f"""
            <div class="alert alert-danger" role="alert">
                <h4 class="alert-heading">❌ Hata Oluştu!</h4>
                <p class="mb-0">{str(e)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if selected_model == "OpenAI ChatGPT":
                st.markdown("""
                <div class="alert alert-info" role="alert">
                    💡 OpenAI API anahtarınızı kontrol edin ve tekrar deneyin.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert alert-info" role="alert">
                    💡 Ollama servisinin çalıştığından emin olun ve tekrar deneyin.
                </div>
                """, unsafe_allow_html=True)
    
    elif submit_button:
        # Enhanced error messages with Bootstrap
        if not api_key:
            st.markdown(f"""
            <div class="alert alert-warning" role="alert">
                <h4 class="alert-heading">⚠️ API Anahtarı Gerekli</h4>
                <p class="mb-0">Lütfen {selected_model} API anahtarınızı sol panelden girin.</p>
            </div>
            """, unsafe_allow_html=True)
        elif not product_name:
            st.markdown("""
            <div class="alert alert-warning" role="alert">
                <h4 class="alert-heading">⚠️ Ürün Adı Gerekli</h4>
                <p class="mb-0">Lütfen ürün adını girin.</p>
            </div>
            """, unsafe_allow_html=True)
        elif not product_features:
            st.markdown("""
            <div class="alert alert-warning" role="alert">
                <h4 class="alert-heading">⚠️ Ürün Özellikleri Gerekli</h4>
                <p class="mb-0">Lütfen ürün özelliklerini detaylı bir şekilde girin.</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Welcome screen with Bootstrap
        st.markdown("""
        <div class="card bg-primary text-white mb-4">
            <div class="card-body text-center">
                <h4 class="card-title">🚀 Başlamaya Hazır!</h4>
                <p class="card-text">Sol panelden API anahtarınızı girin, ürün bilgilerini doldurun ve profesyonel içerik oluşturun.</p>
                
                <div class="row mt-4">
                    <div class="col-md-4">
                        <div class="card bg-light text-dark h-100">
                            <div class="card-body text-center">
                                <h6 class="card-title">1️⃣ API Anahtarı</h6>
                                <p class="card-text small">Sidebar'dan girin</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card bg-light text-dark h-100">
                            <div class="card-body text-center">
                                <h6 class="card-title">2️⃣ Ürün Bilgisi</h6>
                                <p class="card-text small">Detaylı yazın</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card bg-light text-dark h-100">
                            <div class="card-body text-center">
                                <h6 class="card-title">3️⃣ İçerik Oluştur</h6>
                                <p class="card-text small">Butona tıklayın</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bootstrap example display
        st.markdown("""
        <div class="card bg-light">
            <div class="card-header">
                <h6 class="mb-0">📋 Örnek Çıktı Formatı</h6>
            </div>
            <div class="card-body">
                <div class="card border-primary mb-3">
                    <div class="card-header bg-primary text-white">
                        <small><strong>TITLE:</strong></small>
                    </div>
                    <div class="card-body">
                        <p class="card-text small">Sony WH-1000XM4 Wireless Bluetooth Headphones with Active Noise Cancellation</p>
                    </div>
                </div>
                
                <div class="card border-warning mb-3">
                    <div class="card-header bg-warning text-dark">
                        <small><strong>KEY FEATURES:</strong></small>
                    </div>
                    <div class="card-body">
                        <p class="card-text small">• Industry-leading active noise cancellation<br>
                        • 30-hour battery life with quick charge<br>
                        • Premium sound quality with LDAC codec<br>
                        • Touch controls and voice assistant support</p>
                    </div>
                </div>
                
                <div class="card border-success">
                    <div class="card-header bg-success text-white">
                        <small><strong>DESCRIPTION:</strong></small>
                    </div>
                    <div class="card-body">
                        <p class="card-text small">The Sony WH-1000XM4 wireless headphones deliver exceptional audio quality with industry-leading active noise cancellation technology...</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# Bootstrap Footer
st.markdown("---")
st.markdown("""
<div class="container-fluid bg-primary text-white py-5 mt-5">
    <div class="container">
        <div class="text-center mb-4">
            <h3 class="mb-3">🛒 Walmart İçerik Üreteci</h3>
        </div>
        
        <div class="row">
            <div class="col-md-4">
                <div class="card bg-dark text-white h-100">
                    <div class="card-body text-center">
                        <h5 class="card-title">🤖 AI Teknolojisi</h5>
                        <p class="card-text">{0}</p>
                        <small class="badge bg-light text-dark">Güvenilir & Hızlı</small>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card bg-dark text-white h-100">
                    <div class="card-body text-center">
                        <h5 class="card-title">🎯 Walmart Standartları</h5>
                        <p class="card-text">SEO Uyumlu İçerik</p>
                        <small class="badge bg-success">%100 Uyumlu</small>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card bg-dark text-white h-100">
                    <div class="card-body text-center">
                        <h5 class="card-title">⚡ Profesyonel Sonuçlar</h5>
                        <p class="card-text">Anında İçerik Üretimi</p>
                        <small class="badge bg-warning text-dark">Kalite Garantisi</small>
                    </div>
                </div>
            </div>
        </div>
        
        <hr class="border-light my-4">
        
        <div class="text-center">
            <p class="mb-2">
                🔧 <strong>Geliştirici Notu:</strong> Bu araç <strong>{0}</strong> kullanarak Walmart için optimize edilmiş ürün içeriği oluşturur.
            </p>
            <p class="mb-0">
                <small>© 2025 - Walmart İçerik Üreteci | Güvenli & Hızlı AI Çözümü</small>
            </p>
        </div>
    </div>
</div>
""".format(selected_model), unsafe_allow_html=True)