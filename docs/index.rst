.. CosmicExcuse documentation master file

Welcome to CosmicExcuse's documentation!
=========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   api
   examples
   contributing

CosmicExcuse - Generate quantum-grade excuses for your code failures!
----------------------------------------------------------------------

When your code doesn't work, you need excuses that sound technical enough to be believable.
CosmicExcuse generates creative, technically-sophisticated excuses using Markov chains and
severity analysis.

Features
--------

* **Zero Dependencies** - Pure Python implementation
* **Multi-language Support** - English and Bengali built-in
* **Smart Analysis** - Automatically adapts to error severity
* **Multiple Formats** - Plain text, Markdown, JSON, and even Haiku!
* **Quality Scoring** - Track the best excuses with our scoring system
* **Extensible** - Easy to add new languages and categories

Quick Example
-------------

.. code-block:: python

    from cosmicexcuse import CosmicExcuse

    generator = CosmicExcuse()
    excuse = generator.generate("Database connection failed")
    print(excuse.text)

Installation
------------

Install from PyPI::

    pip install cosmicexcuse

Or install from source::

    git clone https://github.com/shamspias/cosmicexcuse.git
    cd cosmicexcuse
    pip install -e .

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
