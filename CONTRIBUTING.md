# Contributing to Atlas Research Notebooks

This collection showcases the capabilities of the [atlas-research.io](https://atlas-research.io) platform through practical examples and research implementations.

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

1. **New Research Notebooks**: Original analysis, tutorials, or academic paper reproductions
2. **Improvements to Existing Code**: Bug fixes, optimizations, or enhanced documentation
3. **New Research Areas**: Adding examples in new domains (crypto, economics, geography, geopolitics, machine learning, backtesting, political data, and more)
4. **Documentation**: Improving README files, adding comments, or creating tutorials
5. **Platform Feature Demonstrations**: Showcasing specific atlas-research.io capabilities

### Getting Started

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/<your-username>/atlas-research-notebooks.git
   cd atlas-research-notebooks
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-contribution-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

4. **Set up API keys (if needed)**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Install pre-commit hooks (recommended)**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Working with Jupytext

This repository uses **Jupytext** to version control notebooks as Python script files (`.py`) with special formatting. This provides cleaner diffs and easier code review.

#### Why Jupytext?
- Better version control (`.py` files vs binary `.ipynb` files)
- Cleaner git diffs showing actual code changes
- Easier code review in pull requests
- No merge conflicts from notebook metadata

#### Exporting from Atlas Research Platform (Recommended)

**Primary Workflow:**

1. **Create or edit your notebook** in the [atlas-research.io](https://atlas-research.io) platform
2. **Click the Jupytext export button** in the top toolbar of the notebook editor
3. **Save the exported `.py` file** to the appropriate directory in this repository
4. **Commit only the `.py` file** to git

This is the recommended workflow as it ensures consistent formatting and leverages the platform's built-in export functionality.

#### Alternative: Local Conversion (Command-Line)

**For contributors working locally:**

1. **Converting .py to .ipynb for editing:**
   ```bash
   # Convert a single file
   jupytext --to notebook crypto/001_crypto_correlation.py

   # This creates crypto/001_crypto_correlation.ipynb locally
   ```

2. **Syncing changes back to .py:**
   ```bash
   # After editing the .ipynb file, sync back to .py
   jupytext --sync crypto/001_crypto_correlation.ipynb

   # Only commit the .py file, not the .ipynb
   ```

3. **Creating a new notebook:**
   ```bash
   # Create your notebook in Jupyter as usual (.ipynb)
   # Then convert it to .py format for version control
   jupytext --to py:percent your_notebook.ipynb

   # Commit only the .py file
   ```

#### Format Details
- All notebooks use the **percent format** (`# %%` cell markers)
- Markdown cells start with `# %% [markdown]`
- Code cells start with `# %%`
- The format is compatible with VS Code, PyCharm, and Spyder

#### Important Notes
- **Never commit `.ipynb` files** - they are gitignored
- Always commit the `.py` version of your notebook
- The `.ipynb` files are temporary and for local development only
- When using command-line tools, run `jupytext --sync` before committing to ensure `.py` is up-to-date

#### VS Code Integration
If you use VS Code, you can open `.py` files directly and they will render as notebooks with the Jupyter extension. The `# %%` markers create interactive cells without needing to convert to `.ipynb`.

## Contribution Guidelines

### Notebook Standards

#### Naming Convention
- Use descriptive, numbered names: `NNN_descriptive_name.py`
- Create as Jupytext Python script: `NNN_descriptive_name.py` (percent format)
- Place in appropriate domain folder: `crypto/`, `economics/`, `geography/`, `machine-learning/`, `programming/`
- See `_templates/notebook_template.py` for a starter template

#### Visual Style
All notebooks in this repository use **dark theme** styling. This is a repository standard:
```python
plt.style.use('dark_background')
# For custom backgrounds, use dark colors like:
# fig.patch.set_facecolor('#1E1E1E')
```

#### Notebook Structure
Each notebook should include:

1. **Title Cell** (Markdown)
   - Clear title describing the analysis
   - Brief description of the research objective

2. **Dependencies Cell** (Code)
   ```python
   !pip install package1 package2 package3
   ```

3. **Imports and Setup** (Code)
   ```python
   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   plt.style.use('dark_background')
   ```

4. **Main Analysis** (Mixed Cells)
   - Well-documented code with markdown explanations
   - Clear variable names and function definitions
   - Intermediate results and visualizations

5. **Results and Conclusions** (Markdown)
   - Summary of findings
   - Potential improvements or next steps

#### Code Quality Standards

- **Comments**: Include clear, concise comments explaining complex logic
- **Documentation**: Use docstrings for custom functions
- **Error Handling**: Include appropriate try/catch blocks for external API calls
- **Reproducibility**: Ensure notebooks can be run from top to bottom without errors
- **Performance**: Include timing information for long-running operations

#### Data and APIs

- **External Data**: Prefer public APIs and datasets when possible
- **API Keys**: Never hardcode API keys or secrets -- use `os.environ.get()` (see `.env.example`)
- **Data Size**: Keep example datasets reasonably sized for quick execution

### Submission Process

1. **Test Your Contribution**
   - Run notebooks from start to finish
   - Verify all visualizations render correctly
   - Check that external dependencies install properly

2. **Update Documentation**
   - Include brief description of the analysis
   - Update any relevant table of contents

3. **Create a Pull Request**
   - Use a descriptive title
   - Fill out the PR template
   - Reference any related issues

## Code Review Process

1. **Automated Checks**: CI validates Jupytext format and scans for hardcoded secrets
2. **Maintainer Review**: Final review by repository maintainers
3. **Testing**: Verification that notebooks execute successfully

## Community Guidelines

### Be Respectful
- Use inclusive language
- Respect different research approaches and methodologies
- Provide constructive feedback

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for full community standards.

### Academic Integrity
- Properly cite sources and academic papers
- Give credit to original authors when reproducing work
- Include appropriate licenses for any external code

### Quality Over Quantity
- Focus on well-documented, educational examples
- Prefer depth of analysis over breadth
- Ensure contributions add unique value

## License

By contributing to this repository, you agree that your contributions will be licensed under the same MIT License that covers the project.

---
