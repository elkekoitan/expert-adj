"""
MQL4/MQL5 Parameter Parser
Extracts input parameters from Expert Advisor source code
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MQLParameter:
    """Represents a parsed MQL input parameter"""

    name: str
    param_type: str  # int, double, string, bool, enum
    default_value: Optional[str]
    description: Optional[str]
    group: Optional[str]
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    step_value: Optional[str] = None
    enum_values: List[str] = None

    def __post_init__(self):
        if self.enum_values is None:
            self.enum_values = []


class MQLParameterParser:
    """
    Parser for MQL4/MQL5 input parameters

    Supports:
    - Basic input types (int, double, string, bool)
    - Enum types
    - Input groups
    - Default values and comments
    """

    # MQL type mapping to generic types
    TYPE_MAPPING = {
        "int": "int",
        "uint": "int",
        "long": "int",
        "ulong": "int",
        "short": "int",
        "ushort": "int",
        "char": "int",
        "uchar": "int",
        "double": "double",
        "float": "double",
        "string": "string",
        "bool": "bool",
        "datetime": "datetime",
        "color": "color",
        "ENUM_TIMEFRAMES": "enum",
        "ENUM_MA_METHOD": "enum",
        "ENUM_APPLIED_PRICE": "enum",
    }

    def __init__(self):
        self.current_group: Optional[str] = None
        self.parameters: List[MQLParameter] = []

    def parse_file(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse MQL source code and extract input parameters

        Args:
            content: MQL source code as string

        Returns:
            List of parameter dictionaries
        """
        self.current_group = None
        self.parameters = []

        lines = content.split("\n")

        for i, line in enumerate(lines):
            line = line.strip()

            # Check for input group declaration
            if self._is_group_declaration(line):
                self.current_group = self._extract_group_name(line)
                continue

            # Check for input parameter
            if line.startswith("input "):
                param = self._parse_input_line(line)
                if param:
                    # Add group information
                    param.group = self.current_group
                    self.parameters.append(param)

        return [self._parameter_to_dict(p) for p in self.parameters]

    def _is_group_declaration(self, line: str) -> bool:
        """Check if line declares an input group"""
        return line.startswith("input group ")

    def _extract_group_name(self, line: str) -> str:
        """Extract group name from group declaration"""
        # input group "════════ GENERAL SETTINGS ════════"
        match = re.search(r'input\s+group\s+"([^"]+)"', line)
        if match:
            group_name = match.group(1)
            # Remove decorative characters
            group_name = re.sub(r"[═╔╗╠╣│─█]", "", group_name).strip()
            return group_name
        return "General"

    def _parse_input_line(self, line: str) -> Optional[MQLParameter]:
        """
        Parse a single input parameter line

        Examples:
        input int MaxCascadeRobots = 5;  // Active Robot Count
        input double LotPercent = 100.0;  // Lot Multiplier (%)
        input string Comment = "EA v1.0";
        """
        # Remove 'input ' prefix
        line = line[6:].strip()

        # Extract inline comment (description)
        description = None
        if "//" in line:
            parts = line.split("//", 1)
            line = parts[0].strip()
            description = parts[1].strip()

        # Remove trailing semicolon
        line = line.rstrip(";").strip()

        # Parse: type name = value
        # Pattern: (type) (name) (= value)?
        pattern = r"(\w+)\s+(\w+)(?:\s*=\s*(.+))?"
        match = re.match(pattern, line)

        if not match:
            return None

        param_type_raw = match.group(1)
        param_name = match.group(2)
        default_value = match.group(3)

        # Normalize type
        param_type = self._normalize_type(param_type_raw)

        # Clean default value
        if default_value:
            default_value = default_value.strip().strip('"')

        return MQLParameter(
            name=param_name,
            param_type=param_type,
            default_value=default_value,
            description=description,
            group=None,  # Will be set by caller
        )

    def _normalize_type(self, raw_type: str) -> str:
        """Normalize MQL type to generic type"""
        return self.TYPE_MAPPING.get(raw_type, "string")

    def _parameter_to_dict(self, param: MQLParameter) -> Dict[str, Any]:
        """Convert MQLParameter to dictionary"""
        return {
            "name": param.name,
            "parameter_type": param.param_type,
            "default_value": param.default_value,
            "description": param.description,
            "group": param.group,
            "min_value": param.min_value,
            "max_value": param.max_value,
            "step_value": param.step_value,
            "enum_values": param.enum_values,
            "is_optimizable": param.param_type in ["int", "double"],
        }


def extract_parameters_from_mql(content: str) -> List[Dict[str, Any]]:
    """
    Convenience function to extract parameters from MQL source

    Args:
        content: MQL source code

    Returns:
        List of parameter dictionaries
    """
    parser = MQLParameterParser()
    return parser.parse_file(content)


def group_parameters_by_category(
    parameters: List[Dict[str, Any]],
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group parameters by their group/category

    Args:
        parameters: List of parameter dictionaries

    Returns:
        Dictionary mapping group names to parameter lists
    """
    grouped = {}

    for param in parameters:
        group = param.get("group", "General")
        if group not in grouped:
            grouped[group] = []
        grouped[group].append(param)

    return grouped


def generate_parameter_summary(parameters: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate summary statistics about parameters

    Args:
        parameters: List of parameter dictionaries

    Returns:
        Summary dictionary with counts and types
    """
    type_counts = {}
    groups = set()
    optimizable_count = 0

    for param in parameters:
        # Count types
        param_type = param["parameter_type"]
        type_counts[param_type] = type_counts.get(param_type, 0) + 1

        # Track groups
        if param.get("group"):
            groups.add(param["group"])

        # Count optimizable
        if param.get("is_optimizable", False):
            optimizable_count += 1

    return {
        "total_parameters": len(parameters),
        "type_counts": type_counts,
        "group_count": len(groups),
        "groups": sorted(list(groups)),
        "optimizable_count": optimizable_count,
    }
