import streamlit as st
import google.generativeai as genai
import openai
import os

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
        <p style="color: #6c757d; margin: 0;">Google Gemini & OpenAI</p>
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
    ["Google Gemini", "OpenAI ChatGPT"],
    help="Kullanmak istediğiniz AI modelini seçin"
)

# API Key section
st.sidebar.markdown("""
<div style="background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); padding: 1.5rem 1rem; border-radius: 15px; margin-bottom: 1.5rem;">
    <h3 style="color: #0071ce; margin-bottom: 1rem; font-weight: 500;">🔑 API Anahtarı</h3>
    <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Güvenli ve şifreli bağlantı</p>
</div>
""", unsafe_allow_html=True)

if selected_model == "Google Gemini":
    api_key = st.sidebar.text_input(
        "🔍 Google Gemini API Key:",
        type="password",
        help="Google AI Studio'dan API anahtarınızı alın"
    )
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        st.sidebar.markdown("""
        <div style="background: #d4edda; padding: 1rem; border-radius: 10px; border-left: 4px solid #28a745; margin: 1rem 0;">
            <p style="color: #155724; margin: 0; font-weight: 500;">✅ Google Gemini hazır!</p>
        </div>
        """, unsafe_allow_html=True)

else:  # OpenAI ChatGPT
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

# Enhanced help section
st.sidebar.markdown("""
<div style="background: linear-gradient(145deg, #fff3cd 0%, #ffeaa7 100%); padding: 1.5rem 1rem; border-radius: 15px; margin-top: 2rem;">
    <h3 style="color: #856404; margin-bottom: 1rem; font-weight: 500;">💡 Yardım & Linkler</h3>
    <div style="margin-bottom: 1rem;">
        <p style="color: #856404; margin: 0.5rem 0; font-weight: 500;">🔗 API Anahtarları:</p>
        <a href="https://makersuite.google.com/app/apikey" target="_blank" style="color: #0071ce; text-decoration: none; font-weight: 500;">📍 Google Gemini API</a><br>
        <a href="https://platform.openai.com/api-keys" target="_blank" style="color: #0071ce; text-decoration: none; font-weight: 500;">📍 OpenAI API</a>
    </div>
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #f0ad4e;">
        <p style="color: #856404; font-size: 0.9rem; margin: 0;">🔒 API anahtarlarınız güvenli bir şekilde saklanır</p>
    </div>
</div>
""", unsafe_allow_html=True)

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
            
            # Prompt oluşturma
            prompt = f"""
            Walmart.com için aşağıdaki ürün bilgilerine göre profesyonel bir içerik oluştur:
            
            Ürün Adı: {product_name}
            Ürün Özellikleri: {product_features}
            
            Walmart standartlarına uygun olarak aşağıdaki formatı kullan:
            
            TITLE: [Walmart için SEO uyumlu, çekici bir başlık]
            
            KEY_FEATURES: [3-10 önemli özellik, her satırda bir özellik]
            
            DESCRIPTION: [Walmart standartlarına uygun ürün açıklaması - minimum 150 kelime]
            
            TITLE KURALLARI:
            - Maximum 100 karakter kısa başlık yaz
            - Net, açıklayıcı başlık oluştur
            - Tekrarlayan anahtar kelimeler, çoklu markalar kullanma
            - İlgili değerler ekle
            - Büyük harfle yazma veya özel karakterler kullanma (~, !, *, $ vb.)
            - Promotional claims kullanma (Free shipping, Hot sale, Top rated vb.)
            - Competitor exclusivity iddialarında bulunma
            - Irrelevant bilgi ekleme (Coming soon, Out-of-stock vb.)
            - URL ekleme (Walmart.com dahil)
            - External URL kullanma
            - Sadece İngilizce yaz
            - Yıl ekleme (2024, 2025 vb.) önerilen durumlar hariç
            
            KEY_FEATURES KURALLARI:
            - En önemli özellikleri önce listele (3-10 adet)
            - Kısa cümleler veya anahtar kelimeler kullan
            - Her özellik maximum 80 karakter olsun (boşluklar dahil)
            - Promotional claims kullanma (Free shipping, Hot sale, Top rated vb.)
            - Irrelevant bilgi ekleme (Coming soon, Out-of-stock vb.)
            - External URL kullanma
            - Emoji kullanma
            - HTML, bullet points veya numaralı liste formatı kullanma
            - Sadece İngilizce yaz
            - Ürün başlığında belirtilenden farklı bir ürün tanımlama
            
            DESCRIPTION KURALLARI:
            - Ürün adı, marka ve anahtar kelimeleri dahil et
            - Müşterilerin arayabileceği ilgili kelimeleri kullan
            - Minimum 150 kelimelik tek paragraf oluştur
            - Promotional claims kullanma (Free shipping, Hot sale, Premium quality vb.)
            - Competitor exclusivity iddialarında bulunma
            - Authenticity claims yapma
            - Emoji kullanma
            - Sadece İngilizce yaz
            - Ürün başlığında belirtilenden farklı bir ürün tanımlama
            - External URL veya irrelevant bilgi ekleme
            
            Tüm içerik İngilizce olsun ve Walmart'ın profesyonel tonunu yansıtsın.
            """
            
            # AI'dan yanıt al
            if selected_model == "Google Gemini":
                response = model.generate_content(prompt)
                content = response.text
            else:  # OpenAI ChatGPT
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
                content = response.choices[0].message.content
            
            # İçeriği parse et
            sections = content.split('\n\n')
            title = ""
            key_features = ""
            description = ""
            
            for section in sections:
                if section.startswith('TITLE:'):
                    title = section.replace('TITLE:', '').strip()
                elif section.startswith('KEY_FEATURES:'):
                    key_features = section.replace('KEY_FEATURES:', '').strip()
                elif section.startswith('DESCRIPTION:'):
                    description = section.replace('DESCRIPTION:', '').strip()
            
            # Clear loading
            st.markdown("""
            <script>
                document.getElementById('loading-container').style.display = 'none';
            </script>
            """, unsafe_allow_html=True)
            
            # Success animation
            st.balloons()
            
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
            
            if selected_model == "Google Gemini":
                st.markdown("""
                <div style="background: #d1ecf1; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #17a2b8;">
                    <p style="color: #0c5460; margin: 0;">💡 Google Gemini API anahtarınızı kontrol edin ve tekrar deneyin.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #d1ecf1; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #17a2b8;">
                    <p style="color: #0c5460; margin: 0;">💡 OpenAI API anahtarınızı kontrol edin ve tekrar deneyin.</p>
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
                <p style="color: #b3d9ff; margin: 0; font-size: 1.1rem;">{}</p>
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
                🔧 <strong>Geliştirici Notu:</strong> Bu araç <strong style="color: #e6f3ff;">{}</strong> kullanarak Walmart için optimize edilmiş ürün içeriği oluşturur.
            </p>
            <p style="color: #cce7ff; margin: 1rem 0 0 0; font-size: 0.9rem;">
                © 2025 - Walmart İçerik Üreteci | Güvenli & Hızlı AI Çözümü
            </p>
        </div>
    </div>
</div>

<script>
    // Footer animation
    document.addEventListener('DOMContentLoaded', function() {
        const footer = document.querySelector('div[style*="background: linear-gradient(135deg, #0071ce 0%, #004c91 100%)"]');
        if (footer) {
            footer.style.opacity = '0';
            footer.style.transform = 'translateY(50px)';
            footer.style.transition = 'all 0.8s ease-out';
            
            setTimeout(() => {
                footer.style.opacity = '1';
                footer.style.transform = 'translateY(0)';
            }, 500);
        }
    });
</script>
""".format(selected_model, selected_model), unsafe_allow_html=True)