"""
Trading instruments model
"""
from sqlalchemy import Column, String, Integer, Boolean, Numeric

from app.models.base import BaseModel


class Instrument(BaseModel):
    """
    Trading instruments (symbols)
    """

    __tablename__ = "instruments"

    symbol = Column(String(20), unique=True, nullable=False, index=True)
    broker = Column(String(100), nullable=True)
    description = Column(String(255), nullable=True)

    digits = Column(Integer, nullable=False, default=5)
    point = Column(Numeric(10, 8), nullable=False)
    pip_value = Column(Numeric(10, 8), nullable=False)

    # Contract specifications
    contract_size = Column(Numeric(15, 2), nullable=True)
    min_lot = Column(Numeric(10, 2), nullable=True)
    max_lot = Column(Numeric(10, 2), nullable=True)
    lot_step = Column(Numeric(10, 2), nullable=True)

    is_active = Column(Boolean, default=True)
