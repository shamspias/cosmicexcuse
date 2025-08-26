# 🚀 CosmicExcuse

<div align="center">

[![PyPI version](https://badge.fury.io/py/cosmicexcuse.svg)](https://badge.fury.io/py/cosmicexcuse)
[![Python Support](https://img.shields.io/pypi/pyversions/cosmicexcuse.svg)](https://pypi.org/project/cosmicexcuse/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/cosmicexcuse/badge/?version=latest)](https://cosmicexcuse.readthedocs.io/)
[![Tests](https://github.com/shamspias/cosmicexcuse/actions/workflows/tests.yml/badge.svg)](https://github.com/shamspias/cosmicexcuse/actions/workflows/tests.yml)

<img src="https://raw.githubusercontent.com/shamspias/cosmicexcuse/main/docs/assets/logo.png" alt="CosmicExcuse Logo" width="200"/>

**Generate quantum-grade excuses for your code failures!** 🐛✨

*"It's not a bug, it's a quantum feature!"*

[**Installation**](#-installation) • [**Quick Start**](#-quick-start) • [**Documentation
**](https://cosmicexcuse.readthedocs.io/) • [**Examples**](#-examples) • [**API Reference**](#-api-reference)

</div>

---

## 📖 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Examples](#-examples)
- [CLI Usage](#-cli-usage)
- [API Reference](#-api-reference)
- [Configuration](#️-configuration)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Features

- 🌍 **Multi-language Support** - English and Bengali with easy extensibility
- 🎯 **Smart Severity Analysis** - Automatically adapts to error severity
- 🔬 **Technical Jargon Generation** - Markov chain-based technobabble
- 📊 **Excuse Quality Scoring** - Rate and track the best excuses
- 🎨 **Multiple Output Formats** - Plain text, Markdown, JSON, Haiku
- 🏆 **Leaderboard System** - Track and rank excuses
- 📦 **Zero Dependencies** - Pure Python implementation
- 🚀 **Fast & Lightweight** - Instant generation with minimal overhead

### Excuse Categories

- **Quantum** - Quantum mechanics and physics-based excuses
- **Cosmic** - Space and astronomical phenomena
- **AI** - Machine learning and artificial intelligence
- **Technical** - General technical difficulties
- **Blame** - Redirect responsibility creatively

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install cosmicexcuse
```

### From Source

```bash
git clone https://github.com/shamspias/cosmicexcuse.git
cd cosmicexcuse
pip install -e .
```

### Development Installation

```bash
pip install cosmicexcuse[dev]  # Includes testing and linting tools
```

## 🚀 Quick Start

### Python API

```python
from cosmicexcuse import CosmicExcuse

# Initialize generator
generator = CosmicExcuse()

# Generate an excuse for your error
excuse = generator.generate("FATAL ERROR: Database connection failed!")

print(excuse.text)
# Output: "The error was catastrophically caused by quantum entanglement 
#          in the CPU cache, resulting in solar flare interference..."

print(excuse.recommendation)
# Output: "Try turning it off and on again, but quantumly"
```

### One-Liner

```python
import cosmicexcuse

print(cosmicexcuse.generate("Segmentation fault"))
```

### CLI Usage

```bash
# Generate a random excuse
cosmicexcuse

# Generate for specific error
cosmicexcuse --error "Failed to compile"

# Generate haiku
cosmicexcuse --haiku

# Generate in Bengali
cosmicexcuse --language bn
```

## 📚 Examples

### Basic Usage

```python
from cosmicexcuse import CosmicExcuse

generator = CosmicExcuse()

# Simple generation
excuse = generator.generate()
print(f"Excuse: {excuse.text}")
print(f"Recommendation: {excuse.recommendation}")
print(f"Severity: {excuse.severity}")
print(f"Quality Score: {excuse.quality_score}/100")
```

### Category-Specific Excuses

```python
# Generate quantum-themed excuse
quantum_excuse = generator.generate(
    error_message="Array index out of bounds",
    category="quantum"
)

# Generate AI-themed excuse
ai_excuse = generator.generate(
    error_message="Model training failed",
    category="ai"
)

# Generate cosmic-themed excuse
cosmic_excuse = generator.generate(
    error_message="Connection timeout",
    category="cosmic"
)
```

### Batch Generation

```python
# Generate multiple excuses
excuses = generator.generate_batch(count=5)

for i, excuse in enumerate(excuses, 1):
    print(f"{i}. {excuse.text[:50]}...")
    print(f"   Score: {excuse.quality_score}/100")
```

### Haiku Mode

```python
# Generate poetic excuse
haiku = generator.generate_haiku("Memory leak detected")
print(haiku)

# Output:
# Quantum states collapsed
# The servers cry digital tears
# Bits flipped in the void
```

### History and Best Excuses

```python
# Track history
generator = CosmicExcuse()

# Generate several excuses
for i in range(10):
    generator.generate(f"Error {i}")

# Get the best excuse
best = generator.get_best_excuse()
print(f"Best excuse (score {best.quality_score}): {best.text}")

# Export history
history = generator.export_history(format='json')
```

### Custom Formatting

```python
from cosmicexcuse.formatter import MarkdownFormatter, TwitterFormatter

# Markdown format
md_formatter = MarkdownFormatter()
markdown_output = md_formatter.format(excuse.__dict__)

# Twitter-ready format (280 chars)
twitter_formatter = TwitterFormatter()
tweet = twitter_formatter.format({'text': excuse.text})
```

### Error Handler Integration

```python
from cosmicexcuse import CosmicExcuse

generator = CosmicExcuse()


def cosmic_handler(func):
    """Decorator to handle errors with cosmic excuses."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            excuse = generator.generate(str(e))
            print(f"Error: {e}")
            print(f"Excuse: {excuse.text}")
            print(f"Fix: {excuse.recommendation}")
            raise

    return wrapper


@cosmic_handler
def risky_function():
    return 1 / 0  # This will generate an excuse!
```

## 🎮 CLI Usage

### Basic Commands

```bash
# Generate random excuse
cosmicexcuse

# Generate for specific error
cosmicexcuse --error "NullPointerException"

# Generate multiple excuses
cosmicexcuse --count 5

# Generate in different language
cosmicexcuse --language bn
```

### Advanced Options

```bash
# Generate haiku format
cosmicexcuse --haiku

# Specify category
cosmicexcuse --category quantum

# Show quality scores
cosmicexcuse --show-score

# Set minimum quality
cosmicexcuse --min-score 80

# Output as JSON
cosmicexcuse --json
```

### Examples

```bash
# Generate high-quality quantum excuse
cosmicexcuse --category quantum --min-score 90

# Generate Bengali haiku
cosmicexcuse --language bn --haiku

# Generate 3 excuses with scores in JSON
cosmicexcuse --count 3 --show-score --json
```

## 📊 API Reference

### CosmicExcuse Class

```python
class CosmicExcuse:
    def __init__(self, language: str = 'en', data_path: Optional[Path] = None)

        def generate(self, error_message: str = '', context: str = None,
                     category: str = None) -> Excuse

        def generate_batch(self, count: int = 5) -> List[Excuse]

        def generate_haiku(self, error_message: str = '') -> str

        def get_best_excuse(self) -> Optional[Excuse]

        def clear_history(self) -> None

        def export_history(self, format: str = 'json') -> Union[str, List[Dict]]
```

### Excuse Object

```python
@dataclass
class Excuse:
    text: str  # The generated excuse text
    recommendation: str  # Suggested fix
    severity: str  # 'mild', 'medium', or 'severe'
    category: str  # Category used
    quality_score: int  # 0-100 quality rating
    quantum_probability: float  # Random quantum factor
    language: str  # Language code
    timestamp: float  # Generation time
    metadata: Dict[str, Any]  # Additional data
```

### SeverityAnalyzer

```python
class SeverityAnalyzer:
    def analyze(self, error_message: str) -> str

        def get_severity_details(self, error_message: str) -> Dict[str, Any]
```

## ⚙️ Configuration

### Custom Data Path

```python
from pathlib import Path
from cosmicexcuse import CosmicExcuse

# Use custom excuse data
custom_path = Path("./my_excuses")
generator = CosmicExcuse(data_path=custom_path)
```

### Adding New Languages

1. Create directory: `cosmicexcuse/data/{language_code}/`
2. Add JSON files for each category
3. Update `SUPPORTED_LANGUAGES` in `generator.py`

### Extending Categories

Create a new JSON file in the appropriate language directory:

```json
{
  "category": "custom",
  "language": "en",
  "version": "1.0.0",
  "excuses": [
    "Your custom excuse here",
    "Another creative excuse"
  ]
}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cosmicexcuse --cov-report=html

# Run specific test
pytest tests/test_generator.py -v

# Type checking
mypy cosmicexcuse

# Linting
flake8 cosmicexcuse tests
black cosmicexcuse tests --check
```

## 📈 Performance

- **Generation Speed**: < 1ms per excuse
- **Memory Usage**: < 10MB
- **Startup Time**: < 100ms
- **Zero Dependencies**: No external packages required

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Start for Contributors

```bash
# Fork and clone the repo
git clone https://github.com/YOUR_USERNAME/cosmicexcuse.git

# Install in development mode
pip install -e .[dev]

# Create a branch
git checkout -b feature/amazing-feature

# Make changes and test
pytest
black cosmicexcuse tests
flake8 cosmicexcuse tests

# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature
```

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- The cosmic rays that flipped the bits to create this project
- The quantum entanglement that brought you to this README
- All developers who've ever needed a good excuse

## ⚠️ Disclaimer

This tool is for entertainment purposes only. Please do not use these excuses in:

- Production incident reports
- Performance reviews
- Court testimony
- NASA mission control

## 📊 Project Statistics

- 200+ unique quantum excuses
- 150+ cosmic event scenarios
- 100+ AI sentience situations
- 2 supported languages
- ∞ possible combinations

## 🔗 Links

- [PyPI Package](https://pypi.org/project/cosmicexcuse/)
- [Documentation](https://cosmicexcuse.readthedocs.io/)
- [GitHub Repository](https://github.com/shamspias/cosmicexcuse)
- [Issue Tracker](https://github.com/shamspias/cosmicexcuse/issues)

---

<div align="center">

**Built with 💙 and quantum uncertainty by [Shamsuddin Ahmed](https://github.com/shamspias)**

*Remember: With great code comes great need for excuses.*

⭐ Star us on GitHub if this saved your standup meeting!

</div>