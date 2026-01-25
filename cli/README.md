# Diversity Standard CLI

A command-line tool for inspecting and generating best practices documents for your free and open source projects.

## Installation

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

The CLI has 3 commands:

### 1. Help

Get help on commands:

```bash
diversity-standard --help
diversity-standard <command> --help
```

### 2. Inspect

Check which documents already exists in your project:

```bash
diversity-standard inspect [path]
```

**Note**: `[path]` is optional and defaults to the current directory (`.`) if not specified.

This command shows:
- Found documents (with their locations)
- Missing documents
- Intentionally skipped documents (based on questionnaire answers)

**Examples:**
```bash
diversity-standard inspect .
diversity-standard inspect /path/to/my-project
```

### 3. Init

Initialize your project with diversity standards documents personalized using a wizzard:

```bash
diversity-standard init [path] [--backup] [--force]
```

The `init` command will guide you through:
1. Core project information (name, description, license, etc.)
2. Document selection (choose which documents to generate)
3. Category-specific questions (Daily, Procedural, Long-Term)
4. Document-specific questions (customize individual documents)

**Available options:**
- `--backup` - Backup existing files before overwriting
- `--force` - Overwrite existing files without backup

Answers are saved to `.diversity-standard.yml` in the project root for future use.

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

3. **Wizzard**:
   - Guides you through personalizing documents
   - Asks conditional questions (e.g., "Do you have funding?" → skips FUNDING.md if no)
   - Allows custom text input for key sections
   - Lets you choose which documents to generate

4. **Generation**: Missing documents are generated from templates with:
   - Project-specific information filled in
   - Conditional sections based on your answers
   - Custom text you provided
   - Placeholders replaced with values from config
   - Files created in appropriate locations

## Conditional Logic

The questionnaire uses conditional logic to personalize documents:

- **If you answer "No" to funding**: FUNDING.md is automatically skipped
- **If you answer "No" to meetings**: MEETINGS.md is automatically skipped
- **If you select "custom" governance**: You're asked to describe your custom model
- **If you emphasize non-code contributions**: CONTRIBUTING.md highlights this

## Output Structure

During the wizard, you'll be asked where you want documents placed. Options include:

- **Blueprint structure**: `Daily/`, `Procedural/`, `Long-Term/` directories
- **docs/ subdirectories**: `docs/daily/`, `docs/procedural/`, `docs/long-term/`
- **Project root**: All files in the root directory
- **Custom path**: Specify your own base path (e.g., `documentation` or `docs/policies`)

If you don't specify a preference, the tool auto-detects based on existing structure:
- Uses blueprint structure if `Daily/`, `Procedural/`, or `Long-Term/` directories exist
- Otherwise uses `docs/` subdirectories if `docs/` exists
- Otherwise places files in project root

Your choice is saved to `.diversity-standard.yml` and used for future document generation.

## Project Structure

```
cli/
├── diversity_standard/          # Python package
│   ├── __init__.py
│   ├── cli.py                   # Main CLI entry point
│   ├── inspector.py             # Document inspection logic
│   ├── generator.py              # Template generation
│   ├── questionnaire.py         # Interactive questionnaire system
│   ├── config.py                # Configuration management
│   ├── utils.py                 # Utility functions
│   ├── document_mapping.yml      # Document mapping rules
│   ├── questions.yml             # Questionnaire definitions
│   ├── template_examples.md     # Template syntax examples
│   └── templates/                # Copied templates (via setup_templates.py)
├── tests/
│   ├── __init__.py
│   └── test_cli.py
├── setup.py                      # Package setup
├── setup_templates.py            # Template copying script
├── pyproject.toml                # Package configuration
├── requirements.txt              # Python dependencies
├── MANIFEST.in                   # Package manifest
├── README.md                     # This file
├── INSTALL.md                    # Installation guide
└── QUESTIONNAIRE_GUIDE.md        # Questionnaire documentation
```

## License

GPL-3.0 (same as the main repository)
