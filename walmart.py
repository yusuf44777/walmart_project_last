import streamlit as st
import openai
import os
import json
import requests
from datetime import datetime
import pandas as pd

# Environment detection
def get_ollama_base_url():
    """Ollama base URL'ini environment'a göre belirle"""
    # Heroku, Railway, Streamlit Cloud için environment variables kontrol et
    if os.environ.get('STREAMLIT_CLOUD_ENV'):
        # Cloud Ollama URL varsa kullan
        cloud_url = os.environ.get('CLOUD_OLLAMA_URL')
        if cloud_url:
            return cloud_url
        return None  # Streamlit Cloud'da Ollama yok
    elif os.environ.get('HEROKU_APP_NAME'):
        # Heroku'da cloud Ollama URL kontrol et
        cloud_url = os.environ.get('CLOUD_OLLAMA_URL')
        if cloud_url:
            return cloud_url
        return None  # Heroku'da Ollama yok
    elif os.environ.get('RAILWAY_ENVIRONMENT'):
        # Railway'de cloud Ollama URL kontrol et
        cloud_url = os.environ.get('CLOUD_OLLAMA_URL')
        if cloud_url:
            return cloud_url
        return None  # Railway'de Ollama yok
    else:
        # Local environment
        return "http://localhost:11434"

# Global Ollama base URL
OLLAMA_BASE_URL = get_ollama_base_url()

def is_local_environment():
    """Local environment kontrolü - İyileştirilmiş"""
    # Environment variable kontrolü
    if (os.environ.get('STREAMLIT_CLOUD_ENV') or 
        os.environ.get('HEROKU_APP_NAME') or 
        os.environ.get('RAILWAY_ENVIRONMENT')):
        return False
    
    # Ollama URL kontrolü
    ollama_url = get_ollama_base_url()
    if ollama_url and "localhost" in ollama_url:
        return True
    
    # Son kontrol - local Ollama servisi çalışıyor mu?
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=1)
        return response.status_code == 200
    except:
        return False

# Export fonksiyonu
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
                formatted_item = {
                    "messages": [
                        {"role": "system", "content": "Sen Walmart.com için profesyonel ürün açıklaması yazan bir içerik uzmanısın."},
                        {"role": "user", "content": f"Bu ürün için Walmart.com'a uygun bir ürün açıklaması oluştur:\n\nÜrün Adı: {item['input']['product_name']}\nÜrün Özellikleri: {item['input']['product_features']}"},
                        {"role": "assistant", "content": f"Başlık: {item['output']['title']}\n\nAnahtar Özellikler: {item['output']['key_features']}\n\nÜrün Açıklaması: {item['output']['description']}"}
                    ]
                }
                formatted_data.append(formatted_item)
            
            # JSONL
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

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Walmart Ürün Açıklaması Üreteci",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sade header
st.title("🛒 Walmart Ürün Açıklaması Üreteci")
st.subheader("AI ile profesyonel ürün içerikleri oluşturun")

# Environment info
if not is_local_environment():
    st.info("ℹ️ **Deploy Ortamı**: Bu uygulama cloud'da çalışıyor.")
    st.warning("⚠️ **Not**: Yerel Ollama kullanılamaz, ancak Cloud Ollama kurabilirsiniz.")
else:
    st.success("💻 **Yerel Ortam**: Hem Ollama hem OpenAI ChatGPT kullanılabilir.")

# Sidebar başlığı
st.sidebar.title("⚙️ Ayarlar")

# Model selection
available_models = ["OpenAI ChatGPT"]

# Local Ollama kontrolü
try:
    local_test = requests.get("http://localhost:11434/api/tags", timeout=2)
    if local_test.status_code == 200:
        available_models.append("Ollama (Yerel/Cloud)")
except:
    pass

# Cloud Ollama kontrolü
if not is_local_environment() and 'cloud_ollama_url' in st.session_state and st.session_state['cloud_ollama_url']:
    if "Ollama (Yerel/Cloud)" not in available_models:
        available_models.append("Ollama (Yerel/Cloud)")

selected_model = st.sidebar.selectbox(
    "🤖 AI Model Seçin:",
    available_models,
    index=0,
    help="Kullanmak istediğiniz AI modelini seçin"
)

# API Key section
st.sidebar.subheader("🔑 API Anahtarı")

if selected_model == "OpenAI ChatGPT":
    api_key = st.sidebar.text_input(
        "OpenAI API Key:",
        type="password",
        help="OpenAI Platform'dan API anahtarınızı alın"
    )
    
    if api_key:
        st.sidebar.success("✅ OpenAI ChatGPT hazır!")

elif selected_model == "Ollama (Yerel/Cloud)":
    # Yerel Ollama kontrolü
    if is_local_environment():
        st.sidebar.success("✅ Yerel Ollama Hazır! (Tamamen Ücretsiz)")
        
        ollama_model = st.sidebar.selectbox(
            "Ollama Model:",
            ["llama3.1:8b", "walmart-gpt", "walmart-gpt-expert", "walmart-gpt-advanced", "walmart-gpt-basic", "llama3.1:70b", "mistral:7b", "codellama:7b", "qwen2.5:7b"],
            index=0,
            help="Kullanılacak Ollama modelini seçin. Walmart modelleri özel eğitilmiştir."
        )
        
        # Model durumunu kontrol et
        try:
            if OLLAMA_BASE_URL:
                response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [model["name"] for model in models]
                    
                    # Model ismini kontrol et
                    model_available = False
                    for model_name in model_names:
                        if ollama_model in model_name or model_name.startswith(ollama_model.split(':')[0]):
                            model_available = True
                            break
                    
                    if model_available:
                        if "walmart-gpt" in ollama_model:
                            if "expert" in ollama_model:
                                st.sidebar.success("🏆 Walmart-GPT Expert hazır! (Uzman Seviye)")
                            elif "advanced" in ollama_model:
                                st.sidebar.info("🎯 Walmart-GPT Advanced hazır! (Gelişmiş)")
                            elif "basic" in ollama_model:
                                st.sidebar.info("🎯 Walmart-GPT Basic hazır! (Temel)")
                            else:
                                st.sidebar.info("🎯 Walmart-GPT hazır! (Özel Model)")
                        else:
                            st.sidebar.info(f"🎯 {ollama_model} hazır!")
                    else:
                        if "walmart-gpt" in ollama_model:
                            st.sidebar.warning(f"⚠️ {ollama_model} henüz oluşturulmadı")
                            if st.sidebar.button("📥 Model İndir"):
                                with st.spinner("Model indiriliyor..."):
                                    import subprocess
                                    result = subprocess.run(["ollama", "pull", ollama_model], capture_output=True, text=True)
                                    if result.returncode == 0:
                                        st.sidebar.success("✅ Model indirildi!")
                                        st.rerun()
                                    else:
                                        st.sidebar.error("❌ Model indirilemedi")
                        else:
                            st.sidebar.warning(f"⚠️ {ollama_model} yüklü değil")
                            if st.sidebar.button("📥 Model İndir"):
                                with st.spinner("Model indiriliyor..."):
                                    import subprocess
                                    result = subprocess.run(["ollama", "pull", ollama_model], capture_output=True, text=True)
                                    if result.returncode == 0:
                                        st.sidebar.success("✅ Model indirildi!")
                                        st.rerun()
                                    else:
                                        st.sidebar.error("❌ Model indirilemedi")
                else:
                    st.sidebar.error("❌ Ollama servisine bağlanamıyor")
                    st.sidebar.info("🔧 Terminal'de çalıştırın: `brew services start ollama`")
            else:
                st.sidebar.error("❌ Ollama URL bulunamadı")
        except Exception as e:
            st.sidebar.error("❌ Ollama bağlantı hatası")
            st.sidebar.info("🔧 Terminal'de çalıştırın: `ollama serve`")
        
        api_key = "ollama_local"
    
    # Cloud Ollama kontrolü
    elif 'cloud_ollama_url' in st.session_state and st.session_state['cloud_ollama_url']:
        st.sidebar.success("✅ Cloud Ollama Hazır!")
        
        # Cloud Ollama için model seçimi
        try:
            cloud_url = st.session_state['cloud_ollama_url']
            response = requests.get(f"{cloud_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                cloud_model_names = [model["name"] for model in models]
                
                if cloud_model_names:
                    ollama_model = st.sidebar.selectbox(
                        "Cloud Ollama Model:",
                        cloud_model_names,
                        help="Cloud'daki mevcut modeller"
                    )
                    st.sidebar.info(f"🌐 Cloud'da {len(cloud_model_names)} model mevcut")
                else:
                    st.sidebar.warning("⚠️ Cloud'da model bulunamadı")
                    ollama_model = "llama3.1:8b"
            else:
                st.sidebar.error("❌ Cloud Ollama'dan model listesi alınamadı")
                ollama_model = "llama3.1:8b"
        except:
            st.sidebar.error("❌ Cloud Ollama bağlantı hatası")
            ollama_model = "llama3.1:8b"
        
        api_key = "cloud_ollama"
    
    else:
        st.sidebar.error("❌ Ollama bulunamadı!")
        st.sidebar.info("💡 Yerel ortamda Ollama başlatın veya Cloud Ollama URL'i girin")
        api_key = None

# Enhanced help section
st.sidebar.markdown("---")
if is_local_environment():
    st.sidebar.subheader("🎯 Ollama Avantajları")
    st.sidebar.info("• Tamamen ücretsiz\n• Yerel çalışır (gizlilik)\n• Çok hızlı\n• Veri güvenliği")
else:
    st.sidebar.subheader("☁️ Deploy Ortamı")
    st.sidebar.warning("Bu uygulama deploy edilmiş durumda.")
    st.sidebar.info("💡 OpenAI ChatGPT kullanın veya Cloud Ollama kurabilirsiniz.")
    
    # Cloud Ollama configuration
    st.sidebar.markdown("### 🌐 Cloud Ollama (Opsiyonel)")
    cloud_ollama_url = st.sidebar.text_input(
        "Cloud Ollama URL:",
        placeholder="https://your-cloud-ollama.com",
        help="Google Colab, RunPod veya kendi sunucunuzdaki Ollama URL'i"
    )
    
    if cloud_ollama_url:
        # Test connection
        try:
            test_response = requests.get(f"{cloud_ollama_url}/api/tags", timeout=5)
            if test_response.status_code == 200:
                st.sidebar.success("✅ Cloud Ollama bağlantısı başarılı!")
                # Update global URL for this session
                st.session_state['cloud_ollama_url'] = cloud_ollama_url
                
                # Show available models
                models = test_response.json().get("models", [])
                if models:
                    model_names = [model["name"] for model in models]
                    st.sidebar.info(f"� Mevcut modeller: {', '.join(model_names[:3])}")
            else:
                st.sidebar.error("❌ Cloud Ollama'ya bağlanamıyor")
        except Exception as e:
            st.sidebar.error(f"❌ Bağlantı hatası: {str(e)[:50]}...")
    
    st.sidebar.markdown("### 📚 Cloud Ollama Kurulum")
    with st.sidebar.expander("🚀 Nasıl Kurarım?"):
        st.write("""
        **Ücretsiz Seçenekler:**
        1. **Google Colab** (15GB RAM, GPU)
        2. **Kaggle Notebooks** (13GB RAM)
        3. **HuggingFace Spaces** (16GB RAM)
        
        **Uygun Fiyatlı:**
        1. **RunPod** ($0.20/saat)
        2. **Vast.ai** ($0.10/saat)
        3. **DigitalOcean** ($5/ay)
        
        Detaylar için cloud_ollama_setup.md dosyasını inceleyin.
        """)

# Fine-tuning data collection
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Veri Toplama")
collect_data = st.sidebar.checkbox("📊 Veri Toplama", value=True, help="Model eğitimi için veri toplar")

# Training data stats
if os.path.exists("training_data.json"):
    try:
        with open("training_data.json", "r", encoding="utf-8") as f:
            training_data = json.load(f)
        
        st.sidebar.info(f"📊 Toplam veri: {len(training_data)} örnek")
        
        # Model eğitimi butonları (sadece local environment'da)
        if is_local_environment():
            st.sidebar.markdown("### 🏋️ Model Eğitimi")
            
            col_train1, col_train2 = st.sidebar.columns(2)
            
            with col_train1:
                if st.button("🔧 Temel Model Oluştur", help="Training data ile temel model oluştur"):
                    with st.spinner("Temel model oluşturuluyor..."):
                        import subprocess
                        result = subprocess.run(
                            ["python3", "create_walmart_model.py"],
                            cwd="/Users/mahiracan/Desktop/walmart_project_last",
                            capture_output=True,
                            text=True
                        )
                        
                        if result.returncode == 0:
                            st.sidebar.success("✅ Temel model oluşturuldu!")
                        else:
                            st.sidebar.error(f"❌ Hata: {result.stderr}")
            
            with col_train2:
                if st.button("🚀 Gelişmiş Model Oluştur", help="Optimize edilmiş veri ile gelişmiş model oluştur"):
                    with st.spinner("Gelişmiş model oluşturuluyor..."):
                        import subprocess
                        result = subprocess.run(
                            ["python3", "model_optimizer.py"],
                            cwd="/Users/mahiracan/Desktop/walmart_project_last",
                            capture_output=True,
                            text=True
                        )
                        
                        if result.returncode == 0:
                            st.sidebar.success("✅ Gelişmiş modeller oluşturuldu!")
                        else:
                            st.sidebar.error(f"❌ Hata: {result.stderr}")
            
            # Yeni satır - Analytics butonları
            col_train3, col_train4 = st.sidebar.columns(2)
            
            with col_train4:
                if st.button("📈 Model Analytics", help="Model performansını analiz et"):
                    with st.spinner("Analytics çalıştırılıyor..."):
                        import subprocess
                        result = subprocess.run(
                            ["python3", "model_analytics.py"],
                            cwd="/Users/mahiracan/Desktop/walmart_project_last",
                            capture_output=True,
                            text=True
                        )
                        
                        if result.returncode == 0:
                            st.sidebar.success("✅ Analytics tamamlandı!")
                        else:
                            st.sidebar.error(f"❌ Hata: {result.stderr}")
        else:
            st.sidebar.info("💡 Model eğitimi yerel ortamda kullanılabilir.")
        
        # Export işlemleri (her ortamda kullanılabilir)
        st.sidebar.markdown("### 📊 Veri Export")
        col_export1, col_export2 = st.sidebar.columns(2)
        
        with col_export1:
            if st.button("📊 Export JSONL"):
                export_file = export_training_data_for_finetuning("jsonl")
                if export_file:
                    st.sidebar.success(f"✅ {export_file} oluşturuldu!")
                    
                    with open(export_file, "r", encoding="utf-8") as f:
                        data = f.read()
                    
                    st.sidebar.download_button(
                        "💾 JSONL İndir",
                        data=data,
                        file_name=export_file,
                        mime="application/jsonl"
                    )
        
        with col_export2:
            if st.button("� Export CSV"):
                export_file = export_training_data_for_finetuning("csv")
                if export_file:
                    st.sidebar.success(f"✅ {export_file} oluşturuldu!")
                    
                    with open(export_file, "rb") as f:
                        data = f.read()
                    
                    st.sidebar.download_button(
                        "💾 CSV İndir",
                        data=data,
                        file_name=export_file,
                        mime="text/csv"
                    )
        
        # Training data clear button
        if st.sidebar.button("🗑️ Veriyi Temizle"):
            os.remove("training_data.json")
            st.sidebar.success("✅ Training data temizlendi!")
            st.rerun()
    except Exception as e:
        st.sidebar.error(f"Veri okuma hatası: {str(e)}")
else:
    st.sidebar.info("Henüz training data yok. İçerik üretmeye başlayın!")

# AI Model Functions
def call_ollama_api(prompt, model="llama3.1:8b"):
    """Ollama API çağrısı - Cloud desteği ile geliştirilmiş versiyon"""
    
    # Cloud Ollama URL varsa kullan
    ollama_url = OLLAMA_BASE_URL
    if not is_local_environment() and 'cloud_ollama_url' in st.session_state:
        ollama_url = st.session_state['cloud_ollama_url']
    
    # URL kontrolü
    if not ollama_url:
        st.error("❌ Ollama servisi bulunamadı!")
        if not is_local_environment():
            st.info("💡 Cloud Ollama URL'inizi yan panelden girin veya OpenAI ChatGPT kullanın.")
        else:
            st.info("💡 Local ortamda Ollama'yı başlatın: `brew services start ollama`")
        return None
    
    try:
        # Model'e göre parametreleri optimize et
        if "walmart-gpt" in model:
            # Walmart modelleri için özel parametreler
            options = {
                "temperature": 0.3,  # Daha tutarlı sonuçlar için düşük
                "num_ctx": 4096,
                "top_k": 20,
                "top_p": 0.8,
                "repeat_penalty": 1.2,
                "num_predict": 1500  # Daha uzun yanıtlar için
            }
        elif model == "llama3.1:8b":
            options = {
                "temperature": 0.6,  # Dengeli ayar
                "num_ctx": 4096,
                "top_k": 30,
                "top_p": 0.85,
                "repeat_penalty": 1.15,
                "num_predict": 1200
            }
        else:
            options = {
                "temperature": 0.5,  # Varsayılan ayar
                "num_ctx": 4096,
                "top_k": 30,
                "top_p": 0.85,
                "repeat_penalty": 1.15,
                "num_predict": 1000
            }
        
        # Model ismini normalize et (eğer :latest yoksa ekle)
        model_name = model
        if "walmart-gpt" in model and ":latest" not in model:
            model_name = f"{model}:latest"
        
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": options
            },
            timeout=180  # Daha uzun timeout
        )
        
        if response.status_code == 200:
            result = response.json()["response"]
            
            # Debug için yanıt bilgileri
            if is_local_environment():
                st.info(f"✅ Ollama yanıtı alındı ({len(result)} karakter) - Model: {model_name}")
            else:
                st.info(f"✅ Cloud Ollama yanıtı alındı ({len(result)} karakter) - Model: {model_name}")
            
            return result
        else:
            st.error(f"Ollama API hatası: {response.status_code}")
            if response.text:
                st.code(response.text)
            return None
            
    except requests.exceptions.ConnectionError:
        if is_local_environment():
            st.error("❌ Ollama servisine bağlanamıyor!")
            st.info("🔧 Çözüm: `brew services start ollama` komutu ile Ollama'yı başlatın")
        else:
            st.error("❌ Cloud Ollama servisine bağlanamıyor!")
            st.info("💡 Cloud Ollama URL'inizi kontrol edin veya OpenAI ChatGPT kullanın")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Ollama yanıt verme süresi aşıldı")
        st.info("💡 Daha küçük bir model deneyin veya prompt'u kısaltın")
        return None
    except Exception as e:
        st.error(f"Ollama bağlantı hatası: {str(e)}")
        return None

def get_ai_response(prompt, selected_model, api_key):
    """AI modellerinden yanıt al - Deploy ortamı uyumlu"""
    if selected_model == "OpenAI ChatGPT":
        if not api_key:
            st.error("❌ OpenAI API anahtarı gerekli!")
            return None
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
    elif selected_model == "Ollama (Yerel/Cloud)":
        if not api_key:
            st.error("❌ Ollama servisi bulunamadı!")
            return None
        return call_ollama_api(prompt, ollama_model)
    else:
        st.error("Desteklenmeyen model")
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
    st.subheader("📝 Ürün Bilgileri")
    
    with st.form("product_form"):
        st.write("🏷️ **Ürün Adı**")
        product_name = st.text_input(
            "Ürün adını girin:",
            placeholder="Örn: Sony WH-1000XM4 Wireless Bluetooth Headphones"
        )
        
        st.write("🔧 **Ürün Özellikleri**")
        product_features = st.text_area(
            "Ürün özelliklerini girin:",
            placeholder="Ürün özelliklerini detaylı yazın...",
            height=250
        )
        
        submit_button = st.form_submit_button(
            "🚀 İçerik Oluştur", 
            use_container_width=True
        )

with col2:
    st.subheader("✨ Oluşturulan İçerik")
    
    if submit_button and product_name and product_features:
        # API key kontrolü
        if selected_model == "OpenAI ChatGPT" and not api_key:
            st.warning("⚠️ Lütfen OpenAI API anahtarınızı sol panelden girin.")
            st.stop()
        elif selected_model == "Ollama (Yerel/Cloud)" and not api_key:
            st.error("❌ Ollama servisi bulunamadı!")
            st.info("💡 Yerel ortamda Ollama başlatın veya Cloud Ollama URL'i girin.")
            st.stop()
        
        with st.spinner("🤖 AI içerik oluşturuyor..."):
            # Progress simulation
            progress_bar = st.progress(0)
            
            import time
            for i in range(0, 101, 20):
                progress_bar.progress(i)
                time.sleep(0.3)
        try:
            # Walmart Guidelines Compliant Prompt
            prompt = f"""You are a professional content writer for Walmart.com. Follow Walmart's official content guidelines strictly.

Product Name: {product_name}
Product Features: {product_features}

Create content using this EXACT format:

TITLE: [Write a compelling, SEO-optimized product title for Walmart.com following strict guidelines:

DO:
- Write brief titles not exceeding 100 characters
- Create clear, descriptive titles without repetitive keywords, multiple brands or product types
- Include relevant values that exclude phrases like "Coming soon" or "Out-of-stock"
- Include brand, product name, and key selling points

DON'T:
- Write in all caps or use special characters (e.g. '~', '!', '*', '$')
- Make promotional claims (e.g., "Free shipping", "Hot sale", "Top rated", "Premium quality", "Best-selling", "Clearance", "Black Friday", "Savings", "Low price", "40% off")
- Make competitor exclusivity claims (e.g., "Amazon Exclusive", "Target Exclusive")
- Include irrelevant information (e.g., "Coming soon", "Out-of-stock", "Discontinued")
- Incorporate any URLs in any format, including Walmart.com
- Use external URLs
- Use languages other than English
- Include years (e.g. 2025, 2024) unless recommended by Content Standards

Maximum 100 characters total.]

KEY_FEATURES: [List 3-10 key product features following Walmart's guidelines:

DO:
- List the most important features first
- Include 3 to 10 of the most important benefits and features
- Use short phrases or keywords
- Focus on benefits that matter to customers

DON'T:
- Use more than 80 characters (space included) per key feature
- Make promotional claims (e.g., "Free shipping", "Hot sale", "Top rated", "Premium quality", "Best-selling", "Clearance", "Black Friday", "Savings", "Low price")
- Include irrelevant information (e.g., "Coming soon", "Out-of-stock", "Discontinued")
- Use external URLs
- Use emojis
- Use additional text formatting like HTML, bullets or numbered lists
- Use languages other than English
- Describe a different product than mentioned in the title

Each feature should be on a new line starting with "•" and be under 80 characters.]

DESCRIPTION: [Write a comprehensive product description following Walmart's guidelines:

DO:
- Describe the item's features and benefits, including Product Name, Brand and keywords
- Include related words that customers are likely to search for
- Create one paragraph with a minimum of 150 words
- Use professional, persuasive language
- Focus on benefits, use cases, and why customers should buy this product

DON'T:
- Make competitor exclusivity claims (e.g., "Amazon Exclusive", "Target Exclusive")
- Make promotional claims (e.g., "Free shipping", "Hot sale", "Top rated", "Premium quality", "Best-selling", "Clearance", "Black Friday", "Savings", "Low price")
- Make authenticity claims (e.g., "100% Authentic", "Genuine")
- Include irrelevant information (e.g., "Coming soon", "Out-of-stock", "Discontinued")
- Use external URLs
- Use emojis
- Use languages other than English
- Describe a different product than mentioned in the title

Write a single, comprehensive paragraph of at least 150 words.]

Now create content for the product above using this exact format. Make sure to include all three sections: TITLE, KEY_FEATURES, and DESCRIPTION."""
            
            # AI'dan yanıt al
            content = get_ai_response(prompt, selected_model, api_key)
            
            if content is None:
                st.error("AI model yanıt veremiyor. Lütfen ayarları kontrol edin.")
                st.stop()
            
            # Debug için ham yanıtı göster
            with st.expander("🔍 Debug: Ham AI Yanıtı", expanded=False):
                st.code(content, language="text")
                st.info(f"Yanıt uzunluğu: {len(content)} karakter")
                st.info(f"Kullanılan model: {selected_model}")
                if selected_model == "Ollama (Yerel/Cloud)":
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
            
            # Success animation
            st.balloons()
            
            # Training data'yı kaydet
            save_training_data(product_name, product_features, title, key_features, description, selected_model)
            
            # Success message
            st.success("🎉 İçerik Başarıyla Oluşturuldu!")
            
            # Results display
            st.write("**📍 Ürün Başlığı**")
            st.info(title if title else "Başlık oluşturulamadı")
            
            st.write("**⭐ Önemli Özellikler**")
            st.text_area("", value=key_features if key_features else "Özellikler oluşturulamadı", height=150, disabled=True)
            
            st.write("**📄 Detaylı Açıklama**")
            st.text_area("", value=description if description else "Açıklama oluşturulamadı", height=200, disabled=True)
            
            # Action buttons
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("📋 Tümünü Görüntüle", use_container_width=True):
                    full_content = f"TITLE:\n{title}\n\nKEY FEATURES:\n{key_features}\n\nDESCRIPTION:\n{description}"
                    st.code(full_content, language="text")
            
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
            st.error(f"❌ Hata Oluştu: {str(e)}")
            
            if selected_model == "OpenAI ChatGPT":
                st.info("💡 OpenAI API anahtarınızı kontrol edin ve tekrar deneyin.")
            else:
                st.info("💡 Ollama servisinin çalıştığından emin olun ve tekrar deneyin.")
    
    elif submit_button:
        # Error messages
        if selected_model == "OpenAI ChatGPT" and not api_key:
            st.warning("⚠️ Lütfen OpenAI API anahtarınızı sol panelden girin.")
        elif selected_model == "Ollama (Yerel/Cloud)" and not api_key:
            st.error("❌ Ollama servisi bulunamadı!")
            st.info("💡 Yerel ortamda Ollama başlatın veya Cloud Ollama URL'i girin.")
        elif not product_name:
            st.warning("⚠️ Lütfen ürün adını girin.")
        elif not product_features:
            st.warning("⚠️ Lütfen ürün özelliklerini detaylı bir şekilde girin.")
    
    else:
        # Welcome screen
        st.info("🚀 **Başlamaya Hazır!**")
        st.write("Sol panelden API anahtarınızı girin, ürün bilgilerini doldurun ve profesyonel içerik oluşturun.")
        
        # Example display
        st.subheader("📋 Örnek Çıktı Formatı")
        
        st.write("**TITLE:**")
        st.code("Sony WH-1000XM4 Wireless Bluetooth Headphones with Active Noise Cancellation")
        
        st.write("**KEY FEATURES:**")
        st.code("• Industry-leading active noise cancellation\n• 30-hour battery life with quick charge\n• Premium sound quality with LDAC codec\n• Touch controls and voice assistant support")
        
        st.write("**DESCRIPTION:**")
        st.code("The Sony WH-1000XM4 wireless headphones deliver exceptional audio quality with industry-leading active noise cancellation technology...")

# Footer
st.markdown("---")
st.markdown("### 🛒 Walmart İçerik Üreteci")
st.write(f"🤖 AI Teknolojisi: **{selected_model}**")
if is_local_environment():
    st.write("💻 **Ortam**: Yerel (Ollama + OpenAI destekli)")
else:
    st.write("☁️ **Ortam**: Deploy (OpenAI destekli)")
st.write("🎯 Walmart standartlarına uygun SEO dostu içerik üretimi")
st.write("© 2025 - Walmart İçerik Üreteci | Güvenli & Hızlı AI Çözümü")
st.write("Mahir Yusuf Açan Tarafından Geliştirildi")