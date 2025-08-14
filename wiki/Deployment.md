# 🚀 Deployment Rehberi

> **Canlı Ortam Kurulumu** - Production deployment için kapsamlı rehber

## 🎯 Deployment Seçenekleri

### 1. Streamlit Cloud (Ücretsiz) ⭐
```yaml
Avantajları:
  - Tamamen ücretsiz
  - GitHub entegrasyonu
  - Otomatik deployment
  - SSL sertifikası dahil
  - Custom domain desteği

Dezavantajları:
  - Ollama desteği yok
  - Sadece OpenAI kullanılabilir
  - Resource limitleri
  - Public repository gerekli
```

### 2. Heroku (Freemium)
```yaml
Avantajları:
  - Kolay setup
  - Add-on ecosystem
  - Scaling options
  - Database desteği

Dezavantajları:
  - Ollama için memory yetersiz
  - Sleep mode (inactivity)
  - Ücretli planlar pahalı
```

### 3. Railway (Modern)
```yaml
Avantajları:
  - Modern platform
  - GitHub integration
  - Environment variables
  - Better resource limits

Dezavantajları:
  - Yeni platform
  - Limited free tier
  - Ollama için GPU gerekli
```

### 4. VPS/Cloud Server (Tam Kontrol)
```yaml
Avantajları:
  - Tam kontrol
  - Ollama desteği
  - Custom configuration
  - No vendor lock-in

Dezavantajları:
  - Server yönetimi gerekli
  - Security responsibility
  - Backup/monitoring setup
```

## 🌐 Streamlit Cloud Deployment

### Adım 1: Repository Hazırlığı
```bash
# Repository'yi public yapın (GitHub'da)
# Gerekli dosyaların varlığını kontrol edin
ls -la requirements.txt
ls -la walmart.py
ls -la runtime.txt  # Python versiyon belirteci
```

### Adım 2: Streamlit Cloud Setup
1. [share.streamlit.io](https://share.streamlit.io) adresine gidin
2. **GitHub ile giriş** yapın
3. **New app** butonuna tıklayın
4. **Repository seçin**: `yusuf44777/walmart_project_last`
5. **Branch**: `main`
6. **Main file path**: `walmart.py`
7. **Deploy** butonuna tıklayın

### Adım 3: Environment Variables
```python
# Streamlit Cloud'da Secrets kullanın
# .streamlit/secrets.toml oluşturun (local test için)
[general]
OPENAI_API_KEY = "your-api-key-here"
ENVIRONMENT = "production"
ENABLE_DATA_COLLECTION = "false"
```

### Adım 4: Configuration
```python
# walmart.py'de production ayarları
import streamlit as st

def is_production():
    return st.secrets.get("ENVIRONMENT") == "production"

if is_production():
    st.set_page_config(
        page_title="Walmart AI Content Generator",
        page_icon="🛒",
        layout="wide"
    )
```

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health

# Expose port
EXPOSE 8501

# Run command
CMD ["streamlit", "run", "walmart.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

### Docker Compose (Ollama ile)
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - ENVIRONMENT=production
    depends_on:
      - ollama
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  ollama_data:
```

### Build ve Deploy
```bash
# Docker build
docker build -t walmart-ai .

# Local test
docker run -p 8501:8501 walmart-ai

# Docker Hub push
docker tag walmart-ai username/walmart-ai:latest
docker push username/walmart-ai:latest

# Production deploy
docker-compose up -d
```

## ☁️ Cloud Platform Deployments

### AWS EC2
```bash
# EC2 instance oluşturun (t3.medium+ önerilen)
# Security group: 8501, 22 portları

# Instance'a bağlanın
ssh -i your-key.pem ubuntu@your-ec2-ip

# Docker kurulumu
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker ubuntu

# Application deploy
git clone https://github.com/yusuf44777/walmart_project_last.git
cd walmart_project_last
docker-compose up -d

# Nginx reverse proxy (opsiyonel)
sudo apt install nginx -y
```

### Google Cloud Run
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/walmart-ai', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/walmart-ai']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: [
      'run', 'deploy', 'walmart-ai',
      '--image', 'gcr.io/$PROJECT_ID/walmart-ai',
      '--platform', 'managed',
      '--region', 'us-central1',
      '--allow-unauthenticated',
      '--port', '8501',
      '--memory', '2Gi',
      '--cpu', '2'
    ]
```

### Azure Container Instances
```bash
# Resource group oluşturun
az group create --name walmart-rg --location eastus

# Container deploy
az container create \
  --resource-group walmart-rg \
  --name walmart-ai \
  --image your-registry/walmart-ai:latest \
  --ports 8501 \
  --dns-name-label walmart-ai-unique \
  --environment-variables \
    ENVIRONMENT=production \
    OPENAI_API_KEY=$OPENAI_API_KEY
```

## 🔒 Production Security

### Environment Variables
```bash
# .env dosyası (production)
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-long-random-secret-key
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
SENTRY_DSN=your-sentry-dsn

# Güvenlik
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### API Key Management
```python
# secure_config.py
import os
from cryptography.fernet import Fernet

class SecureConfig:
    @staticmethod
    def encrypt_api_key(key: str) -> str:
        """API key şifreleme"""
        f = Fernet(os.environ.get('ENCRYPTION_KEY'))
        return f.encrypt(key.encode()).decode()
    
    @staticmethod
    def decrypt_api_key(encrypted_key: str) -> str:
        """API key çözme"""
        f = Fernet(os.environ.get('ENCRYPTION_KEY'))
        return f.decrypt(encrypted_key.encode()).decode()
```

### SSL/TLS Setup
```nginx
# nginx.conf
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoring ve Analytics

### Application Monitoring
```python
# monitoring.py
import sentry_sdk
from sentry_sdk.integrations.streamlit import StreamlitIntegration

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[StreamlitIntegration()],
    traces_sample_rate=1.0,
    environment=os.environ.get("ENVIRONMENT", "development")
)

# Custom metrics
import logging
import time

class PerformanceMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def track_request(self, model_name, response_time, success):
        self.logger.info(f"Request: model={model_name}, time={response_time}, success={success}")
```

### Health Checks
```python
# health.py
import streamlit as st
import requests
from datetime import datetime

def health_check():
    """System health check"""
    status = {
        "timestamp": datetime.now().isoformat(),
        "status": "healthy",
        "services": {}
    }
    
    # Ollama check
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=5)
        status["services"]["ollama"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        status["services"]["ollama"] = "offline"
    
    # OpenAI check
    if st.secrets.get("OPENAI_API_KEY"):
        status["services"]["openai"] = "configured"
    else:
        status["services"]["openai"] = "not_configured"
    
    return status
```

### Logging Setup
```python
# logging_config.py
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    """Production logging setup"""
    logHandler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s"
    )
    logHandler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    
    # Streamlit specific
    st_logger = logging.getLogger("streamlit")
    st_logger.setLevel(logging.WARNING)
```

## 🔄 CI/CD Pipeline

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest black flake8
        
    - name: Run tests
      run: |
        pytest tests/
        
    - name: Code quality
      run: |
        black . --check
        flake8 .

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Streamlit Cloud
      run: |
        # Streamlit Cloud otomatik deploy yapar
        echo "Deploying to Streamlit Cloud..."
        
    - name: Deploy to Docker Hub
      run: |
        docker build -t ${{ secrets.DOCKER_USERNAME }}/walmart-ai:latest .
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push ${{ secrets.DOCKER_USERNAME }}/walmart-ai:latest
```

### Automated Testing
```python
# tests/test_deployment.py
import pytest
import requests
import time

class TestDeployment:
    def test_app_health(self):
        """Test application health"""
        response = requests.get("https://your-app-url.streamlit.app/_stcore/health")
        assert response.status_code == 200
    
    def test_content_generation(self):
        """Test content generation endpoint"""
        # Integration test
        pass
    
    def test_performance(self):
        """Test response time"""
        start = time.time()
        response = requests.get("https://your-app-url.streamlit.app")
        duration = time.time() - start
        assert duration < 5.0  # 5 second max
```

## 📈 Scaling Strategies

### Horizontal Scaling
```yaml
# kubernetes.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: walmart-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: walmart-ai
  template:
    metadata:
      labels:
        app: walmart-ai
    spec:
      containers:
      - name: walmart-ai
        image: your-registry/walmart-ai:latest
        ports:
        - containerPort: 8501
        env:
        - name: ENVIRONMENT
          value: "production"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

### Load Balancing
```nginx
# nginx-lb.conf
upstream walmart_ai {
    server app1:8501;
    server app2:8501;
    server app3:8501;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://walmart_ai;
        proxy_set_header Host $host;
        
        # Load balancing
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
    }
}
```

## 🔧 Maintenance

### Backup Strategy
```bash
# Database backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz \
    --exclude=venv \
    --exclude=__pycache__ \
    --exclude=.git \
    .
```

### Update Process
```bash
# Zero-downtime deployment
git pull origin main
docker build -t walmart-ai:new .
docker stop walmart-ai-old
docker run --name walmart-ai-new -d walmart-ai:new
# Health check
# Switch DNS/Load Balancer
# Remove old container
```

### Performance Optimization
```python
# optimization.py
import streamlit as st
from functools import lru_cache

# Caching
@st.cache_data(ttl=3600)
def cached_model_response(prompt, model):
    """Cache model responses"""
    return generate_content(prompt, model)

# Connection pooling
@lru_cache(maxsize=1)
def get_openai_client():
    """Singleton OpenAI client"""
    return openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
```

---

## 🎉 Production Ready!

Deployment tamamlandıktan sonra:

- ✅ **Health checks** çalışıyor
- ✅ **Monitoring** aktif
- ✅ **SSL/HTTPS** kurulu
- ✅ **Backup** stratejisi mevcut
- ✅ **CI/CD pipeline** çalışıyor

### Post-Deployment Checklist
- [ ] Domain/DNS ayarları
- [ ] SSL sertifikası
- [ ] Environment variables
- [ ] Database connection
- [ ] Monitoring dashboards
- [ ] Error tracking
- [ ] Performance metrics
- [ ] Backup verification
- [ ] Security audit
- [ ] Documentation update

---

*🚀 Deployment versiyon: 2.0 | 🌐 Platform desteği: 5+ provider | ⏱️ Deployment süresi: 15-60 dk | 📞 DevOps destek: [[Proje Yönetimi]]*
