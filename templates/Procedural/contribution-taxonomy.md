# Contribution Taxonomy

This document defines how different kinds of work are **classified**.

Its purpose is to reduce repeated discussions about what counts as contribution, to make non-code work visible, and to support consistent labeling, triage, review, and recognition.

This taxonomy is a **procedural tool**, not a hierarchy of value.

---

## Roots: OCEAN research and ACROSS labeling

This taxonomy is informed by the book’s discussion of the Open Source Complex Ecosystems and Networks (OCEAN) research
and the [“Attributing Contributor Roles” ACROSS](https://whodoesthe.dev/) labeling approach, a response to the lack of standardized acknowledgment in open source, especially for non-code contributions such as documentation, moderation, fundraising, security triage, and community organization.

This file adapts those ideas into a usable practice: labels that can be applied to issues and pull requests.

---

## What this taxonomy is for

Use this taxonomy to:
- label issues and pull requests
- route work to the right people
- clarify expectations during review
- make non-code work visible
- support later summaries (changelog, adopters, credit)

It answers:
> What kind of work is this?

It does not answer:
- how important the work is
- who deserves more credit
- who gets to decide outcomes

---

## How to use the taxonomy

### In issues
- Apply one or more taxonomy labels when opening or triaging an issue.
- Labels describe the **type of work**.
- Multiple labels are allowed.

### In pull requests
- Use taxonomy labels to signal what kind of contribution is being made.

### In review and coordination
- Labels help reviewers understand what kind of attention is needed.
- Labels help maintainers distribute work more precisely.

---

## Labels map

### Core technical work
| Label | Description |
|------|-------------|
| `code` | Implementation, refactoring, fixes |
| `architecture` | Structural or design-level changes |
| `performance` | Benchmarking and optimization |
| `security` | Security fixes and hardening |

### Review, maintenance, and quiet safety (OCEAN-aligned)
| Label | Description |
|------|-------------|
| `security-review` | Threat review, dependency risk checks |
| `repo-audit` | Repository hygiene and policy checks |
| `cleanup` | Maintenance work that prevents drift |
| `triage` | Sorting, labeling, and routing issues |

### Documentation and knowledge
| Label | Description |
|------|-------------|
| `documentation` | Writing, restructuring, clarifying docs |
| `examples` | Tutorials, samples, walkthroughs |
| `research` | Investigation and background work |

### Testing and quality
| Label | Description |
|------|-------------|
| `testing` | Test creation and QA |
| `bug-reproduction` | Reproducing and documenting issues |

### Accessibility and inclusion
| Label | Description |
|------|-------------|
| `accessibility` | Reducing access barriers |
| `localization` | Contextual adaptation beyond translation |
| `usability` | Workflow clarity and UX |

### Community, coordination, and care
| Label | Description |
|------|-------------|
| `support` | Helping users and contributors |
| `moderation` | Maintaining community safety |
| `conflict-resolution` | Restorative and relational work |
| `facilitation` | Running meetings and discussions |
| `mentorship` | Onboarding and guidance |

### Adoption and ecosystem (OCEAN-aligned)
| Label | Description |
|------|-------------|
| `adoption-advocate` | Supporting adoption relationships |
| `case-study` | Documenting real-world use |
| `user-liaison` | Maintaining feedback loops |

### Governance and sustainability
| Label | Description |
|------|-------------|
| `governance` | Policy and decision process work |
| `fundraising` | Grants and sponsorship |
| `financial-stewardship` | Budgeting and transparency |
| `operations` | Infrastructure and automation |

---

## Label set definitions

### Code and technical change
- `code` — implementation, refactoring, fixes
- `architecture` — structural changes and design work
- `performance` — benchmarking and optimization
- `security` — security fixes and hardening

### Review, maintenance
- `security-review` — threat review, dependency risk checks, vulnerability review 
- `repo-audit` — repository hygiene, policy checks, scans
- `cleanup` — maintenance tasks that prevent drift and reduce risk
- `triage` — sorting, reproducing, labeling, and routing issues

### Documentation and knowledge
- `documentation` — writing, restructuring, clarifying docs
- `examples` — tutorials, samples, walkthroughs
- `research` — investigation, analysis, background work

### Testing and quality
- `testing` — test creation, manual testing, QA
- `bug-reproduction` — narrowing down and documenting reproducible cases

### Accessibility and inclusion
- `accessibility` — reducing barriers in product or collaboration
- `localization` — contextual adaptation across languages/regions/assumptions
- `usability` — clarity, workflow friction, and user experience

### Community, coordination, and care
- `support` — answering questions, helping users and contributors
- `moderation` — maintaining community safety and focus
- `conflict-resolution` — relational and restorative work when tensions arise  
- `facilitation` — running meetings, workshops, discussions
- `mentorship` — onboarding and guidance

### Adoption and ecosystem work
- `adoption-advocate` — supporting adoption relationships and outreach  
- `case-study-coordinator` — documenting adopter stories and use cases  
- `user-liaison` — maintaining feedback loops with adopters and user communities  

### Governance and sustainability
- `governance` — governance process work and policy shaping
- `fundraising` — funding and sponsor work
- `financial-stewardship` — budgets, allocation, financial transparency roles
- `operations` — infrastructure, automation, maintenance workflows

---

## Labeling principles

When applying labels:
- describe the work, not the person
- prefer clarity over precision
- avoid collapsing everything into `code`
- update labels if the nature of the work changes

Unlabeled work is often invisible work.

---

## Governance of the taxonomy

Changes to this taxonomy affect how labor is seen and routed.
To propose a new label or change an existing one:

- open an issue labeled `governance`
- describe the gap the change addresses
- include examples of work that currently has no clear label
- document the decision outcome in [`Procedural/decision-log.md`](Procedural/decision-log.md)

