# ⚡ MT Expert Optimizer - Quick Start Guide

Bu rehber, projeyi **5 dakikada** çalıştırmanızı sağlar.

---

## 📋 Hızlı Checklist

### ✅ Ön Hazırlık (Bir Kere)

- [ ] Docker Desktop yüklü mü? → [İndir](https://www.docker.com/products/docker-desktop/)
- [ ] Docker çalışıyor mu? → Taskbar'da Docker ikonu yeşil olmalı
- [ ] Git Bash yüklü mü? → [İndir](https://git-scm.com/download/win)

### 🚀 Çalıştırma (Her Seferinde)

```powershell
# 1. Proje klasörüne git
cd C:\Users\qw\Desktop\expert-adj

# 2. Docker servislerini başlat
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# 3. 2-3 dakika bekle (ilk seferde biraz uzun sürebilir)

# 4. Tarayıcıda aç
start http://localhost
```

**Login Bilgileri:**
- Email: `admin@mtoptimizer.local`
- Password: `Admin2025!SuperSecure#Pass`

---

## 🎯 Önemli URL'ler

| Servis | URL | Kullanıcı | Şifre |
|--------|-----|-----------|-------|
| 🏠 **Ana Platform** | http://localhost | admin@mtoptimizer.local | Admin2025!SuperSecure#Pass |
| 📊 **API Docs** | http://localhost/api/docs | - | - |
| 🌸 **Flower (Celery)** | http://localhost/flower/ | admin | Admin2025 |
| 📈 **Grafana** | http://localhost/grafana/ | admin | Grafana2025!Admin#Pass |
| 💾 **MinIO** | http://localhost:9001 | minioadmin | MinIO2025!StorageSecure#Pass |

---

## 🧪 İlk Backtest Nasıl Çalıştırılır?

### 1. EA Upload Edin

1. http://localhost adresine git
2. Login ol
3. Sol menüden **"Expert Advisors"** → **"Upload EA"**
4. Dosya seç: `C:\Users\qw\Desktop\expert-adj\examples\EAs\MASSTER_v3.0_FINAL.ex4`
5. Upload et

### 2. MT5 Hesabı Ekle

1. Sol menüden **"Accounts"** → **"Add Account"**
2. Bilgileri gir:
   ```
   Name: Tickmill Demo
   Login: 20266961
   Password: =ə>#qB9RFjzC
   Server: TickmillEU-Demo
   Platform: MT5
   ```
3. **"Test Connection"** → Yeşil ✓ görmelisiniz

### 3. Backtest Başlat

1. Sol menüden **"Backtests"** → **"New Backtest"**
2. Ayarlar:
   - EA: `MASSTER_v3.0_FINAL`
   - Account: `Tickmill Demo`
   - Symbol: `EURUSD`
   - Timeframe: `H1`
   - Date Range: `2024-01-01` to `2024-12-31`
3. **"Start Backtest"**
4. Sonuçları izle!

---

## 🛑 Servisleri Durdurma

```powershell
# Tüm servisleri durdur (veriler korunur)
docker-compose -f docker-compose.prod.yml stop

# Tekrar başlat
docker-compose -f docker-compose.prod.yml start
```

---

## 🔧 Sorun mu Var?

### Container başlamadı?

```powershell
# Logları kontrol et
docker-compose -f docker-compose.prod.yml logs

# Servisleri yeniden başlat
docker-compose -f docker-compose.prod.yml restart
```

### Port zaten kullanımda?

```powershell
# Port 80'i kullanan uygulamayı kapat
# Veya docker-compose.prod.yml'de portları değiştir:
#   - "8080:80"  # 80 yerine 8080 kullan
```

### Frontend'e erişemiyorum?

```powershell
# Servislerin durumunu kontrol et
docker-compose -f docker-compose.prod.yml ps

# Nginx loglarını kontrol et
docker-compose -f docker-compose.prod.yml logs nginx
```

---

## 📚 Detaylı Dökümantasyon

Daha fazla bilgi için:
- **Tam Deployment Guide**: `DEPLOYMENT_GUIDE.md`
- **API Dökümantasyon**: http://localhost/api/docs
- **Proje Planı**: `docs/MT Expert Optimizer - Production Deployment & Frontend Innovation Plan.md`

---

## 💡 Pro Tips

1. **İlk çalıştırmada** container'lar build edilir (5-10 dk)
2. **Sonraki çalıştırmalarda** 30 saniyede başlar
3. **Backup almak** için: `./scripts/backup.sh daily`
4. **Monitoring** için Grafana dashboard'larını kullan
5. **Log izlemek** için: `docker-compose -f docker-compose.prod.yml logs -f`

---

**🚀 Hadi başlayalım! Good luck trading!**
