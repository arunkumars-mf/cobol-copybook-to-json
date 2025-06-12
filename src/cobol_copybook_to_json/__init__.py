#!/usr/bin/env python3
"""
COBOL Copybook to JSON Schema Converter

This script converts COBOL copybooks to JSON schema format. It handles various
COBOL data structures including groups, elementary items, OCCURS clauses,
REDEFINES, and different USAGE types.

Usage as command-line tool:
    python cobol_copybook_to_json.py -c <input_copybook> -j <output_json> [-d]

Usage as library:
    from cobol_copybook_to_json import convert_copybook_to_json
    result = convert_copybook_to_json(copybook_content, copybook_name="my_copybook.cpy")
"""

import re
import json
import argparse
import sys
import os
import datetime
from typing import List, Tuple, Dict, Any, TextIO, Optional, Union

# Global variables for program configuration
DEBUG = False
FILLER_COUNTER = 1000

class Field:
    """Represents a COBOL field structure with all its attributes."""
    def __init__(self):
        self.name: str = ""
        self.type: str = ""
        self.level: int = 0
        self.precision: int = 0
        self.scale: int = 0
        self.usage: str = ""
        self.occurs: 'OccursInfo' = None
        self.redefines: str = ""
        self.picture: str = ""
        self.is_group: bool = False
        self.children: List['Field'] = []
        self.offset: int = 0
        self.min_length: int = 0
        self.max_length: int = 0
        self.order: int = 0
        self.signed: bool = False

class OccursInfo:
    """Represents COBOL OCCURS clause information."""
    def __init__(self):
        self.min: int = 0
        self.max: int = 0
        self.depending_on: str = ""

# Compile regular expressions for better performance
LEVEL_REGEX = re.compile(r'^\s*(\d+)\s+(\S+)')
PIC_REGEX = re.compile(r'PIC\s+(\S+)')
OCCURS_REGEX = re.compile(r'OCCURS\s+(?:(\d+)(?:\s+TO\s+(\d+))?)(?:\s+TIMES)?(?:\s+DEPENDING\s+ON\s+(\S+))?')
REDEFINES_REGEX = re.compile(r'REDEFINES\s+(\S+)')
USAGE_REGEX = re.compile(r'(USAGE\s+)?(COMP-3|COMPUTATIONAL-3|PACKED-DECIMAL|BINARY|COMP|COMPUTATIONAL|DISPLAY)[\s\.]')
PIC_CONTENT_REGEX = re.compile(r'(?P<sign>\+|-|S|DB|CR)|(?P<char>\$|,|/|\*|B)|(?P<decimal>V|\.)|(?P<repeat>[AX9Z0](\(\d+\))?|[AX9Z0]+)')
def clean_copybook(copybook: str) -> str:
    """
    Preprocess the copybook content by removing sequence numbers, comments, and normalizing line continuations.
    Uses the same logic as cobol_tokenizer.py for consistent cleaning.
    
    Args:
        copybook (str): Raw copybook content.
    
    Returns:
        str: Cleaned and normalized copybook content.
    """
    # Step 1: Clean the copybook using the same logic as cobol_tokenizer.py
    # Extract content from columns 7-72, skip comment lines and directives
    cleaned_lines = [line[6:72].rstrip() for line in copybook.split('\n') 
                    if len(line) > 6 and line[6] not in ('*', '/')]
    cleaned_lines = [line for line in cleaned_lines 
                    if line.strip() not in ("EJECT", "SKIP1", "SKIP2", "SKIP3")]
    cleaned_lines = [line for line in cleaned_lines if len(line) > 0]
    
    # Join all lines with spaces to create a single string
    cleaned_data = ' '.join(cleaned_lines)
    
    # Step 2: Tokenize and reconstruct statements
    line_sep = r'[.,;]?$|[.,;]?\s'
    s_quote = r"'[^']*'"
    d_quote = r'"[^"]*"'
    reg_ex = re.compile(f"({line_sep}|{s_quote}|{d_quote})")
    
    # Split the cleaned data into tokens
    tokens = [token.strip() for token in re.split(reg_ex, cleaned_data) if token.strip()]
    
    # Reconstruct statements based on periods
    processed_lines = []
    current_line = []
    
    for token in tokens:
        if token == '.':
            current_line.append('.')
            processed_lines.append(' '.join(current_line))
            current_line = []
        else:
            current_line.append(token)
    
    # Add any remaining tokens as a line
    if current_line:
        processed_lines.append(' '.join(current_line))
    
    if DEBUG:
        print("Processed COBOL statements:")
        for i, line in enumerate(processed_lines):
            print(f"{i+1}: {line}")
    
    return '\n'.join(processed_lines)

def find_field_by_name(fields: List[Field], name: str) -> Field:
    """
    Recursively search for a field by name in the field hierarchy.
    
    Args:
        fields (List[Field]): List of fields to search.
        name (str): Name of the field to find.
    
    Returns:
        Field: The found Field object or None if not found.
    """
    for field in fields:
        if field.name == name:
            return field
        if field.is_group:
            subfield = find_field_by_name(field.children, name)
            if subfield:
                return subfield
    return None
def parse_fields(lines: List[str], parent_level: int, start_offset: int, parent_usage: str) -> Tuple[List[Field], int, int, int]:
    """
    Parse COBOL fields from the copybook lines.
    
    Args:
        lines (List[str]): Lines of the copybook to parse.
        parent_level (int): Level number of the parent field.
        start_offset (int): Starting byte offset for fields.
        parent_usage (str): Usage of the parent field.
    
    Returns:
        Tuple[List[Field], int, int, int]: 
            - List of parsed fields
            - Number of lines processed
            - Minimum length of the structure
            - Maximum length of the structure
    """
    global FILLER_COUNTER
    fields = []
    i = 0
    current_offset = start_offset
    min_length = max_length = 0
    current_redefines = []
    last_redefined_name = ""

    while i < len(lines):
        field = parse_line(lines[i])
        if not field:
            i += 1
            continue
        if field.level <= parent_level:
            break
            
        # Skip 88, 66, and 77 levels
        if field.level in [88, 66, 77]:
            if DEBUG:
                print(f"Debug: Skipping level {field.level} field: {field.name}")
            i += 1
            continue

        field.offset = current_offset

        if not field.usage and parent_usage:
            field.usage = parent_usage
            if DEBUG:
                print(f"Debug: Inherited usage {parent_usage} for field {field.name}")

        if field.redefines:
            redefined_field = find_field_by_name(fields, field.redefines)
            if redefined_field:
                field.offset = redefined_field.offset
                if field.is_group:
                    sub_fields, processed, sub_min_length, sub_max_length = parse_fields(lines[i+1:], field.level, field.offset, field.usage)
                    field.children = sub_fields
                    field.min_length = sub_min_length
                    field.max_length = sub_max_length
                    i += processed

                if field.redefines != last_redefined_name and current_redefines:
                    idx = next((i for i, f in enumerate(fields) if f.name == last_redefined_name), -1)
                    if idx >= 0:
                        fields[idx+1:idx+1] = current_redefines
                    current_redefines = []

                last_redefined_name = field.redefines
                current_redefines.append(field)
            else:
                print(f"Warning: Redefined field {field.redefines} not found for {field.name}")
        else:
            if field.is_group:
                sub_fields, processed, sub_min_length, sub_max_length = parse_fields(lines[i+1:], field.level, current_offset, field.usage)
                field.children = sub_fields
                field.min_length = sub_min_length
                field.max_length = sub_max_length
                i += processed

            calculate_field_size(field)

            if field.occurs:
                if DEBUG:
                    print(f"Debug: Applying OCCURS to {field.name}: base size={field.min_length}, occurs min={field.occurs.min}, max={field.occurs.max}")
                field.min_length *= field.occurs.min
                field.max_length *= field.occurs.max

            if current_redefines:
                idx = next((i for i, f in enumerate(fields) if f.name == last_redefined_name), -1)
                if idx >= 0:
                    fields[idx+1:idx+1] = current_redefines
                current_redefines = []

            fields.append(field)
            current_offset += field.max_length
            min_length += field.min_length
            max_length = max(max_length, field.max_length)

        i += 1

    if current_redefines:
        idx = next((i for i, f in enumerate(fields) if f.name == last_redefined_name), -1)
        if idx >= 0:
            fields[idx+1:idx+1] = current_redefines

    return fields, i, min_length, current_offset - start_offset
def parse_line(line: str) -> Field:
    """
    Parse a single line of COBOL copybook and create a Field structure.
    
    Args:
        line (str): Single line from the copybook.
    
    Returns:
        Field: Created Field object or None if line is invalid.
    """
    global FILLER_COUNTER
    if DEBUG:
        print(f"Debug: Parsing line: {line}")

    level_match = LEVEL_REGEX.match(line)
    if not level_match:
        return None

    level = int(level_match.group(1))
    field = Field()
    field.name = level_match.group(2).rstrip('.')
    field.level = level
    field.is_group = "PIC" not in line

    if field.name.startswith("FILLER"):
        FILLER_COUNTER += 1
        field.name = f"FILLER-X-{FILLER_COUNTER}"

    pic_match = PIC_REGEX.search(line)
    if pic_match:
        field.picture = pic_match.group(1)
        field.type, field.min_length, field.max_length, field.precision, field.scale, field.signed = parse_pic(field.picture)

    usage_match = USAGE_REGEX.search(line)
    if usage_match:
        if DEBUG:
            print(f"Debug: Usage match: {usage_match.groups()}")
        usage = usage_match.group(2).rstrip('.')
        field.usage = normalize_usage(usage)

    occurs_match = OCCURS_REGEX.search(line)
    if occurs_match:
        field.occurs = OccursInfo()
        field.occurs.min = int(occurs_match.group(1) or 0)
        field.occurs.max = int(occurs_match.group(2) or field.occurs.min)
        if occurs_match.group(3):
            field.occurs.depending_on = occurs_match.group(3).rstrip('.')

    redefines_match = REDEFINES_REGEX.search(line)
    if redefines_match:
        field.redefines = redefines_match.group(1).rstrip('.')

    if DEBUG:
        print(f"Debug: Parsed field: {vars(field)}")
    return field

def parse_pic(pic: str) -> Tuple[str, int, int, int, int, bool]:
    """
    Analyze a COBOL PICTURE clause and determine field characteristics.
    
    Args:
        pic (str): PICTURE clause string.
    
    Returns:
        Tuple[str, int, int, int, int, bool]: 
            - Field type ("string" or "number")
            - Minimum field length
            - Maximum field length
            - Precision (total number of digits for numeric fields)
            - Scale (number of decimal places)
            - Whether the number is signed
    """
    if DEBUG:
        print(f"Debug: parsePIC input: {pic}")
    pic = pic.upper().replace('.', '')
    matches = PIC_CONTENT_REGEX.findall(pic)

    total_length = precision = scale = 0
    is_numeric = is_decimal = is_signed = False

    is_numeric = all(match[3].startswith(('9', 'P')) for match in matches if match[3])

    for match in matches:
        if match[0]:  # sign
            is_signed = True
        elif match[1]:  # char
            total_length += 1
        elif match[2]:  # decimal
            is_decimal = True
        elif match[3]:  # repeat
            repeat_item = match[3]
            count = int(repeat_item[2:-1]) if '(' in repeat_item else len(repeat_item)
            total_length += count
            if is_numeric and '9' in repeat_item:
                precision += count
                if is_decimal:
                    scale += count

    if not is_numeric:
        if DEBUG:
            print(f"Debug: parsePIC result: string, length: {total_length}")
        return "string", total_length, total_length, 0, 0, False

    if DEBUG:
        print(f"Debug: parsePIC result: number, length: {total_length}, precision: {precision}, scale: {scale}, signed: {is_signed}")
    return "number", total_length, total_length, precision, scale, is_signed
def normalize_usage(usage: str) -> str:
    """
    Standardize COBOL usage clauses to consistent values.
    
    Args:
        usage (str): Original usage clause from copybook.
    
    Returns:
        str: Normalized usage string (COMP, COMP-3, DISPLAY, etc.)
    """
    usage = usage.upper()
    if usage in ["BINARY", "COMP", "COMP-4", "COMP-5", "COMPUTATIONAL", "COMPUTATIONAL-4", "COMPUTATIONAL-5"]:
        return "COMP"
    elif usage in ["PACKED-DECIMAL", "COMP-3", "COMPUTATIONAL-3"]:
        return "COMP-3"
    elif usage in ["COMP-1", "COMPUTATIONAL-1"]:
        return "COMP-1"
    elif usage in ["COMP-2", "COMPUTATIONAL-2"]:
        return "COMP-2"
    else:
        return "DISPLAY"


def calculate_field_size(field: Field) -> None:
    """
    Determine the byte size of a field based on its usage.

    Args:
        field (Field): Field structure to calculate size for.
    """
    if field.is_group:
        return
    if field.usage == "COMP":
        field.min_length, field.max_length = comp_size(field.precision)
    elif field.usage == "COMP-3":
        field.min_length = field.max_length = comp3_size(field.precision)
    elif field.usage in ["COMP-1", "COMP-2"]:
        field.min_length = field.max_length = 4 if field.usage == "COMP-1" else 8

def comp_size(precision: int) -> Tuple[int, int]:
    """
    Calculate the byte size for COMPUTATIONAL fields.

    Args:
        precision (int): Number of digits in the field.

    Returns:
        Tuple[int, int]: Minimum and maximum sizes in bytes.
    """
    if precision <= 4:
        return 2, 2
    elif precision <= 9:
        return 4, 4
    else:
        return 8, 8

def comp3_size(precision: int) -> int:
    """
    Calculate the byte size for COMPUTATIONAL-3 (packed decimal) fields.

    Args:
        precision (int): Number of digits in the field.

    Returns:
        int: Size in bytes.
    """
    return max(1, (precision + 2) // 2)
def create_json_schema(root_field: Field) -> Dict[str, Any]:
    """
    Create the JSON schema representation of the COBOL structure.

    Args:
        root_field (Field): Top-level field of the COBOL structure.

    Returns:
        Dict[str, Any]: JSON schema as a dictionary
    """
    record_type = "fixed" if root_field.min_length == root_field.max_length else "variable"

    schema = {
        "type": "object",
        "name": root_field.name.rstrip('.'),
        "recordType": record_type,
        "minLength": root_field.min_length,
        "maxLength": root_field.max_length,
        "properties": {}
    }

    add_fields_to_schema(root_field.children, schema["properties"])
    return schema

def add_fields_to_schema(fields: List[Field], properties: Dict[str, Any]) -> None:
    """
    Recursively add field definitions to the JSON schema.

    Args:
        fields (List[Field]): List of fields to output.
        properties (Dict[str, Any]): Dictionary to store the field properties.
    """
    for field in fields:
        field_schema = {
            "type": "object" if field.is_group else field.type
        }

        if field.picture:
            field_schema["picture"] = field.picture.rstrip('.')
        if field.precision > 0:
            field_schema["precision"] = field.precision
        if field.scale > 0 or (field.type == "number" and field.precision > 0):
            field_schema["scale"] = field.scale
        if field.usage and field.usage != "DISPLAY":
            field_schema["usage"] = field.usage

        if field.occurs:
            field_schema["occurs"] = {
                "min": field.occurs.min,
                "max": field.occurs.max
            }
            if field.occurs.depending_on:
                field_schema["occurs"]["dependingOn"] = field.occurs.depending_on

        if field.redefines:
            field_schema["redefines"] = field.redefines
        if field.signed:
            field_schema["signed"] = True

        field_schema["offset"] = field.offset
        field_schema["minLength"] = field.min_length
        field_schema["maxLength"] = field.max_length

        if field.is_group and field.children:
            field_schema["properties"] = {}
            add_fields_to_schema(field.children, field_schema["properties"])

        properties[field.name.rstrip('.')] = field_schema

def clean_schema(schema_obj):
    """
    Clean up the schema by removing redundant properties.
    
    Args:
        schema_obj: Schema object to clean
    """
    if isinstance(schema_obj, dict):
        # Process current level
        if "minLength" in schema_obj and "maxLength" in schema_obj:
            if schema_obj["minLength"] == schema_obj["maxLength"]:
                schema_obj.pop("minLength")

        # Process nested objects
        for key, value in list(schema_obj.items()):
            if isinstance(value, (dict, list)):
                clean_schema(value)
    elif isinstance(schema_obj, list):
        for item in schema_obj:
            if isinstance(item, (dict, list)):
                clean_schema(item)
def convert_copybook_to_json(
    copybook_content: Union[str, List[str]],
    copybook_name: str = "copybook.cpy",
    debug: bool = False
) -> Dict[str, Any]:
    """
    Convert COBOL copybook to JSON schema format.

    Handles groups, elementary items, OCCURS clauses, REDEFINES, and different USAGE types.

    Args:
        copybook_content: COBOL copybook content as string or list of strings
        copybook_name: Name to use for the copybook (optional, defaults to "copybook.cpy")
        debug: Enable debug output (optional)

    Returns:
        Dictionary with the result of the conversion including the JSON schema
    """
    global DEBUG
    DEBUG = debug

    try:
        # Handle different input types for copybook_content
        if isinstance(copybook_content, list):
            copybook_content = '\n'.join(copybook_content)
        elif not isinstance(copybook_content, str):
            return {
                "status": "error",
                "message": f"Error: copybook_content must be a string or list, got {type(copybook_content)}"
            }

        # Process the copybook content
        cleaned_copybook = clean_copybook(copybook_content)
        if DEBUG:
            print("Cleaned copybook:")
            print(cleaned_copybook)

        lines = cleaned_copybook.split('\n')
        fields, _, min_length, max_length = parse_fields(lines, 0, 0, "")

        root_field = next((field for field in fields if field.level == 1), None)
        if not root_field:
            # No 01 level found, create one with a generic name
            root_name = "GENERATED-LEVEL-01"

            if DEBUG:
                print(f"No 01 level found. Creating root level with name: {root_name}")

            # Create a new root field
            root_field = Field()
            root_field.name = root_name
            root_field.level = 1
            root_field.is_group = True
            root_field.children = fields
            
            # Adjust the level numbers of all existing fields
            for field in fields:
                field.level += 1

        root_field.min_length = min_length
        root_field.max_length = max_length

        # Create the JSON schema
        record_schema = create_json_schema(root_field)

        # Create the final schema with metadata
        json_schema = {
            "metadata": {
                "version": "1.0",
                "generatedAt": datetime.datetime.now().isoformat(),
                "sourceFile": copybook_name
            },
            "record": record_schema
        }

        # Clean the schema before output
        clean_schema(json_schema)

        # Convert to JSON string
        json_string = json.dumps(json_schema, indent=4)

        return {
            "status": "success",
            "copybook_name": copybook_name,
            "record_size": max_length,
            "field_count": len(fields),
            "schema": json_schema,
            "json_string": json_string
        }

    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
            "traceback": traceback.format_exc()
        }
def parse_args() -> Tuple[str, str, bool]:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Convert COBOL copybook to JSON schema")
    parser.add_argument("-c", "--input-copybook", required=True, help="Input copybook file")
    parser.add_argument("-j", "--output-json-file", required=True, help="Output JSON file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    return args.input_copybook, args.output_json_file, args.debug

def main():
    """Main function to orchestrate the conversion process when run as a command-line tool."""
    input_file, output_file, debug = parse_args()

    try:
        with open(input_file, 'r') as file:
            copybook_data = file.read()
    except IOError as e:
        print(f"Error reading file {input_file}: {e}")
        sys.exit(1)

    # Use the API function for conversion
    result = convert_copybook_to_json(
        copybook_content=copybook_data,
        copybook_name=os.path.basename(input_file),
        debug=debug
    )

    if result["status"] == "error":
        print(f"Error converting copybook: {result['message']}")
        if debug and "traceback" in result:
            print(result["traceback"])
        sys.exit(1)

    try:
        with open(output_file, 'w') as file:
            file.write(result["json_string"])
        print(f"JSON schema has been written to {output_file}")
        print(f"Record size: {result['record_size']} bytes")
        print(f"Field count: {result['field_count']}")
    except IOError as e:
        print(f"Error creating output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
