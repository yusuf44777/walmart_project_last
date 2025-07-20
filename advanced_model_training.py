#!/usr/bin/env python3
"""
Advanced Walmart Model Training System
Gelişmiş model eğitimi, veri analizi ve optimizasyon sistemi
"""

import json
import os
import requests
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class WalmartModelTrainer:
    def __init__(self, data_path="training_data.json"):
        self.data_path = data_path
        self.training_data = []
        self.model_versions = []
        
    def load_and_analyze_data(self):
        """Training data'yı yükle ve analiz et"""
        if not os.path.exists(self.data_path):
            print("❌ Training data bulunamadı!")
            return False
        
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.training_data = json.load(f)
        
        print(f"✅ {len(self.training_data)} eğitim örneği yüklendi")
        
        # Veri kalitesi analizi
        self.analyze_data_quality()
        return True
    
    def analyze_data_quality(self):
        """Veri kalitesini analiz et"""
        print("\n📊 VERİ KALİTESİ ANALİZİ")
        print("=" * 50)
        
        # Temel istatistikler
        title_lengths = []
        desc_lengths = []
        feature_counts = []
        
        for item in self.training_data:
            title = item['output']['title']
            desc = item['output']['description']
            features = item['output']['key_features']
            
            title_lengths.append(len(title))
            desc_lengths.append(len(desc))
            feature_counts.append(len(features.split('\n')))
        
        print(f"📝 Başlık uzunlukları: Ort={np.mean(title_lengths):.1f}, Min={min(title_lengths)}, Max={max(title_lengths)}")
        print(f"📄 Açıklama uzunlukları: Ort={np.mean(desc_lengths):.1f}, Min={min(desc_lengths)}, Max={max(desc_lengths)}")
        print(f"⭐ Özellik sayısı: Ort={np.mean(feature_counts):.1f}, Min={min(feature_counts)}, Max={max(feature_counts)}")
        
        # Walmart uyumluluk kontrolü
        self.check_walmart_compliance()
        
    def check_walmart_compliance(self):
        """Walmart kurallarına uygunluk kontrolü"""
        print("\n🎯 WALMART UYGUNLUK KONTROLÜ")
        print("=" * 40)
        
        violations = {
            'long_titles': 0,
            'promotional_claims': 0,
            'short_descriptions': 0,
            'invalid_characters': 0
        }
        
        prohibited_words = [
            'best-selling', 'premium quality', 'top rated', 'hot sale',
            'free shipping', 'clearance', 'savings', 'low price'
        ]
        
        for item in self.training_data:
            title = item['output']['title'].lower()
            desc = item['output']['description'].lower()
            
            # Başlık uzunluğu kontrolü
            if len(item['output']['title']) > 100:
                violations['long_titles'] += 1
            
            # Yasaklı kelime kontrolü
            for word in prohibited_words:
                if word in title or word in desc:
                    violations['promotional_claims'] += 1
                    break
            
            # Açıklama uzunluğu kontrolü
            if len(item['output']['description']) < 150:
                violations['short_descriptions'] += 1
            
            # Geçersiz karakter kontrolü
            if re.search(r'[~!*$]', item['output']['title']):
                violations['invalid_characters'] += 1
        
        total_samples = len(self.training_data)
        print(f"✅ Uygun başlık uzunluğu: {((total_samples - violations['long_titles']) / total_samples * 100):.1f}%")
        print(f"✅ Yasaklı kelime kullanımı: {((total_samples - violations['promotional_claims']) / total_samples * 100):.1f}%")
        print(f"✅ Yeterli açıklama uzunluğu: {((total_samples - violations['short_descriptions']) / total_samples * 100):.1f}%")
        print(f"✅ Geçerli karakterler: {((total_samples - violations['invalid_characters']) / total_samples * 100):.1f}%")
        
        return violations
    
    def create_advanced_system_prompt(self):
        """Gelişmiş sistem promptu oluştur"""
        
        # En kaliteli örnekleri seç
        quality_examples = self.select_quality_examples()
        
        system_prompt = f"""You are WalmartGPT-Advanced, an elite AI specialist trained on {len(self.training_data)} high-quality Walmart product listings. You are the most advanced AI for creating professional Walmart.com content.

CORE EXPERTISE:
🎯 Walmart Marketplace Mastery: Deep understanding of Walmart's content guidelines, SEO requirements, and customer preferences
📊 Data-Driven Content: Trained on analyzed patterns from successful Walmart listings
🚀 Conversion Optimization: Content designed to maximize customer engagement and sales
🔍 Advanced SEO: Keyword optimization without keyword stuffing

ADVANCED CAPABILITIES:
- Ultra-precise Walmart compliance (Title ≤100 chars, Features ≤80 chars each, Description ≥150 words)
- Intelligent keyword integration based on product category
- Customer psychology-driven feature prioritization
- Competitive differentiation without competitor mentions
- Brand voice consistency across all content types

RESPONSE PROTOCOL:
Generate content in this EXACT format with no deviations:

TITLE: [Compelling, SEO-optimized title under 100 characters]

KEY_FEATURES: [3-10 strategically ordered features, each under 80 characters]
• [Most important customer benefit]
• [Key technical specification]
• [Unique selling proposition]
• [Additional compelling features...]

DESCRIPTION: [Professional paragraph, minimum 150 words, maximum customer appeal]

QUALITY BENCHMARKS FROM TRAINING:
{self.format_quality_examples(quality_examples)}

OPTIMIZATION RULES:
✅ Always prioritize customer benefits over technical specs
✅ Use action-oriented language that drives purchase decisions
✅ Include relevant search keywords naturally
✅ Maintain professional, trustworthy tone
✅ Focus on value proposition and problem-solving
❌ Never use promotional claims or competitor mentions
❌ Never exceed character limits
❌ Never use prohibited special characters or formatting

You are now ready to create the most effective Walmart product content possible."""

        return system_prompt
    
    def select_quality_examples(self, count=3):
        """En kaliteli örnekleri seç"""
        if len(self.training_data) < count:
            return self.training_data
        
        # Kalite skorlaması
        scored_examples = []
        for item in self.training_data:
            score = self.calculate_quality_score(item)
            scored_examples.append((score, item))
        
        # En yüksek skorlu örnekleri seç
        scored_examples.sort(reverse=True, key=lambda x: x[0])
        return [item[1] for item in scored_examples[:count]]
    
    def calculate_quality_score(self, item):
        """Örnek için kalite skoru hesapla"""
        score = 0
        
        title = item['output']['title']
        desc = item['output']['description']
        features = item['output']['key_features']
        
        # Başlık kontrolü
        if 50 <= len(title) <= 100:
            score += 20
        elif len(title) <= 100:
            score += 10
        
        # Açıklama kontrolü
        if len(desc) >= 150:
            score += 20
        if len(desc) >= 200:
            score += 10
        
        # Özellik kontrolü
        feature_lines = features.split('\n')
        valid_features = sum(1 for f in feature_lines if len(f.strip()) <= 80 and f.strip().startswith('•'))
        score += min(valid_features * 5, 30)
        
        # Walmart uyumluluk bonusu
        prohibited = ['best-selling', 'premium', 'top rated', 'hot sale']
        if not any(word in title.lower() or word in desc.lower() for word in prohibited):
            score += 20
        
        return score
    
    def format_quality_examples(self, examples):
        """Kaliteli örnekleri formatla"""
        formatted = ""
        for i, example in enumerate(examples, 1):
            formatted += f"""
EXAMPLE {i}:
Input: {example['input']['product_name']}
Title: {example['output']['title']}
Features: {example['output']['key_features'].replace(chr(10), ' | ')}
Description: {example['output']['description'][:100]}...
"""
        return formatted
    
    def create_advanced_modelfile(self, system_prompt, version="v2.0"):
        """Gelişmiş Modelfile oluştur"""
        
        modelfile_content = f"""FROM llama3.1:8b

# WalmartGPT Advanced - Version {version}
# Trained on {len(self.training_data)} high-quality examples
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SYSTEM \"\"\"{system_prompt}\"\"\"

# Optimized parameters for professional content generation
PARAMETER temperature 0.6          # Balanced creativity and consistency
PARAMETER top_k 35                 # Focused vocabulary selection
PARAMETER top_p 0.85               # Controlled randomness
PARAMETER repeat_penalty 1.15      # Avoid repetition
PARAMETER num_ctx 6144             # Extended context for complex products
PARAMETER num_predict 2000         # Allow detailed descriptions
PARAMETER stop "Human:"           # Clean response termination
PARAMETER stop "Assistant:"       # Clean response termination

# Professional response template
TEMPLATE \"\"\"{{{{ if .System }}}}<|start_header_id|>system<|end_header_id|>

{{{{ .System }}}}<|eot_id|>{{{{ end }}}}{{{{ if .Prompt }}}}<|start_header_id|>user<|end_header_id|>

{{{{ .Prompt }}}}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{{{{ end }}}}{{{{ .Response }}}}<|eot_id|>\"\"\"
"""
        
        filename = f"Modelfile.walmart-advanced-{version}"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(modelfile_content)
        
        print(f"✅ {filename} oluşturuldu")
        return filename
    
    def create_model_with_versioning(self, base_model="llama3.1:8b"):
        """Versiyonlu model oluştur"""
        version = f"v{len(self.model_versions) + 1}.0"
        model_name = f"walmart-gpt-advanced"
        
        print(f"\n🚀 WalmartGPT Advanced {version} oluşturuluyor...")
        print("=" * 60)
        
        # Gelişmiş sistem promptu oluştur
        system_prompt = self.create_advanced_system_prompt()
        
        # Modelfile oluştur
        modelfile_path = self.create_advanced_modelfile(system_prompt, version)
        
        # Model oluştur
        success = self.build_ollama_model(modelfile_path, model_name)
        
        if success:
            # Model bilgilerini kaydet
            model_info = {
                "version": version,
                "model_name": model_name,
                "training_samples": len(self.training_data),
                "created_at": datetime.now().isoformat(),
                "base_model": base_model,
                "modelfile": modelfile_path
            }
            self.model_versions.append(model_info)
            
            # Test et
            self.comprehensive_model_test(model_name)
            
            return model_name
        
        return None
    
    def build_ollama_model(self, modelfile_path, model_name):
        """Ollama modeli oluştur"""
        try:
            print(f"🔧 {model_name} modeli oluşturuluyor...")
            
            result = subprocess.run(
                ["ollama", "create", model_name, "-f", modelfile_path],
                capture_output=True,
                text=True,
                timeout=300  # 5 dakika timeout
            )
            
            if result.returncode == 0:
                print(f"✅ {model_name} modeli başarıyla oluşturuldu!")
                return True
            else:
                print(f"❌ Model oluşturma hatası: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Model oluşturma zaman aşımına uğradı!")
            return False
        except Exception as e:
            print(f"❌ Hata: {str(e)}")
            return False
    
    def comprehensive_model_test(self, model_name):
        """Kapsamlı model testi"""
        print(f"\n🧪 {model_name} kapsamlı test...")
        print("=" * 50)
        
        test_products = [
            {
                "name": "Sony WH-1000XM5 Wireless Headphones",
                "features": "Active noise cancellation, 30-hour battery, multipoint connection, premium sound quality, lightweight design"
            },
            {
                "name": "Apple MacBook Pro 14-inch M3",
                "features": "M3 Pro chip, 18GB RAM, 512GB SSD, Liquid Retina XDR display, ProRes support, 18-hour battery"
            },
            {
                "name": "Samsung 65-inch QLED 4K Smart TV",
                "features": "Quantum Dot technology, 4K resolution, Smart TV features, HDR10+, voice control, gaming mode"
            }
        ]
        
        test_results = []
        
        for i, product in enumerate(test_products, 1):
            print(f"\n📱 Test {i}: {product['name']}")
            
            prompt = f"""Bu ürün için Walmart.com'a uygun bir ürün açıklaması oluştur:

Ürün Adı: {product['name']}
Ürün Özellikleri: {product['features']}"""

            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": model_name,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()["response"]
                    
                    # Sonuçları analiz et
                    analysis = self.analyze_response(result)
                    test_results.append({
                        "product": product['name'],
                        "response": result,
                        "analysis": analysis,
                        "success": True
                    })
                    
                    print(f"✅ Test {i} başarılı!")
                    print(f"📊 Analiz: {analysis}")
                    
                else:
                    print(f"❌ Test {i} başarısız: HTTP {response.status_code}")
                    test_results.append({
                        "product": product['name'],
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                print(f"❌ Test {i} hatası: {str(e)}")
                test_results.append({
                    "product": product['name'],
                    "success": False,
                    "error": str(e)
                })
        
        # Test sonuçlarını kaydet
        self.save_test_results(model_name, test_results)
        
        # Genel başarı oranını hesapla
        successful_tests = sum(1 for result in test_results if result.get('success', False))
        success_rate = (successful_tests / len(test_results)) * 100
        
        print(f"\n📊 TEST SONUÇLARI")
        print(f"✅ Başarı oranı: {success_rate:.1f}%")
        print(f"🎯 Başarılı testler: {successful_tests}/{len(test_results)}")
        
        return test_results
    
    def analyze_response(self, response):
        """Model yanıtını analiz et"""
        analysis = {
            "has_title": "TITLE:" in response,
            "has_features": "KEY_FEATURES:" in response,
            "has_description": "DESCRIPTION:" in response,
            "title_length": 0,
            "feature_count": 0,
            "desc_length": 0,
            "walmart_compliant": True
        }
        
        # Bölümleri ayıkla
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('TITLE:'):
                current_section = 'title'
                title_text = line.replace('TITLE:', '').strip()
                analysis["title_length"] = len(title_text)
                if len(title_text) > 100:
                    analysis["walmart_compliant"] = False
                    
            elif line.startswith('KEY_FEATURES:'):
                current_section = 'features'
                
            elif line.startswith('DESCRIPTION:'):
                current_section = 'description'
                desc_text = line.replace('DESCRIPTION:', '').strip()
                analysis["desc_length"] = len(desc_text)
                
            elif current_section == 'features' and line.startswith('•'):
                analysis["feature_count"] += 1
                if len(line) > 80:
                    analysis["walmart_compliant"] = False
                    
            elif current_section == 'description' and line:
                analysis["desc_length"] += len(line) + 1
        
        if analysis["desc_length"] < 150:
            analysis["walmart_compliant"] = False
        
        return analysis
    
    def save_test_results(self, model_name, test_results):
        """Test sonuçlarını kaydet"""
        filename = f"test_results_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "model_name": model_name,
                "test_date": datetime.now().isoformat(),
                "results": test_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Test sonuçları {filename} dosyasına kaydedildi")
    
    def create_training_pipeline(self):
        """Otomatik eğitim pipeline'ı"""
        print("🔄 OTOMATIK EĞİTİM PİPELİNE'I")
        print("=" * 60)
        
        # 1. Veri yükle ve analiz et
        if not self.load_and_analyze_data():
            return False
        
        # 2. Veri kalitesini kontrol et
        violations = self.check_walmart_compliance()
        
        # 3. Kalite eşiği kontrolü
        total_violations = sum(violations.values())
        violation_rate = (total_violations / len(self.training_data)) * 100
        
        if violation_rate > 20:  # %20'den fazla hata varsa
            print(f"⚠️ Veri kalitesi düşük! Hata oranı: {violation_rate:.1f}%")
            print("💡 Daha fazla kaliteli veri toplamayı öneririz.")
        
        # 4. Model oluştur
        model_name = self.create_model_with_versioning()
        
        if model_name:
            print(f"\n🎉 {model_name} başarıyla oluşturuldu!")
            print("\n📋 SONRAKİ ADIMLAR:")
            print(f"1. Streamlit uygulamanızda model adını '{model_name}' olarak güncelleyin")
            print("2. Daha fazla kaliteli veri toplayarak modeli geliştirin")
            print("3. A/B testleri yaparak performansı ölçün")
            print("4. Müşteri geri bildirimlerine göre ince ayar yapın")
            
            return model_name
        
        return None

def main():
    """Ana fonksiyon"""
    print("🛒 WalmartGPT Advanced Training System")
    print("=" * 60)
    print("🚀 Üst düzey model eğitimi başlatılıyor...\n")
    
    trainer = WalmartModelTrainer()
    model_name = trainer.create_training_pipeline()
    
    if model_name:
        print(f"\n✅ Model eğitimi tamamlandı: {model_name}")
    else:
        print("\n❌ Model eğitimi başarısız!")

if __name__ == "__main__":
    main()
