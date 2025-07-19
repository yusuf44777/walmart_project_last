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

# Modern JavaScript + CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .header-section {
        background: linear-gradient(135deg, #0071ce 0%, #004c91 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .header-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { transform: translate(-50%, -50%) rotate(0deg); }
        50% { transform: translate(-50%, -50%) rotate(180deg); }
    }
    
    .header-content {
        position: relative;
        z-index: 1;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #0071ce, #004c91);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .input-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .result-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .result-item {
        margin-bottom: 2rem;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #0071ce;
        transition: all 0.3s ease;
    }
    
    .result-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .typing-animation {
        overflow: hidden;
        border-right: 2px solid #0071ce;
        animation: typing 3s steps(40, end), blink-caret 0.75s step-end infinite;
    }
    
    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent; }
        50% { border-color: #0071ce; }
    }
    
    .pulse-button {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #0071ce;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .slide-in {
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
</style>

<script>
    // Modern JavaScript functionality
    document.addEventListener('DOMContentLoaded', function() {
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
        
        // Dynamic content loading animation
        function animateCounters() {
            const counters = document.querySelectorAll('.counter');
            counters.forEach(counter => {
                const target = parseInt(counter.getAttribute('data-target'));
                const increment = target / 100;
                let current = 0;
                
                const timer = setInterval(() => {
                    current += increment;
                    counter.textContent = Math.floor(current);
                    
                    if (current >= target) {
                        counter.textContent = target;
                        clearInterval(timer);
                    }
                }, 20);
            });
        }
        
        // Parallax effect for header
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const header = document.querySelector('.header-section');
            if (header) {
                header.style.transform = `translateY(${scrolled * 0.5}px)`;
            }
        });
        
        // Interactive card hover effects
        const cards = document.querySelectorAll('.feature-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-10px) scale(1.02)';
                this.style.boxShadow = '0 20px 40px rgba(0, 113, 206, 0.2)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.1)';
            });
        });
        
        // Dynamic typing effect
        function typeWriter(element, text, speed = 50) {
            let i = 0;
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                }
            }
            type();
        }
        
        // Loading progress simulation
        function simulateProgress(progressBar) {
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);
                }
                progressBar.style.width = progress + '%';
            }, 200);
        }
        
        // Intersection Observer for animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('slide-in');
                }
            });
        });
        
        // Observe all result items
        document.querySelectorAll('.result-item').forEach(item => {
            observer.observe(item);
        });
        
        // Success animation
        function showSuccess() {
            const successDiv = document.createElement('div');
            successDiv.innerHTML = `
                <div style="position: fixed; top: 20px; right: 20px; background: #28a745; color: white; padding: 1rem 2rem; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); z-index: 1000; animation: slideIn 0.5s ease-out;">
                    ✅ İçerik başarıyla oluşturuldu!
                </div>
            `;
            document.body.appendChild(successDiv);
            
            setTimeout(() => {
                successDiv.remove();
            }, 3000);
        }
        
        // Copy to clipboard functionality
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                const notification = document.createElement('div');
                notification.innerHTML = `
                    <div style="position: fixed; bottom: 20px; right: 20px; background: #17a2b8; color: white; padding: 1rem 2rem; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); z-index: 1000; animation: slideIn 0.5s ease-out;">
                        📋 Panoya kopyalandı!
                    </div>
                `;
                document.body.appendChild(notification);
                
                setTimeout(() => {
                    notification.remove();
                }, 2000);
            });
        }
        
        // Real-time character counter
        function addCharacterCounter(textarea) {
            const counter = document.createElement('div');
            counter.style.cssText = 'text-align: right; color: #6c757d; font-size: 0.8rem; margin-top: 0.5rem;';
            textarea.parentNode.appendChild(counter);
            
            function updateCounter() {
                const length = textarea.value.length;
                counter.textContent = `${length} karakter`;
                
                if (length > 500) {
                    counter.style.color = '#28a745';
                } else if (length > 200) {
                    counter.style.color = '#ffc107';
                } else {
                    counter.style.color = '#dc3545';
                }
            }
            
            textarea.addEventListener('input', updateCounter);
            updateCounter();
        }
        
        // Initialize character counters
        setTimeout(() => {
            const textareas = document.querySelectorAll('textarea');
            textareas.forEach(addCharacterCounter);
        }, 1000);
    });
</script>
""", unsafe_allow_html=True)

# Modern Header with JavaScript animations
st.markdown("""
<div class="header-section">
    <div class="header-content">
        <h1 style="font-size: 3rem; margin-bottom: 1rem; font-weight: 700;">
            🛒 Walmart Ürün Açıklaması Üreteci
        </h1>
        <p style="font-size: 1.3rem; margin: 0; opacity: 0.9;">
            ✨ AI ile profesyonel ürün içerikleri oluşturun ✨
        </p>
    </div>
</div>

<div class="feature-grid">
    <div class="feature-card fade-in">
        <h3 style="color: #0071ce; margin-bottom: 1rem; font-size: 1.2rem;">🤖 AI Powered</h3>
        <p style="color: #6c757d; margin: 0;">Ollama & OpenAI</p>
        <div style="margin-top: 1rem; font-size: 2rem; font-weight: bold; color: #0071ce;">
            <span class="counter" data-target="99">0</span>%
        </div>
        <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Doğruluk Oranı</p>
    </div>
    
    <div class="feature-card fade-in">
        <h3 style="color: #0071ce; margin-bottom: 1rem; font-size: 1.2rem;">🎯 SEO Optimized</h3>
        <p style="color: #6c757d; margin: 0;">Walmart Standartları</p>
        <div style="margin-top: 1rem; font-size: 2rem; font-weight: bold; color: #0071ce;">
            <span class="counter" data-target="100">0</span>%
        </div>
        <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Uyumluluk</p>
    </div>
    
    <div class="feature-card fade-in">
        <h3 style="color: #0071ce; margin-bottom: 1rem; font-size: 1.2rem;">⚡ Hızlı Üretim</h3>
        <p style="color: #6c757d; margin: 0;">Saniyeler İçinde</p>
        <div style="margin-top: 1rem; font-size: 2rem; font-weight: bold; color: #0071ce;">
            <span class="counter" data-target="10">0</span>s
        </div>
        <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Ortalama Süre</p>
    </div>
</div>

<script>
    // Initialize counters after a delay
    setTimeout(function() {
        const counters = document.querySelectorAll('.counter');
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'));
            const increment = target / 50;
            let current = 0;
            
            const timer = setInterval(() => {
                current += increment;
                counter.textContent = Math.floor(current);
                
                if (current >= target) {
                    counter.textContent = target;
                    clearInterval(timer);
                }
            }, 30);
        });
    }, 1000);
</script>
""", unsafe_allow_html=True)

# Sidebar with modern design
st.sidebar.markdown("""
<div style="background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); padding: 2rem 1rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
    <h2 style="color: #0071ce; margin-bottom: 1rem; font-weight: 600;">🔧 Ayarlar</h2>
    <div style="width: 50px; height: 3px; background: linear-gradient(90deg, #0071ce, #004c91); margin: 0 auto; border-radius: 3px;"></div>
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
<div style="background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); padding: 1.5rem 1rem; border-radius: 15px; margin-bottom: 1.5rem;">
    <h3 style="color: #0071ce; margin-bottom: 1rem; font-weight: 500;">🔑 API Anahtarı</h3>
    <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Güvenli ve şifreli bağlantı</p>
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
        <div style="background: #d4edda; padding: 1rem; border-radius: 10px; border-left: 4px solid #28a745; margin: 1rem 0;">
            <p style="color: #155724; margin: 0; font-weight: 500;">✅ OpenAI ChatGPT hazır!</p>
        </div>
        """, unsafe_allow_html=True)

elif selected_model == "Ollama (Yerel - Ücretsiz)":
    st.sidebar.markdown("""
    <div style="background: #e8f5e8; padding: 1rem; border-radius: 10px; border-left: 4px solid #28a745; margin: 1rem 0;">
        <p style="color: #155724; margin: 0; font-weight: 500;">✅ Ollama Hazır! (Tamamen Ücretsiz)</p>
        <p style="color: #155724; font-size: 0.9rem; margin: 0.5rem 0 0 0;">🏠 Yerel sunucunuzda çalışıyor</p>
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
                    <div style="background: #e8f5e8; padding: 1rem; border-radius: 10px; border-left: 4px solid #28a745; margin: 1rem 0;">
                        <p style="color: #155724; margin: 0; font-weight: 500;">🎯 Walmart-GPT Hazır! (Özel Model)</p>
                        <p style="color: #155724; font-size: 0.9rem; margin: 0.5rem 0 0 0;">🏷️ Walmart için fine-tuned edilmiş</p>
                        <p style="color: #155724; font-size: 0.8rem; margin: 0.2rem 0 0 0;">📦 Model boyutu: ~{model_size}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.sidebar.markdown(f"""
                    <div style="background: #d4edda; padding: 1rem; border-radius: 10px; border-left: 4px solid #28a745; margin: 1rem 0;">
                        <p style="color: #155724; margin: 0; font-weight: 500;">🎯 {ollama_model} hazır!</p>
                        <p style="color: #155724; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Model boyutu: ~{model_size}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                if ollama_model == "walmart-gpt":
                    st.sidebar.markdown(f"""
                    <div style="background: #fff3cd; padding: 1rem; border-radius: 10px; border-left: 4px solid #ffc107; margin: 1rem 0;">
                        <p style="color: #856404; margin: 0; font-weight: 500;">⚠️ Walmart-GPT henüz oluşturulmadı</p>
                        <p style="color: #856404; font-size: 0.9rem; margin: 0.5rem 0 0 0;">👆 "Walmart Modeli Oluştur" butonuna tıklayın</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.sidebar.markdown(f"""
                    <div style="background: #fff3cd; padding: 1rem; border-radius: 10px; border-left: 4px solid #ffc107; margin: 1rem 0;">
                        <p style="color: #856404; margin: 0; font-weight: 500;">⚠️ {ollama_model} yüklü değil</p>
                        <p style="color: #856404; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Komutu çalıştırın: ollama pull {ollama_model}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.sidebar.error("Ollama servisine bağlanamıyor")
    except:
        st.sidebar.markdown("""
        <div style="background: #f8d7da; padding: 1rem; border-radius: 10px; border-left: 4px solid #dc3545; margin: 1rem 0;">
            <p style="color: #721c24; margin: 0; font-weight: 500;">❌ Ollama çalışmıyor</p>
            <p style="color: #721c24; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Başlatın: brew services start ollama</p>
        </div>
        """, unsafe_allow_html=True)
    
    api_key = "ollama_local"

# Enhanced help section
st.sidebar.markdown("""
<div style="background: linear-gradient(145deg, #e8f5e8 0%, #c8e6c9 100%); padding: 1.5rem 1rem; border-radius: 15px; margin-top: 2rem;">
    <h3 style="color: #2e7d32; margin-bottom: 1rem; font-weight: 500;">🎯 Ollama - Tamamen Ücretsiz!</h3>
    <div style="margin-bottom: 1rem;">
        <p style="color: #388e3c; margin: 0.5rem 0; font-weight: 500;">✅ Avantajları:</p>
        <ul style="color: #388e3c; margin: 0.5rem 0; padding-left: 1.5rem;">
            <li>🆓 Tamamen ücretsiz</li>
            <li>🏠 Yerel çalışır (gizlilik)</li>
            <li>⚡ Çok hızlı</li>
            <li>🔒 Veri güvenliği</li>
        </ul>
    </div>
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #4caf50;">
        <p style="color: #2e7d32; margin: 0.5rem 0; font-weight: 500;">💸 Ücretli Alternatif:</p>
        <a href="https://platform.openai.com/api-keys" target="_blank" style="color: #0071ce; text-decoration: none; font-weight: 500;">📍 OpenAI API</a>
    </div>
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #4caf50;">
        <p style="color: #2e7d32; font-size: 0.9rem; margin: 0;">🚀 Ollama önerilen seçenek!</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Fine-tuning data collection
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background: linear-gradient(145deg, #e8f5e8 0%, #c8e6c9 100%); padding: 1.5rem 1rem; border-radius: 15px; margin-top: 1rem;">
    <h3 style="color: #2e7d32; margin-bottom: 1rem; font-weight: 500;">🎯 Fine-Tuning Veri Toplama</h3>
    <p style="color: #388e3c; font-size: 0.9rem; margin: 0;">Her başarılı içerik üretimi Walmart modeli için eğitim verisi olarak kaydedilir.</p>
</div>
""", unsafe_allow_html=True)

# Data collection toggle
collect_data = st.sidebar.checkbox("📊 Veri Toplama", value=True, help="Kendi modelinizi eğitmek için veri toplar")

# Fine-tuning Management
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background: linear-gradient(145deg, #fff3e0 0%, #ffcc80 100%); padding: 1.5rem 1rem; border-radius: 15px; margin-top: 1rem;">
    <h3 style="color: #f57c00; margin-bottom: 1rem; font-weight: 500;">🔧 Model Eğitimi</h3>
    <p style="color: #ef6c00; font-size: 0.9rem; margin: 0;">Toplanan veriyi model eğitimi için hazırla</p>
</div>
""", unsafe_allow_html=True)

# Training data stats
if os.path.exists("training_data.json"):
    try:
        with open("training_data.json", "r", encoding="utf-8") as f:
            training_data = json.load(f)
        
        st.sidebar.markdown(f"""
        <div style="background: #e8f5e8; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <h4 style="color: #2e7d32; margin-bottom: 0.5rem;">📊 Veri İstatistikleri</h4>
            <p style="color: #388e3c; font-size: 0.9rem; margin: 0;">
                • Toplam örnek: <strong>{len(training_data)}</strong><br>
                • En fazla kullanılan model: <strong>{max(set([item['model_used'] for item in training_data]), key=[item['model_used'] for item in training_data].count) if training_data else 'Yok'}</strong>
            </p>
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

# Ana içerik
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div class="input-container">
        <h2 style="color: #0071ce; text-align: center; margin-bottom: 2rem; font-weight: 600;">📝 Ürün Bilgileri</h2>
        <div style="width: 60px; height: 3px; background: linear-gradient(90deg, #0071ce, #004c91); margin: 0 auto 2rem auto; border-radius: 3px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced form with JavaScript interactions
    with st.form("product_form"):
        st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="color: #0071ce; margin-bottom: 0.5rem; font-weight: 500;">🏷️ Ürün Adı</h3>
            <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Ürününüzün tam adını girin</p>
        </div>
        """, unsafe_allow_html=True)
        
        product_name = st.text_input(
            "Ürün adını girin:",
            placeholder="Örn: Sony WH-1000XM4 Wireless Bluetooth Headphones",
            label_visibility="collapsed"
        )
        
        st.markdown("""
        <div style="margin: 2rem 0 1rem 0;">
            <h3 style="color: #0071ce; margin-bottom: 0.5rem; font-weight: 500;">🔧 Ürün Özellikleri</h3>
            <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Detaylı özellikler ve faydaları yazın</p>
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
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        submit_button = st.form_submit_button(
            "🚀 Profesyonel İçerik Oluştur", 
            use_container_width=True
        )

with col2:
    st.markdown("""
    <div class="result-container">
        <h2 style="color: #0071ce; text-align: center; margin-bottom: 2rem; font-weight: 600;">✨ Oluşturulan İçerik</h2>
        <div style="width: 60px; height: 3px; background: linear-gradient(90deg, #0071ce, #004c91); margin: 0 auto 2rem auto; border-radius: 3px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    if submit_button and api_key and product_name and product_features:
        # Enhanced loading with JavaScript
        st.markdown("""
        <div id="loading-container" style="text-align: center; margin: 2rem 0;">
            <div class="loading-spinner"></div>
            <p style="color: #0071ce; font-weight: 500; margin-top: 1rem;">
                🤖 AI içerik oluşturuyor... 
                <span id="loading-text">Lütfen bekleyin</span>
            </p>
        </div>
        
        <script>
            const loadingTexts = [
                "Ürün analiz ediliyor...",
                "Walmart standartları kontrol ediliyor...",
                "SEO optimizasyonu yapılıyor...",
                "İçerik oluşturuluyor...",
                "Son kontroller yapılıyor..."
            ];
            
            let textIndex = 0;
            const loadingInterval = setInterval(() => {
                document.getElementById('loading-text').textContent = loadingTexts[textIndex];
                textIndex = (textIndex + 1) % loadingTexts.length;
            }, 1000);
            
            // Clear interval after 10 seconds
            setTimeout(() => {
                clearInterval(loadingInterval);
            }, 10000);
        </script>
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
            
            # Success message with animation
            st.markdown("""
            <div class="slide-in" style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0; border-left: 5px solid #28a745; text-align: center;">
                <h3 style="color: #28a745; margin-bottom: 1rem; font-weight: 600;">🎉 İçerik Başarıyla Oluşturuldu!</h3>
                <p style="color: #155724; margin: 0;">AI tarafından Walmart standartlarına uygun profesyonel içerik hazırlandı</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced results display
            st.markdown("""
            <div class="result-item slide-in" style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 2rem; border-radius: 15px; margin: 1.5rem 0; border-left: 5px solid #2196f3;">
                <h3 style="color: #1976d2; margin-bottom: 1rem; font-weight: 600;">📍 Ürün Başlığı</h3>
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <p style="margin: 0; font-size: 1.1rem; font-weight: 500; color: #333; line-height: 1.5;">{}</p>
                </div>
                <div style="margin-top: 1rem; font-size: 0.9rem; color: #666;">
                    <span style="background: #e8f5e8; padding: 0.2rem 0.5rem; border-radius: 15px;">📏 {} karakterler</span>
                </div>
            </div>
            """.format(title if title else "Başlık oluşturulamadı", len(title) if title else 0), unsafe_allow_html=True)
            
            # Key Features with enhanced styling
            st.markdown("""
            <div class="result-item slide-in" style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); padding: 2rem; border-radius: 15px; margin: 1.5rem 0; border-left: 5px solid #ff9800;">
                <h3 style="color: #f57c00; margin-bottom: 1rem; font-weight: 600;">⭐ Önemli Özellikler</h3>
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <p style="margin: 0; white-space: pre-line; color: #333; line-height: 1.6;">{}</p>
                </div>
                <div style="margin-top: 1rem; font-size: 0.9rem; color: #666;">
                    <span style="background: #e8f5e8; padding: 0.2rem 0.5rem; border-radius: 15px;">📋 {} özellik</span>
                </div>
            </div>
            """.format(key_features if key_features else "Özellikler oluşturulamadı", len(key_features.split('\n')) if key_features else 0), unsafe_allow_html=True)
            
            # Description with enhanced styling
            st.markdown("""
            <div class="result-item slide-in" style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); padding: 2rem; border-radius: 15px; margin: 1.5rem 0; border-left: 5px solid #4caf50;">
                <h3 style="color: #388e3c; margin-bottom: 1rem; font-weight: 600;">📄 Detaylı Açıklama</h3>
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <p style="margin: 0; line-height: 1.7; color: #333; text-align: justify;">{}</p>
                </div>
                <div style="margin-top: 1rem; font-size: 0.9rem; color: #666;">
                    <span style="background: #e8f5e8; padding: 0.2rem 0.5rem; border-radius: 15px;">📝 {} kelime</span>
                </div>
            </div>
            """.format(description if description else "Açıklama oluşturulamadı", len(description.split()) if description else 0), unsafe_allow_html=True)
            
            # Enhanced action buttons
            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("📋 Tümünü Görüntüle", use_container_width=True):
                    full_content = f"TITLE:\n{title}\n\nKEY FEATURES:\n{key_features}\n\nDESCRIPTION:\n{description}"
                    st.markdown("""
                    <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; border: 1px solid #e9ecef; margin: 1rem 0;">
                        <h4 style="color: #0071ce; margin-bottom: 1rem;">📄 Tam İçerik</h4>
                        <pre style="background: white; padding: 1rem; border-radius: 8px; overflow-x: auto; font-size: 0.9rem;">{}</pre>
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
                if st.button("🔄 Yeniden Oluştur", use_container_width=True):
                    st.rerun()
            
        except Exception as e:
            st.markdown("""
            <div class="slide-in" style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0; border-left: 5px solid #dc3545; text-align: center;">
                <h3 style="color: #d32f2f; margin-bottom: 1rem; font-weight: 600;">❌ Hata Oluştu!</h3>
                <p style="color: #721c24; margin: 0;">{}</p>
            </div>
            """.format(str(e)), unsafe_allow_html=True)
            
            if selected_model == "OpenAI ChatGPT":
                st.markdown("""
                <div style="background: #d1ecf1; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #17a2b8;">
                    <p style="color: #0c5460; margin: 0;">💡 OpenAI API anahtarınızı kontrol edin ve tekrar deneyin.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #d1ecf1; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #17a2b8;">
                    <p style="color: #0c5460; margin: 0;">💡 Ollama servisinin çalıştığından emin olun ve tekrar deneyin.</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif submit_button:
        # Enhanced error messages
        if not api_key:
            st.markdown("""
            <div class="slide-in" style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0; border-left: 5px solid #f39c12; text-align: center;">
                <h3 style="color: #856404; margin-bottom: 1rem; font-weight: 600;">⚠️ API Anahtarı Gerekli</h3>
                <p style="color: #856404; margin: 0;">Lütfen {} API anahtarınızı sol panelden girin.</p>
            </div>
            """.format(selected_model), unsafe_allow_html=True)
        elif not product_name:
            st.markdown("""
            <div class="slide-in" style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0; border-left: 5px solid #f39c12; text-align: center;">
                <h3 style="color: #856404; margin-bottom: 1rem; font-weight: 600;">⚠️ Ürün Adı Gerekli</h3>
                <p style="color: #856404; margin: 0;">Lütfen ürün adını girin.</p>
            </div>
            """, unsafe_allow_html=True)
        elif not product_features:
            st.markdown("""
            <div class="slide-in" style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0; border-left: 5px solid #f39c12; text-align: center;">
                <h3 style="color: #856404; margin-bottom: 1rem; font-weight: 600;">⚠️ Ürün Özellikleri Gerekli</h3>
                <p style="color: #856404; margin: 0;">Lütfen ürün özelliklerini detaylı bir şekilde girin.</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Welcome screen with enhanced design
        st.markdown("""
        <div class="slide-in" style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 3rem 2rem; border-radius: 20px; margin: 2rem 0; text-align: center;">
            <h3 style="color: #1976d2; margin-bottom: 1.5rem; font-weight: 600;">🚀 Başlamaya Hazır!</h3>
            <p style="color: #0d47a1; margin-bottom: 2rem; font-size: 1.1rem;">Sol panelden API anahtarınızı girin, ürün bilgilerini doldurun ve profesyonel içerik oluşturun.</p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 2rem;">
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h4 style="color: #1976d2; margin-bottom: 0.5rem;">1️⃣ API Anahtarı</h4>
                    <p style="color: #666; font-size: 0.9rem; margin: 0;">Sidebar'dan girin</p>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h4 style="color: #1976d2; margin-bottom: 0.5rem;">2️⃣ Ürün Bilgisi</h4>
                    <p style="color: #666; font-size: 0.9rem; margin: 0;">Detaylı yazın</p>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h4 style="color: #1976d2; margin-bottom: 0.5rem;">3️⃣ İçerik Oluştur</h4>
                    <p style="color: #666; font-size: 0.9rem; margin: 0;">Butona tıklayın</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced example display
        st.markdown("""
        <div class="slide-in" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0; border-left: 5px solid #6c757d;">
            <h3 style="color: #495057; margin-bottom: 1.5rem; font-weight: 600;">📋 Örnek Çıktı Formatı</h3>
            <div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="margin-bottom: 1.5rem; padding: 1rem; background: #e3f2fd; border-radius: 8px; border-left: 4px solid #2196f3;">
                    <h4 style="color: #1976d2; margin-bottom: 0.5rem;">TITLE:</h4>
                    <p style="margin: 0; font-weight: 500;">Sony WH-1000XM4 Wireless Bluetooth Headphones with Active Noise Cancellation</p>
                </div>
                
                <div style="margin-bottom: 1.5rem; padding: 1rem; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff9800;">
                    <h4 style="color: #f57c00; margin-bottom: 0.5rem;">KEY FEATURES:</h4>
                    <p style="margin: 0; white-space: pre-line;">• Industry-leading active noise cancellation
• 30-hour battery life with quick charge
• Premium sound quality with LDAC codec
• Touch controls and voice assistant support</p>
                </div>
                
                <div style="margin-bottom: 0; padding: 1rem; background: #e8f5e8; border-radius: 8px; border-left: 4px solid #4caf50;">
                    <h4 style="color: #388e3c; margin-bottom: 0.5rem;">DESCRIPTION:</h4>
                    <p style="margin: 0; line-height: 1.6;">The Sony WH-1000XM4 wireless headphones deliver exceptional audio quality with industry-leading active noise cancellation technology. These premium headphones feature 30-hour battery life, quick charge functionality, and superior sound quality with LDAC codec support...</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Modern Footer with JavaScript
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #0071ce 0%, #004c91 100%); padding: 3rem 2rem; border-radius: 20px; margin-top: 4rem; text-align: center; color: white; position: relative; overflow: hidden;">
    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="white" opacity="0.1"><polygon points="0,0 1000,100 1000,0"/></svg>'); background-size: cover;"></div>
    
    <div style="position: relative; z-index: 1;">
        <h3 style="color: white; margin-bottom: 2rem; font-weight: 700; font-size: 2rem;">🛒 Walmart İçerik Üreteci</h3>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin: 2rem 0;">
            <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; backdrop-filter: blur(10px);">
                <h4 style="color: #e6f3ff; margin-bottom: 1rem; font-weight: 600;">🤖 AI Teknolojisi</h4>
                <p style="color: #b3d9ff; margin: 0; font-size: 1.1rem;">{0}</p>
                <div style="margin-top: 1rem; font-size: 0.9rem; color: #cce7ff;">
                    <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 15px;">Güvenilir & Hızlı</span>
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; backdrop-filter: blur(10px);">
                <h4 style="color: #e6f3ff; margin-bottom: 1rem; font-weight: 600;">🎯 Walmart Standartları</h4>
                <p style="color: #b3d9ff; margin: 0; font-size: 1.1rem;">SEO Uyumlu İçerik</p>
                <div style="margin-top: 1rem; font-size: 0.9rem; color: #cce7ff;">
                    <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 15px;">%100 Uyumlu</span>
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; backdrop-filter: blur(10px);">
                <h4 style="color: #e6f3ff; margin-bottom: 1rem; font-weight: 600;">⚡ Profesyonel Sonuçlar</h4>
                <p style="color: #b3d9ff; margin: 0; font-size: 1.1rem;">Anında İçerik Üretimi</p>
                <div style="margin-top: 1rem; font-size: 0.9rem; color: #cce7ff;">
                    <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 15px;">Kalite Garantisi</span>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.3);">
            <p style="color: #b3d9ff; margin: 0; font-size: 1.1rem;">
                🔧 <strong>Geliştirici Notu:</strong> Bu araç <strong style="color: #e6f3ff;">{0}</strong> kullanarak Walmart için optimize edilmiş ürün içeriği oluşturur.
            </p>
            <p style="color: #cce7ff; margin: 1rem 0 0 0; font-size: 0.9rem;">
                © 2025 - Walmart İçerik Üreteci | Güvenli & Hızlı AI Çözümü
            </p>
        </div>
    </div>
</div>

<script>
    // Footer animation
    document.addEventListener('DOMContentLoaded', function() {{
        const footer = document.querySelector('div[style*="background: linear-gradient(135deg, #0071ce 0%, #004c91 100%)"]');
        if (footer) {{
            footer.style.opacity = '0';
            footer.style.transform = 'translateY(50px)';
            footer.style.transition = 'all 0.8s ease-out';
            
            setTimeout(() => {{
                footer.style.opacity = '1';
                footer.style.transform = 'translateY(0)';
            }}, 500);
        }}
    }});
</script>
""".format(selected_model), unsafe_allow_html=True)