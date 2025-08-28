# API Reference

## Main Classes

### CosmicExcuse

```python
from cosmicexcuse import CosmicExcuse
```

The main class for generating excuses.

#### Constructor

```python
CosmicExcuse(language: str = 'en', data_path: Optional[Path] = None)
```

#### Methods

- `generate()`: Generate a single excuse
- `generate_batch()`: Generate multiple excuses
- `generate_haiku()`: Generate excuse in haiku format
- `get_best_excuse()`: Get highest quality excuse from history
- `clear_history()`: Clear excuse history
- `export_history()`: Export history in various formats

### SeverityAnalyzer

```python
from cosmicexcuse.analyzer import SeverityAnalyzer
```

Analyzes error messages to determine severity level.

#### Methods

- `analyze(error_message: str) -> str`: Get severity level
- `get_severity_details(error_message: str) -> Dict`: Get detailed analysis

### MarkovChain

```python
from cosmicexcuse.markov import MarkovChain
```

Generates technical jargon using Markov chains.

#### Methods

- `train(corpus: List[str])`: Train on new corpus
- `generate(length: int) -> str`: Generate text
- `reset()`: Reset to default corpus

## Formatters

Various formatters for different output formats:

- `ExcuseFormatter`: Standard formatting
- `MarkdownFormatter`: Markdown output
- `JSONFormatter`: JSON output
- `TwitterFormatter`: Tweet-sized output (280 chars)
- `HaikuFormatter`: 5-7-5 syllable haiku format

## Exceptions

- `CosmicExcuseError`: Base exception
- `LanguageNotSupportedError`: Invalid language code
- `DataLoadError`: Data file loading error
- `InvalidCategoryError`: Invalid category specified
