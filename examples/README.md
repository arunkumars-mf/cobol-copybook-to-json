# Examples

This directory contains example COBOL copybooks and demonstration scripts.

## Files

- `EMP.cpy` - Sample employee record COBOL copybook with various data types and structures
- `convert_emp_example.py` - Python script demonstrating how to convert the EMP.cpy file

## Running the Example

```bash
# From the examples directory
python convert_emp_example.py

# Or from the project root
python examples/convert_emp_example.py
```

## EMP.cpy Features

The sample employee copybook demonstrates:

- **Basic fields**: Employee ID, Name, Date of Birth
- **REDEFINES clause**: EMP-ID-X redefines EMP-ID
- **OCCURS clause**: Employee addresses (array of 3 addresses)
- **Different USAGE types**: COMP, COMP-3
- **Signed fields**: Years of experience, salary differences
- **Decimal fields**: Salary with decimal places (V99)
- **FILLER fields**: Padding/unused space

This provides a comprehensive test of the converter's capabilities with real-world COBOL structures.
