#!/usr/bin/env python3
"""
Walmart Modelfile Creator - Ollama Fine-Tuning
Bu script toplanan training data'yı kullanarak Ollama için özel bir Walmart modeli oluşturur.
"""

import json
import os
import requests
import subprocess

def load_training_data():
    """Training data'yı yükle"""
    if not os.path.exists("training_data.json"):
        print("❌ Training data bulunamadı!")
        return None
    
    with open("training_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"✅ {len(data)} eğitim örneği yüklendi")
    return data

def create_system_prompt(training_data):
    """Training data'dan sistem promptu oluştur"""
    
    # En iyi örnekleri analiz et
    examples = []
    for item in training_data[:5]:  # İlk 5 örneği kullan
        example = f"""
Input: {item['input']['product_name']} - {item['input']['product_features']}
Output: TITLE: {item['output']['title']}
KEY_FEATURES: {item['output']['key_features']}
DESCRIPTION: {item['output']['description']}
"""
        examples.append(example)
    
    system_prompt = f"""You are WalmartGPT, a specialized AI assistant for creating professional Walmart.com product listings. You have been fine-tuned on {len(training_data)} high-quality Walmart product content examples.

EXPERTISE:
- Walmart marketplace standards and guidelines
- SEO-optimized product titles and descriptions
- Professional e-commerce content writing
- Consumer-focused product highlighting

RESPONSE FORMAT:
Always respond in this exact format:

TITLE: [SEO-optimized product title for Walmart.com]

KEY_FEATURES: [3-10 bullet points highlighting key product features]

DESCRIPTION: [Comprehensive product description, minimum 150 words, Walmart professional tone]

TRAINING EXAMPLES:
{chr(10).join(examples)}

Always maintain Walmart's professional, customer-focused tone and ensure all content is SEO-optimized for maximum discoverability."""

    return system_prompt

def create_modelfile(system_prompt, base_model="llama3.1:8b"):
    """Modelfile oluştur"""
    
    modelfile_content = f"""FROM {base_model}

# Walmart-specific system prompt
SYSTEM \"\"\"{system_prompt}\"\"\"

# Fine-tuned parameters for Walmart content generation
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 4096

# Walmart-specific template
TEMPLATE \"\"\"{{{{ if .System }}}}<|im_start|>system
{{{{ .System }}}}<|im_end|>
{{{{ end }}}}{{{{ if .Prompt }}}}<|im_start|>user
{{{{ .Prompt }}}}<|im_end|>
<|im_start|>assistant
{{{{ end }}}}{{{{ .Response }}}}<|im_end|>\"\"\"
"""
    
    # Modelfile'ı kaydet
    with open("Modelfile.walmart", "w", encoding="utf-8") as f:
        f.write(modelfile_content)
    
    print("✅ Modelfile.walmart oluşturuldu")
    return "Modelfile.walmart"

def create_ollama_model(modelfile_path, model_name="walmart-gpt"):
    """Ollama modeli oluştur"""
    try:
        print(f"🔧 {model_name} modeli oluşturuluyor...")
        
        # Ollama create komutu
        result = subprocess.run(
            ["ollama", "create", model_name, "-f", modelfile_path],
            capture_output=True,
            text=True,
            cwd="/Users/mahiracan/Desktop/walmart_project_last"
        )
        
        if result.returncode == 0:
            print(f"✅ {model_name} modeli başarıyla oluşturuldu!")
            print("📋 Çıktı:", result.stdout)
            return True
        else:
            print(f"❌ Model oluşturma hatası: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        return False

def test_walmart_model(model_name="walmart-gpt"):
    """Oluşturulan modeli test et"""
    print(f"\n🧪 {model_name} modeli test ediliyor...")
    
    test_prompt = """Bu ürün için Walmart.com'a uygun bir ürün açıklaması oluştur:

Ürün Adı: Apple iPhone 15 Pro Max
Ürün Özellikleri: 256GB storage, Titanium design, A17 Pro chip, Advanced camera system with 5x telephoto, Action Button, USB-C connector, iOS 17, 6.7-inch Super Retina XDR display"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": test_prompt,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()["response"]
            print("✅ Test başarılı!")
            print("📄 Sonuç:")
            print("-" * 50)
            print(result)
            print("-" * 50)
            return True
        else:
            print(f"❌ Test hatası: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test hatası: {str(e)}")
        return False

def main():
    """Ana fonksiyon"""
    print("🛒 Walmart Model Creator - Ollama Fine-Tuning")
    print("=" * 50)
    
    # 1. Training data yükle
    training_data = load_training_data()
    if not training_data:
        return
    
    # 2. Sistem promptu oluştur
    print("🔧 Sistem promptu oluşturuluyor...")
    system_prompt = create_system_prompt(training_data)
    
    # 3. Modelfile oluştur
    print("📝 Modelfile oluşturuluyor...")
    modelfile_path = create_modelfile(system_prompt)
    
    # 4. Ollama modeli oluştur
    model_name = "walmart-gpt"
    success = create_ollama_model(modelfile_path, model_name)
    
    if success:
        # 5. Modeli test et
        test_walmart_model(model_name)
        
        print(f"""
🎉 Walmart modeli başarıyla oluşturuldu!

📋 Kullanım:
- Model adı: {model_name}
- Test için: ollama run {model_name}
- API'de kullanım: http://localhost:11434/api/generate

🔧 Streamlit uygulamanızda kullanmak için:
1. Sidebar'da Ollama Model seçeneğine '{model_name}' ekleyin
2. Veya call_ollama_api fonksiyonunda model parametresini '{model_name}' olarak ayarlayın
        """)
    else:
        print("❌ Model oluşturma başarısız!")

if __name__ == "__main__":
    main()
