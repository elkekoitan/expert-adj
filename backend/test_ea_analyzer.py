"""
Test EA Analyzer on MASSTER_v3.0_FINAL.ex4
"""

import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.services.ea_analyzer import analyze_ea_file

if __name__ == "__main__":
    ea_path = (
        Path(__file__).parent.parent / "examples" / "EAs" / "MASSTER_v3.0_FINAL.ex4"
    )

    print(f"Analyzing: {ea_path}")
    print("=" * 80)

    results = analyze_ea_file(str(ea_path))

    print(json.dumps(results, indent=2, default=str))
