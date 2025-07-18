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

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0071ce 0%, #004c91 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: #e6f3ff !important;
        font-size: 1.2rem;
        margin: 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #0071ce;
        margin-bottom: 1rem;
    }
    
    .result-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border: 1px solid #dee2e6;
    }
    
    .result-card h3 {
        color: #0071ce;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .sidebar-content {
        background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #0071ce 0%, #004c91 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-top: 3px solid #0071ce;
    }
    
    .footer {
        background: linear-gradient(90deg, #0071ce 0%, #004c91 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-top: 3rem;
        text-align: center;
        color: white;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #f39c12;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #17a2b8;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0071ce;
        box-shadow: 0 0 0 0.2rem rgba(0, 113, 206, 0.25);
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 0.75rem;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #0071ce;
        box-shadow: 0 0 0 0.2rem rgba(0, 113, 206, 0.25);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Başlık
st.markdown("""
<div class="main-header">
    <h1>🛒 Walmart Ürün Açıklaması Üreteci</h1>
    <p>✨ AI ile profesyonel ürün içerikleri oluşturun ✨</p>
</div>
""", unsafe_allow_html=True)

# Özellik kartları
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>🤖 AI Powered</h3>
        <p>Google Gemini & OpenAI</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>🎯 SEO Optimized</h3>
        <p>Walmart Standartları</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>⚡ Hızlı Üretim</h3>
        <p>Saniyeler İçinde</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar - API Key girişi ve model seçimi
st.sidebar.markdown("""
<div class="sidebar-content">
    <h2 style="color: #0071ce; text-align: center; margin-bottom: 1rem;">🔧 Ayarlar</h2>
</div>
""", unsafe_allow_html=True)

# Model seçimi
selected_model = st.sidebar.selectbox(
    "🤖 AI Model Seçin:",
    ["Google Gemini", "OpenAI ChatGPT"],
    help="Kullanmak istediğiniz AI modelini seçin"
)

# API Key girişi için daha güzel bir container
st.sidebar.markdown("""
<div class="sidebar-content">
    <h3 style="color: #0071ce; margin-bottom: 1rem;">🔑 API Anahtarı</h3>
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
        st.sidebar.success("✅ Google Gemini hazır!")

else:  # OpenAI ChatGPT
    api_key = st.sidebar.text_input(
        "🔍 OpenAI API Key:",
        type="password",
        help="OpenAI Platform'dan API anahtarınızı alın"
    )
    
    if api_key:
        st.sidebar.success("✅ OpenAI ChatGPT hazır!")

# Sidebar'a yardım bilgileri
st.sidebar.markdown("""
<div class="sidebar-content">
    <h3 style="color: #0071ce;">💡 Yardım</h3>
    <p><strong>Google Gemini:</strong> <a href="https://makersuite.google.com/app/apikey" target="_blank">API Key Al</a></p>
    <p><strong>OpenAI:</strong> <a href="https://platform.openai.com/api-keys" target="_blank">API Key Al</a></p>
</div>
""", unsafe_allow_html=True)

# Ana içerik
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div class="feature-card">
        <h2 style="color: #0071ce; text-align: center; margin-bottom: 1rem;">📝 Ürün Bilgileri</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Ürün özelliklerini girme formu
    with st.form("product_form"):
        st.markdown("### 🏷️ Ürün Adı")
        product_name = st.text_input(
            "Ürün adını girin:",
            placeholder="Örn: Sony WH-1000XM4 Wireless Bluetooth Headphones",
            label_visibility="collapsed"
        )
        
        st.markdown("### 🔧 Ürün Özellikleri")
        product_features = st.text_area(
            "Ürün özelliklerini girin:",
            placeholder="Ürünün tüm özelliklerini, markasını ve faydalarını detaylı bir şekilde yazın...\n\n• Marka ve model\n• Teknik özellikler\n• Avantajlar ve faydalar\n• Hedef kitle\n• Kullanım alanları",
            height=200,
            help="Ürün adı, marka, özellikler ve müşterilerin arayabileceği anahtar kelimeleri ekleyin",
            label_visibility="collapsed"
        )
        
        # Form gönder butonu
        st.markdown("<br>", unsafe_allow_html=True)
        submit_button = st.form_submit_button("🚀 Açıklama Oluştur", use_container_width=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h2 style="color: #0071ce; text-align: center; margin-bottom: 1rem;">✨ Oluşturulan İçerik</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if submit_button and api_key and product_name and product_features:
        with st.spinner("🤖 AI içerik oluşturuyor... Lütfen bekleyin..."):
            try:
                # Progress bar
                progress_bar = st.progress(0)
                progress_bar.progress(25)
                
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
                
                progress_bar.progress(50)
                
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
                
                progress_bar.progress(75)
                
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
                
                progress_bar.progress(100)
                
                # Sonuçları göster
                st.balloons()
                st.markdown("""
                <div class="success-box">
                    <h3 style="color: #28a745; margin: 0;">✅ İçerik başarıyla oluşturuldu!</h3>
                    <p style="margin: 0.5rem 0 0 0;">AI tarafından Walmart standartlarına uygun içerik hazırlandı.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Title kutusu
                st.markdown("""
                <div class="result-card">
                    <h3>📍 Ürün Başlığı</h3>
                    <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; border-left: 4px solid #2196f3;">
                        <p style="margin: 0; font-size: 1.1rem; font-weight: 500;">{}</p>
                    </div>
                </div>
                """.format(title if title else "Başlık oluşturulamadı"), unsafe_allow_html=True)
                
                # Key Features kutusu
                st.markdown("""
                <div class="result-card">
                    <h3>⭐ Key Features</h3>
                    <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; border-left: 4px solid #ff9800;">
                        <p style="margin: 0; white-space: pre-line;">{}</p>
                    </div>
                </div>
                """.format(key_features if key_features else "Özellikler oluşturulamadı"), unsafe_allow_html=True)
                
                # Description kutusu
                st.markdown("""
                <div class="result-card">
                    <h3>📄 Ürün Açıklaması</h3>
                    <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; border-left: 4px solid #4caf50;">
                        <p style="margin: 0; line-height: 1.6;">{}</p>
                    </div>
                </div>
                """.format(description if description else "Açıklama oluşturulamadı"), unsafe_allow_html=True)
                
                # İndirme seçenekleri
                st.markdown("---")
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("📋 Tümünü Görüntüle", use_container_width=True):
                        full_content = f"TITLE:\n{title}\n\nKEY FEATURES:\n{key_features}\n\nDESCRIPTION:\n{description}"
                        st.code(full_content, language="text")
                
                with col_b:
                    if title:
                        st.download_button(
                            "💾 Metin Olarak İndir",
                            data=f"TITLE:\n{title}\n\nKEY FEATURES:\n{key_features}\n\nDESCRIPTION:\n{description}",
                            file_name=f"{product_name.replace(' ', '_')}_walmart_content.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                
                with col_c:
                    if st.button("🔄 Yeni İçerik Oluştur", use_container_width=True):
                        st.rerun()
                
            except Exception as e:
                st.markdown("""
                <div class="warning-box">
                    <h3 style="color: #d32f2f; margin: 0;">❌ Hata oluştu!</h3>
                    <p style="margin: 0.5rem 0 0 0;">{}</p>
                </div>
                """.format(str(e)), unsafe_allow_html=True)
                
                if selected_model == "Google Gemini":
                    st.markdown("""
                    <div class="info-box">
                        <p style="margin: 0;">💡 Lütfen Google Gemini API anahtarınızı kontrol edin ve tekrar deneyin.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="info-box">
                        <p style="margin: 0;">💡 Lütfen OpenAI API anahtarınızı kontrol edin ve tekrar deneyin.</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    elif submit_button:
        if not api_key:
            if selected_model == "Google Gemini":
                st.markdown("""
                <div class="warning-box">
                    <h3 style="color: #f57c00; margin: 0;">⚠️ Eksik API Anahtarı</h3>
                    <p style="margin: 0.5rem 0 0 0;">Lütfen Google Gemini API anahtarınızı sol panelden girin.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="warning-box">
                    <h3 style="color: #f57c00; margin: 0;">⚠️ Eksik API Anahtarı</h3>
                    <p style="margin: 0.5rem 0 0 0;">Lütfen OpenAI API anahtarınızı sol panelden girin.</p>
                </div>
                """, unsafe_allow_html=True)
        elif not product_name:
            st.markdown("""
            <div class="warning-box">
                <h3 style="color: #f57c00; margin: 0;">⚠️ Eksik Ürün Adı</h3>
                <p style="margin: 0.5rem 0 0 0;">Lütfen ürün adını girin.</p>
            </div>
            """, unsafe_allow_html=True)
        elif not product_features:
            st.markdown("""
            <div class="warning-box">
                <h3 style="color: #f57c00; margin: 0;">⚠️ Eksik Ürün Özellikleri</h3>
                <p style="margin: 0.5rem 0 0 0;">Lütfen ürün özelliklerini girin.</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Placeholder content when no action is taken
        st.markdown("""
        <div class="info-box">
            <h3 style="color: #17a2b8; margin: 0;">🚀 Başlamaya Hazır!</h3>
            <p style="margin: 0.5rem 0 0 0;">Sol panelden API anahtarınızı girin, ürün bilgilerini doldurun ve "Açıklama Oluştur" butonuna tıklayın.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Örnek gösterimi
        st.markdown("""
        <div class="result-card">
            <h3>📋 Örnek Çıktı Formatı</h3>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border: 1px solid #e9ecef;">
                <p><strong>TITLE:</strong> Sony WH-1000XM4 Wireless Bluetooth Headphones with Active Noise Cancellation</p>
                <p><strong>KEY FEATURES:</strong><br>
                • Industry-leading active noise cancellation<br>
                • 30-hour battery life with quick charge<br>
                • Premium sound quality with LDAC codec<br>
                • Touch controls and voice assistant support</p>
                <p><strong>DESCRIPTION:</strong> The Sony WH-1000XM4 wireless headphones deliver exceptional audio quality with industry-leading active noise cancellation technology...</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <div style="max-width: 800px; margin: 0 auto;">
        <h3 style="color: white; margin-bottom: 1rem;">🛒 Walmart Ürün Açıklaması Üreteci</h3>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 2rem;">
            <div>
                <h4 style="color: #e6f3ff; margin-bottom: 0.5rem;">🤖 AI Teknolojisi</h4>
                <p style="color: #b3d9ff; margin: 0;">Google Gemini & OpenAI ChatGPT</p>
            </div>
            <div>
                <h4 style="color: #e6f3ff; margin-bottom: 0.5rem;">🎯 Walmart Standartları</h4>
                <p style="color: #b3d9ff; margin: 0;">SEO Uyumlu İçerik Üretimi</p>
            </div>
            <div>
                <h4 style="color: #e6f3ff; margin-bottom: 0.5rem;">⚡ Hızlı ve Güvenilir</h4>
                <p style="color: #b3d9ff; margin: 0;">Profesyonel Sonuçlar</p>
            </div>
        </div>
        <hr style="border-color: #4d94d9; margin: 2rem 0;">
        <p style="color: #b3d9ff; margin: 0; text-align: center;">
            🔧 <strong>Geliştirici Notu:</strong> Bu araç {} kullanarak Walmart için optimize edilmiş ürün içeriği oluşturur.
        </p>
    </div>
</div>
""".format(selected_model), unsafe_allow_html=True)