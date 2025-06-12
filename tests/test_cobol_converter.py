#!/usr/bin/env python3
"""
Test suite for the COBOL copybook to JSON converter.
"""

import os
import sys
import unittest
from pathlib import Path

# Add the src directory to the path so we can import our module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cobol_copybook_to_json import convert_copybook_to_json


class TestCobolConverter(unittest.TestCase):
    """Test cases for COBOL copybook to JSON conversion."""

    def setUp(self):
        """Set up test fixtures."""
        self.examples_dir = Path(__file__).parent.parent / "examples"
        
    def test_emp_copybook_conversion(self):
        """Test conversion of the EMP.cpy sample file."""
        emp_file = self.examples_dir / "EMP.cpy"
        
        # Read the copybook file
        with open(emp_file, 'r') as f:
            copybook_content = f.read()
        
        # Convert to JSON
        result = convert_copybook_to_json(
            copybook_content=copybook_content,
            copybook_name="EMP.cpy",
            debug=True
        )
        
        # Assertions
        self.assertEqual(result["status"], "success", f"Conversion failed: {result.get('message', 'Unknown error')}")
        self.assertIn("json_string", result)
        self.assertIn("record_size", result)
        self.assertIn("field_count", result)
        
        # Print results for manual verification
        print(f"\n=== EMP.cpy Conversion Results ===")
        print(f"Status: {result['status']}")
        print(f"Record size: {result['record_size']} bytes")
        print(f"Field count: {result['field_count']}")
        print(f"\nJSON Schema:")
        print(result["json_string"])
        
        # Basic validation of the JSON structure
        self.assertGreater(result["record_size"], 0)
        self.assertGreaterEqual(result["field_count"], 1)
        
    def test_error_handling(self):
        """Test error handling with invalid input."""
        # Test with invalid input type
        result = convert_copybook_to_json(
            copybook_content=123,  # Invalid type
            copybook_name="test.cpy"
        )
        
        self.assertEqual(result["status"], "error")
        self.assertIn("message", result)


def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()
