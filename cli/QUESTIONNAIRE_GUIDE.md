# Interactive Questionnaire Guide

## Overview

The interactive questionnaire system helps you create personalized, working documents (not templates) by asking relevant questions and adapting content based on your answers.

## How It Works

### Question Flow

1. **Core Questions** - Basic project information
2. **Document Selection** - Choose which documents to generate
3. **Category Questions** - Questions organized by Daily/Procedural/Long-Term
4. **Document-Specific** - Questions for individual documents

### Conditional Logic

The questionnaire uses conditional logic to personalize documents:

#### Yes/No Questions

- **"Do you have funding?"**
  - If **Yes**: Asks for funding sources, generates FUNDING.md with your details
  - If **No**: Skips FUNDING.md entirely

- **"Do you hold regular meetings?"**
  - If **Yes**: Asks for meeting frequency, generates MEETINGS.md
  - If **No**: Skips MEETINGS.md

- **"Do you support multiple languages?"**
  - If **Yes**: Asks which languages, generates LOCALIZATION.md
  - If **No**: Skips LOCALIZATION.md

#### Multiple Choice Questions

- **"What governance model?"**
  - Options: consensus-seeking, council-based, voting-based, benevolent-dictator, custom
  - If **custom**: Asks you to describe your model
  - Documents adapt based on your choice

- **"How is Code of Conduct enforced?"**
  - Options: Restorative process, Traditional enforcement, Hybrid
  - Affects both CODE_OF_CONDUCT.md and restorative-process.md

#### Freeform Text

You can provide custom text for:
- Project description
- License rationale
- Code review philosophy
- Accessibility approach
- Governance participants
- And more...

This text is inserted directly into documents, allowing you to express your project's unique approach.

## Document Selection

During the questionnaire, you'll see a list of missing documents organized by category:

```
Daily:
  [✓] CONTRIBUTING.md
  [✓] SUPPORT.md
  [ ] MEETINGS.md - Skip if no meetings

Procedural:
  [✓] SECURITY.md
  [ ] FUNDING.md - Skip if no funding
  [✓] ACCESSIBILITY.md

Long-Term:
  [✓] CODE_OF_CONDUCT.md
  [✓] GOVERNANCE.md
```

You can:
- Select which documents to generate
- Skip documents you don't need
- Documents with conditional logic show hints (e.g., "Skip if no funding")

## Custom Solutions

The questionnaire allows you to provide your own solutions:

1. **Freeform text fields** - Write your own approach, philosophy, or process
2. **Custom governance** - Describe your unique governance model
3. **Custom contribution types** - List exactly what contributions you accept
4. **Custom accessibility approach** - Describe your specific commitments

Your custom text is preserved exactly as you write it - no template processing.

## Example Questions

### Core Questions

- Project name (auto-detected)
- Project description (freeform)
- Repository URL (auto-detected)
- Number of maintainers
- For each maintainer: name, email, role
- License type (multiple choice)
- License rationale (freeform, optional)
- Support email
- Security email

### Daily Operations

- "Do you want to emphasize non-code contributions?" (yes/no)
- "What types of contributions do you accept?" (freeform)
- "Where do users get help?" (multiple choice, can select multiple)
- "What is typical response time?" (text)
- "Do you hold regular meetings?" (yes/no)
- "What is your code review philosophy?" (freeform, optional)

### Procedural

- "How should security issues be reported?" (text)
- "What is your security disclosure policy?" (freeform)
- "Do you have accessibility commitments?" (yes/no)
- "Do you support multiple languages?" (yes/no)
- "Do you receive funding?" (yes/no)
- "Do you maintain a changelog?" (yes/no)
- "What versioning scheme?" (multiple choice)

### Long-Term

- "What governance model?" (multiple choice)
- "Who participates in governance?" (freeform)
- "How is Code of Conduct enforced?" (multiple choice)
- "How is ownership structured?" (freeform, optional)
- "How are maintainers selected?" (freeform, optional)
- "How can maintainers step down?" (freeform, optional)

## Usage

### Generate Documents (Always Interactive)

```bash
diversity-standard generate .
```

This runs the complete questionnaire and generates documents.

### Questionnaire Only

```bash
diversity-standard questionnaire .
```

Run the questionnaire, save answers, generate documents later.

## Saving and Reusing Answers

All answers are saved to `.diversity-standard.yml`:

```yaml
project:
  name: "My Project"
  # ...

answers:
  has_funding: false
  has_meetings: true
  governance_model: "consensus-seeking"
  # ... all your answers

selected_documents:
  - CONTRIBUTING.md
  - SUPPORT.md
  # ... only selected docs
```

You can:
- Edit the config file directly
- Re-run the questionnaire to update answers
- Use the config for future document generation

## Tips

1. **Skip questions you're unsure about** - You can always edit the generated documents later
2. **Use freeform text liberally** - This is where you make documents truly yours
3. **Review generated documents** - They're starting points, customize as needed
4. **Save your config** - Makes it easy to regenerate or update documents later

