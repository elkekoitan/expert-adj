"""
Test MQL Parameter Parser with sample EA
"""

import sys

sys.path.insert(0, "backend")

from backend.app.utils.mql_parser import (
    extract_parameters_from_mql,
    generate_parameter_summary,
    group_parameters_by_category,
)

# Read the sample EA file
with open(
    "NewBornDongu_ParalelRobotlar.mq4", "r", encoding="utf-8", errors="ignore"
) as f:
    content = f.read()

print("=" * 80)
print("MQL4 PARAMETER PARSER TEST")
print("=" * 80)
print(f"\nFile: NewBornDongu_ParalelRobotlar.mq4")
print(f"File Size: {len(content)} bytes\n")

# Extract parameters
parameters = extract_parameters_from_mql(content)

print(f"✓ Extracted {len(parameters)} parameters\n")

# Generate summary
summary = generate_parameter_summary(parameters)

print("SUMMARY:")
print("-" * 80)
print(f"Total Parameters: {summary['total_parameters']}")
print(f"Optimizable: {summary['optimizable_count']}")
print(f"Groups: {summary['group_count']}")
print(f"\nParameter Types:")
for ptype, count in summary["type_counts"].items():
    print(f"  - {ptype}: {count}")

print(f"\nGroups Found:")
for group in summary["groups"]:
    print(f"  - {group}")

# Group parameters by category
grouped = group_parameters_by_category(parameters)

print("\n" + "=" * 80)
print("PARAMETERS BY GROUP:")
print("=" * 80)

for group, params in grouped.items():
    print(f"\n[{group}] ({len(params)} parameters)")
    print("-" * 80)
    for param in params[:5]:  # Show first 5 of each group
        print(
            f"  {param['name']:<30} {param['parameter_type']:<10} = {param['default_value']}"
        )
        if param.get("description"):
            print(f"    → {param['description']}")
    if len(params) > 5:
        print(f"  ... and {len(params) - 5} more")

print("\n" + "=" * 80)
print("SAMPLE PARAMETERS (First 10):")
print("=" * 80)

for i, param in enumerate(parameters[:10], 1):
    print(f"\n{i}. {param['name']}")
    print(f"   Type: {param['parameter_type']}")
    print(f"   Default: {param['default_value']}")
    print(f"   Group: {param['group']}")
    if param.get("description"):
        print(f"   Description: {param['description']}")
    print(f"   Optimizable: {param['is_optimizable']}")

print("\n" + "=" * 80)
print("TEST COMPLETE!")
print("=" * 80)
