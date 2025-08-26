# Contributing to CosmicExcuse

Thank you for your interest in contributing to CosmicExcuse! We welcome contributions from the community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)
- [Adding Excuses](#adding-excuses)
- [Adding Languages](#adding-languages)

## Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project
you agree to abide by its terms.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a branch** for your changes
4. **Make your changes** and test them
5. **Push your changes** to your fork
6. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment tool (venv, virtualenv, etc.)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cosmicexcuse.git
cd cosmicexcuse

# Add upstream remote
git remote add upstream https://github.com/shamspias/cosmicexcuse.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

## Making Changes

### Creating a Feature Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name
```

### Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

Run these before committing:

```bash
# Format code
black cosmicexcuse tests

# Check linting
flake8 cosmicexcuse tests

# Type checking
mypy cosmicexcuse
```

### Commit Messages

Write clear and descriptive commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

Example:

```
Add quantum entanglement excuses

- Add 10 new quantum-themed excuses
- Update quantum.json with new entries
- Add tests for quantum category

Fixes #123
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cosmicexcuse --cov-report=html

# Run specific test file
pytest tests/test_generator.py -v

# Run specific test
pytest tests/test_generator.py::TestCosmicExcuse::test_generate_saves_history
```

### Writing Tests

- Write tests for any new functionality
- Maintain or improve code coverage
- Use descriptive test names
- Follow existing test patterns

Example test:

```python
def test_new_feature():
    """Test that new feature works correctly."""
    generator = CosmicExcuse()
    result = generator.new_feature()
    assert result is not None
    assert isinstance(result, ExpectedType)
```

## Submitting Changes

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Run all tests** and ensure they pass
4. **Update README.md** if adding new features
5. **Submit pull request** with clear description

### Pull Request Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing

- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Updated documentation

## Related Issues

Fixes #(issue number)
```

## Style Guidelines

### Python Style

Follow [PEP 8](https://pep8.org/) with these additions:

- Maximum line length: 88 characters (Black default)
- Use type hints where appropriate
- Document all public functions and classes
- Use descriptive variable names

### Documentation Style

- Use clear, concise language
- Include code examples where helpful
- Keep README.md updated
- Document all public APIs

## Adding Excuses

### Adding to Existing Categories

1. Open the appropriate JSON file in `cosmicexcuse/data/{language}/`
2. Add your excuses to the `excuses` array
3. Keep excuses creative but appropriate
4. Test that they load correctly

Example:

```json
{
  "category": "quantum",
  "language": "en",
  "version": "1.0.0",
  "excuses": [
    "existing excuse",
    "your new creative excuse here"
  ]
}
```

### Adding New Categories

1. Create a new JSON file in the appropriate language directory
2. Follow the schema:

```json
{
  "category": "category_name",
  "language": "en",
  "version": "1.0.0",
  "excuses": [
    "excuse 1",
    "excuse 2"
  ]
}
```

3. Update the data loader if necessary
4. Add tests for the new category

## Adding Languages

### Steps to Add a New Language

1. **Create language directory**: `cosmicexcuse/data/{language_code}/`

2. **Create JSON files** for each category:
    - quantum.json
    - cosmic.json
    - ai.json
    - technical.json
    - blame.json
    - recommendations.json
    - connectors.json
    - intensifiers.json

3. **Update supported languages** in `generator.py`:

```python
SUPPORTED_LANGUAGES = ['en', 'bn', 'your_language_code']
```

4. **Add tests** for the new language:

```python
def test_new_language():
    generator = CosmicExcuse(language='your_language_code')
    excuse = generator.generate()
    assert excuse.language == 'your_language_code'
```

5. **Update documentation** to mention the new language

### Translation Guidelines

- Maintain the humor and technical feel
- Adapt cultural references appropriately
- Keep technical terms recognizable
- Test with native speakers if possible

## Questions?

Feel free to:

- Open an [issue](https://github.com/shamspias/cosmicexcuse/issues)
- Start a [discussion](https://github.com/shamspias/cosmicexcuse/discussions)
- Contact the maintainers

## Recognition

Contributors will be recognized in:

- The project README
- The AUTHORS file
- Release notes

Thank you for contributing to CosmicExcuse! 🚀