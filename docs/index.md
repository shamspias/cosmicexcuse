# CosmicExcuse Documentation

Welcome to the official documentation for CosmicExcuse - your quantum-grade excuse generator for code failures!

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [API Reference](#api-reference)
5. [CLI Reference](#cli-reference)
6. [Advanced Usage](#advanced-usage)
7. [Architecture](#architecture)
8. [Contributing](#contributing)
9. [FAQ](#faq)

## Introduction

CosmicExcuse is a Python package that generates creative, technically-sophisticated excuses for when your code doesn't
work. Using Markov chains for technical jargon generation and a sophisticated severity analyzer, it creates believable (
and hilarious) explanations for any error.

### Why CosmicExcuse?

- **Zero Dependencies**: Pure Python implementation
- **Multi-language Support**: English and Bengali built-in
- **Smart Analysis**: Automatically adapts to error severity
- **Multiple Formats**: Plain text, Markdown, JSON, and even Haiku!
- **Quality Scoring**: Track the best excuses with our scoring system
- **Extensible**: Easy to add new languages and categories

## Installation

### Requirements

- Python 3.9 or higher
- No external dependencies for core functionality

### Install from PyPI

```bash
pip install cosmicexcuse
```

### Install from Source

```bash
git clone https://github.com/shamspias/cosmicexcuse.git
cd cosmicexcuse
pip install -e .
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/shamspias/cosmicexcuse.git
cd cosmicexcuse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with extras
pip install -e .[dev]
```

### Verify Installation

```bash
# CLI verification
cosmicexcuse --version

# Python verification
python -c "from cosmicexcuse import CosmicExcuse; print('Success!')"
```

## Quick Start

### Basic Usage

```python
from cosmicexcuse import CosmicExcuse

# Initialize generator
generator = CosmicExcuse()

# Generate an excuse
excuse = generator.generate("Database connection failed")
print(excuse.text)
```

### One-Liner

```python
import cosmicexcuse

print(cosmicexcuse.generate("Segmentation fault"))
```

### CLI Usage

```bash
# Generate random excuse
cosmicexcuse

# Generate for specific error
cosmicexcuse --error "NullPointerException"

# Generate haiku
cosmicexcuse --haiku
```

## API Reference

### CosmicExcuse Class

The main class for generating excuses.

#### Constructor

```python
CosmicExcuse(language: str = 'en', data_path: Optional[Path] = None)
```

**Parameters:**

- `language` (str): Language code ('en' for English, 'bn' for Bengali)
- `data_path` (Optional[Path]): Custom path to data directory

**Example:**

```python
# Default English
generator = CosmicExcuse()

# Bengali
generator_bn = CosmicExcuse(language='bn')

# Custom data path
from pathlib import Path

generator = CosmicExcuse(data_path=Path('./my_data'))
```

#### Methods

##### generate()

Generate a single excuse.

```python
generate(
    error_message: str = '',
context: Optional[str] = None,
category: Optional[str] = None,
save_history: bool = True
) -> Excuse
```

**Parameters:**

- `error_message` (str): The error message to analyze
- `context` (Optional[str]): Additional context about the error
- `category` (Optional[str]): Specific category ('quantum', 'cosmic', 'ai', 'technical', 'blame')
- `save_history` (bool): Whether to save to history

**Returns:**

- `Excuse` object containing the generated excuse and metadata

**Example:**

```python
# Simple generation
excuse = generator.generate()

# With error message
excuse = generator.generate("FATAL: Database crashed")

# With specific category
excuse = generator.generate(category='quantum')

# With context
excuse = generator.generate(
    error_message="Connection timeout",
    context="During peak hours",
    category='cosmic'
)
```

##### generate_batch()

Generate multiple excuses.

```python
generate_batch(count: int = 5) -> List[Excuse]
```

**Parameters:**

- `count` (int): Number of excuses to generate

**Returns:**

- List of `Excuse` objects

**Example:**

```python
excuses = generator.generate_batch(10)
for excuse in excuses:
    print(f"Score {excuse.quality_score}: {excuse.text}")
```

##### generate_haiku()

Generate an excuse in haiku format.

```python
generate_haiku(error_message: str = '') -> str
```

**Parameters:**

- `error_message` (str): Optional error message for context

**Returns:**

- String containing haiku (5-7-5 syllables)

**Example:**

```python
haiku = generator.generate_haiku("Memory leak")
print(haiku)
# Output:
# Bits flow like water
# Memory pools overflow now
# Quantum states collapse
```

##### get_best_excuse()

Get the highest quality excuse from history.

```python
get_best_excuse() -> Optional[Excuse]
```

**Returns:**

- `Excuse` object with highest quality score, or None if history is empty

**Example:**

```python
# Generate some excuses
for i in range(10):
    generator.generate(f"Error {i}")

# Get the best one
best = generator.get_best_excuse()
print(f"Best excuse (score {best.quality_score}): {best.text}")
```

##### clear_history()

Clear the excuse history.

```python
clear_history() -> None
```

##### export_history()

Export history in specified format.

```python
export_history(format: str = 'json') -> Union[str, List[Dict]]
```

**Parameters:**

- `format` (str): Export format ('json' or 'text')

**Returns:**

- Formatted history data

### Excuse Object

The `Excuse` dataclass contains all information about a generated excuse.

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
    metadata: Dict[str, Any]  # Additional metadata
```

**Example:**

```python
excuse = generator.generate("Database error")

print(f"Text: {excuse.text}")
print(f"Fix: {excuse.recommendation}")
print(f"Severity: {excuse.severity}")
print(f"Score: {excuse.quality_score}/100")
print(f"Category: {excuse.category}")
print(f"Quantum Probability: {excuse.quantum_probability:.4f}")
```

### SeverityAnalyzer

Analyzes error messages to determine severity.

```python
from cosmicexcuse.analyzer import SeverityAnalyzer

analyzer = SeverityAnalyzer()
severity = analyzer.analyze("FATAL ERROR: System crash!")
# Returns: 'severe'

details = analyzer.get_severity_details("Warning: deprecated function")
# Returns detailed analysis dictionary
```

### Formatters

Various formatters for different output formats.

```python
from cosmicexcuse.formatter import (
    ExcuseFormatter,
    MarkdownFormatter,
    JSONFormatter,
    TwitterFormatter,
    HaikuFormatter
)

# Markdown format
md_formatter = MarkdownFormatter()
markdown = md_formatter.format(excuse.__dict__)

# Twitter format (280 chars)
twitter_formatter = TwitterFormatter()
tweet = twitter_formatter.format({'text': excuse.text})

# JSON format
json_formatter = JSONFormatter()
json_output = json_formatter.format(excuse.__dict__)
```

## CLI Reference

### Basic Commands

```bash
cosmicexcuse [OPTIONS]
```

### Options

| Option         | Short | Description                          | Default |
|----------------|-------|--------------------------------------|---------|
| `--error`      | `-e`  | Error message to generate excuse for | ""      |
| `--language`   | `-l`  | Language code (en/bn)                | en      |
| `--count`      | `-c`  | Number of excuses to generate        | 1       |
| `--category`   |       | Specific category                    | None    |
| `--haiku`      |       | Generate haiku format                | False   |
| `--json`       |       | Output in JSON format                | False   |
| `--no-banner`  |       | Skip banner display                  | False   |
| `--show-score` |       | Show quality scores                  | False   |
| `--min-score`  |       | Minimum quality score                | 0       |
| `--version`    | `-v`  | Show version                         |         |
| `--help`       | `-h`  | Show help                            |         |

### Examples

```bash
# Generate random excuse
cosmicexcuse

# Generate for specific error
cosmicexcuse -e "Segmentation fault"

# Generate 5 quantum excuses
cosmicexcuse --category quantum -c 5

# Generate high-quality excuse
cosmicexcuse --min-score 90

# Generate Bengali haiku
cosmicexcuse -l bn --haiku

# Export as JSON
cosmicexcuse --json > excuse.json

# Show scores and details
cosmicexcuse --show-score -c 3
```

## Advanced Usage

### Custom Error Handler

```python
from cosmicexcuse import CosmicExcuse
import sys

generator = CosmicExcuse()


def cosmic_exception_handler(exc_type, exc_value, exc_traceback):
    """Custom exception handler with cosmic excuses."""
    if exc_type is KeyboardInterrupt:
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    excuse = generator.generate(str(exc_value))
    print("\n" + "=" * 60)
    print("💥 ERROR DETECTED!")
    print("=" * 60)
    print(f"Actual error: {exc_type.__name__}: {exc_value}")
    print(f"\n🎭 Official explanation: {excuse.text}")
    print(f"\n💡 Recommended fix: {excuse.recommendation}")
    print("=" * 60)


# Install the handler
sys.excepthook = cosmic_exception_handler

# Now any uncaught exception will generate an excuse!
raise ValueError("This will generate an excuse")
```

### Flask Integration

```python
from flask import Flask, jsonify
from cosmicexcuse import CosmicExcuse

app = Flask(__name__)
generator = CosmicExcuse()


@app.errorhandler(Exception)
def handle_error(error):
    excuse = generator.generate(str(error))
    return jsonify({
        'error': str(error),
        'excuse': excuse.text,
        'recommendation': excuse.recommendation,
        'severity': excuse.severity,
        'quantum_probability': excuse.quantum_probability
    }), 500


@app.route('/crash')
def crash():
    raise ValueError("Intentional crash for testing")


if __name__ == '__main__':
    app.run(debug=True)
```

### Logging Integration

```python
import logging
from cosmicexcuse import CosmicExcuse


class CosmicExcuseHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.generator = CosmicExcuse()

    def emit(self, record):
        if record.levelno >= logging.ERROR:
            excuse = self.generator.generate(record.getMessage())
            record.msg = f"{record.msg}\nExcuse: {excuse.text}"
        super().emit(record)


# Setup logging with cosmic excuses
logger = logging.getLogger(__name__)
logger.addHandler(CosmicExcuseHandler())
logger.setLevel(logging.DEBUG)

# Now errors will include excuses!
logger.error("Database connection failed")
```

### Pytest Integration

```python
# conftest.py
import pytest
from cosmicexcuse import CosmicExcuse


@pytest.fixture
def cosmic_excuse():
    generator = CosmicExcuse()

    def _make_excuse(error):
        excuse = generator.generate(error)
        return f"\nTest failed!\nExcuse: {excuse.text}\nFix: {excuse.recommendation}"

    return _make_excuse


# test_example.py
def test_something(cosmic_excuse):
    try:
        assert 1 == 2
    except AssertionError as e:
        print(cosmic_excuse(str(e)))
        raise
```

### Custom Categories

Create custom excuse categories by adding JSON files:

```python
# custom_excuses.json
{
    "category": "network",
    "language": "en",
    "version": "1.0.0",
    "excuses": [
        "the packets got lost in the void",
        "TCP handshake became a high-five",
        "router achieved enlightenment and refuses to route",
        "bandwidth was stolen by interdimensional beings"
    ]
}

# Use custom data
from pathlib import Path

generator = CosmicExcuse(data_path=Path('./custom_data'))
```

### Leaderboard System

```python
from cosmicexcuse.leaderboard import ExcuseLeaderboard

leaderboard = ExcuseLeaderboard(max_size=100)

# Add excuses
for i in range(20):
    excuse = generator.generate(f"Error {i}")
    leaderboard.add_from_excuse_object(excuse)

# Vote on excuses
leaderboard.vote(excuse.text, upvote=True)

# Get rankings
top_quality = leaderboard.get_top_by_quality(5)
top_voted = leaderboard.get_top_by_votes(5)
controversial = leaderboard.get_most_controversial(5)

# Get statistics
stats = leaderboard.get_stats()
print(f"Total: {stats['total_excuses']}")
print(f"Average Quality: {stats['average_quality']:.1f}")

# Export leaderboard
markdown_report = leaderboard.export(format='markdown')
csv_data = leaderboard.export(format='csv')
```

## Architecture

### Component Overview

```
CosmicExcuse/
├── Generator (Main Engine)
│   ├── ExcuseGenerator (Base)
│   └── CosmicExcuse (Extended)
├── Analyzer (Severity Analysis)
│   └── SeverityAnalyzer
├── Markov (Text Generation)
│   └── MarkovChain
├── Formatter (Output Formatting)
│   ├── ExcuseFormatter
│   ├── MarkdownFormatter
│   ├── JSONFormatter
│   ├── TwitterFormatter
│   └── HaikuFormatter
├── Leaderboard (Ranking System)
│   └── ExcuseLeaderboard
└── Data (Excuse Database)
    ├── en/ (English)
    └── bn/ (Bengali)
```

### Data Flow

1. **Input**: Error message received
2. **Analysis**: SeverityAnalyzer determines severity level
3. **Selection**: Categories and excuses selected based on severity
4. **Generation**: MarkovChain generates technical jargon
5. **Formatting**: ExcuseFormatter combines components
6. **Scoring**: Quality score calculated
7. **Output**: Excuse object returned

### Adding New Languages

1. Create language directory:

```bash
mkdir cosmicexcuse/data/es  # Spanish
```

2. Add category files:

```bash
# Create JSON files for each category
quantum.json, cosmic.json, ai.json, etc.
```

3. Update supported languages:

```python
# In generator.py
SUPPORTED_LANGUAGES = ['en', 'bn', 'es']  # Add 'es'
```

## FAQ

### Q: How does the quality scoring work?

The quality score (0-100) is calculated based on:

- Length of the excuse
- Presence of technical keywords
- Category bonus points
- Quantum seed randomization

### Q: Can I use this in production?

While technically possible, we recommend against using cosmic excuses in:

- Production error logs
- Client communications
- Legal documents
- NASA mission control

### Q: How do I add custom excuses?

Create JSON files in the data directory following the schema:

```json
{
  "category": "your_category",
  "language": "en",
  "version": "1.0.0",
  "excuses": [
    "excuse 1",
    "excuse 2"
  ]
}
```

### Q: Is this package maintained?

Yes! We regularly update with new excuses and features. Check our [GitHub](https://github.com/shamspias/cosmicexcuse)for
the latest updates.

### Q: Can I contribute?

Absolutely! We welcome contributions. See our [Contributing Guide](CONTRIBUTING.md).

## Support

- **Issues**: [GitHub Issues](https://github.com/shamspias/cosmicexcuse/issues)
- **Discussions**: [GitHub Discussions](https://github.com/shamspias/cosmicexcuse/discussions)
- **Email**: info@shamspias.com

---

Remember: *It's not a bug, it's a quantum feature!* 🐛✨