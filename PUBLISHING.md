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
- Current version: 1.0.0
