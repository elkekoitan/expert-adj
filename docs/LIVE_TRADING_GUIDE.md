# 🔴 Live Trading Guide - SmartMartingale EA

Bu rehber, SmartMartingale Pro EA'sını Tickmill MT4 demo hesabınıza bağlayıp web'den izlemenizi sağlar.

---

## 📋 Gereksinimler

- ✅ Docker & Docker Compose kurulu
- ✅ MT4 Terminal (Tickmill)
- ✅ Demo hesap bilgileri
- ✅ SmartMartingale Pro EA dosyası

---

## 🚀 Hızlı Başlangıç

### 1. Sistemi Başlat

```bash
# Projeyi başlat
cd expert-adj
docker-compose up -d

# Logları izle
docker-compose logs -f
```

### 2. MT4'e BA bağlan

#### Option A: Python Script ile Otomatik
```bash
# Hesap bilgilerini düzenle
nano scripts/deploy_ea_to_mt4.py

# Account bilgilerini gir:
ACCOUNT_NUMBER = 12345678  # Tickmill demo account
PASSWORD = "your_password"
SERVER = "Tickmill-Demo"

# Scripti çalıştır
python scripts/deploy_ea_to_mt4.py
```

#### Option B: Manuel MT4'te

1. **MT4 Terminalini Aç**
2. **Demo Hesaba Giriş Yap**
   - File → Login to Trade Account
   - Server: Tickmill-Demo
   - Login: Hesap numaranız
   - Password: Şifreniz

3. **EA'yı Yükle**
   - File → Open Data Folder
   - MQL4 → Experts klasörüne `SmartMartingale_Pro_v6.ex4` kopyala
   - MT4'ü yeniden başlat

4. **EA'yı Chart'a Ekle**
   - EURUSD M15 chart aç
   - Navigator → Expert Advisors
   - SmartMartingale_Pro_v6'yı chart'a sürükle
   - "Allow live trading" işaretle
   - OK

5. **AutoTrading'i Aktif Et**
   - Toolbar'da "AutoTrading" butonuna bas (yeşil olmalı)
   - Expert Advisors'ın gülümseyen simgesi görünmeli

---

## 📊 Web Dashboard'dan İzleme

### Dashboard'u Aç

```
http://localhost:3000/dashboard
```

### Ne Göreceksiniz?

✅ **Canlı Hesap Bilgileri**
- Balance (Bakiye)
- Equity (Özsermaye)
- Profit (Kar/Zarar)
- Free Margin (Serbest Marjin)

✅ **Açık Pozisyonlar**
- Ticket number
- Symbol (Parite)
- Type (BUY/SELL)
- Volume (Lot)
- Open Price (Açılış Fiyatı)
- Current Price (Anlık Fiyat)
- Profit (Kar/Zarar)

✅ **Son İşlemler**
- Açılan/Kapanan pozisyonlar
- Real-time güncellemeler
- Trade geçmişi

---

## ⚙️ SmartMartingale EA Ayarları

### Önerilen Başlangıç Ayarları (Demo)

```
═══════ GENEL AYARLAR ═══════
MaxCascadeRobots = 5          // 5 robot aktif
TriggerLevel = 2              // 2. kademede tetikleme
DistancePercent = 50%         // Mesafe çarpanı
LotPercent = 100%             // Lot çarpanı

═══════ ZAMAN AYARLARI ═══════
StartHour = 1                 // Sabah 1'de başla
StartMinute = 15
EndHour = 22                  // Gece 22'de dur
EndMinute = 0
LoopWaitMinutes = 30          // 30 dk bekleme

═══════ TİCARET AYARLARI ═══════
TradeDirection = 2            // İki yönlü (Buy+Sell)
DailyProfitTarget = 500$      // Günlük hedef

═══════ ROBOT 1 ═══════
Robot1_BuyMagic = 10001       // Buy magic number
Robot1_SellMagic = 10002      // Sell magic number
Robot1_BuyProfit = 50$        // Buy zincir hedefi
Robot1_SellProfit = 50$       // Sell zincir hedefi

═══════ KADEME 1 ═══════
R1_K1_Lot = 0.01              // İlk lot
R1_K1_TP = 500                // TP mesafesi (point)

═══════ KADEME 2 ═══════
R1_K2_Lot = 0.02              // 2x lot
R1_K2_Distance = 1000         // Mesafe (point)
R1_K2_TP = 550                // TP mesafesi
```

### Risk Yönetimi

**⚠️ Demo Hesap İçin:**
- Başlangıç Lot: 0.01
- Max Cascade: 5 robot
- Daily Profit Target: $500
- Max Drawdown: %20

**🔴 Canlı Hesap İçin (İLERİDE):**
- Minimum balance: $10,000
- Risk per trade: %1
- Daily loss limit: %5
- Monthly profit target: %10-15

---

## 🔍 Real-Time Monitoring

### WebSocket Bağlantısı

Dashboard otomatik olarak WebSocket ile bağlanır:

```typescript
// Frontend otomatik bağlanır:
ws://localhost:8000/socket.io

// Events:
- account_update: Hesap bilgileri güncellendi
- positions_update: Pozisyonlar güncellendi
- trade_opened: Yeni işlem açıldı
- trade_closed: İşlem kapandı
```

### API Endpoints

Manuel kontrol için:

```bash
# Hesap bilgilerini al
curl http://localhost:8000/api/v1/accounts

# Açık pozisyonları al
curl http://localhost:8000/api/v1/accounts/{account_id}/sessions/{session_id}/positions

# Trade geçmişi
curl http://localhost:8000/api/v1/accounts/{account_id}/sessions/{session_id}/trades
```

---

## 🎯 Kullanım Senaryoları

### Senaryo 1: Demo Hesapta Test

1. **Hesabı Ekle**
```bash
curl -X POST http://localhost:8000/api/v1/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "MT4",
    "broker_server": "Tickmill-Demo",
    "account_number": "12345678",
    "password": "your_password",
    "label": "Tickmill Demo",
    "account_type": "demo"
  }'
```

2. **Live Session Başlat**
```bash
curl -X POST http://localhost:8000/api/v1/accounts/{account_id}/sessions/start \
  -H "Content-Type: application/json" \
  -d '{
    "ea_version_id": "smartmartingale_v6",
    "symbol": "EURUSD",
    "timeframe": "M15",
    "parameters": {
      "MaxCascadeRobots": 5,
      "TriggerLevel": 2,
      "Robot1_BuyMagic": 10001,
      "Robot1_SellMagic": 10002
    },
    "magic_numbers": [10001, 10002, 10011, 10012, 10021, 10022]
  }'
```

3. **Dashboard'dan İzle**
   - http://localhost:3000/dashboard
   - Real-time pozisyonları gör
   - Kar/zarar takip et

### Senaryo 2: Çoklu Robot İzleme

```javascript
// 5 robot için magic numbers
Robot 1: BUY=10001, SELL=10002
Robot 2: BUY=10011, SELL=10012
Robot 3: BUY=10021, SELL=10022
Robot 4: BUY=10031, SELL=10032
Robot 5: BUY=10041, SELL=10042

// Tümünü dashboard'da izle
```

---

## 🐛 Troubleshooting

### Problem: Dashboard bağlanmıyor

**Çözüm:**
```bash
# WebSocket servisini kontrol et
docker-compose logs api | grep -i websocket

# Frontend'i yeniden başlat
docker-compose restart frontend
```

### Problem: EA çalışmıyor

**Kontrol Listesi:**
1. ✅ AutoTrading aktif mi? (Yeşil buton)
2. ✅ EA gülen yüz gösteriyor mu?
3. ✅ "Allow live trading" seçili mi?
4. ✅ Trading saatleri içinde mi?
5. ✅ Hesapta yeterli margin var mı?

**Logları Kontrol Et:**
```
MT4 → Experts Tab → Journal
```

### Problem: Pozisyonlar dashboard'da görünmüyor

**Çözüm:**
```bash
# Runner servisini kontrol et
docker-compose logs runner

# API'ye manuel sorgu at
curl http://localhost:8000/api/v1/accounts/{account_id}/sessions/{session_id}/positions
```

---

## 📈 Performans Takibi

### Metrikleri İzle

**Dashboard'da:**
- Günlük kar/zarar
- Açık pozisyon sayısı
- Win rate (kazanma oranı)
- Average profit per trade

**MT4'te:**
- Equity curve
- Drawdown grafiği
- Trade history

---

## ⚡ İleri Seviye

### Otomatik Re-optimization

```bash
# Her gece optimizasyon çalıştır
crontab -e

# Ekle:
0 2 * * * cd /path/to/expert-adj && python scripts/auto_optimize.py
```

### Alerts Kurma

```bash
# Kar hedefine ulaşınca bildirim
curl -X POST http://localhost:8000/api/v1/accounts/{account_id}/alerts \
  -d '{
    "type": "profit_target",
    "threshold": 500,
    "action": "email"
  }'

# Max drawdown'da bildirim
curl -X POST http://localhost:8000/api/v1/accounts/{account_id}/alerts \
  -d '{
    "type": "max_drawdown",
    "threshold": 20,
    "action": "stop_trading"
  }'
```

---

## 🎓 Best Practices

### Demo'da Test Et

1. **En az 1 ay demo**
   - Tüm market koşullarını gör
   - Parametreleri optimize et
   - Risk yönetimini test et

2. **Forward Test**
   - Backtest sonuçlarını doğrula
   - OOS (out-of-sample) performansı kontrol et

3. **Küçük Lot ile Başla**
   - İlk canlı: minimum lot
   - 1 ay başarılı → lot artır

### Risk Yönetimi

```
Altın Kurallar:
- Risk per trade: Max %1-2
- Daily loss limit: Max %5
- Monthly drawdown: Max %15
- Diversification: Birden fazla EA
```

---

## 📞 Destek

**Sorun mu var?**

1. 📖 [Documentation](../README.md)
2. 🐛 [GitHub Issues](https://github.com/yourusername/expert-adj/issues)
3. 💬 [Discord Community](#)
4. 📧 [Email Support](#)

---

## ✅ Checklist

Başlamadan önce:

- [ ] Docker servisleri çalışıyor
- [ ] MT4 terminaline giriş yaptım
- [ ] EA'yı chart'a ekledim
- [ ] AutoTrading aktif
- [ ] Dashboard'u açtım (localhost:3000/dashboard)
- [ ] WebSocket bağlı (yeşil nokta)
- [ ] İlk pozisyon açıldı
- [ ] Dashboard'da görünüyor

---

**🎉 Hazırsın! İyi kazançlar!**

**⚠️ Unutma:** Bu demo hesap. Gerçek parayla trade yapmadan önce mutlaka yeterli test yap!
