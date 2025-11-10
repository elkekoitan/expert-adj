# 🚀 MT Expert Optimizer

> **Otomatik EA Optimizasyon ve Test Platformu**
> MetaTrader 4/5 Expert Advisor'ları için tam otomatik parametre optimizasyonu, backtest ve live trading yönetimi.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 20+](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Mimari](#-mimari)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Dokümantasyon](#-dokümantasyon)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

---

## ✨ Özellikler

### 🤖 EA Yönetimi
- ✅ Drag & drop EA yükleme (.ex4, .ex5, .mq4, .mq5)
- ✅ Otomatik parametre çıkarımı
- ✅ Versiyon kontrolü
- ✅ EA kütüphane yönetimi

### ⚡ Otomatik Optimizasyon
- ✅ **Genetic Algorithm** - Popülasyon tabanlı optimizasyon
- ✅ **Bayesian Optimization** - Akıllı parametre tarama
- ✅ **Grid Search** - Exhaustive arama
- ✅ **Random Search** - Hızlı keşif
- ✅ **Walk-Forward Analysis** - Overfitting önleme
- ✅ **Multi-Symbol Testing** - En iyi market keşfi

### 📊 Backtest Engine
- ✅ MT5 Strategy Tester entegrasyonu
- ✅ Paralel backtest işleme
- ✅ Detaylı performans metrikleri
- ✅ Equity curve analizi
- ✅ Risk metrikleri (Sharpe, Sortino, Calmar)

### 🎯 Live Trading
- ✅ Demo hesap bağlantısı
- ✅ Otomatik EA deployment
- ✅ Real-time performans izleme
- ✅ Otomatik re-optimizasyon
- ✅ Alert sistemi

### 🎨 Modern Web UI
- ✅ Responsive dashboard
- ✅ Interactive charts (TradingView)
- ✅ Real-time updates (WebSocket)
- ✅ Kolay kullanım

### 🔐 Güvenlik
- ✅ JWT authentication
- ✅ 2FA support
- ✅ RBAC (Role-Based Access Control)
- ✅ Encrypted credentials
- ✅ Audit logging

---

## 🏗️ Mimari

```
┌─────────────────────────────────────────────────────────────┐
│                      WEB FRONTEND                           │
│              React + Next.js + TailwindCSS                  │
└────────────────────┬────────────────────────────────────────┘
                     │ REST API / WebSocket
┌────────────────────▼────────────────────────────────────────┐
│                   API GATEWAY (Kong)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬────────────┐
        │            │            │            │
┌───────▼──┐  ┌─────▼────┐  ┌────▼────┐  ┌───▼──────┐
│   EA     │  │ Backtest │  │  Optim  │  │  Trading │
│ Service  │  │ Service  │  │ Service │  │  Service │
└───────┬──┘  └─────┬────┘  └────┬────┘  └───┬──────┘
        │            │            │            │
        └────────────┼────────────┴────────────┘
                     │
        ┌────────────▼─────────────────────────────┐
        │    MESSAGE QUEUE (Redis + Celery)        │
        └────────────┬─────────────────────────────┘
                     │
        ┌────────────▼─────────────────────────────┐
        │         MT5 RUNNER AGENTS                │
        │   (Python MT5 Terminal Controllers)      │
        └────────────┬─────────────────────────────┘
                     │
        ┌────────────▼─────────────────────────────┐
        │   MT4/MT5 TERMINALS (Windows/Wine)       │
        └──────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                    DATA LAYER                            │
│  PostgreSQL │ TimescaleDB │ Redis │ S3/MinIO            │
└──────────────────────────────────────────────────────────┘
```

### Tech Stack

**Backend**
- Python 3.11+ (FastAPI)
- PostgreSQL 15 + TimescaleDB
- Redis 7 (Cache + Queue)
- Celery (Task Queue)
- SQLAlchemy (ORM)

**Frontend**
- React 18
- Next.js 14 (App Router)
- TailwindCSS + shadcn/ui
- TanStack Query
- Socket.IO

**Infrastructure**
- Docker + Docker Compose
- Kubernetes (production)
- GitHub Actions (CI/CD)
- Prometheus + Grafana

---

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Docker & Docker Compose
- Git
- (Opsiyonel) MT5 Terminal (Windows veya Wine)

### 1. Repo'yu Clone'la

```bash
git clone https://github.com/yourusername/expert-adj.git
cd expert-adj
```

### 2. Environment Variables

```bash
cp .env.example .env
# .env dosyasını düzenle
```

### 3. Docker ile Çalıştır

```bash
docker-compose up -d
```

### 4. Veritabanı Migration

```bash
docker-compose exec api alembic upgrade head
```

### 5. Tarayıcıda Aç

```
http://localhost:3000
```

**Varsayılan Giriş**:
- Email: `admin@example.com`
- Password: `admin123`

---

## 📦 Kurulum

### Development Ortamı

#### Backend Setup

```bash
# Virtual environment oluştur
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies yükle
pip install -r requirements.txt

# Database migration
alembic upgrade head

# Development server çalıştır
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

#### MT5 Runner Setup

```bash
cd runner
pip install -r requirements.txt
python runner.py
```

### Production Deployment

```bash
# Build Docker images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# SSL sertifikası (Let's Encrypt)
./scripts/setup-ssl.sh
```

---

## 📖 Kullanım

### 1. EA Yükleme

```bash
# Web UI üzerinden
Dashboard → EA Library → Upload EA

# API ile
curl -X POST http://localhost:8000/api/v1/eas/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@SmartMartingale.ex5"
```

### 2. Optimizasyon Başlatma

```python
# Python SDK
from mt_optimizer import Client

client = Client(api_key="YOUR_API_KEY")

# Optimizasyon yapılandırması
optimization = client.optimize(
    ea_id="ea-123",
    symbols=["EURUSD", "GBPUSD"],
    timeframes=["M15", "H1"],
    date_from="2020-01-01",
    date_to="2024-12-31",
    method="genetic",  # veya "bayesian", "grid", "random"
    metric="profit_factor",
    walk_forward=True
)

# Sonuçları bekle
results = optimization.wait()
print(f"Best config: {results.best_config}")
print(f"Profit Factor: {results.profit_factor}")
```

### 3. Live Trading

```python
# Demo hesaba deploy
deployment = client.deploy(
    ea_id="ea-123",
    config_id="config-456",
    account_id="demo-789",
    symbol="EURUSD",
    timeframe="M15"
)

# Monitoring
for update in deployment.stream():
    print(f"P&L: {update.pnl}")
    print(f"DD: {update.drawdown}%")
```

---

## 📚 Dokümantasyon

### API Dokümantasyonu
- [REST API Reference](docs/api/rest.md)
- [WebSocket API](docs/api/websocket.md)
- [Python SDK](docs/sdk/python.md)
- [Authentication](docs/api/auth.md)

### Kullanıcı Kılavuzları
- [EA Yükleme Rehberi](docs/guides/upload-ea.md)
- [Optimizasyon Stratejileri](docs/guides/optimization.md)
- [Backtest Sonuçlarını Okuma](docs/guides/reading-results.md)
- [Live Trading Kurulumu](docs/guides/live-trading.md)

### Geliştirici Dökümanları
- [Architecture Overview](docs/dev/architecture.md)
- [Database Schema](docs/dev/database.md)
- [Contributing Guide](CONTRIBUTING.md)
- [API Design](docs/dev/api-design.md)

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up
```

---

## 📊 Proje Yapısı

```
expert-adj/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core config
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── alembic/            # DB migrations
│   ├── tests/
│   └── requirements.txt
│
├── frontend/               # Next.js frontend
│   ├── app/               # App router
│   ├── components/        # React components
│   ├── lib/               # Utilities
│   ├── public/            # Static files
│   └── package.json
│
├── runner/                # MT5 runner service
│   ├── mt5_controller.py  # Terminal controller
│   ├── backtest.py        # Backtest engine
│   ├── optimizer.py       # Optimization algorithms
│   └── requirements.txt
│
├── shared/                # Shared code
│   └── schemas/           # Shared schemas
│
├── docs/                  # Documentation
│   ├── api/
│   ├── guides/
│   └── dev/
│
├── scripts/               # Utility scripts
│   ├── setup-ssl.sh
│   └── backup.sh
│
├── docker/               # Docker files
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── runner.Dockerfile
│
├── k8s/                  # Kubernetes manifests
│   ├── api/
│   ├── frontend/
│   └── runner/
│
├── .github/
│   └── workflows/        # CI/CD pipelines
│
├── docker-compose.yml    # Development
├── docker-compose.prod.yml
├── PRD.md               # Product Requirements
└── README.md            # This file
```

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen [Contributing Guide](CONTRIBUTING.md)'ı okuyun.

### Development Workflow

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

### Commit Convention

[Conventional Commits](https://www.conventionalcommits.org/) kullanıyoruz:

```
feat: Yeni özellik
fix: Bug düzeltmesi
docs: Dokümantasyon
style: Kod formatı
refactor: Kod iyileştirme
test: Test ekleme/düzeltme
chore: Build/config değişiklikleri
```

---

## 📈 Roadmap

### ✅ Phase 1: MVP (Completed)
- [x] Basic API structure
- [x] EA upload & management
- [x] Simple backtest
- [x] Web UI prototype

### 🚧 Phase 2: Advanced Features (In Progress)
- [x] Genetic algorithm optimization
- [x] Walk-forward analysis
- [ ] Multi-symbol testing
- [ ] Real-time monitoring

### 📋 Phase 3: Live Trading (Planned)
- [ ] Demo account integration
- [ ] Auto-deployment
- [ ] Alert system
- [ ] Performance tracking

### 🔮 Phase 4: ML & Scale (Future)
- [ ] ML-based optimization
- [ ] Market regime detection
- [ ] Ensemble trading
- [ ] Mobile app

---

## 🐛 Bilinen Sorunlar

- MT5 terminal Linux'ta Wine ile çalışırken bazen stabil değil
- Walk-forward analysis > 10 yıl veri ile yavaş olabiliyor
- WebSocket reconnection bazen gecikebiliyor

[Tüm issues](https://github.com/yourusername/expert-adj/issues)

---

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 👥 Ekip

- **Lead Developer**: [@yourusername](https://github.com/yourusername)
- **Contributors**: [All contributors](https://github.com/yourusername/expert-adj/graphs/contributors)

---

## 🙏 Teşekkürler

- [MetaTrader 5](https://www.metatrader5.com/) - Trading platform
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Next.js](https://nextjs.org/) - Frontend framework
- [TradingView](https://www.tradingview.com/) - Charting library

---

## 📞 İletişim

- **Website**: [mtoptimizer.com](https://mtoptimizer.com)
- **Email**: support@mtoptimizer.com
- **Discord**: [Join our community](https://discord.gg/mtoptimizer)
- **Twitter**: [@mtoptimizer](https://twitter.com/mtoptimizer)

---

## ⭐ Destek

Projeyi beğendiyseniz ⭐ vermeyi unutmayın!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/expert-adj&type=Date)](https://star-history.com/#yourusername/expert-adj&Date)

---

**Made with ❤️ by traders, for traders**
