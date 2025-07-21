# 🌐 Ollama API Wrapper Servisi

## Kendi Ollama API Servisinizi Oluşturun

### 1. DigitalOcean Droplet ($5/ay)

```bash
# Ubuntu 22.04 Droplet oluşturun
# SSH ile bağlanın

# Ollama kurulumu
curl -fsSL https://ollama.ai/install.sh | sh

# Modeli indirin
ollama pull llama3.1:8b
ollama pull walmart-gpt  # Eğer özel modeliniz varsa

# Public API için nginx reverse proxy
sudo apt update
sudo apt install nginx

# Nginx konfigürasyonu
sudo nano /etc/nginx/sites-available/ollama
```

### Nginx Config:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:11434;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. Fly.io (Kolay Deploy)

```dockerfile
# Dockerfile
FROM ollama/ollama:latest

# Model dosyalarını kopyala
COPY models/ /root/.ollama/models/

# Port expose et
EXPOSE 11434

# Ollama'yı başlat
CMD ["ollama", "serve"]
```

```toml
# fly.toml
app = "your-ollama-api"

[build]
  dockerfile = "Dockerfile"

[[services]]
  http_checks = []
  internal_port = 11434
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

### 3. Railway (GPU Destekli)

```yaml
# railway.json
{
  "build": {
    "builder": "DOCKER"
  },
  "deploy": {
    "numReplicas": 1,
    "sleepApplication": false
  }
}
```

### 4. Render (Ücretsiz Tier)

```yaml
# render.yaml
services:
  - type: web
    name: ollama-api
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: OLLAMA_HOST
        value: 0.0.0.0:11434
```
