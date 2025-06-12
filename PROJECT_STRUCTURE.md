# Project Structure

This document outlines the structure of the COBOL Copybook to JSON Schema Converter project.

## Directory Structure

```
cobol_copybook_to_json/
├── src/
│   └── cobol_copybook_to_json/
│       └── __init__.py              # Main module with conversion logic
├── tests/
│   ├── __init__.py                  # Test package initialization
│   └── test_cobol_converter.py      # Unit tests
├── examples/
│   ├── EMP.cpy                      # Sample COBOL copybook
│   ├── EMP.json                     # Generated JSON schema (auto-created)
│   ├── convert_emp_example.py       # Example usage script
│   └── README.md                    # Examples documentation
├── docs/                            # Documentation directory (future use)
├── dist/                            # Built packages (created by build process)
├── pyproject.toml                   # Modern Python project configuration
├── setup.py                         # Legacy setup script (for compatibility)
├── README.md                        # Main project documentation
├── LICENSE                          # MIT license
├── MANIFEST.in                      # Package manifest
├── .gitignore                       # Git ignore rules
└── PROJECT_STRUCTURE.md             # This file
```

## Key Files

### Core Module
- `src/cobol_copybook_to_json/__init__.py`: Contains the main conversion logic and API

### Configuration
- `pyproject.toml`: Modern Python packaging configuration (PEP 518)
- `setup.py`: Legacy setup script for backward compatibility
- `MANIFEST.in`: Specifies additional files to include in the package

### Testing
- `tests/test_cobol_converter.py`: Comprehensive unit tests including EMP.cpy conversion
- Tests can be run with: `python -m unittest tests.test_cobol_converter -v`

### Examples
- `examples/EMP.cpy`: Real-world COBOL copybook with various data types
- `examples/convert_emp_example.py`: Demonstration script
- Run example: `python examples/convert_emp_example.py`

## Package Features

The package supports:
- **Command-line usage**: `cobol-to-json -c input.cpy -j output.json`
- **Library usage**: `from cobol_copybook_to_json import convert_copybook_to_json`
- **Comprehensive COBOL support**: Groups, arrays (OCCURS), REDEFINES, COMP/COMP-3, signed fields
- **Debug mode**: Detailed parsing information
- **Error handling**: Graceful error reporting

## Build and Distribution

- Build: `pyproject-build`
- Check: `twine check dist/*`
- Upload to PyPI: `twine upload dist/*`

## Testing

All tests pass successfully:
- EMP.cpy conversion test (comprehensive)
- Error handling test
- Run tests: `python -m unittest tests.test_cobol_converter -v`
