# COBOL Copybook to JSON Schema Converter

A Python utility that converts COBOL copybooks to JSON schema format. This tool is particularly useful for mainframe modernization projects and data integration scenarios where you need to understand and work with COBOL data structures in modern applications.

## Features

- **Comprehensive COBOL Support**: Handles various COBOL data structures including:
  - Group items and elementary items
  - OCCURS clauses (arrays)
  - REDEFINES clauses
  - Different USAGE types (COMP, COMP-3, etc.)
  - PICTURE clauses with various data types
  - Signed and unsigned numeric fields

- **Dual Usage**: Can be used both as a command-line tool and as a Python library
- **Debug Support**: Built-in debugging capabilities for troubleshooting
- **Error Handling**: Comprehensive error handling with detailed messages

## Installation

```bash
pip install cobol-copybook-to-json
```

## Usage

### Command Line Tool

```bash
# Convert a COBOL copybook to JSON schema
cobol-to-json -c input_copybook.cpy -j output_schema.json

# Enable debug mode
cobol-to-json -c input_copybook.cpy -j output_schema.json -d
```

### Python Library

```python
from cobol_copybook_to_json import convert_copybook_to_json

# Read your COBOL copybook
with open('your_copybook.cpy', 'r') as f:
    copybook_content = f.read()

# Convert to JSON schema
result = convert_copybook_to_json(
    copybook_content=copybook_content,
    copybook_name="your_copybook.cpy",
    debug=False
)

if result["status"] == "success":
    print("JSON Schema:")
    print(result["json_string"])
    print(f"Record size: {result['record_size']} bytes")
    print(f"Field count: {result['field_count']}")
else:
    print(f"Error: {result['message']}")
```

## Example

### Input COBOL Copybook
```cobol
      * 
      * Sample Employee Record COBOL Layout
      * 
       01 EMP-RECORD.
         05 EMP-ID                      PIC 9(5).
         05 EMP-ID-X REDEFINES EMP-ID   PIC X(5).
         05 EMP-NAME                    PIC X(25).
         05 EMP-DOB                     PIC X(10).
         05 EMP-ADDRESS OCCURS 3 TIMES.
            10 EMP-ADDR-LINE            PIC X(25).
         05 EMP-YOE-CUR                 PIC S9(4) COMP.
         05 EMP-YOE-TOTAL               PIC 9(4)V99 COMP-3.
         05 EMP-SALARY                  PIC S9(4)V99.
         05 EMP-SALARY-DIFF             PIC S9999V99 COMP-3.         
         05 EMP-DEPENDENTS-NUM          PIC S9(2).
         05 FILLER                      PIC X(17).
```

### Output JSON Schema
```json
{
    "metadata": {
        "version": "1.0",
        "generatedAt": "2025-06-12T16:21:33.277217",
        "sourceFile": "EMP.cpy"
    },
    "record": {
        "type": "object",
        "name": "EMP-RECORD",
        "recordType": "fixed",
        "maxLength": 150,
        "properties": {
            "EMP-ID": {
                "type": "number",
                "picture": "9(5)",
                "precision": 5,
                "scale": 0,
                "offset": 0,
                "maxLength": 5
            },
            "EMP-ID-X": {
                "type": "string",
                "picture": "X(5)",
                "redefines": "EMP-ID",
                "offset": 0,
                "maxLength": 5
            },
            "EMP-NAME": {
                "type": "string",
                "picture": "X(25)",
                "offset": 5,
                "maxLength": 25
            },
            "EMP-DOB": {
                "type": "string",
                "picture": "X(10)",
                "offset": 30,
                "maxLength": 10
            },
            "EMP-ADDRESS": {
                "type": "object",
                "occurs": {
                    "min": 3,
                    "max": 3
                },
                "offset": 40,
                "maxLength": 75,
                "properties": {
                    "EMP-ADDR-LINE": {
                        "type": "string",
                        "picture": "X(25)",
                        "offset": 40,
                        "maxLength": 25
                    }
                }
            },
            "EMP-YOE-CUR": {
                "type": "number",
                "picture": "S9(4)",
                "precision": 4,
                "scale": 0,
                "usage": "COMP",
                "signed": true,
                "offset": 115,
                "maxLength": 2
            },
            "EMP-YOE-TOTAL": {
                "type": "number",
                "picture": "9(4)V99",
                "precision": 6,
                "scale": 2,
                "usage": "COMP-3",
                "offset": 117,
                "maxLength": 4
            },
            "EMP-SALARY": {
                "type": "number",
                "picture": "S9(4)V99",
                "precision": 6,
                "scale": 2,
                "signed": true,
                "offset": 121,
                "maxLength": 6
            },
            "EMP-SALARY-DIFF": {
                "type": "number",
                "picture": "S9999V99",
                "precision": 6,
                "scale": 2,
                "usage": "COMP-3",
                "signed": true,
                "offset": 127,
                "maxLength": 4
            },
            "EMP-DEPENDENTS-NUM": {
                "type": "number",
                "picture": "S9(2)",
                "precision": 2,
                "scale": 0,
                "signed": true,
                "offset": 131,
                "maxLength": 2
            },
            "FILLER-X-1001": {
                "type": "string",
                "picture": "X(17)",
                "offset": 133,
                "maxLength": 17
            }
        }
    }
}
```

The tool generates a comprehensive JSON schema that includes:
- **Field names and types** with proper data type mapping
- **Data lengths and precision** for numeric fields
- **Array structures** for OCCURS clauses (EMP-ADDRESS occurs 3 times)
- **REDEFINES handling** (EMP-ID-X redefines EMP-ID)
- **USAGE types** (COMP, COMP-3) with appropriate storage calculations
- **Signed field indicators** for fields with sign
- **Field offsets** showing exact byte positions in the record
- **Metadata** including generation timestamp and source file

## API Reference

### convert_copybook_to_json(copybook_content, copybook_name="copybook.cpy", debug=False)

**Parameters:**
- `copybook_content` (str or list): COBOL copybook content as string or list of strings
- `copybook_name` (str, optional): Name for the copybook (default: "copybook.cpy")
- `debug` (bool, optional): Enable debug output (default: False)

**Returns:**
Dictionary with the following keys:
- `status`: "success" or "error"
- `json_string`: Generated JSON schema (if successful)
- `record_size`: Total record size in bytes
- `field_count`: Number of fields processed
- `message`: Error message (if failed)
- `traceback`: Detailed error information (if debug enabled)

## Requirements

- Python 3.7 or higher
- No external dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Use Cases

- **Mainframe Modernization**: Convert legacy COBOL data structures for modern applications
- **Data Integration**: Understand COBOL data formats for ETL processes
- **API Development**: Generate schemas for APIs that interface with mainframe systems
- **Documentation**: Create readable documentation of COBOL data structures
