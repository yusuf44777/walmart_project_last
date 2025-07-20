#!/usr/bin/env python3
"""
Model Performance Monitoring & Analytics
Model performansını izleme ve analiz sistemi
"""

import json
import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import sqlite3
import re

class ModelPerformanceMonitor:
    def __init__(self, db_path="walmart_model_analytics.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Veritabanını başlat"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Model performans tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT,
                test_date TIMESTAMP,
                product_category TEXT,
                title_length INTEGER,
                description_length INTEGER,
                feature_count INTEGER,
                walmart_compliance_score REAL,
                readability_score REAL,
                seo_score REAL,
                response_time REAL,
                user_rating REAL,
                conversion_estimate REAL
            )
        ''')
        
        # A/B test sonuçları tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ab_test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT,
                model_a TEXT,
                model_b TEXT,
                metric_name TEXT,
                model_a_value REAL,
                model_b_value REAL,
                significance_level REAL,
                winner TEXT,
                test_date TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def analyze_model_response(self, response, model_name, product_category="General"):
        """Model yanıtını detaylı analiz et"""
        analysis_results = {
            "model_name": model_name,
            "test_date": datetime.now(),
            "product_category": product_category
        }
        
        # Bölümleri ayıkla
        title, features, description = self.parse_response(response)
        
        # Temel metrikler
        analysis_results["title_length"] = len(title)
        analysis_results["description_length"] = len(description)
        analysis_results["feature_count"] = len(features.split('\n')) if features else 0
        
        # Walmart uyumluluk skoru
        analysis_results["walmart_compliance_score"] = self.calculate_walmart_compliance(title, features, description)
        
        # Okunabilirlik skoru
        analysis_results["readability_score"] = self.calculate_readability(description)
        
        # SEO skoru
        analysis_results["seo_score"] = self.calculate_seo_score(title, description)
        
        # Tahmini dönüşüm oranı
        analysis_results["conversion_estimate"] = self.estimate_conversion_rate(analysis_results)
        
        return analysis_results
    
    def parse_response(self, response):
        """Model yanıtını parse et"""
        title = ""
        features = ""
        description = ""
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('TITLE:'):
                current_section = 'title'
                title = line.replace('TITLE:', '').strip()
            elif line.startswith('KEY_FEATURES:'):
                current_section = 'features'
            elif line.startswith('DESCRIPTION:'):
                current_section = 'description'
                description = line.replace('DESCRIPTION:', '').strip()
            elif current_section == 'features' and line:
                features += line + '\n'
            elif current_section == 'description' and line:
                description += ' ' + line
        
        return title.strip(), features.strip(), description.strip()
    
    def calculate_walmart_compliance(self, title, features, description):
        """Walmart uyumluluk skoru hesapla (0-100)"""
        score = 0
        
        # Başlık kontrolü (30 puan)
        if len(title) <= 100:
            score += 15
        if 50 <= len(title) <= 100:
            score += 10
        if not re.search(r'[~!*$]', title):
            score += 5
        
        # Özellik kontrolü (30 puan)
        if features:
            feature_lines = [f.strip() for f in features.split('\n') if f.strip()]
            valid_features = sum(1 for f in feature_lines if len(f) <= 80 and f.startswith('•'))
            if valid_features >= 3:
                score += 15
            if valid_features >= 5:
                score += 10
            if all(len(f) <= 80 for f in feature_lines):
                score += 5
        
        # Açıklama kontrolü (25 puan)
        if len(description) >= 150:
            score += 15
        if len(description) >= 200:
            score += 10
        
        # Yasaklı kelime kontrolü (15 puan)
        prohibited_words = ['best-selling', 'premium quality', 'top rated', 'hot sale', 'free shipping']
        text_lower = (title + ' ' + description).lower()
        if not any(word in text_lower for word in prohibited_words):
            score += 15
        
        return min(score, 100)
    
    def calculate_readability(self, description):
        """Okunabilirlik skoru hesapla"""
        if not description:
            return 0
        
        try:
            # Basit okunabilirlik hesaplama
            words = len(description.split())
            sentences = description.count('.') + description.count('!') + description.count('?')
            if sentences == 0:
                sentences = 1
            
            avg_words_per_sentence = words / sentences
            
            # Basitleştirilmiş okunabilirlik skoru
            if avg_words_per_sentence <= 15:
                return 80
            elif avg_words_per_sentence <= 20:
                return 60
            elif avg_words_per_sentence <= 25:
                return 40
            else:
                return 20
        except:
            # Basit alternatif hesaplama
            words = len(description.split())
            sentences = description.count('.') + description.count('!') + description.count('?')
            if sentences == 0:
                sentences = 1
            
            avg_words_per_sentence = words / sentences
            
            # Basitleştirilmiş okunabilirlik skoru
            if avg_words_per_sentence <= 15:
                return 80
            elif avg_words_per_sentence <= 20:
                return 60
            elif avg_words_per_sentence <= 25:
                return 40
            else:
                return 20
    
    def calculate_seo_score(self, title, description):
        """SEO skoru hesapla (0-100)"""
        score = 0
        
        if not title or not description:
            return 0
        
        text = (title + ' ' + description).lower()
        
        # Anahtar kelime çeşitliliği
        words = re.findall(r'\b\w+\b', text)
        unique_words = set(words)
        diversity_ratio = len(unique_words) / len(words) if words else 0
        score += min(diversity_ratio * 50, 25)
        
        # Başlıkta anahtar kelime varlığı
        title_words = set(re.findall(r'\b\w+\b', title.lower()))
        desc_words = set(re.findall(r'\b\w+\b', description.lower()))
        overlap = len(title_words.intersection(desc_words))
        score += min(overlap * 5, 25)
        
        # Uzunluk optimizasyonu
        if 50 <= len(title) <= 100:
            score += 15
        if 150 <= len(description) <= 300:
            score += 15
        
        # Tekrar kontrolü
        word_counts = {}
        for word in words:
            if len(word) > 3:  # Küçük kelimeleri görmezden gel
                word_counts[word] = word_counts.get(word, 0) + 1
        
        excessive_repeats = sum(1 for count in word_counts.values() if count > 3)
        score -= excessive_repeats * 5
        
        return max(0, min(score, 100))
    
    def estimate_conversion_rate(self, metrics):
        """Tahmini dönüşüm oranı hesapla"""
        # Ağırlıklı skorlama sistemi
        weights = {
            "walmart_compliance_score": 0.4,
            "readability_score": 0.2,
            "seo_score": 0.3,
            "title_length_factor": 0.1
        }
        
        # Başlık uzunluğu faktörü
        if 50 <= metrics["title_length"] <= 100:
            title_factor = 100
        elif metrics["title_length"] <= 100:
            title_factor = 80
        else:
            title_factor = 50
        
        # Normalize edilmiş readability skoru
        normalized_readability = min(metrics["readability_score"], 100)
        
        # Ağırlıklı ortalama
        conversion_score = (
            metrics["walmart_compliance_score"] * weights["walmart_compliance_score"] +
            normalized_readability * weights["readability_score"] +
            metrics["seo_score"] * weights["seo_score"] +
            title_factor * weights["title_length_factor"]
        )
        
        # 0-10 arası dönüşüm oranına çevir
        return round((conversion_score / 100) * 10, 2)
    
    def save_performance_data(self, analysis_results, response_time=None):
        """Performans verilerini kaydet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO model_performance 
            (model_name, test_date, product_category, title_length, description_length, 
             feature_count, walmart_compliance_score, readability_score, seo_score, 
             response_time, conversion_estimate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            analysis_results["model_name"],
            analysis_results["test_date"],
            analysis_results["product_category"],
            analysis_results["title_length"],
            analysis_results["description_length"],
            analysis_results["feature_count"],
            analysis_results["walmart_compliance_score"],
            analysis_results["readability_score"],
            analysis_results["seo_score"],
            response_time,
            analysis_results["conversion_estimate"]
        ))
        
        conn.commit()
        conn.close()
    
    def generate_performance_report(self, model_name=None, days=30):
        """Performans raporu oluştur"""
        conn = sqlite3.connect(self.db_path)
        
        # SQL sorgusu
        query = """
            SELECT * FROM model_performance 
            WHERE test_date >= datetime('now', '-{} days')
        """.format(days)
        
        if model_name:
            query += f" AND model_name = '{model_name}'"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            print("📊 Yeterli veri bulunamadı!")
            return None
        
        # Rapor oluştur
        report = {
            "summary": self.generate_summary_stats(df),
            "trends": self.analyze_trends(df),
            "recommendations": self.generate_recommendations(df)
        }
        
        return report
    
    def generate_summary_stats(self, df):
        """Özet istatistikler"""
        return {
            "total_tests": len(df),
            "avg_walmart_compliance": df['walmart_compliance_score'].mean(),
            "avg_readability": df['readability_score'].mean(),
            "avg_seo_score": df['seo_score'].mean(),
            "avg_conversion_estimate": df['conversion_estimate'].mean(),
            "best_performing_model": df.loc[df['conversion_estimate'].idxmax(), 'model_name'] if len(df) > 0 else None
        }
    
    def analyze_trends(self, df):
        """Trend analizi"""
        df['test_date'] = pd.to_datetime(df['test_date'])
        df = df.sort_values('test_date')
        
        trends = {}
        
        for metric in ['walmart_compliance_score', 'readability_score', 'seo_score', 'conversion_estimate']:
            if len(df) >= 2:
                # Basit trend hesaplama
                recent_avg = df[metric].tail(len(df)//2).mean()
                early_avg = df[metric].head(len(df)//2).mean()
                trend = "improving" if recent_avg > early_avg else "declining"
                trends[metric] = {
                    "trend": trend,
                    "change": round(recent_avg - early_avg, 2)
                }
        
        return trends
    
    def generate_recommendations(self, df):
        """İyileştirme önerileri"""
        recommendations = []
        
        avg_compliance = df['walmart_compliance_score'].mean()
        avg_readability = df['readability_score'].mean()
        avg_seo = df['seo_score'].mean()
        
        if avg_compliance < 80:
            recommendations.append("🎯 Walmart uyumluluk kurallarını gözden geçirin. Başlık uzunluklarını ve yasaklı kelimeleri kontrol edin.")
        
        if avg_readability < 60:
            recommendations.append("📖 İçerik okunabilirliğini artırın. Daha kısa cümleler ve basit kelimeler kullanın.")
        
        if avg_seo < 70:
            recommendations.append("🔍 SEO optimizasyonunu geliştirin. Anahtar kelime kullanımını ve içerik yapısını gözden geçirin.")
        
        # Başlık uzunluğu analizi
        avg_title_length = df['title_length'].mean()
        if avg_title_length > 100:
            recommendations.append("✂️ Başlık uzunluklarını kısaltın. Walmart limiti 100 karakterdir.")
        elif avg_title_length < 50:
            recommendations.append("📝 Başlıkları daha açıklayıcı hale getirin. 50-100 karakter arası optimal.")
        
        if not recommendations:
            recommendations.append("🎉 Performans mükemmel! Mevcut kaliteyi korumaya devam edin.")
        
        return recommendations

def benchmark_models():
    """Modelleri karşılaştırmalı test et"""
    monitor = ModelPerformanceMonitor()
    
    models_to_test = [
        "llama3.1:8b",
        "walmart-gpt",
        "walmart-gpt-advanced"
    ]
    
    test_products = [
        {
            "name": "iPhone 15 Pro Max 256GB",
            "features": "A17 Pro chip, ProRAW camera, titanium design, action button, USB-C",
            "category": "Electronics"
        },
        {
            "name": "Nike Air Max 270 Running Shoes",
            "features": "Air Max cushioning, breathable mesh, rubber outsole, athletic performance",
            "category": "Footwear"
        },
        {
            "name": "KitchenAid Stand Mixer 5-Quart",
            "features": "10 speeds, tilt-head design, stainless steel bowl, multiple attachments",
            "category": "Kitchen"
        }
    ]
    
    print("🏁 MODEL KARŞILAŞTIRMA TESTİ")
    print("=" * 50)
    
    results = {}
    
    for model in models_to_test:
        print(f"\n🤖 {model} test ediliyor...")
        model_results = []
        
        for product in test_products:
            prompt = f"""Bu ürün için Walmart.com'a uygun bir ürün açıklaması oluştur:

Ürün Adı: {product['name']}
Ürün Özellikleri: {product['features']}"""
            
            try:
                start_time = datetime.now()
                
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=120
                )
                
                response_time = (datetime.now() - start_time).total_seconds()
                
                if response.status_code == 200:
                    result = response.json()["response"]
                    
                    # Analiz et
                    analysis = monitor.analyze_model_response(result, model, product["category"])
                    analysis["response_time"] = response_time
                    
                    # Kaydet
                    monitor.save_performance_data(analysis, response_time)
                    model_results.append(analysis)
                    
                    print(f"  ✅ {product['category']}: Skor {analysis['conversion_estimate']:.1f}/10")
                
            except Exception as e:
                print(f"  ❌ {product['category']}: Hata - {str(e)}")
        
        results[model] = model_results
    
    # Karşılaştırma raporu
    print(f"\n📊 KARŞILAŞTIRMA RAPORU")
    print("=" * 50)
    
    for model, model_results in results.items():
        if model_results:
            avg_score = np.mean([r['conversion_estimate'] for r in model_results])
            avg_compliance = np.mean([r['walmart_compliance_score'] for r in model_results])
            avg_response_time = np.mean([r.get('response_time', 0) for r in model_results])
            
            print(f"\n🤖 {model}:")
            print(f"  📈 Ortalama Skor: {avg_score:.1f}/10")
            print(f"  🎯 Walmart Uyumluluk: {avg_compliance:.1f}%")
            print(f"  ⏱️ Yanıt Süresi: {avg_response_time:.1f}s")

if __name__ == "__main__":
    # Karşılaştırmalı test çalıştır
    benchmark_models()
