# Atlas Research Notebooks

A collection of open source sample codes and research notebooks created using the [atlas-research.io](https://atlas-research.io) platform.

## About Atlas Research

Atlas Research enables researchers, developers, and analysts to:

- **Prototype Code**: Rapidly develop and test ideas in interactive environments
- **Data Wrangling**: Clean, transform, and analyze complex datasets
- **Trading Strategies**: Prototype and backtest financial trading algorithms
- **Academic Research**: Reproduce code from academic papers and research publications
- **Collaborative Research**: Share and collaborate on research projects

## Repository Structure

```
atlas-research-notebooks/
├── crypto/                 # Cryptocurrency analysis and trading strategies
│   ├── 001_crypto_correlation.py
│   ├── 002_implied_volatility_surface_analysis.py
│   └── 003_volume_profile_market_regime.py
├── economics/              # Economics Research
├── machine-learning/       # ML models and experiments
├── CONTRIBUTING.md         # Contribution guidelines
├── LICENSE                 # MIT License
└── README.md
```

### Prerequisites
- Python 3.11+
- Jupyter Notebook or JupyterLab
- Required packages (installed per notebook as needed)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-org/atlas-research-notebooks.git
cd atlas-research-notebooks
```

3. Open any notebook and run the cells - dependencies will be installed automatically via pip install cells.

## Working with Notebooks

This repository uses [Jupytext](https://jupytext.readthedocs.io/) to manage notebooks as Python scripts (`.py` files) instead of `.ipynb` files. This approach provides better version control and easier code review.

### Exporting from Atlas Research

**Recommended:** Create and edit notebooks in [atlas-research.io](https://atlas-research.io), then use the **Jupytext export button** in the top toolbar to export as `.py` files.

### Converting Locally (Alternative)

For local development, you can convert between formats:

```bash
# Install jupytext (or use requirements.txt)
pip install jupytext

# Convert a single .py file to .ipynb
jupytext --to notebook crypto/001_crypto_correlation.py

# Convert all .py files to .ipynb
jupytext --to notebook **/*.py

# Sync changes from .ipynb back to .py
jupytext --sync crypto/001_crypto_correlation.ipynb
```

**Note:** The repository only tracks `.py` files. Generated `.ipynb` files are ignored by git and can be created locally as needed.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to:
- Submit new research notebooks
- Improve existing examples  
- Report issues and suggest enhancements
- Follow coding standards and best practices


## Platform Features Showcased

These notebooks demonstrate key capabilities of the atlas-research.io platform:

- **Interactive Development**: Jupyter-based research environment
- **Data Integration**: Seamless connection to external APIs and data sources
- **Visualization**: Rich plotting and charting capabilities
- **Reproducibility**: Self-contained notebooks with dependency management
- **Collaboration**: Shareable research workflows

## Acknowledgments

- Built with the Atlas Research platform
- Powered by open source libraries including Jupyter, pandas, matplotlib, and many others


---

*Start your research journey at [atlas-research.io](https://atlas-research.io)*