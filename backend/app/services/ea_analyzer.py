"""
EA Analyzer Service
Advanced analysis of compiled EA files (.ex4/.ex5)
Extracts metadata, parameters, and trading logic patterns
"""

import hashlib
import logging
import struct
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class EAMetadata:
    """EA Metadata extracted from binary"""

    name: str
    version: str
    build: int
    copyright: str
    link: str
    description: str
    file_size: int
    file_hash: str
    compiled_date: Optional[datetime]
    platform: str  # MT4 or MT5


@dataclass
class EAParameter:
    """EA Parameter definition"""

    name: str
    type: str  # int, double, bool, string, color, datetime
    default_value: Any
    min_value: Optional[float]
    max_value: Optional[float]
    step: Optional[float]
    description: str
    is_optimizable: bool


@dataclass
class TradingLogic:
    """Detected trading logic patterns"""

    uses_indicators: List[str]
    uses_pending_orders: bool
    uses_stop_loss: bool
    uses_take_profit: bool
    uses_trailing_stop: bool
    uses_martingale: bool
    uses_grid: bool
    max_positions: Optional[int]
    timeframes: List[str]
    symbols: List[str]


class EAAnalyzer:
    """
    Advanced EA binary analyzer
    Supports both MT4 (.ex4) and MT5 (.ex5) files
    """

    # MT4/MT5 binary signatures
    MT4_SIGNATURE = b"\x00\x00\x00\x00"
    MT5_SIGNATURE = b"\x00\x00\x00\x01"

    # Common MQL function signatures for pattern detection
    INDICATOR_FUNCTIONS = [
        b"iMA",
        b"iRSI",
        b"iMACD",
        b"iStochastic",
        b"iBands",
        b"iADX",
        b"iCCI",
        b"iATR",
        b"iMomentum",
        b"iOBV",
        b"iSAR",
        b"iWPR",
        b"iIchimoku",
        b"iAlligator",
        b"iFractals",
    ]

    ORDER_FUNCTIONS = [
        b"OrderSend",
        b"OrderModify",
        b"OrderClose",
        b"OrderDelete",
        b"OrderSelect",
        b"OrdersTotal",
        b"OrdersHistoryTotal",
    ]

    POSITION_FUNCTIONS = [
        b"PositionOpen",
        b"PositionClose",
        b"PositionModify",
        b"PositionSelect",
        b"PositionsTotal",
    ]

    RISK_KEYWORDS = [
        b"StopLoss",
        b"TakeProfit",
        b"TrailingStop",
        b"Martingale",
        b"Grid",
        b"Hedging",
        b"MaxLoss",
        b"RiskPercent",
    ]

    def __init__(self):
        self.binary_data: Optional[bytes] = None
        self.metadata: Optional[EAMetadata] = None
        self.parameters: List[EAParameter] = []
        self.trading_logic: Optional[TradingLogic] = None

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Main analysis entry point

        Args:
            file_path: Path to .ex4 or .ex5 file

        Returns:
            Complete analysis results
        """
        try:
            # Read binary file
            with open(file_path, "rb") as f:
                self.binary_data = f.read()

            # Extract metadata
            self.metadata = self._extract_metadata(file_path)

            # Extract parameters (attempt)
            self.parameters = self._extract_parameters()

            # Analyze trading logic
            self.trading_logic = self._analyze_trading_logic()

            # Generate risk assessment
            risk_score = self._calculate_risk_score()

            return {
                "status": "success",
                "metadata": self._metadata_to_dict(),
                "parameters": [self._param_to_dict(p) for p in self.parameters],
                "trading_logic": self._logic_to_dict(),
                "risk_assessment": {
                    "score": risk_score,
                    "level": self._get_risk_level(risk_score),
                    "factors": self._get_risk_factors(),
                },
                "recommendations": self._generate_recommendations(),
            }

        except Exception as e:
            logger.error(f"EA analysis failed: {e}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "metadata": None,
                "parameters": [],
            }

    def _extract_metadata(self, file_path: str) -> EAMetadata:
        """Extract basic metadata from EA binary"""
        file_size = len(self.binary_data)
        file_hash = hashlib.sha256(self.binary_data).hexdigest()

        # Detect platform
        platform = "MT4" if file_path.endswith(".ex4") else "MT5"

        # Try to extract strings from binary
        strings = self._extract_strings(self.binary_data)

        # Look for common metadata patterns
        name = (
            self._find_metadata_value(strings, ["Name:", "EA_NAME", "EXPERT"])
            or Path(file_path).stem
        )
        version = self._find_metadata_value(strings, ["Version:", "v", "Ver"]) or "1.0"
        copyright_text = (
            self._find_metadata_value(strings, ["Copyright", "©", "(c)"]) or "Unknown"
        )
        link = self._find_metadata_value(strings, ["http://", "https://", "www."]) or ""
        description = (
            self._find_metadata_value(strings, ["Description:", "Info:"]) or ""
        )

        # Try to extract build number
        build = self._extract_build_number(strings)

        return EAMetadata(
            name=name,
            version=version,
            build=build,
            copyright=copyright_text,
            link=link,
            description=description,
            file_size=file_size,
            file_hash=file_hash,
            compiled_date=None,  # Hard to extract from binary
            platform=platform,
        )

    def _extract_strings(self, data: bytes, min_length: int = 4) -> List[str]:
        """Extract printable strings from binary data"""
        strings = []
        current_string = []

        for byte in data:
            # Check if printable ASCII
            if 32 <= byte <= 126:
                current_string.append(chr(byte))
            else:
                if len(current_string) >= min_length:
                    strings.append("".join(current_string))
                current_string = []

        if len(current_string) >= min_length:
            strings.append("".join(current_string))

        return strings

    def _find_metadata_value(
        self, strings: List[str], keywords: List[str]
    ) -> Optional[str]:
        """Find metadata value by searching for keywords"""
        for i, s in enumerate(strings):
            for keyword in keywords:
                if keyword.lower() in s.lower():
                    # Try to get the value after the keyword
                    if ":" in s:
                        return s.split(":", 1)[1].strip()
                    elif i + 1 < len(strings):
                        return strings[i + 1]
        return None

    def _extract_build_number(self, strings: List[str]) -> int:
        """Extract build number from strings"""
        for s in strings:
            if "build" in s.lower():
                # Extract number
                import re

                match = re.search(r"\d+", s)
                if match:
                    return int(match.group())
        return 0

    def _extract_parameters(self) -> List[EAParameter]:
        """
        Attempt to extract EA parameters from binary
        This is challenging without decompilation, so we look for patterns
        """
        parameters = []
        strings = self._extract_strings(self.binary_data)

        # Common parameter patterns
        param_keywords = [
            "Lots",
            "Risk",
            "StopLoss",
            "TakeProfit",
            "Magic",
            "Slippage",
            "Period",
            "Shift",
            "MA_Period",
            "Signal",
            "Timeframe",
            "MaxTrades",
            "TrailingStop",
            "BreakEven",
            "UseTime",
            "StartHour",
            "EndHour",
        ]

        for keyword in param_keywords:
            # Search for parameter-like patterns
            for i, s in enumerate(strings):
                if keyword.lower() in s.lower():
                    # Try to detect type and default value
                    param_type = self._guess_parameter_type(s, strings[i : i + 3])
                    default_value = self._guess_default_value(
                        strings[i : i + 3], param_type
                    )

                    parameters.append(
                        EAParameter(
                            name=keyword,
                            type=param_type,
                            default_value=default_value,
                            min_value=None,
                            max_value=None,
                            step=None,
                            description=f"Auto-detected: {keyword}",
                            is_optimizable=True
                            if param_type in ["int", "double"]
                            else False,
                        )
                    )

        return parameters

    def _guess_parameter_type(self, param_str: str, context: List[str]) -> str:
        """Guess parameter type from context"""
        combined = " ".join(context).lower()

        if any(word in combined for word in ["lot", "size", "risk", "percent"]):
            return "double"
        elif any(
            word in combined for word in ["magic", "slippage", "period", "shift", "bar"]
        ):
            return "int"
        elif any(word in combined for word in ["use", "enable", "disable", "show"]):
            return "bool"
        elif any(word in combined for word in ["color", "clr"]):
            return "color"
        elif any(word in combined for word in ["comment", "text", "name"]):
            return "string"
        else:
            return "int"  # Default

    def _guess_default_value(self, context: List[str], param_type: str) -> Any:
        """Guess default value from context"""
        import re

        combined = " ".join(context)

        # Try to find numbers
        numbers = re.findall(r"\d+\.?\d*", combined)

        if param_type == "double":
            return float(numbers[0]) if numbers else 0.01
        elif param_type == "int":
            return int(float(numbers[0])) if numbers else 0
        elif param_type == "bool":
            return True if "true" in combined.lower() else False
        elif param_type == "string":
            return ""
        else:
            return 0

    def _analyze_trading_logic(self) -> TradingLogic:
        """Analyze trading logic patterns in binary"""

        # Detect indicator usage
        indicators = []
        for indicator in self.INDICATOR_FUNCTIONS:
            if indicator in self.binary_data:
                indicators.append(indicator.decode("ascii"))

        # Detect order management
        uses_pending = b"OrderSend" in self.binary_data and (
            b"OP_BUYSTOP" in self.binary_data or b"OP_SELLSTOP" in self.binary_data
        )

        uses_sl = b"StopLoss" in self.binary_data or b"SL" in self.binary_data
        uses_tp = b"TakeProfit" in self.binary_data or b"TP" in self.binary_data
        uses_trailing = (
            b"TrailingStop" in self.binary_data or b"Trailing" in self.binary_data
        )

        # Detect risky strategies
        uses_martingale = (
            b"Martingale" in self.binary_data or b"LotMultiplier" in self.binary_data
        )
        uses_grid = b"Grid" in self.binary_data or b"GridStep" in self.binary_data

        # Try to detect max positions
        max_positions = self._detect_max_positions()

        # Detect timeframes
        timeframes = self._detect_timeframes()

        return TradingLogic(
            uses_indicators=indicators,
            uses_pending_orders=uses_pending,
            uses_stop_loss=uses_sl,
            uses_take_profit=uses_tp,
            uses_trailing_stop=uses_trailing,
            uses_martingale=uses_martingale,
            uses_grid=uses_grid,
            max_positions=max_positions,
            timeframes=timeframes,
            symbols=[],  # Hard to detect
        )

    def _detect_max_positions(self) -> Optional[int]:
        """Try to detect maximum positions"""
        strings = self._extract_strings(self.binary_data)

        for s in strings:
            if "max" in s.lower() and any(
                word in s.lower() for word in ["trade", "position", "order"]
            ):
                import re

                match = re.search(r"\d+", s)
                if match:
                    return int(match.group())

        return None

    def _detect_timeframes(self) -> List[str]:
        """Detect used timeframes"""
        timeframes = []
        tf_patterns = [
            (b"PERIOD_M1", "M1"),
            (b"PERIOD_M5", "M5"),
            (b"PERIOD_M15", "M15"),
            (b"PERIOD_M30", "M30"),
            (b"PERIOD_H1", "H1"),
            (b"PERIOD_H4", "H4"),
            (b"PERIOD_D1", "D1"),
            (b"PERIOD_W1", "W1"),
            (b"PERIOD_MN1", "MN1"),
        ]

        for pattern, tf_name in tf_patterns:
            if pattern in self.binary_data:
                timeframes.append(tf_name)

        return timeframes

    def _calculate_risk_score(self) -> int:
        """
        Calculate risk score (0-100)
        Higher score = higher risk
        """
        risk_score = 0

        if self.trading_logic:
            # No stop loss = +30 risk
            if not self.trading_logic.uses_stop_loss:
                risk_score += 30

            # No take profit = +10 risk
            if not self.trading_logic.uses_take_profit:
                risk_score += 10

            # Martingale = +25 risk
            if self.trading_logic.uses_martingale:
                risk_score += 25

            # Grid trading = +15 risk
            if self.trading_logic.uses_grid:
                risk_score += 15

            # No indicators = +10 risk (blind trading)
            if not self.trading_logic.uses_indicators:
                risk_score += 10

            # Multiple positions without limit = +10 risk
            if (
                self.trading_logic.max_positions is None
                or self.trading_logic.max_positions > 10
            ):
                risk_score += 10

        return min(risk_score, 100)

    def _get_risk_level(self, score: int) -> str:
        """Get risk level label"""
        if score < 30:
            return "LOW"
        elif score < 60:
            return "MEDIUM"
        else:
            return "HIGH"

    def _get_risk_factors(self) -> List[Dict[str, str]]:
        """Get identified risk factors"""
        factors = []

        if self.trading_logic:
            if not self.trading_logic.uses_stop_loss:
                factors.append(
                    {
                        "factor": "No Stop Loss",
                        "severity": "high",
                        "description": "EA does not use stop loss protection",
                    }
                )

            if self.trading_logic.uses_martingale:
                factors.append(
                    {
                        "factor": "Martingale Strategy",
                        "severity": "high",
                        "description": "Uses lot multiplication after losses",
                    }
                )

            if self.trading_logic.uses_grid:
                factors.append(
                    {
                        "factor": "Grid Trading",
                        "severity": "medium",
                        "description": "Opens multiple positions at different levels",
                    }
                )

            if not self.trading_logic.uses_trailing_stop:
                factors.append(
                    {
                        "factor": "No Trailing Stop",
                        "severity": "low",
                        "description": "Does not use trailing stop for profit protection",
                    }
                )

        return factors

    def _generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []

        if self.trading_logic:
            if not self.trading_logic.uses_stop_loss:
                recommendations.append(
                    "Add stop loss protection to limit potential losses"
                )

            if self.trading_logic.uses_martingale:
                recommendations.append(
                    "Consider using fixed lot sizes instead of martingale"
                )
                recommendations.append(
                    "Set maximum trade count to prevent account blow-up"
                )

            if not self.trading_logic.uses_trailing_stop:
                recommendations.append("Implement trailing stop to lock in profits")

            if len(self.trading_logic.uses_indicators) < 2:
                recommendations.append(
                    "Add confirmation indicators to improve signal quality"
                )

            if not self.trading_logic.timeframes:
                recommendations.append("Test on multiple timeframes for robustness")

        return recommendations

    # Conversion methods for API responses
    def _metadata_to_dict(self) -> Dict[str, Any]:
        if not self.metadata:
            return {}

        return {
            "name": self.metadata.name,
            "version": self.metadata.version,
            "build": self.metadata.build,
            "copyright": self.metadata.copyright,
            "link": self.metadata.link,
            "description": self.metadata.description,
            "file_size": self.metadata.file_size,
            "file_hash": self.metadata.file_hash,
            "platform": self.metadata.platform,
        }

    def _param_to_dict(self, param: EAParameter) -> Dict[str, Any]:
        return {
            "name": param.name,
            "type": param.type,
            "default_value": param.default_value,
            "min_value": param.min_value,
            "max_value": param.max_value,
            "step": param.step,
            "description": param.description,
            "is_optimizable": param.is_optimizable,
        }

    def _logic_to_dict(self) -> Dict[str, Any]:
        if not self.trading_logic:
            return {}

        return {
            "indicators": self.trading_logic.uses_indicators,
            "uses_pending_orders": self.trading_logic.uses_pending_orders,
            "uses_stop_loss": self.trading_logic.uses_stop_loss,
            "uses_take_profit": self.trading_logic.uses_take_profit,
            "uses_trailing_stop": self.trading_logic.uses_trailing_stop,
            "uses_martingale": self.trading_logic.uses_martingale,
            "uses_grid": self.trading_logic.uses_grid,
            "max_positions": self.trading_logic.max_positions,
            "timeframes": self.trading_logic.timeframes,
            "symbols": self.trading_logic.symbols,
        }


# Convenience function
def analyze_ea_file(file_path: str) -> Dict[str, Any]:
    """
    Analyze an EA file and return complete results

    Args:
        file_path: Path to .ex4 or .ex5 file

    Returns:
        Analysis results dictionary
    """
    analyzer = EAAnalyzer()
    return analyzer.analyze_file(file_path)
