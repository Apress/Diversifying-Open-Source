# Diversity Standard CLI

A command-line tool for inspecting and generating diversity and inclusion documentation for open source projects.

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

### Command Structure

All commands follow this pattern:
```bash
diversity-standard <command> [path] [options]
```

**Important**: Options like `--dry-run` are specific to each command, not global options.

### Inspect a Project

Check what diversity documentation already exists in your project:

```bash
diversity-standard inspect [path]
```

Example:
```bash
diversity-standard inspect /path/to/my-project
# or
diversity-standard inspect .
```

### Generate Missing Documents

Generate missing documentation from templates with an interactive questionnaire:

```bash
diversity-standard generate [path] [options]
```

**Note**: `[path]` is optional and defaults to the current directory (`.`) if not specified.

The `generate` command is **always interactive** and will guide you through:
1. Core project information (name, description, license, etc.)
2. Document selection (choose which documents to generate)
3. Category-specific questions (Daily, Procedural, Long-Term)
4. Document-specific questions (customize individual documents)

**Available options for `generate` command:**
- `--dry-run` - Show what would be generated without creating files
- `--backup` - Backup existing files before overwriting
- `--force` - Overwrite existing files
- `--config FILE` - Specify configuration file path

**Examples:**
```bash
# Dry run (preview without generating)
# [path] can be omitted (defaults to current directory)
diversity-standard generate --dry-run
# Or specify [path] explicitly
diversity-standard generate [path] --dry-run
diversity-standard generate . --dry-run
diversity-standard generate /path/to/project --dry-run

# Generate with full questionnaire (default behavior)
diversity-standard generate [path]
diversity-standard generate .

# Generate with backup
diversity-standard generate [path] --backup
diversity-standard generate . --backup
```

**Interactive Questionnaire:**
The questionnaire guides you through personalizing your documentation:

- **Core questions**: Project name, description, repository, license, maintainers, contact info
- **Daily questions**: Contribution types, support channels, meeting preferences, code review philosophy
- **Procedural questions**: Security policies, accessibility commitments, localization, funding, versioning
- **Long-term questions**: Governance model, code of conduct enforcement, ownership structure

Questions support conditional logic:
- **Yes/No questions**: If you answer "no" to "Do you have funding?", FUNDING.md will be skipped
- **Multiple choice**: Select governance model, and documents adapt accordingly
- **Freeform text**: Provide custom text for key sections

All answers are saved to `.diversity-standard.yml` for future use.

### Initialize Configuration

Create a configuration file with interactive prompts:

```bash
diversity-standard init [path] [options]
```

**Available options for `init` command:**
- `--full` - Run full questionnaire (not just basic config)
- `--config FILE` - Specify config file path

**Basic mode** (default):
Asks for core project information only.

**Full mode** (`--full`):
Runs the complete questionnaire to gather all information needed for personalized documents.

This creates a `.diversity-standard.yml` file in your project root with project-specific information.

**Examples:**
```bash
# Basic config
diversity-standard init .

# Full questionnaire
diversity-standard init . --full
```

### Run Questionnaire Only

Run the interactive questionnaire without generating documents:

```bash
diversity-standard questionnaire [path]
```

This is useful if you want to answer questions and save the configuration, then generate documents later.

**Example:**
```bash
diversity-standard questionnaire .
```

### Quick Check

Check if a project is compliant (useful for CI/CD):

```bash
diversity-standard check [path]
```

Exit code 0 if compliant, 1 if documents are missing.

**Example:**
```bash
diversity-standard check .
```

## Getting Help

To see all available commands:
```bash
diversity-standard --help
```

To see options for a specific command:
```bash
diversity-standard generate --help
diversity-standard init --help
```

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

3. **Questionnaire** (interactive mode):
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

All answers are saved in `.diversity-standard.yml` for future use.

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

