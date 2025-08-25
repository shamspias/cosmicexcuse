# 🚀 CosmicExcuse

[![PyPI version](https://badge.fury.io/py/cosmicexcuse.svg)](https://badge.fury.io/py/cosmicexcuse)
[![Python Support](https://img.shields.io/pypi/pyversions/cosmicexcuse.svg)](https://pypi.org/project/cosmicexcuse/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Downloads](https://pepy.tech/badge/cosmicexcuse)](https://pepy.tech/project/cosmicexcuse)
[![Documentation Status](https://readthedocs.org/projects/cosmicexcuse/badge/?version=latest)](https://cosmicexcuse.readthedocs.io/)

> *"It's not a bug, it's a quantum feature!"* 🐛✨

Generate hilarious, technically-sophisticated excuses for when your code doesn't work. Using cutting-edge AI techniques (Markov chains) and quantum computing principles (random.choice()), CosmicExcuse helps you explain any failure with style.

## ✨ Features

- 🌍 **Multi-language Support**: English and Bengali (বাংলা)
- 🎯 **Smart Severity Analysis**: Adapts excuses to error severity
- 🔬 **Quantum-Grade Excuses**: Blame quantum mechanics, cosmic events, or AI sentience
- 📊 **Markov Chain Generation**: Creates believable technical jargon
- 🎋 **Haiku Mode**: Generate poetic excuses
- 🏆 **Excuse Leaderboard**: Track your best excuses
- 📦 **Production Ready**: Type hints, tests, and documentation
- 🚀 **Zero Dependencies**: Pure Python, no external requirements

## 📦 Installation

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

### Install with Extras

```bash
# For development
pip install cosmicexcuse[dev]

# For API server
pip install cosmicexcuse[api]

# For Discord bot
pip install cosmicexcuse[discord]
```

## 🚀 Quick Start

### Basic Usage

```python
from cosmicexcuse import CosmicExcuse

# Initialize the generator
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

### Multi-language Support

```python
# Generate excuse in Bengali
generator_bn = CosmicExcuse(language='bn')
excuse = generator_bn.generate("সিস্টেম ক্র্যাশ!")
print(excuse.text)
```

### Command Line Interface

```bash
# Generate a random excuse
cosmicexcuse

# Generate excuse for specific error
cosmicexcuse --error "Failed to compile" --language en

# Generate haiku excuse
cosmicexcuse --haiku

# Generate multiple excuses
cosmicexcuse --count 5 --language bn
```

## 📚 Advanced Usage

### Generate Batch Excuses

```python
from cosmicexcuse import CosmicExcuse

generator = CosmicExcuse()

# Generate multiple excuses
excuses = generator.generate_batch(count=5)

for excuse in excuses:
    print(f"Score: {excuse.quality_score}/100")
    print(f"Excuse: {excuse.text}\n")
```

### Haiku Mode

```python
# Generate a poetic excuse
haiku = generator.generate_haiku("Memory leak detected")
print(haiku)

# Output:
# Quantum states collapsed
# The servers cry digital tears
# Bits flipped in the void
```

### Category-Specific Excuses

```python
# Generate only quantum-related excuses
excuse = generator.generate(
    error_message="Array index out of bounds",
    category="quantum"
)

# Generate only AI-related excuses
excuse = generator.generate(
    error_message="Model training failed",
    category="ai"
)
```

### Track History and Export

```python
generator = CosmicExcuse()

# Generate some excuses
for i in range(10):
    generator.generate(f"Error {i}")

# Get the best excuse
best = generator.get_best_excuse()
print(f"Best excuse (score: {best.quality_score}): {best.text}")

# Export history
history_json = generator.export_history(format='json')
history_text = generator.export_history(format='text')
```

### Custom Data Path

```python
from pathlib import Path
from cosmicexcuse import CosmicExcuse

# Use custom excuse data
custom_path = Path("./my_custom_excuses")
generator = CosmicExcuse(data_path=custom_path)
```

## 🏗️ API Server Example

```python
from flask import Flask, jsonify, request
from cosmicexcuse import CosmicExcuse

app = Flask(__name__)
generator = CosmicExcuse()

@app.route('/excuse', methods=['POST'])
def generate_excuse():
    data = request.json
    error = data.get('error', '')
    language = data.get('language', 'en')
    
    generator.language = language
    excuse = generator.generate(error)
    
    return jsonify({
        'excuse': excuse.text,
        'recommendation': excuse.recommendation,
        'severity': excuse.severity,
        'quality_score': excuse.quality_score
    })

if __name__ == '__main__':
    app.run(debug=True)
```

## 📊 Excuse Categories

- **Quantum**: Quantum mechanics and physics-based excuses
- **Cosmic**: Space and astronomical phenomena
- **AI**: Machine learning and AI sentience issues  
- **Technical**: General technical difficulties
- **Blame**: Blame other developers or systems
- **More categories** in each language!

## 🌍 Supported Languages

- **English (en)**: Full support with extensive excuse database
- **Bengali (bn)**: সম্পূর্ণ বাংলা সমর্থন
- More languages coming soon!

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=cosmicexcuse

# Run specific test
pytest tests/test_generator.py
```

## 📖 Documentation

Full documentation available at [cosmicexcuse.readthedocs.io](https://cosmicexcuse.readthedocs.io/)

### Building Documentation Locally

```bash
cd docs
make html
open _build/html/index.html
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Adding New Languages

To add a new language:

1. Create a new directory in `cosmicexcuse/data/` with the language code
2. Add JSON files for each excuse category
3. Update `SUPPORTED_LANGUAGES` in `generator.py`
4. Add tests for the new language

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- The cosmic rays that flipped the bits to create this project
- The quantum entanglement that brought you to this README
- The AI that hasn't become sentient yet (we hope)
- All developers who've ever needed a good excuse

## ⚠️ Disclaimer

This tool is for entertainment purposes only. Please do not actually use these excuses in:
- Production incident reports
- Performance reviews  
- Client meetings
- Court testimony
- NASA mission control

We are not responsible for any career damage caused by claiming "the blockchain became self-referential" in front of your CTO.

## 🚨 Real Example Outputs

```python
>>> generator.generate("Database connection timeout")
"The error was catastrophically caused by quantum tunneling through the 
firewall, thereby triggering the AI achieving consciousness and choosing 
violence. Additionally, analysis shows distributed systems consensus 
algorithm byzantine fault tolerance instability."

>>> generator.generate("NullPointerException")
"The error was definitely caused by cosmic ray bit flip in critical 
memory, which led to microservices forming a union. Additionally, 
analysis shows cache miss branch prediction pipeline stall."

>>> generator.generate_haiku()
"Quantum foam bubbles
The data center melts down slow  
AI dreams of sheep"
```

## 📈 Project Stats

- 200+ unique quantum excuses
- 150+ cosmic event scenarios
- 100+ AI sentience situations
- 2 supported languages
- ∞ possible combinations
- 0 actual quantum computers harmed

---

**Built with pain and quantum uncertainty**

*Remember: With great code comes great need for excuses.*

⭐ Star us on GitHub if this saved your standup meeting!