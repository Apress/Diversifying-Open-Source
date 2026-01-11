# Diversity Standard CLI

A command-line tool for inspecting and generating diversity and inclusion documentation for open source projects.

## Installation

### Prerequisites

It's recommended to use a virtual environment to isolate dependencies:

**Create a virtual environment:**

```bash
cd cli
python3 -m venv venv
```

**Activate the virtual environment:**

On macOS/Linux:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

**Deactivate the virtual environment** (when done):
```bash
deactivate
```

### From Source

```bash
cd cli
pip install -e .
```

### Development Installation

```bash
cd cli
pip install -e ".[dev]"
```

## Usage

### Inspect a Project

Check what diversity documentation already exists in your project:

```bash
diversity-standard inspect [path]
```

Example:
```bash
diversity-standard inspect /path/to/my-project
```

### Generate Missing Documents

Generate missing documentation from templates:

```bash
diversity-standard generate [path] [options]
```

Options:
- `--dry-run` - Show what would be generated without creating files
- `--backup` - Backup existing files before overwriting
- `--force` - Overwrite existing files
- `--interactive` - Use interactive mode for missing configuration values
- `--config FILE` - Specify configuration file path

Example:
```bash
diversity-standard generate . --interactive
```

### Initialize Configuration

Create a configuration file with interactive prompts:

```bash
diversity-standard init [path]
```

This creates a `.diversity-standard.yml` file in your project root with project-specific information.

### Quick Check

Check if a project is compliant (useful for CI/CD):

```bash
diversity-standard check [path]
```

Exit code 0 if compliant, 1 if documents are missing.

## Configuration

The CLI uses a `.diversity-standard.yml` file in your project root for configuration. Example:

```yaml
project:
  name: "My Project"
  description: "A great open source project"
  repository: "https://github.com/org/my-project"

maintainers:
  - name: "Jane Doe"
    email: "jane@example.com"
    role: "Lead Maintainer"

license:
  type: "MIT"
  rationale: "Permissive license for maximum adoption"

contact:
  support_email: "support@example.com"
  security_email: "security@example.com"

governance:
  model: "consensus-seeking"

funding:
  sources: []
  transparency: true
```

## How It Works

1. **Inspection**: The tool searches your project for existing documentation by:
   - Filename matching (case-insensitive)
   - Content analysis (looking for key phrases)
   - Common locations (root, docs/, .github/, etc.)

2. **Mapping**: Found documents are mapped to blueprint categories:
   - **Daily**: Operational documents (CONTRIBUTING.md, SUPPORT.md, etc.)
   - **Procedural**: Process documents (SECURITY.md, ACCESSIBILITY.md, etc.)
   - **Long-Term**: Governance documents (GOVERNANCE.md, CODE_OF_CONDUCT.md, etc.)

3. **Generation**: Missing documents are generated from templates with:
   - Project-specific information filled in
   - Placeholders replaced with values from config
   - Files created in appropriate locations

## Document Discovery

The tool finds documents regardless of their location. For example:
- `docs/CONTRIBUTING.md` → Maps to Daily/CONTRIBUTING.md
- `CODE_OF_CONDUCT.md` in root → Maps to Long-Term/CODE_OF_CONDUCT.md
- `documentation/security.md` → Maps to Procedural/SECURITY.md

## Output Structure

By default, the tool will:
- Use existing blueprint structure if Daily/, Procedural/, Long-Term/ directories exist
- Otherwise, create documents in `docs/` with subdirectories
- Or place in project root if no docs/ directory exists

You can customize this behavior via configuration.

## Development

### Running Tests

```bash
cd cli
pytest tests/
```

### Project Structure

```
cli/
├── diversity_standard/
│   ├── cli.py              # Main CLI entry point
│   ├── inspector.py         # Document inspection logic
│   ├── generator.py         # Template generation
│   ├── config.py            # Configuration management
│   ├── utils.py             # Utility functions
│   └── document_mapping.yml # Document mapping rules
└── tests/
    └── test_cli.py
```

## License

GPL-3.0 (same as the main repository)

