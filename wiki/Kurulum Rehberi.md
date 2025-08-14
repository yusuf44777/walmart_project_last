# 🛠️ Kurulum Rehberi

> **Geliştiriciler İçin** - Detaylı kurulum ve geliştirme ortamı hazırlığı

## 🎯 Geliştirici Profilleri

### 👨‍💻 Backend Developer
- **Focus**: API entegrasyonu, model training
- **Skills**: Python, AI/ML, API design
- **Setup Time**: 15-20 dakika

### 🎨 Frontend Developer  
- **Focus**: UI/UX, Streamlit customization
- **Skills**: Python, HTML/CSS, JavaScript
- **Setup Time**: 10-15 dakika

### 🤖 AI/ML Engineer
- **Focus**: Model optimization, training pipeline
- **Skills**: PyTorch, Transformers, MLOps
- **Setup Time**: 30-45 dakika

### 🏢 DevOps Engineer
- **Focus**: Deployment, monitoring, scaling
- **Skills**: Docker, CI/CD, Cloud platforms
- **Setup Time**: 25-30 dakika

## 📋 Sistem Gereksinimleri

### Minimum Gereksinimler
```yaml
Hardware:
  CPU: 2 cores, 2.0GHz
  RAM: 4GB
  Storage: 10GB SSD
  Network: Stable internet connection

Software:
  OS: Windows 10, macOS 10.15, Ubuntu 18.04+
  Python: 3.11.0+
  Git: 2.30+
  IDE: VS Code, PyCharm, or similar
```

### Önerilen Gereksinimler
```yaml
Hardware:
  CPU: 8 cores, 3.0GHz (Intel i7/AMD Ryzen 7)
  RAM: 16GB DDR4
  Storage: 50GB NVMe SSD
  GPU: NVIDIA RTX 3060+ (AI model training için)

Software:
  OS: Latest versions
  Python: 3.11.5
  Docker: 24.0+
  IDE: VS Code with Python extensions
```

## 🔧 Geliştirme Ortamı Kurulumu

### 1. Repository Setup
```bash
# Repository'yi fork edin (GitHub'da)
# Sonra local'e klonlayın
git clone https://github.com/[YOUR_USERNAME]/walmart_project_last.git
cd walmart_project_last

# Remote upstream ayarlayın
git remote add upstream https://github.com/yusuf44777/walmart_project_last.git

# Branch'leri kontrol edin
git branch -a
```

### 2. Python Ortamı
```bash
# Python versiyonunu kontrol edin
python --version  # 3.11.0+ olmalı

# Virtual environment oluşturun
python -m venv venv_dev

# Aktif edin
source venv_dev/bin/activate  # macOS/Linux
# veya
venv_dev\Scripts\activate     # Windows

# pip güncelleyin
pip install --upgrade pip setuptools wheel
```

### 3. Dependencies Installation
```bash
# Development dependencies
pip install -r requirements-dev.txt

# Production dependencies
pip install -r requirements.txt

# Development tools
pip install black isort flake8 pytest mypy

# Documentation tools
pip install mkdocs mkdocs-material

# Jupyter for experimentation
pip install jupyter ipykernel
```

### 4. Environment Variables
```bash
# .env dosyası oluşturun
touch .env

# .env içeriği:
ENVIRONMENT=development
DEBUG=true
OPENAI_API_KEY=your_openai_key_here
OLLAMA_BASE_URL=http://localhost:11434
ENABLE_DATA_COLLECTION=true
LOG_LEVEL=DEBUG
```

### 5. Pre-commit Hooks
```bash
# Pre-commit kurulumu
pip install pre-commit

# Hooks'ları aktif edin
pre-commit install

# Manuel test
pre-commit run --all-files
```

## 🤖 AI Model Kurulumu

### Ollama (Local Development)
```bash
# macOS Kurulum
brew install ollama

# Linux Kurulum
curl -fsSL https://ollama.ai/install.sh | sh

# Windows Kurulum
# https://ollama.ai/download adresinden indirin

# Servis başlatma
ollama serve

# Model indirme
ollama pull llama3.1:8b      # Base model (4GB)
ollama pull codellama:7b     # Code generation (4GB)
ollama pull mistral:7b       # Alternative model (4GB)

# Model listesi
ollama list
```

### Custom Model Setup
```bash
# Walmart modellerini oluştur
python create_walmart_model.py

# Model test
python test_ollama.py

# Performance analizi
python model_analytics.py
```

## 📊 Database Setup

### SQLite (Development)
```bash
# Database dosyası otomatik oluşturulur
# İlk çalıştırmada training_data.json oluşur

# Database schema kontrolü
python -c "
import sqlite3
conn = sqlite3.connect('model_performance.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=table;')
print(cursor.fetchall())
"
```

### PostgreSQL (Production Ready)
```bash
# Docker ile PostgreSQL
docker run --name walmart-postgres \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=walmart_db \
  -p 5432:5432 \
  -d postgres:15

# Connection string
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/walmart_db
```

## 🧪 Testing Setup

### Unit Tests
```bash
# Test dizinini oluşturun
mkdir tests
touch tests/__init__.py
touch tests/test_walmart.py
touch tests/test_api.py
touch tests/test_models.py

# Test çalıştırma
pytest tests/ -v

# Coverage raporu
pytest --cov=. tests/

# Specific test
pytest tests/test_walmart.py::test_content_generation -v
```

### Integration Tests
```bash
# API endpoint testleri
python -m pytest tests/test_api.py

# Model performance testleri
python -m pytest tests/test_models.py

# End-to-end testleri
python -m pytest tests/test_e2e.py
```

## 🔍 Development Tools

### IDE Setup (VS Code)
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv_dev/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### Extensions
```bash
# VS Code extensions
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
code --install-extension ms-python.isort
code --install-extension ms-python.flake8
code --install-extension ms-toolsai.jupyter
```

### Debug Configuration
```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Streamlit App",
            "type": "python",
            "request": "launch",
            "program": "venv_dev/bin/streamlit",
            "args": ["run", "walmart.py"],
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

## 🔧 Advanced Configuration

### Docker Development
```dockerfile
# Dockerfile.dev
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements*.txt ./

# Install Python dependencies
RUN pip install -r requirements-dev.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8501

# Development command
CMD ["streamlit", "run", "walmart.py", "--server.address", "0.0.0.0"]
```

```bash
# Docker build ve run
docker build -f Dockerfile.dev -t walmart-dev .
docker run -p 8501:8501 -v $(pwd):/app walmart-dev
```

### Docker Compose
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8501:8501"
    volumes:
      - .:/app
      - /app/venv_dev
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: devpass
      POSTGRES_DB: walmart_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

## 📈 Performance Monitoring

### Local Monitoring
```bash
# Memory usage monitoring
pip install memory-profiler

# Profile script
python -m memory_profiler walmart.py

# CPU profiling
pip install py-spy
py-spy record -o profile.svg -- python walmart.py
```

### Production Monitoring
```bash
# APM tools
pip install sentry-sdk
pip install newrelic

# Logging
pip install structlog
pip install python-json-logger
```

## 🚀 Development Workflow

### Git Workflow
```bash
# Feature development
git checkout -b feature/new-feature
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature

# Pull request oluşturun
# Code review bekleyin
# Merge sonrası cleanup
git checkout main
git pull upstream main
git branch -d feature/new-feature
```

### Code Quality
```bash
# Linting
flake8 walmart.py
black walmart.py --check
isort walmart.py --check-only

# Type checking
mypy walmart.py

# Security scan
pip install bandit
bandit -r .
```

### Continuous Integration
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

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
        pip install -r requirements-dev.txt
        
    - name: Run tests
      run: |
        pytest tests/ --cov=.
        
    - name: Code quality
      run: |
        flake8 .
        black . --check
```

## 🔒 Security Setup

### API Key Management
```python
# config.py
import os
from typing import Optional

class SecurityConfig:
    @staticmethod
    def get_api_key(service: str) -> Optional[str]:
        """Secure API key retrieval"""
        key = os.getenv(f'{service.upper()}_API_KEY')
        if not key:
            raise ValueError(f"Missing {service} API key")
        return key
    
    @staticmethod
    def validate_api_key(key: str, service: str) -> bool:
        """API key validation"""
        # Implementation specific to service
        pass
```

### Input Validation
```python
# validators.py
from typing import List, Dict, Any
import re

class InputValidator:
    @staticmethod
    def validate_product_name(name: str) -> bool:
        """Product name validation"""
        if not name or len(name) < 3:
            return False
        if len(name) > 200:
            return False
        return True
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Input sanitization"""
        # Remove dangerous characters
        return re.sub(r'[<>"\']', '', text)
```

## 📚 Documentation

### Code Documentation
```python
# walmart.py example
def generate_content(
    product_name: str,
    features: List[str],
    model: str = "ollama"
) -> Dict[str, Any]:
    """
    Generate product content using AI models.
    
    Args:
        product_name: Name of the product
        features: List of product features
        model: AI model to use ('ollama' or 'openai')
        
    Returns:
        Dict containing generated title, features, and description
        
    Raises:
        ValueError: If input validation fails
        APIError: If AI model request fails
        
    Example:
        >>> content = generate_content(
        ...     "iPhone 15",
        ...     ["128GB", "Blue", "A17 chip"],
        ...     "ollama"
        ... )
        >>> print(content['title'])
        "Apple iPhone 15 - 128GB Blue with A17 Chip"
    """
    pass
```

### API Documentation
```bash
# FastAPI docs (gelecek için)
pip install fastapi uvicorn

# Swagger/OpenAPI otomatik oluşur
# http://localhost:8000/docs
```

## 🎯 Development Best Practices

### Code Structure
```
walmart_project_last/
├── app/
│   ├── __init__.py
│   ├── main.py           # Streamlit app
│   ├── api/              # API endpoints
│   ├── models/           # AI model wrappers
│   ├── utils/            # Utility functions
│   └── config/           # Configuration
├── tests/
├── docs/
├── scripts/              # Deployment scripts
└── requirements/
    ├── base.txt
    ├── dev.txt
    └── prod.txt
```

### Error Handling
```python
# error_handlers.py
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom API error"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def handle_api_error(func):
    """Decorator for API error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"API Error: {str(e)}")
            raise APIError(f"API request failed: {str(e)}")
    return wrapper
```

### Configuration Management
```python
# config.py
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App settings
    app_name: str = "Walmart AI Content Generator"
    debug: bool = False
    
    # API settings
    openai_api_key: Optional[str] = None
    ollama_base_url: str = "http://localhost:11434"
    
    # Database
    database_url: str = "sqlite:///./walmart.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 🎉 Kurulum Tamamlandı!

Geliştirme ortamınız hazır. Şimdi şunları yapabilirsiniz:

1. **📝 İlk kodunuzu yazın** - `git checkout -b feature/my-feature`
2. **🧪 Testleri çalıştırın** - `pytest tests/`
3. **🚀 Uygulamayı başlatın** - `streamlit run walmart.py`
4. **📊 Performansı izleyin** - Monitoring dashboard'ları
5. **🔄 CI/CD pipeline** - Automated testing ve deployment

### Sonraki Adımlar
- [[API Dokümantasyonu]] - REST API endpoints
- [[Model Eğitimi]] - Custom model development
- [[Deployment]] - Production deployment guide
- [[Proje Yönetimi]] - Development workflow

---

*🛠️ Setup versiyon: 2.1 | ⏱️ Kurulum süresi: 15-45 dk | 🎯 Başarı oranı: %98 | 📞 Destek: Development team*
