# Examples

## Basic Usage

```python
from cosmicexcuse import CosmicExcuse

# Create generator
generator = CosmicExcuse()

# Generate excuse
excuse = generator.generate("Database connection failed")
print(excuse.text)
```

## Advanced Examples

### Custom Error Handler

```python
import sys
from cosmicexcuse import CosmicExcuse

generator = CosmicExcuse()

def cosmic_exception_handler(exc_type, exc_value, exc_traceback):
    if exc_type is KeyboardInterrupt:
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    excuse = generator.generate(str(exc_value))
    print(f"Error: {exc_value}")
    print(f"Excuse: {excuse.text}")
    print(f"Fix: {excuse.recommendation}")

sys.excepthook = cosmic_exception_handler
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
        'recommendation': excuse.recommendation
    }), 500
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
```
