# Installation Guide

## Quick Start

1. **Create and activate a virtual environment** (recommended):
   ```bash
   cd cli
   python3 -m venv venv
   
   # Activate on macOS/Linux:
   source venv/bin/activate
   
   # Activate on Windows:
   venv\Scripts\activate
   ```

2. **Install the CLI**:
   ```bash
   pip install -e .
   ```

3. **Setup templates** (optional, but recommended):
   ```bash
   python setup_templates.py
   ```
   This copies the blueprint files to the CLI templates directory.

4. **Test the installation**:
   ```bash
   diversity-standard --help
   ```

## Development Installation

For development with testing:

```bash
cd cli
pip install -e ".[dev]"
pytest tests/
```

## Usage Example

```bash
# Inspect a project
diversity-standard inspect /path/to/project

# Generate missing documents (interactive questionnaire)
diversity-standard generate /path/to/project

# Initialize configuration
diversity-standard init /path/to/project
```

## Notes

- The CLI will automatically find blueprint templates from the repository structure
- If templates are not found in the repository, run `setup_templates.py` to copy them
- Templates use Jinja2 syntax: `{{project_name}}`, `{{maintainer_email}}`, etc.

