#!/usr/bin/env python3
"""
Example script demonstrating how to use the COBOL copybook to JSON converter
with the EMP.cpy sample file.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path so we can import our module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cobol_copybook_to_json import convert_copybook_to_json


def main():
    """Main function to demonstrate the conversion."""
    # Get the path to the EMP.cpy file
    emp_file = Path(__file__).parent / "EMP.cpy"
    
    if not emp_file.exists():
        print(f"Error: {emp_file} not found!")
        return 1
    
    print("=== COBOL Copybook to JSON Converter Demo ===")
    print(f"Converting: {emp_file}")
    print()
    
    # Read the copybook file
    try:
        with open(emp_file, 'r') as f:
            copybook_content = f.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        return 1
    
    print("Original COBOL Copybook:")
    print("-" * 50)
    print(copybook_content)
    print("-" * 50)
    print()
    
    # Convert to JSON
    result = convert_copybook_to_json(
        copybook_content=copybook_content,
        copybook_name="EMP.cpy",
        debug=True
    )
    
    if result["status"] == "success":
        print("✅ Conversion successful!")
        print(f"📊 Record size: {result['record_size']} bytes")
        print(f"🔢 Field count: {result['field_count']}")
        print()
        print("Generated JSON Schema:")
        print("-" * 50)
        print(result["json_string"])
        print("-" * 50)
        
        # Optionally save to file
        output_file = emp_file.with_suffix('.json')
        try:
            with open(output_file, 'w') as f:
                f.write(result["json_string"])
            print(f"💾 JSON schema saved to: {output_file}")
        except IOError as e:
            print(f"Warning: Could not save to file: {e}")
        
        return 0
    else:
        print("❌ Conversion failed!")
        print(f"Error: {result['message']}")
        if 'traceback' in result:
            print("Traceback:")
            print(result['traceback'])
        return 1


if __name__ == "__main__":
    sys.exit(main())
