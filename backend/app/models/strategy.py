from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class StrategyPreset(BaseModel):
    """
    Presetlenen strateji konfigürasyonları:
    - Belirli bir EA, sembol, timeframe ve param seti
    - Otomatik veya manuel üretilmiş olabilir
    """

    __tablename__ = "strategy_presets"

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    ea_id = Column(UUID(as_uuid=True), ForeignKey("expert_advisors.id"), nullable=False)

    # Örnek isimlendirme:
    # NBD_EURUSD_M15_MG1.5_K5_TP5_ATR-FIBO_v1
    # [EA Kodu]_[Sembol]_[Timeframe]_[Martingale]_[Kademe/TP bilgisi]_[Volatilite/Mesafe kuralı]_[versiyon]
    name = Column(String(255), nullable=False)

    # slug: makine dostu, benzersiz anahtar
    # Örn: nbd_eurusd_m15_mg1_5_k5_tp5_atr_fibo_v1
    slug = Column(String(255), unique=True, index=True, nullable=False)

    # İnsan tarafından okunabilir açıklama; isimde özetlenen kuralın detayını içerir
    description = Column(Text, nullable=True)

    symbol = Column(String(20), nullable=True)
    timeframe = Column(String(10), nullable=True)

    # manual / auto / hybrid
    mode = Column(String(20), nullable=False, default="manual")

    # Kademe, TP, martingale, mesafe, vb tüm EA parametre seti
    parameters = Column(JSONB, nullable=False, default=dict)

    # Volatilite / MA / Fibo / bar / regime bazlı dinamik kurallar
    dynamic_policies = Column(JSONB, nullable=True)

    # Etiketler (eurusd, martingale, fibo, vb)
    tags = Column(JSONB, nullable=True)

    # draft / candidate / tested / selected / deployed / retired
    status = Column(String(20), nullable=False, default="draft")

    # Son iyi backtest özet metrikleri
    metrics_snapshot = Column(JSONB, nullable=True)

    # Relationships
    owner = relationship("User", foreign_keys=[owner_id])
    organization = relationship("Organization")
    expert_advisor = relationship("ExpertAdvisor", foreign_keys=[ea_id])

    backtest_runs = relationship("BacktestRun", back_populates="preset", cascade="all, delete-orphan")
    forward_runs = relationship("ForwardRun", back_populates="preset", cascade="all, delete-orphan")


class BacktestRun(BaseModel):
    """
    Belirli bir preset veya param seti için yapılan backtest koşumu
    """

    __tablename__ = "backtest_runs"

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)

    preset_id = Column(UUID(as_uuid=True), ForeignKey("strategy_presets.id"), nullable=True)
    ea_version_id = Column(UUID(as_uuid=True), ForeignKey("ea_versions.id"), nullable=True)

    symbol = Column(String(20), nullable=False)
    timeframe = Column(String(10), nullable=False)

    # ISO string (migration ile string olarak tutuluyor)
    date_from = Column(String, nullable=False)
    date_to = Column(String, nullable=False)

    # mt4_local / mt5_local / custom
    engine = Column(String(50), nullable=False, default="mt5_local")

    # Kullanılan efektif param seti
    parameters = Column(JSONB, nullable=False, default=dict)

    # queued / running / completed / failed
    status = Column(String(20), nullable=False, default="queued")

    # PF, DD, vs metrikler
    metrics = Column(JSONB, nullable=True)

    # Rapor ve hata bilgileri
    report_ref = Column(String(500), nullable=True)
    error_message = Column(Text, nullable=True)

    # Relationships
    preset = relationship("StrategyPreset", back_populates="backtest_runs")
    owner = relationship("User", foreign_keys=[owner_id])
    organization = relationship("Organization")
    ea_version = relationship("EAVersion", foreign_keys=[ea_version_id])


class ForwardRun(BaseModel):
    """
    Belirli bir presetin belirli bir trading account üzerinde canlı (özellikle demo) forward testi
    """

    __tablename__ = "forward_runs"

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)

    preset_id = Column(UUID(as_uuid=True), ForeignKey("strategy_presets.id"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("trading_accounts.id"), nullable=False)

    # deploying / running / stopped / error
    status = Column(String(20), nullable=False, default="deploying")

    # Lot, risk, max_dd, vb
    allocation = Column(JSONB, nullable=True)

    # Canlı metrikler (pf_live, dd_live, equity, vs)
    live_metrics = Column(JSONB, nullable=True)

    started_at = Column(String, nullable=True)
    stopped_at = Column(String, nullable=True)
    last_heartbeat_at = Column(String, nullable=True)

    # Relationships
    preset = relationship("StrategyPreset", back_populates="forward_runs")
    owner = relationship("User", foreign_keys=[owner_id])
    organization = relationship("Organization")
    account = relationship("TradingAccount", foreign_keys=[account_id])