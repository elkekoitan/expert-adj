# expert-adj Üretim Ortamına Geçiş ve Sürekli Teslim Planı

Bu doküman, expert-adj platformunu MOCK OLMADAN, gerçek MT4/MT5 entegrasyonu, gerçek kullanıcı/hesap yönetimi, çoklu backtest kuyruğu, EA/preset standardizasyonu, AI destekli strateji üretimi ve .set export ile üretim seviyesine taşımak için izlenecek yol haritasıdır.

Her bölüm:
- Net hedef
- Alt görevler (uygulanabilir)
- Başarı kriterleri
- İlgili dosya/servis referansları
içerir.

Bu dosya proje kökünde tek kaynak olacaktır. Tüm çalışma buradan takip edilmelidir.

## 0. GENEL KURALLAR

- MOCK YOK:
  - Sahte başarı yanıtı, random sonuç, fake account JSON KALMAYACAK.
  - Geçici ise: 501 Not Implemented veya açık TODO olarak bırakılacak.
- GÜVENLİK:
  - Kullanıcı JWT + (ileride) Google OAuth.
  - Hesap bilgileri (MT4/MT5) şifreli saklanır.
- ŞEFFAFLIK:
  - Her test ve canlı işlem izlenebilir, raporlanabilir.
- GENİŞLETİLEBİLİRLİK:
  - NewBorn, MASSTER, yeni EA’lar aynı standartta çalışır.

---

## 1. AUTH, KULLANICI MODÜLÜ, GOOGLE OAUTH

HEDEF:
Gerçek kullanıcı/rol altyapısı: admin ve normal user, JWT login, Google OAuth entegrasyonu, korumalı endpointler.

ALT GÖREVLER:
1.1 [`backend/app/api/v1/auth.py`](backend/app/api/v1/auth.py:1)
- Login endpointini stabilize et:
  - Email + password → `create_access_token` ile JWT.
  - Hatalı girişlerde doğru HTTP 401.
- /auth/me endpointi ekle:
  - `get_current_user()` kullanarak current user JSON döndür.

1.2 [`backend/app/core/security.py`](backend/app/core/security.py:1)
- `get_current_user`, `get_current_active_user`, `get_current_superuser` fonksiyonlarını tüm korumalı endpointlerde kullan.
- Her protected route için:
  - `Depends(get_current_user)` veya `Depends(get_current_superuser)`.

1.3 Kullanıcı modeli ve kayıt:
- [`backend/app/models/user.py`](backend/app/models/user.py:28) zaten uygun.
- Basit kayıt scripti:
  - [`backend/scripts/create_admin.py`](backend/scripts/create_admin.py:1) ile admin user.
  - Demo user oluştur (isteğe bağlı).

1.4 Google OAuth (yeni)
- Yeni config alanları:
  - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI`.
- Yeni endpointler:
  - `GET /auth/google/start` → Google'a yönlendirir.
  - `GET /auth/google/callback` → code ile Google'dan email alır:
    - User yoksa oluştur, varsa login.
    - JWT üret ve FE’ye yönlendir.
- FE:
  - `/login` sayfasına “Google ile giriş yap” butonu eklenir.

BAŞARI KRİTERLERİ:
- Email/şifre ve Google hesabı ile login akışı FE üzerinden eksiksiz çalışır.
- Korumalı endpointlere (backtests, accounts, presets) tokensiz erişim 401 döner.
- Admin sadece admin endpointlerine ulaşabilir.

---

## 2. KULLANICI MODÜLÜ VE BASİT ADMIN PANEL

HEDEF:
Kullanıcıları yönetmek, rolleri ve limitleri belirlemek.

ALT GÖREVLER:
2.1 API:
- `GET /users/me`: Kendi profilini göster.
- `GET /users` (sadece admin):
  - Kullanıcı listesi.
- `PATCH /users/{id}` (admin):
  - is_superuser, is_active gibi alanları yönet.

2.2 FE:
- Basit admin dashboard:
  - Kullanıcı tablosu (email, rol, durum).
  - Rol değiştirme, kullanıcı pasif etme.

BAŞARI KRİTERLERİ:
- Admin, panelden kullanıcı rollerini yönetebilir.
- Kullanıcı kendi profilini görebilir.

---

## 3. MT4/MT5 HESAP BAĞLAMA (MtAccount)

HEDEF:
Kullanıcılar gerçek MetaTrader hesaplarını (demo/live) bağlayabilsin; bu hesaplar test/işlem için kullanılabilsin.

ALT GÖREVLER:
3.1 Model:
- [`backend/app/models/trading.py`](backend/app/models/trading.py:1) veya eşdeğerinde:
  - TradingAccount (MtAccount):
    - id (UUID)
    - owner_id (User.id)
    - broker_name
    - server (örn: demo01.mt4tickmill.com)
    - account_number
    - password_encrypted (security.encrypt_password)
    - account_type (demo/live)
    - is_active, is_verified
    - last_connection_status, last_checked_at

3.2 API (mock KALDIR):
- [`backend/app/api/v1/accounts.py`](backend/app/api/v1/accounts.py:1) revize:
  - Tüm dummy JSON’lar kaldırılacak.
- Yeni uçlar:
  - `POST /accounts`:
    - JWT zorunlu.
    - Hesap bilgilerini al, şifreyi encrypt et, DB’de sakla.
    - İsteğe bağlı: anında bağlantı testi (runner/mt5/live_connection).
  - `GET /accounts`:
    - Sadece kendi hesaplarını göster.
  - `POST /accounts/{id}/test-connection`:
    - DB’den bilgileri al.
    - runner/mt5/live_connection ile gerçek bağlantı testi yap.
    - Sonucu DB’ye yaz, response döndür.

3.3 Tickmill Demo Hesabı:
- `.env.local` veya environment:
  - MT4_LOGIN=20266961
  - MT4_PASSWORD=(sadece lokalde)
  - MT4_SERVER=Tickmill-Demo veya demo01.mt4tickmill.com
- Manuel test:
  - Bu bilgilerle `test-connection` başarılı olmalı.

BAŞARI KRİTERLERİ:
- Bir kullanıcı kendi Tickmill demo hesabını bağlayıp “bağlantı başarılı” görebiliyor.
- Hesap bilgileri encrypted.

---

## 4. EA/PRESET STANDARDİZASYONU (NewBorn + MASSTER)

HEDEF:
Tüm EA’lar için ortak preset formatı; MASSTER_v3.0_FINAL.ex4 ve NewBorn uyumlu.

ALT GÖREVLER:
4.1 EA Kaydı:
- [`backend/app/services/ea_service.py`](backend/app/services/ea_service.py:24) kullanarak:
  - NewBornDongu_ParalelRobotlar
  - MASSTER_v3.0_FINAL.ex4
- Gerekirse script:
  - `backend/scripts/register_builtin_eas.py`

4.2 EA Parametre Şeması:
- EAParameter tablosu kullan:
  - Her EA için parametre adı, tip, aralık, default değerler.
- MASSTER ve NewBorn için manuel schema çıkar:
  - Lot, risk, grid/martingale, TP/SL, filtreler vb.

4.3 StrategyPreset Formatı:
- İsimlendirme:
  - `{EA}-{SYMBOL}-{TF}-{PROFILE}-{VERSION}`
  - Örnek:
    - `NBD-XAUUSD-M15-LOWRISK-v1`
    - `MASSTER-EURUSD-M30-AGGR-v1`
- StrategyPreset.entries:
  - expert_id, symbol, timeframe, parameters (schema’ya uygun).

BAŞARI KRİTERLERİ:
- En az bir NewBorn ve bir MASSTER preset DB’de kayıtlı.
- FE, bu presetleri doğru gösteriyor.

---

## 5. GERÇEK BACKTEST PIPELINE (QUEUE + TERMINAL + METRICS)

HEDEF:
Mock backtest YOK. Tüm backtestler gerçek terminal veya gerçekçi strateji simülasyonu ile üretilir.

ALT GÖREVLER:
5.1 BacktestRun Model Kontrol:
- [`backend/app/models/strategy.py`](backend/app/models/strategy.py:1):
  - owner_id, preset_id, account_id
  - status: queued/running/completed/failed
  - parameters, metrics, report_path alanları.

5.2 Backtest API:
- [`backend/app/api/v1/backtests.py`](backend/app/api/v1/backtests.py:1):
  - `POST /backtests`:
    - JWT zorunlu.
    - Input: preset_id, account_id, tarih aralığı, engine.
    - Çıktı: status=queued BacktestRun kaydı oluştur.
  - `GET /backtests`:
    - Sadece gerçek BacktestRun kayıtlarını döner.

5.3 Runner Servisi:
- [`runner/runner.py`](runner/runner.py:1):
  - Döngü:
    - status=queued BacktestRun’ları bul.
    - İlgili TradingAccount ve StrategyPreset’i çek.
    - [`runner/mt5/terminal_controller.py`](runner/mt5/terminal_controller.py:16) ile:
      - .set dosyası üret (preset parameters → KEY=VALUE).
      - Terminali /config ile başlat.
      - Rapor dosyalarını al, metrikleri parse et.
    - Sonuçları BacktestRun.metrics ve status ile güncelle.

5.4 NewBorn/MASSTER:
- En az bir EA için uçtan uca:
  - FE → Backtest isteği → Runner → Gerçek rapor/metrik.

BAŞARI KRİTERLERİ:
- Kuyruğa atılan her backtest isteği gerçek terminal süreciyle sonuçlanır.
- Mock random metrik yok; başarısızlık durumunda bile gerçek hata döner.

---

## 6. TRADELOG, İŞLEM GEÇMİŞİ, ÇOKLU TEST

HEDEF:
Her backtest ve canlı oturum için detaylı işlem kayıtları ve görselleştirme.

ALT GÖREVLER:
6.1 TradeLog Model:
- Yeni tablo:
  - backtest_run_id veya session_id
  - ticket, symbol, type, volume, price_open, price_close, profit
  - open_time, close_time

6.2 Runner Entegrasyonu:
- MT5 history_deals_get veya report parsing ile TradeLog doldur.

6.3 API:
- `GET /backtests/{id}/trades`
- `GET /backtests/{id}/equity-curve`

6.4 FE:
- Backtest detay sayfası:
  - İşlem listesi
  - Equity curve grafiği

Başarı Kriterleri:
- Kullanıcı, her backtest için hangi işlemlerle sonuca gelindiğini görebiliyor.
- Aynı anda birden çok backtest sorunsuz çalışabiliyor.

---

## 7. EN İYİ SETLERİ DEMOYA AKTARMA

HEDEF:
Gün içinde koşan sonuçlardan en iyi presetleri seçip demo hesabına uygulamak.

ALT GÖREVLER:
7.1 Quality Score:
- Fonksiyon:
  - net_profit, max_drawdown, profit_factor, win_rate, trade_count → tek skor.

7.2 API:
- `GET /presets/best?symbol=XAUUSD&limit=5`
- `POST /accounts/{id}/apply-preset`:
  - Seçilen preset parametrelerini bu account için aktif olarak işaretle.
  - Live runner bu ayarları kullanır.

BAŞARI KRİTERLERİ:
- Dashboard’da “en iyi setler” listeleniyor.
- Tek tıkla en iyi setler Tickmill-Demo hesabına uygulanabiliyor.

---

## 8. AI DESTEKLİ STRATEJİ MOTORU

HEDEF:
XAU/EUR/ETH için:
- SMA, Fibo, yatay destek/direnç, kırılım, Elliott, 7 kademe hibrit strateji ile otomatik preset üretimi.

ALT GÖREVLER:
8.1 AI Servis:
- `/ai/strategy-suggestions` endpoint:
  - Input:
    - Enstrüman (XAU/EUR/ETH),
    - Saat dilimleri,
    - Risk profili,
    - Kademe=7, kullanılan indikatörler.
  - Output:
    - 3–10 adet StrategyPreset parametre seti.

8.2 Otomatik Kuyruk:
- İsteğe bağlı:
  - Bu presetleri direkt backtest kuyruğuna at.

8.3 FE:
- /ai-strategist ekranı:
  - Kullanıcı isteklerini girer.
  - Önerilen presetleri görür.
  - “Test et” butonu ile backtest başlatır.

BAŞARI KRİTERLERİ:
- Kullanıcı doğal isteklerle (XAU 7 kademe, Fibo destekli, düşük DD) preset önerileri alıp test ettirebiliyor.

---

## 9. .SET EXPORT VE MT4’E DİREKT ÇIKTI

HEDEF:
StrategyPreset → MT4/MT5 .set dosyası indirilebilir.

ALT GÖREVLER:
9.1 API:
- `GET /presets/{id}/export-mt4`:
  - StrategyPreset.parameters → KEY=VALUE satırları.
  - `Content-Type: text/plain`, direkt download.

9.2 FE:
- Preset detayında “Export .set” butonu.

BAŞARI KRİTERLERİ:
- İndirilen .set dosyası terminalde sorunsuz import edilebiliyor.

---

## 10. ÜST SEVİYE DASHBOARD VE ÜRÜNLEŞME

HEDEF:
Tüm bileşenlerin entegre edildiği, yatırımcıya gösterilebilir seviye dashboard.

ALT GÖREVLER:
10.1 Ana Dashboard:
- Özet:
  - Toplam backtest sayısı
  - Başarılı oranı
  - En iyi EA/preset/stratejiler
  - Bağlı hesaplar, canlı oturumlar

10.2 Gelişmiş Filtreler:
- EA, symbol, timeframe, tarih, risk profili.

10.3 Hata/Log Görünürlüğü:
- Runner hataları, MT bağlantı sorunları, parse hataları.

BAŞARI KRİTERLERİ:
- Tek ekran üzerinden:
  - Durum izlenebilir,
  - En iyi setler görülebilir,
  - Hesaplar yönetilebilir,
  - Test ve canlı işlemler takip edilebilir.

---

## 11. OTOMASYON: GÖREV KOŞUMLARI VE SCRIPT

HEDEF:
Tek komutla:
- Ortamı hazırlayan,
- Migrasyon çalıştıran,
- Admin/özgün kullanıcıları oluşturan,
- Built-in EA/presetleri kaydeden,
- Runner ve frontend’i ayağa kaldıran script.

ALT GÖREVLER:
11.1 Makefile / Python Script:
- `make bootstrap` veya `python scripts/bootstrap.py`:
  - .env kontrolü.
  - DB migrate.
  - Admin ve demo kullanıcı oluştur.
  - Built-in EA (NewBorn, MASSTER) kaydı.
  - Örnek presetleri ekle.
  - Opsiyonel: Tickmill demo hesabını ekleyip test-connection çalıştır.

11.2 `make up`:
- docker-compose ile:
  - backend
  - frontend
  - runner (worker)
  - opsiyonel redis/db
  ayağa kalksın.

11.3 `make status`:
- Health, queue, runner, hesap bağlantısı özetini versin.

BAŞARI KRİTERLERİ:
- Yeni bir makinede:
  - Repo clone → Tek komut → Sistem ayağa kalkıyor.
  - Login, hesap bağlama, backtest, rapor, .set export, AI öneri zinciri demonstrable.
