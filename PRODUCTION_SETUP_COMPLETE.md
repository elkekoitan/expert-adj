# ✅ MT Expert Optimizer - Production Setup Complete!

## 🎉 Tebrikler! Production ortamı hazır!

Projeniz kendi bilgisayarınızda (localhost) production ortamında çalışmaya hazır.

---

## 📦 Oluşturulan Dosyalar

### 1. Configuration Files

| Dosya | Açıklama |
|-------|----------|
| ✅ `.env.prod` | Production environment variables (Tickmill Demo hesap bilgileri dahil) |
| ✅ `docker-compose.prod.local.yml` | Localhost için optimize edilmiş Docker Compose |
| ✅ `nginx/nginx.local.conf` | Localhost Nginx konfigürasyonu (SSL olmadan) |
| ✅ `nginx/.htpasswd` | Flower basic auth dosyası |

### 2. Monitoring & Metrics

| Dosya | Açıklama |
|-------|----------|
| ✅ `monitoring/prometheus.yml` | Prometheus metrics konfigürasyonu |
| ✅ `monitoring/grafana-datasources.yml` | Grafana veri kaynakları |
| ✅ `monitoring/grafana-dashboards/dashboards.yml` | Dashboard provisioning |

### 3. Backup & Maintenance

| Dosya | Açıklama |
|-------|----------|
| ✅ `scripts/backup.sh` | Otomatik database backup script |
| ✅ `scripts/restore.sh` | Database restore script |
| ✅ `backups/` | Backup klasörü (otomatik oluşturulacak) |
| ✅ `results/` | Backtest sonuçları klasörü |

### 4. Quick Start Scripts (Windows)

| Dosya | Açıklama |
|-------|----------|
| ✅ `START_PRODUCTION.bat` | Tüm servisleri başlat |
| ✅ `STOP_PRODUCTION.bat` | Tüm servisleri durdur |
| ✅ `VIEW_LOGS.bat` | Real-time log görüntüle |

### 5. Documentation

| Dosya | Açıklama |
|-------|----------|
| ✅ `README_PRODUCTION.md` | Production deployment ana doküman |
| ✅ `QUICKSTART.md` | 5 dakikada başlangıç rehberi |
| ✅ `DEPLOYMENT_GUIDE.md` | Detaylı deployment klavuzu |
| ✅ `PRODUCTION_SETUP_COMPLETE.md` | Bu dosya (kurulum özeti) |

---

## 🚀 Hemen Başlamak İçin

### Seçenek 1: Windows Batch Script (En Kolay)

```powershell
# Çift tıklayın:
START_PRODUCTION.bat
```

### Seçenek 2: Manuel Docker Compose

```powershell
# Proje klasörüne gidin
cd C:\Users\qw\Desktop\expert-adj

# Production servisleri başlatın
docker-compose -f docker-compose.prod.local.yml --env-file .env.prod up -d --build

# 2-3 dakika bekleyin, sonra tarayıcıda açın:
start http://localhost
```

---

## 🔑 Erişim Bilgileri

### Web Arayüzleri

| Servis | URL | Kullanıcı | Şifre |
|--------|-----|-----------|-------|
| **Frontend** | http://localhost | admin@mtoptimizer.local | Admin2025!SuperSecure#Pass |
| **API Docs** | http://localhost/api/docs | - | - |
| **Flower** | http://localhost/flower/ | admin | Admin2025 |
| **Grafana** | http://localhost/grafana/ | admin | Grafana2025!Admin#Pass |
| **MinIO** | http://localhost:9001 | minioadmin | MinIO2025!StorageSecure#Pass |
| **Prometheus** | http://localhost:9090 | - | - |

### MT5 Demo Hesap (Tickmill)

```
Hesap Numarası: 20266961
Şifre: =ə>#qB9RFjzC
Yatırımcı Şifresi: cJ78Y9O8nKtZ
Sunucu: TickmillEU-Demo
Tür: Raw
Para Birimi: USD
```

**Demo Hesap Yatırımcı Şifresi:** Salt okunur erişim için kullanabilirsiniz.

### EA Dosyası

```
Konum: C:\Users\qw\Desktop\expert-adj\examples\EAs\MASSTER_v3.0_FINAL.ex4
Otomatik Mount: Docker container'a otomatik olarak /app/ea_files klasörüne mount edilir
```

---

## 📋 İlk Kez Çalıştırma Checklist

### 1. Docker Hazırlığı
- [ ] Docker Desktop yüklü ve çalışıyor
- [ ] WSL 2 backend aktif
- [ ] En az 8 GB RAM ayrılmış

### 2. Servisleri Başlatma
- [ ] `START_PRODUCTION.bat` çalıştırıldı
- [ ] Tüm container'lar başladı (docker ps ile kontrol)
- [ ] Loglar temiz (VIEW_LOGS.bat ile kontrol)

### 3. Database Initialization
```powershell
# API container'ına bağlanın
docker exec -it mt-optimizer-api bash

# Migration çalıştırın
alembic upgrade head

# Admin kullanıcı oluşturun
python backend/scripts/quick_admin.py

# Çıkın
exit
```

### 4. MinIO Bucket Setup
- [ ] http://localhost:9001 açıldı
- [ ] minioadmin / MinIO2025!StorageSecure#Pass ile giriş yapıldı
- [ ] "ea-files" bucket oluşturuldu
- [ ] "backtest-results" bucket oluşturuldu

### 5. Frontend Test
- [ ] http://localhost açıldı
- [ ] Login başarılı
- [ ] Dashboard görüntülendi
- [ ] WebSocket bağlantısı aktif (real-time updates çalışıyor)

### 6. EA Upload Test
- [ ] "Expert Advisors" menüsüne girildi
- [ ] MASSTER_v3.0_FINAL.ex4 upload edildi
- [ ] Parametre extractionu başarılı

### 7. MT5 Hesap Ekleme
- [ ] "Accounts" menüsüne girildi
- [ ] Tickmill Demo hesap bilgileri girildi
- [ ] "Test Connection" başarılı (yeşil ✓)

### 8. İlk Backtest
- [ ] "Backtests" menüsüne girildi
- [ ] Yeni backtest oluşturuldu
- [ ] EA, account, symbol seçildi
- [ ] Backtest başlatıldı
- [ ] Real-time progress görüntülendi
- [ ] Sonuçlar başarıyla gösterildi

---

## 🔧 Servis Durumu Kontrolü

```powershell
# Tüm container'ları listele
docker-compose -f docker-compose.prod.local.yml ps

# Beklenen çıktı (örnek):
NAME                        STATUS          PORTS
mt-optimizer-nginx          Up              0.0.0.0:80->80/tcp
mt-optimizer-frontend       Up              3000/tcp
mt-optimizer-api            Up              8000/tcp
mt-optimizer-db             Up (healthy)    5432/tcp
mt-optimizer-redis          Up (healthy)    6379/tcp
mt-optimizer-minio          Up              9000-9001/tcp
mt-optimizer-celery         Up              
mt-optimizer-flower         Up              5555/tcp
mt-optimizer-runner         Up              
mt-optimizer-prometheus     Up              9090/tcp
mt-optimizer-grafana        Up              3000/tcp
```

**Önemli:** Postgres ve Redis "healthy" durumunda olmalı!

---

## 📊 Monitoring & Logs

### Real-time Logs

```powershell
# Tüm servislerin logları
VIEW_LOGS.bat

# Veya belirli bir servis:
docker-compose -f docker-compose.prod.local.yml logs -f api
docker-compose -f docker-compose.prod.local.yml logs -f celery-worker
docker-compose -f docker-compose.prod.local.yml logs -f runner
```

### Grafana Dashboards

1. http://localhost/grafana/ → Login (admin / Grafana2025!Admin#Pass)
2. Dashboards → Browse
3. "MT Optimizer" folder'ından ilgili dashboard'u seç

**Recommended Dashboards:**
- System Overview
- API Performance
- Celery Worker Metrics
- Database Performance

### Prometheus Queries

http://localhost:9090 → Graph

```promql
# API request rate
rate(http_requests_total[5m])

# Celery task success rate
rate(celery_task_succeeded_total[5m])

# Database connections
pg_stat_database_numbackends

# Redis memory usage
redis_memory_used_bytes
```

---

## 💾 Backup Stratejisi

### Otomatik Backup (Önerilen)

Windows Task Scheduler ile günlük backup kurun:

```powershell
# Git Bash veya WSL ile:
cd C:\Users\qw\Desktop\expert-adj
./scripts/backup.sh daily
```

**Backup Schedule:**
- **Daily**: 7 gün saklanır
- **Weekly**: 30 gün saklanır
- **Monthly**: 365 gün saklanır

### Manuel Backup

```powershell
# PowerShell ile:
docker exec mt-optimizer-db pg_dump -U mt_optimizer -d mt_optimizer_prod | gzip > backups/manual_$(Get-Date -Format "yyyyMMdd_HHmmss").sql.gz
```

### Cloud Backup (İsteğe Bağlı)

Backups klasörünü Google Drive, Dropbox veya OneDrive ile senkronize edin.

---

## 🔐 Güvenlik Kontrol Listesi

### Localhost Deployment (Mevcut Durum)

- [x] Environment dosyası (.env.prod) git'e commit edilmedi
- [x] Güçlü şifreler kullanıldı
- [x] Basic auth (Flower) aktif
- [x] CORS sadece localhost'a izin veriyor
- [ ] **TODO**: Firewall kuralları ayarlandı

### Production Server'a Geçiş İçin (Gelecek)

- [ ] Tüm default şifreler değiştirildi
- [ ] SSL/TLS sertifikası kuruldu (Let's Encrypt)
- [ ] Firewall kuralları aktif
- [ ] Rate limiting yapılandırıldı
- [ ] Database encryption at rest
- [ ] Regular security audits

---

## 🐛 Bilinen Sorunlar ve Çözümler

### Problem: Port 80 zaten kullanımda

**Çözüm:**
```yaml
# docker-compose.prod.local.yml dosyasında nginx portunu değiştirin:
ports:
  - "8080:80"  # 80 yerine 8080 kullan
```

Sonra http://localhost:8080 ile erişin.

### Problem: Docker build çok yavaş (Windows)

**Çözüm:**
1. Docker Desktop → Settings → Resources
2. CPU: 4+ çekirdek
3. Memory: 8+ GB
4. Swap: 2 GB
5. WSL 2 integration aktif

### Problem: Container'lar sürekli restart oluyor

**Çözüm:**
```powershell
# Loglara bakın
docker-compose -f docker-compose.prod.local.yml logs [service-name]

# Database bağlantısı kontrolü
docker exec -it mt-optimizer-db psql -U mt_optimizer -d mt_optimizer_prod

# Redis bağlantısı kontrolü
docker exec -it mt-optimizer-redis redis-cli -a Redis2025!CacheSecure#Pass PING
```

### Problem: MT5 Runner bağlanamıyor

**Çözüm:**
1. MetaTrader 5 Terminal yüklü olmalı
2. Demo hesap aktif olmalı
3. .env.prod dosyasında MT5 bilgileri doğru olmalı
4. Runner container loglarını kontrol edin

---

## 📈 Performance Tuning

### Docker Resource Limits

```yaml
# docker-compose.prod.local.yml içinde her servis için:
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
    reservations:
      cpus: '1'
      memory: 2G
```

### PostgreSQL Optimization

```sql
-- Container içinde:
docker exec -it mt-optimizer-db psql -U mt_optimizer -d mt_optimizer_prod

-- Shared buffers
ALTER SYSTEM SET shared_buffers = '2GB';

-- Work mem
ALTER SYSTEM SET work_mem = '128MB';

-- Reload
SELECT pg_reload_conf();
```

### Redis Tuning

Zaten yapılandırılmış:
- maxmemory: 2GB
- maxmemory-policy: allkeys-lru

---

## 🎓 Sonraki Adımlar

### 1. Platform'u Keşfedin
- [ ] Dashboard'u inceleyin
- [ ] EA parametrelerini görüntüleyin
- [ ] Preset sistem'i deneyin
- [ ] Backtest raporlarını inceleyin

### 2. İlk Optimizasyonu Çalıştırın
- [ ] Genetic Algorithm ile parameter optimization
- [ ] Walk-forward analysis
- [ ] Correlation matrix
- [ ] Multi-strategy backtest

### 3. Monitoring Kurun
- [ ] Grafana dashboards oluşturun
- [ ] Alert kuralları ekleyin
- [ ] Performance metrikleri takip edin

### 4. Geliştirin
- [ ] AI Risk Analyzer ekleyin
- [ ] 3D visualization entegre edin
- [ ] Social trading özellikleri
- [ ] Strategy marketplace

### 5. Production Server'a Deploy
- [ ] VPS veya dedicated server kiralayın
- [ ] Domain adı alın
- [ ] SSL sertifikası kurun
- [ ] Gerçek production deployment

---

## 📞 Destek

### Sorun Yaşıyorsanız

1. **Önce logları kontrol edin**: `VIEW_LOGS.bat`
2. **DEPLOYMENT_GUIDE.md'ye bakın**: Detaylı sorun giderme
3. **Docker durumunu kontrol edin**: `docker ps -a`
4. **Github Issues**: Sorun bildirin

### Kullanışlı Komutlar

```powershell
# Tüm container'ları yeniden başlat
docker-compose -f docker-compose.prod.local.yml restart

# Belirli bir servisi rebuild et
docker-compose -f docker-compose.prod.local.yml up -d --build api

# Tüm container'ları durdur ve sil (volumes korunur)
docker-compose -f docker-compose.prod.local.yml down

# Tüm container'ları ve volumes'leri sil (TEHLİKELİ!)
docker-compose -f docker-compose.prod.local.yml down -v

# Disk alanı temizle
docker system prune -a
```

---

## 🎉 Final Checklist

Production ortamınız çalışıyor mu?

- [x] ✅ Environment dosyaları oluşturuldu
- [x] ✅ Docker Compose konfigürasyonu hazır
- [x] ✅ Nginx reverse proxy yapılandırıldı
- [x] ✅ Monitoring stack kuruldu (Prometheus + Grafana)
- [x] ✅ Backup/restore script'leri hazır
- [x] ✅ Windows batch script'leri oluşturuldu
- [x] ✅ Documentation tamamlandı
- [x] ✅ Tickmill Demo hesap entegre edildi
- [x] ✅ EA dosyası (MASSTER_v3.0_FINAL.ex4) mevcut

**HEPSİ HAZIR! 🚀**

---

## 🌟 Başarı Hikayeniz Başlıyor!

Artık dünya standartlarında bir EA optimization platformuna sahipsiniz:

- 🧬 **Genetic Algorithm** ile otomatik optimizasyon
- 📊 **Advanced Analytics** ile derin analiz
- 🔄 **Real-time Monitoring** ile canlı takip
- 🎯 **Walk-Forward Analysis** ile robust parametreler
- 🌐 **Multi-Account** ile çoklu hesap yönetimi

### İlk Hedefiniz:
**İlk 30 günde 100 backtest çalıştırın ve en iyi EA parametrelerini bulun!**

---

**🚀 Haydi başlayalım!**

```powershell
START_PRODUCTION.bat
```

---

**Good luck & Happy Trading! 💰📈**

---

*Production Setup Date: 2025-11-13*
*Version: 1.0.0-production*
*Status: ✅ Ready for Launch*
