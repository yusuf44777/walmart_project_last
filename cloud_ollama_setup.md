# 🚀 Cloud'da Ollama Kurulumu

## 1. Google Colab (Ücretsiz GPU)

```python
# Colab'da Ollama kurulumu
!curl -fsSL https://ollama.ai/install.sh | sh
!ollama serve &
!ollama pull llama3.1:8b

# Tunnel ile erişim
!pip install pyngrok
from pyngrok import ngrok
import time

# Ollama'yı başlat
time.sleep(5)
public_url = ngrok.connect(11434)
print(f"Ollama URL: {public_url}")
```

## 2. Kaggle (Ücretsiz GPU)

```bash
# Kaggle Notebook'ta
!curl -fsSL https://ollama.ai/install.sh | sh
!nohup ollama serve > ollama.log 2>&1 &
!sleep 5
!ollama pull llama3.1:8b
```

## 3. RunPod (Uygun Fiyatlı GPU)

- GPU instance kirala ($0.20/saat)
- Ollama kur
- Public API endpoint oluştur

## 4. Vast.ai (En Ucuz GPU)

- Community GPU'lar
- $0.10/saat'den başlayan fiyatlar
- Docker container ile kolay kurulum

## 5. HuggingFace Spaces (GPU)

```python
# requirements.txt
streamlit
ollama-python

# app.py
import subprocess
import time

subprocess.run(["ollama", "serve"], daemon=True)
time.sleep(5)
subprocess.run(["ollama", "pull", "llama3.1:8b"])
```
