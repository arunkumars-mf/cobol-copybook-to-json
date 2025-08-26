# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-08-26

### Added
- **Multiple 01-level record support**: Now handles copybooks with multiple 01-level records
- **Auto-generation of missing 01-level**: Creates root record when no 01-level found
- **Consistent API structure**: Uses `recordLayouts` array for both single and multiple records
- **Enhanced field counting**: Recursive field counting for accurate totals
- **Warning messages**: Informative messages for auto-generated structures

### Changed
- **API Structure**: Changed from `record` to `recordLayouts` array for consistency
- **Field counting**: Now counts all fields recursively including nested ones
- **Elementary record handling**: Proper schema generation for elementary 01-level fields
- **Error handling**: Improved handling of incomplete copybooks

### Fixed
- **Multiple 01-level processing**: Previously only processed first 01-level record
- **Field count accuracy**: Now correctly counts all fields including nested ones
- **REDEFINES in multiple records**: Proper handling of REDEFINES across multiple 01-levels

## [1.0.2] - 2024-06-12

### Changed
- Updated author information to Arunkumar Selvam
- Updated email to aruninfy123@gmail.com
- Updated copyright in LICENSE file

## [1.0.1] - 2024-06-12

### Changed
- Enhanced README with real EMP.cpy example
- Added comprehensive JSON schema output example
- Improved documentation with actual COBOL structures

### Added
- Complete EMP.cpy copybook example showing:
  - OCCURS clauses (arrays)
  - REDEFINES clauses
  - COMP and COMP-3 usage types
  - Signed numeric fields
  - Field offsets and lengths

## [1.0.0] - 2024-06-12

### Added
- Initial release of COBOL Copybook to JSON Schema Converter
- Command-line tool `cobol-to-json`
- Python library with `convert_copybook_to_json` function
- Support for complex COBOL structures:
  - Group items and elementary items
  - OCCURS clauses (arrays)
  - REDEFINES clauses
  - Different USAGE types (COMP, COMP-3, etc.)
  - PICTURE clauses with various data types
  - Signed and unsigned numeric fields
- Comprehensive error handling and debug mode
- Professional package structure with tests and examples
- MIT License
- Published to PyPI
