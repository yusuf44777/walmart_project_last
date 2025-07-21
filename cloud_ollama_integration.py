import streamlit as st
import os
import requests

# Cloud Ollama Configuration
def get_cloud_ollama_config():
    """Cloud'daki Ollama instance'ınızın bilgileri"""
    cloud_configs = {
        "google_colab": {
            "url": st.secrets.get("COLAB_OLLAMA_URL", ""),
            "token": st.secrets.get("COLAB_TOKEN", "")
        },
        "runpod": {
            "url": st.secrets.get("RUNPOD_OLLAMA_URL", ""),
            "token": st.secrets.get("RUNPOD_TOKEN", "")
        },
        "vastai": {
            "url": st.secrets.get("VASTAI_OLLAMA_URL", ""),
            "token": st.secrets.get("VASTAI_TOKEN", "")
        }
    }
    return cloud_configs

def get_ollama_base_url():
    """Geliştirilmiş Ollama URL detection"""
    # 1. Önce yerel environment kontrol et
    if not (os.environ.get('STREAMLIT_CLOUD_ENV') or 
            os.environ.get('HEROKU_APP_NAME') or 
            os.environ.get('RAILWAY_ENVIRONMENT')):
        return "http://localhost:11434"
    
    # 2. Cloud Ollama instance'larını kontrol et
    cloud_configs = get_cloud_ollama_config()
    
    for provider, config in cloud_configs.items():
        if config["url"]:
            # Test connection
            try:
                response = requests.get(f"{config['url']}/api/tags", timeout=3)
                if response.status_code == 200:
                    st.info(f"✅ Cloud Ollama bulundu: {provider}")
                    return config["url"]
            except:
                continue
    
    # 3. Hiçbiri yoksa None döndür
    return None

def call_cloud_ollama_api(prompt, model="llama3.1:8b", cloud_url=None):
    """Cloud Ollama API çağrısı"""
    if not cloud_url:
        return None
    
    try:
        response = requests.post(
            f"{cloud_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            st.error(f"Cloud Ollama hatası: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Cloud Ollama bağlantı hatası: {str(e)}")
        return None

# Streamlit secrets konfigürasyonu için
st.sidebar.markdown("### ☁️ Cloud Ollama Ayarları")

if not is_local_environment():
    cloud_ollama_url = st.sidebar.text_input(
        "Cloud Ollama URL:",
        placeholder="https://your-colab-ngrok-url.ngrok.io",
        help="Google Colab, RunPod veya Vast.ai'daki Ollama URL'inizi girin"
    )
    
    if cloud_ollama_url:
        # Test connection
        try:
            test_response = requests.get(f"{cloud_ollama_url}/api/tags", timeout=3)
            if test_response.status_code == 200:
                st.sidebar.success("✅ Cloud Ollama bağlantısı başarılı!")
                # Update global URL
                OLLAMA_BASE_URL = cloud_ollama_url
            else:
                st.sidebar.error("❌ Cloud Ollama'ya bağlanamıyor")
        except:
            st.sidebar.error("❌ Bağlantı hatası")
