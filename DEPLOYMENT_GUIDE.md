# 🚀 MT Expert Optimizer - Local Production Deployment Guide

## 📋 İçindekiler
1. [Sistem Gereksinimleri](#sistem-gereksinimleri)
2. [Kurulum Adımları](#kurulum-adımları)
3. [Production Ortamını Başlatma](#production-ortamını-başlatma)
4. [Demo MT5 Hesabı ile Test](#demo-mt5-hesabı-ile-test)
5. [Monitoring ve Yönetim](#monitoring-ve-yönetim)
6. [Backup ve Restore](#backup-ve-restore)
7. [Sorun Giderme](#sorun-giderme)
8. [Güvenlik Notları](#güvenlik-notları)

---

## 🖥️ Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi**: Windows 10/11 (64-bit)
- **RAM**: 8 GB (16 GB önerilir)
- **Disk**: 50 GB boş alan
- **CPU**: 4 çekirdek (8 çekirdek önerilir)

### Gerekli Yazılımlar
1. **Docker Desktop for Windows** (v4.25+)
   - Download: https://www.docker.com/products/docker-desktop/
   - WSL 2 backend gereklidir
   
2. **Git for Windows**
   - Download: https://git-scm.com/download/win
   
3. **MetaTrader 5 Terminal** (EA çalıştırmak için)
   - Download: https://www.metatrader5.com/en/download

---

## 📦 Kurulum Adımları

### 1. Docker Desktop Kurulumu

```powershell
# Docker Desktop'ı indirip kurun
# Kurulum sonrası bilgisayarı yeniden başlatın
# Docker Desktop'ı açın ve WSL 2 backend'i etkinleştirin
```

**Docker'ın çalıştığını doğrulayın:**
```powershell
docker --version
docker-compose --version
```

### 2. Proje Hazırlığı

```powershell
# Proje dizinine gidin
cd C:\Users\qw\Desktop\expert-adj

# Git durumunu kontrol edin
git status

# Değişiklikleri commit edin (gerekiyorsa)
git add .
git commit -m "Production deployment setup"
```

### 3. Environment Dosyasını Kontrol Edin

`.env.prod` dosyası zaten oluşturuldu ve aşağıdaki bilgileri içeriyor:

- ✅ PostgreSQL yapılandırması
- ✅ Redis yapılandırması
- ✅ MinIO S3 yapılandırması
- ✅ Tickmill Demo MT5 hesap bilgileri
  - **Hesap**: 20266961
  - **Sunucu**: TickmillEU-Demo
- ✅ Grafana admin bilgileri

**⚠️ ÖNEMLİ**: Production ortamında şifreleri mutlaka değiştirin!

### 4. EA Dosyasını Yerleştirin

EA dosyanız zaten mevcut:
```
C:\Users\qw\Desktop\expert-adj\examples\EAs\MASSTER_v3.0_FINAL.ex4
```

Bu dosyayı Docker container'a otomatik olarak mount edeceğiz.

---

## 🚀 Production Ortamını Başlatma

### Adım 1: Docker Compose ile Tüm Servisleri Başlatın

```powershell
# Production docker-compose ile başlatın
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
```

Bu komut aşağıdaki servisleri başlatır:
- ✅ Nginx (Reverse Proxy) - Port 80
- ✅ PostgreSQL (TimescaleDB) - Port 5432
- ✅ Redis (Cache & Queue) - Port 6379
- ✅ MinIO (S3 Storage) - Port 9000, 9001
- ✅ FastAPI Backend - Port 8000
- ✅ Celery Workers (4 replica)
- ✅ Flower (Celery Monitor) - Port 5555
- ✅ Next.js Frontend - Port 3000
- ✅ MT5 Runner Service
- ✅ Prometheus (Metrics) - Port 9090
- ✅ Grafana (Dashboards) - Port 3000

### Adım 2: Servislerin Durumunu Kontrol Edin

```powershell
# Tüm container'ları listeleyin
docker-compose -f docker-compose.prod.yml ps

# Log'ları izleyin
docker-compose -f docker-compose.prod.yml logs -f

# Belirli bir servisin logunu izleyin
docker-compose -f docker-compose.prod.yml logs -f api
```

### Adım 3: Veritabanı Migration

```powershell
# API container'ına bağlanın
docker exec -it mt-optimizer-api bash

# Migration'ları çalıştırın
alembic upgrade head

# Admin kullanıcı oluşturun (backend/scripts/quick_admin.py zaten mevcut)
python backend/scripts/quick_admin.py

# Container'dan çıkın
exit
```

### Adım 4: MinIO Bucket Oluşturma

```powershell
# MinIO Console'a erişin: http://localhost:9001
# Giriş:
#   Username: minioadmin
#   Password: MinIO2025!StorageSecure#Pass

# "ea-files" adında bucket oluşturun
# "backtest-results" adında bucket oluşturun
```

---

## 🧪 Demo MT5 Hesabı ile Test

### 1. MT5 Terminal Kurulumu (Windows)

```powershell
# MetaTrader 5'i indirin ve kurun
# Tickmill Demo hesabınızı ekleyin:
#   Account: 20266961
#   Password: =ə>#qB9RFjzC
#   Server: TickmillEU-Demo
```

### 2. EA Dosyasını MT5'e Yükleyin

```powershell
# MASSTER_v3.0_FINAL.ex4 dosyasını kopyalayın:
# C:\Users\qw\Desktop\expert-adj\examples\EAs\MASSTER_v3.0_FINAL.ex4
# →
# C:\Users\qw\AppData\Roaming\MetaQuotes\Terminal\[TERMINAL_ID]\MQL5\Experts\

# MT5'i yeniden başlatın
```

### 3. Platform'a Giriş ve EA Upload

**Frontend'e erişin:** http://localhost

1. **Login sayfası**
   - Email: `admin@mtoptimizer.local`
   - Password: `Admin2025!SuperSecure#Pass`

2. **Dashboard'a gidin**
   - Sol menüden "Expert Advisors" tıklayın
   
3. **EA Upload**
   - "Upload EA" butonuna tıklayın
   - `MASSTER_v3.0_FINAL.ex4` dosyasını seçin
   - Upload edin

4. **MT5 Hesabı Ekleyin**
   - "Accounts" menüsüne gidin
   - "Add Account" tıklayın
   - Tickmill Demo bilgilerini girin:
     ```
     Name: Tickmill Demo
     Login: 20266961
     Password: =ə>#qB9RFjzC
     Server: TickmillEU-Demo
     Platform: MT5
     ```
   - "Test Connection" butonu ile bağlantıyı test edin

5. **Backtest Oluşturun**
   - "Backtests" menüsüne gidin
   - "New Backtest" tıklayın
   - EA: MASSTER_v3.0_FINAL
   - Account: Tickmill Demo
   - Symbol: EURUSD
   - Timeframe: H1
   - Date Range: 2024-01-01 to 2024-12-31
   - "Start Backtest" tıklayın

---

## 📊 Monitoring ve Yönetim

### 1. Web Arayüzleri

| Servis | URL | Kullanıcı | Şifre |
|--------|-----|-----------|-------|
| **Frontend** | http://localhost | admin@mtoptimizer.local | Admin2025!SuperSecure#Pass |
| **Backend API Docs** | http://localhost/api/docs | - | - |
| **Flower (Celery)** | http://localhost/flower/ | admin | Admin2025 |
| **Grafana** | http://localhost/grafana/ | admin | Grafana2025!Admin#Pass |
| **MinIO Console** | http://localhost:9001 | minioadmin | MinIO2025!StorageSecure#Pass |
| **Prometheus** | http://localhost:9090 | - | - |

### 2. Gerçek Zamanlı Log İzleme

```powershell
# Tüm servislerin logları
docker-compose -f docker-compose.prod.yml logs -f

# Sadece API logları
docker-compose -f docker-compose.prod.yml logs -f api

# Sadece Celery worker logları
docker-compose -f docker-compose.prod.yml logs -f celery-worker

# Sadece Runner logları
docker-compose -f docker-compose.prod.yml logs -f runner
```

### 3. Container Yönetimi

```powershell
# Servisleri durdurun
docker-compose -f docker-compose.prod.yml stop

# Servisleri başlatın
docker-compose -f docker-compose.prod.yml start

# Servisleri yeniden başlatın
docker-compose -f docker-compose.prod.yml restart

# Servisleri tamamen kaldırın (volumes korunur)
docker-compose -f docker-compose.prod.yml down

# Servisleri tamamen kaldırın (volumes dahil)
docker-compose -f docker-compose.prod.yml down -v
```

### 4. Performance Monitoring

**Grafana Dashboard:**
1. http://localhost/grafana/ adresine gidin
2. Login: admin / Grafana2025!Admin#Pass
3. Dashboards → Browse
4. "MT Optimizer" folder'ından dashboard seçin

**Prometheus Metrics:**
- http://localhost:9090
- Query örnekleri:
  ```
  rate(http_requests_total[5m])
  celery_task_succeeded_total
  process_cpu_seconds_total
  ```

---

## 💾 Backup ve Restore

### Otomatik Backup

Production ortamında günlük, haftalık ve aylık backup'lar otomatik olarak alınır.

**Manuel backup:**
```bash
# Git Bash veya WSL kullanarak:
./scripts/backup.sh daily

# Backup dosyaları:
# ./backups/daily/mt_optimizer_daily_YYYYMMDD_HHMMSS.sql.gz
```

**Windows PowerShell için alternatif:**
```powershell
# Docker ile doğrudan backup
docker exec mt-optimizer-db pg_dump -U mt_optimizer -d mt_optimizer_prod | gzip > backups/manual_backup_$(Get-Date -Format "yyyyMMdd_HHmmss").sql.gz
```

### Database Restore

```bash
# Git Bash veya WSL:
./scripts/restore.sh backups/daily/mt_optimizer_daily_20250113_120000.sql.gz
```

**Windows PowerShell için:**
```powershell
# Backup dosyasını decompress edin
gzip -d backups/manual_backup_20250113_120000.sql.gz

# Restore edin
Get-Content backups/manual_backup_20250113_120000.sql | docker exec -i mt-optimizer-db psql -U mt_optimizer -d mt_optimizer_prod
```

---

## 🔧 Sorun Giderme

### Problem 1: Container başlamıyor

```powershell
# Container loglarını kontrol edin
docker-compose -f docker-compose.prod.yml logs [service-name]

# Container'ı yeniden build edin
docker-compose -f docker-compose.prod.yml up -d --build [service-name]
```

### Problem 2: Database bağlantı hatası

```powershell
# PostgreSQL container'ının çalıştığını kontrol edin
docker-compose -f docker-compose.prod.yml ps postgres

# PostgreSQL loglarını kontrol edin
docker-compose -f docker-compose.prod.yml logs postgres

# Manuel bağlantı testi
docker exec -it mt-optimizer-db psql -U mt_optimizer -d mt_optimizer_prod
```

### Problem 3: Frontend API'ye bağlanamıyor

```powershell
# Nginx konfigürasyonunu kontrol edin
docker exec mt-optimizer-nginx nginx -t

# Nginx'i reload edin
docker exec mt-optimizer-nginx nginx -s reload

# API container'ının çalıştığını doğrulayın
curl http://localhost/api/v1/health
```

### Problem 4: Celery worker çalışmıyor

```powershell
# Celery worker loglarını kontrol edin
docker-compose -f docker-compose.prod.yml logs celery-worker

# Redis bağlantısını test edin
docker exec -it mt-optimizer-redis redis-cli -a Redis2025!CacheSecure#Pass PING

# Worker'ları yeniden başlatın
docker-compose -f docker-compose.prod.yml restart celery-worker
```

### Problem 5: MT5 Runner bağlanamıyor

```powershell
# Runner loglarını kontrol edin
docker-compose -f docker-compose.prod.yml logs runner

# MT5 hesap bilgilerini doğrulayın (.env.prod)
# MT5 Terminal'in çalıştığından emin olun
```

### Problem 6: Disk doldu

```powershell
# Docker disk kullanımını kontrol edin
docker system df

# Kullanılmayan image'leri temizleyin
docker image prune -a

# Kullanılmayan volume'leri temizleyin (DİKKAT: Veri kaybı olabilir!)
docker volume prune

# Tüm sistemi temizleyin
docker system prune -a --volumes
```

---

## 🔐 Güvenlik Notları

### 1. Şifre Güvenliği

⚠️ **ÜRETİM ORTAMINDA MUTLAKA DEĞİŞTİRİN:**

```env
# .env.prod dosyasındaki tüm şifreler
POSTGRES_PASSWORD=YourStrongPassword123!
REDIS_PASSWORD=YourRedisPassword456!
MINIO_ROOT_PASSWORD=YourMinIOPassword789!
GRAFANA_PASSWORD=YourGrafanaPassword012!
SECRET_KEY=YourSecretKey345!
```

### 2. Firewall Kuralları

Windows Defender Firewall'da şu portları açın:
- **80**: HTTP (Nginx)
- **443**: HTTPS (Production'da)
- **9001**: MinIO Console (sadece local access)

### 3. SSL/TLS (Gerçek Domain için)

Localhost için SSL gerekmez, ancak gerçek domain için:

```powershell
# Let's Encrypt sertifikası alın
docker-compose -f docker-compose.prod.yml run --rm certbot certonly --webroot -w /var/www/certbot -d yourdomain.com

# Nginx konfigürasyonunu güncelleyin (nginx/nginx.conf)
# HTTPS kısmını aktif edin
```

### 4. Backup Politikası

- **Günlük**: Son 7 gün
- **Haftalık**: Son 4 hafta
- **Aylık**: Son 12 ay

Backup'ları harici disk veya cloud storage'a kopyalayın.

### 5. Monitoring ve Alerts

Grafana'da kritik metrikler için alertler kurun:
- CPU kullanımı > %80
- RAM kullanımı > %90
- Disk kullanımı > %85
- API response time > 5s
- Celery queue size > 1000

---

## 📈 Performans Optimizasyonu

### 1. Resource Limits

Docker Compose'da her servis için resource limitleri ekleyin:

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### 2. Database Tuning

PostgreSQL performansını artırın:

```sql
-- Shared buffers
ALTER SYSTEM SET shared_buffers = '4GB';

-- Work mem
ALTER SYSTEM SET work_mem = '256MB';

-- Maintenance work mem
ALTER SYSTEM SET maintenance_work_mem = '1GB';

-- Effective cache size
ALTER SYSTEM SET effective_cache_size = '12GB';

-- Reload configuration
SELECT pg_reload_conf();
```

### 3. Redis Optimization

```bash
# Redis maxmemory zaten ayarlandı (2GB)
# Eviction policy: allkeys-lru (en az kullanılanları sil)
```

---

## 🎉 Başarılı Deployment Sonrası

Tebrikler! MT Expert Optimizer platformunuz production ortamında çalışıyor.

### Sonraki Adımlar:

1. ✅ **Test edin**: Demo hesap ile backtest çalıştırın
2. ✅ **Monitor edin**: Grafana dashboard'ları kontrol edin
3. ✅ **Optimize edin**: Genetic Algorithm ile EA parametrelerini optimize edin
4. ✅ **Geliştirin**: Yeni özellikler ekleyin (AI, 3D visualization, vb.)
5. ✅ **Paylaşın**: Community ile sonuçlarınızı paylaşın

### Destek ve İletişim:

- 📧 Email: admin@mtoptimizer.local
- 🐛 Issues: GitHub repository
- 📚 Docs: http://localhost/docs
- 💬 Community: Discord/Telegram (gelecekte)

---

## 📝 Changelog

- **2025-11-13**: Initial production deployment setup
  - Docker Compose production configuration
  - Monitoring stack (Prometheus + Grafana)
  - Backup/restore scripts
  - Localhost nginx configuration
  - Tickmill Demo MT5 integration

---

**🚀 Happy Trading & Optimizing!**
