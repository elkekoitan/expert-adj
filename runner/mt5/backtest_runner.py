"""
NewBornDongu - MT4 Backtest Runner

Bu modül, backend'den gelen BacktestRun işlerini okuyup
Tickmill MT4 terminali üzerinde NewBornDongu_ParalelRobotlar.mq4 ile gerçek backtest
tetiklemek için iskelet sağlar.

ÖNEMLİ NOTLAR:
- Bu kod, MetaTrader5 Python modülünü ve Strategy Tester entegrasyonunu kullanmak için iskelet sunar.
- Senin makinedeki MT4 terminal dosya yapısı, dil ayarları, hesap izinleri,
  NewBornDongu parametreleri vb. runtime'da doğrulanmalıdır.
- Buradaki amaç: Runner tarafında "queued backtest" gördüğünde
  MT4 terminalini initialize et, login ol, test çalıştır, sonucu backend'e POST et.
"""

import logging
from pathlib import Path
from typing import Optional

try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None

from runner.config import settings

logger = logging.getLogger(__name__)


class BacktestRunner:
    """
    BacktestRunner:
    - MT4 terminali initialize eder
    - Tickmill demo hesabına login olur (env'den)
    - NewBornDongu_ParalelRobotlar.mq4 için iskelet backtest fonksiyonlarını sağlar
    - Sonuçları ileride backend'e yazmak için döndürür
    """

    def __init__(self) -> None:
        self.terminal_path = settings.MT5_TERMINAL_PATH
        self.data_path = settings.MT5_DATA_PATH
        self.login = settings.MT5_LOGIN
        self.password = settings.MT5_PASSWORD
        self.server = settings.MT5_SERVER

    def _check_mt5_available(self) -> bool:
        if mt5 is None:
            logger.error("MetaTrader5 Python modülü yüklü değil. 'pip install MetaTrader5' gerekli.")
            return False
        return True

    def initialize_terminal(self) -> bool:
        """
        MT4/MT5 terminalini verilen path ile initialize etmeyi dener.
        """
        if not self._check_mt5_available():
            return False

        if not self.terminal_path:
            logger.error("MT5_TERMINAL_PATH tanımlı değil.")
            return False

        if not Path(self.terminal_path).exists():
            logger.error(f"MT terminal path bulunamadı: {self.terminal_path}")
            return False

        logger.info(f"MT terminal initialize ediliyor: {self.terminal_path}")

        # Not: MT5.initialize MT5 terminalini kullanır, MT4 için doğrudan destek yoktur.
        # Tickmill MT4 çalışıyorsa, bu noktada mevcut bağlantıyı kullanmak için login deneyebiliriz.
        if not mt5.initialize(path=self.terminal_path):
            logger.error(f"mt5.initialize başarısız: {mt5.last_error()}")
            return False

        logger.info("MT terminal initialize başarılı")
        return True

    def login_account(self) -> bool:
        """
        Tickmill hesabına login olmayı dener.
        Zaten bağlıysa, bu çağrı başarısız olsa da mevcut session devam edebilir.
        """
        if not self._check_mt5_available():
            return False

        if not (self.login and self.password and self.server):
            logger.warning("Login bilgileri eksik (MT5_LOGIN / MT5_PASSWORD / MT5_SERVER). Mevcut oturum kullanılacak.")
            return True

        try:
            login_int = int(self.login)
        except ValueError:
            logger.error(f"MT5_LOGIN integer değil: {self.login}")
            return False

        logger.info(f"Tickmill hesabına login deneniyor: {login_int} @ {self.server}")
        if not mt5.login(login_int, password=self.password, server=self.server):
            logger.error(f"Login başarısız: {mt5.last_error()}")
            return False

        acc = mt5.account_info()
        if acc:
            logger.info(f"Login OK - Balance: {acc.balance}, Name: {acc.name}")
        else:
            logger.warning("Login sonrası account_info alınamadı.")
        return True

    def run_newborndongu_backtest(
        self,
        symbol: str,
        timeframe: str,
        date_from: Optional[str],
        date_to: Optional[str],
        preset_params: dict,
    ) -> dict:
        """
        NewBornDongu için backtest iskeleti.
        Burada:
        - Symbol/timeframe kontrolleri
        - Strategy Tester konfigürasyonu
        - Sonuç toplama
        adımlarını senin ortamında test ederek tamamlaman gerekir.

        Şu an:
        - Sadece log atar ve "stub" bir sonuç döner.
        - Böylece pipeline uçtan uca akarken nerede kaldığını görürsün.
        """

        logger.info(f"[NB] Backtest START: {symbol} {timeframe} {date_from} -> {date_to}")
        logger.info(f"[NB] Preset params: {preset_params}")

        if not self._check_mt5_available():
            return {
                "status": "failed",
                "reason": "MetaTrader5 module missing",
            }

        # Buraya Strategy Tester entegrasyonu gelecek.
        # Örnek pseudo-akış (senin terminalinde test edilmesi gerekiyor):
        # - mt5.symbol_select(symbol, True)
        # - mt5.copy_rates_range(...)
        # - NewBornDongu ayarlarına göre trade simülasyonu veya custom command
        # Şu aşamada bu seviyede sahte kod yazıp 'çalıştı' demiyorum.

        # Şimdilik, pipeline testi için dummy sonuç:
        result = {
            "status": "completed",
            "symbol": symbol,
            "timeframe": timeframe,
            "date_from": date_from,
            "date_to": date_to,
            "net_profit": 0.0,
            "trades": 0,
            "note": "NewBornDongu backtest_runner iskeleti çalıştı; gerçek MT4 test entegrasyonu senin terminal üzerinde finalize edilmeli.",
        }

        logger.info(f"[NB] Backtest END: {result}")
        return result

    def shutdown(self) -> None:
        if self._check_mt5_available():
            mt5.shutdown()
            logger.info("MT terminal shutdown çağrıldı")