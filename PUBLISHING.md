# Publishing to PyPI

## Prerequisites

1. Create accounts on:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)

2. Install required tools:
   ```bash
   pipx install build twine
   ```

## Steps to Publish

### 1. Update Project Information

Before publishing, update these files with your information:

**pyproject.toml:**
```toml
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
```

**pyproject.toml URLs:**
```toml
[project.urls]
Homepage = "https://github.com/yourusername/cobol_copybook_to_json"
"Bug Reports" = "https://github.com/yourusername/cobol_copybook_to_json/issues"
"Source" = "https://github.com/yourusername/cobol_copybook_to_json"
```

### 2. Test the Package

```bash
# Run tests
python -m unittest tests.test_cobol_converter -v

# Test the example
python examples/convert_emp_example.py
```

### 3. Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
pyproject-build
```

### 4. Check the Package

```bash
# Verify the package
twine check dist/*
```

### 5. Test Upload (Optional but Recommended)

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ cobol-copybook-to-json
```

### 6. Upload to PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

## After Publishing

1. Test installation:
   ```bash
   pip install cobol-copybook-to-json
   ```

2. Test command-line tool:
   ```bash
   cobol-to-json -c examples/EMP.cpy -j output.json
   ```

3. Test library usage:
   ```python
   from cobol_copybook_to_json import convert_copybook_to_json
   # Your code here
   ```

## Version Management

To release a new version:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` (if you create one)
3. Rebuild and republish

## Notes

- Package name: `cobol-copybook-to-json`
- Command-line tool: `cobol-to-json`
- Python import: `cobol_copybook_to_json`
- Current version: 1.1.0

## Recent Changes (v1.1.0)

### Major Features Added:
- **Multiple 01-level record support**: Now handles copybooks with multiple 01-level records
- **Consistent API**: Uses `recordLayouts` array for both single and multiple records  
- **Auto-generation**: Creates root record when no 01-level found with warning message
- **Accurate field counting**: Recursive counting of all fields including nested ones

### API Changes:
- Changed from `record` to `recordLayouts` array structure
- Removed redundant `recordCount` from metadata
- Enhanced field counting accuracy

### Files Modified:
- `src/cobol_copybook_to_json/__init__.py` - Main converter logic
- `setup.py` - Version bumped to 1.1.0
- `CHANGELOG.md` - Added v1.1.0 release notes
