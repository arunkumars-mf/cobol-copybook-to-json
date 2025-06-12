# Contributing to COBOL Copybook to JSON Schema Converter

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the [Issues](https://github.com/arunkumars-mf/cobol-copybook-to-json/issues)
2. If not, create a new issue with:
   - Clear description of the problem or feature request
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Sample COBOL copybook (if applicable)

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run tests** to ensure everything works
   ```bash
   python -m unittest tests.test_cobol_converter -v
   ```
6. **Update documentation** if needed
7. **Commit your changes**
   ```bash
   git commit -m "Add feature: description of your changes"
   ```
8. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
9. **Create a Pull Request**

### Development Setup

1. Clone the repository
   ```bash
   git clone https://github.com/arunkumars-mf/cobol-copybook-to-json.git
   cd cobol-copybook-to-json
   ```

2. Install development dependencies
   ```bash
   pip install -e .
   ```

3. Run tests
   ```bash
   python -m unittest tests.test_cobol_converter -v
   ```

4. Test the example
   ```bash
   python examples/convert_emp_example.py
   ```

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and reasonably sized

### Testing

- Add unit tests for new features
- Ensure all tests pass before submitting
- Include edge cases in your tests
- Test with various COBOL copybook structures

### Areas for Contribution

We welcome contributions in these areas:

1. **COBOL Features**
   - Additional USAGE types
   - More complex OCCURS scenarios
   - DEPENDING ON clauses
   - Conditional fields

2. **Output Formats**
   - Additional schema formats (Avro, Protobuf, etc.)
   - Custom output templates
   - Different JSON schema versions

3. **Performance**
   - Optimization for large copybooks
   - Memory usage improvements
   - Processing speed enhancements

4. **Documentation**
   - More examples
   - Tutorial content
   - API documentation improvements

5. **Testing**
   - Additional test cases
   - Performance benchmarks
   - Integration tests

### Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Contact the maintainer: aruninfy123@gmail.com

Thank you for contributing!
