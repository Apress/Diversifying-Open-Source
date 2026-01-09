# Standard Blueprint

This repository is a practical **template and implementation blueprint** for
the book:

**Diversifying Open Source**  
*An Open Standards Playbook for Inclusive and Equitable Tech Projects*  
by Paloma Oliveira  
Apress / Springer Nature, 2025  
DOI: https://doi.org/10.1007/979-8-8688-0769-5

The repository translates the book's conceptual framework into a **usable
repository architecture**.
It is not an example project; it is a **patterned structure** meant to be
copied, adapted, and applied.

---

## Relationship to the book

The book argues that open standards are not only technical specifications,
but **architectural instruments** that shape participation, labor, governance,
and long-term responsibility in free and open source projects.

This repository operationalizes that argument.

In particular, it implements the model developed in the chapter **"Making It
a Standard"**, where standards are treated as:

- lived practices,
- mechanisms for distributing responsibility,
- tools for addressing participation, labor, and legitimacy in open collaboration.

This blueprint provides the **concrete repository form** of that model.

---

## This template is designed to

- make contribution pathways explicit (including non-code work),
- reduce information imbalance through transparent communication,
- formalize governance and role rotation,
- embed restorative conflict handling,
- document funding and influence,
- keep security and release integrity legible and accountable.

---

## How to read this repository

All documents in this repository are organized by **communication type**.

The distinction helps people know when to care about a standard pattern and
how to use it.

The repository is structured into three folders:

- **Daily**
- **Procedural**
- **Long-Term**

Each folder represents a different mode of communication in open source projects.

---

standard-blueprint/
├── README.md
├── .gitignore
├── .gitattributes
│
├── Daily/
│   ├── README.md
│   ├── CONTRIBUTING.md
│   ├── SUPPORT.md
│   ├── CODE_REVIEW.md
│   ├── MEETINGS.md
│   └── communication-practices.md
│
├── Procedural/
│   ├── README.md
│   ├── SECURITY.md
│   ├── ACCESSIBILITY.md
│   ├── LOCALIZATION.md
│   ├── FUNDING.md
│   ├── CHANGELOG.md
│   ├── ADOPTERS.md
│   ├── contribution-taxonomy.md
│   ├── decision-log.md
│   ├── role-rotation.md
│   ├── audit-checklist.md
│   └── metrics/
│       ├── README.md
│       ├── chaoss-mapping.md
│       ├── dashboard.md
│       ├── data-sources.md
│       └── review-notes.md
│
├── Long-Term/
│   ├── README.md
│   ├── GOVERNANCE.md
│   ├── OWNERSHIP.md
│   ├── MAINTAINERS.md
│   ├── CODE_OF_CONDUCT.md
│   ├── LICENSE.md
│   ├── CREDIT.md
│   └── restorative-process.md
│
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md
    ├── FUNDING.yml
    ├── github-label-sync.yml
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   ├── feature_request.md
    │   └── governance_change.md
    └── workflows/
        ├── lint-docs.yml
        └── policy-checks.yml

---

## Daily Operations

The `Daily/` folder contains documents that support **orientation, coordination, and care** in ongoing work.

These texts are consulted frequently.  
They evolve quickly.  
They lower the barrier to participation for newcomers and active contributors alike.

Daily Operations answers questions such as:

- Where do I go?
- Who do I ask?
- What is expected of me?
- How do we interact while work is happening?

Examples include contribution guidance, support channels, review practices,
meeting coordination, and shared communication norms.

---

## Procedural

The `Procedural/` folder contains documents that define **repeatable
processes**, the procedures or how the project community do things.

These texts are consulted when uncertainty arises.
They are designed to set up repeatable processes, so the same decisions
don't have to be made again and again. This reduces day-to-day effort by
relying on pre-defined procedures. 

Procedural answers questions such as:

- What is the process?
- What happens if something goes wrong?
- How are decisions make?
- How are responsibilities rotated or transferred?

Examples include security handling, accessibility practices, funding
transparency, decision logs, and audit checklists.

### Contribution taxonomy

Within `Procedural/`, the **contribution taxonomy** defines how different
kinds of work are classified.

It supports:

- consistent labeling of issues and pull requests,
- visibility of non-code labor,
- fairer routing and review,
- later summaries and recognition.

### Metrics and signals

The `Procedural/metrics/` folder contains **community health and
sustainability signals**, informed by CHAOSS and related research.

Metrics are used to:

- surface patterns and risks,
- reflect on participation, workload, and sustainability,
- support governance discussions.

---

## Long-Term 

The `Long-Term/` folder contains documents that define **legitimacy,
responsibility, and repair across time**.

These texts are rarely read — but when they are, the project's credibility
depends on them.
They change slowly and require explicit consent to modify.
They carry institutional memory beyond individual contributors.

Long-term answers questions such as:

- Who decides?
- Who is accountable?
- How is harm addressed?
- How is equity being addressed?
- What obligations persist beyond individuals?

Examples include governance, ownership, maintainer responsibility, codes of
conduct, licensing, credit, and restorative processes.

---

## GitHub-specific configuration

The `.github/` folder contains **platform-specific configuration** that
supports the blueprint.

This includes:

- issue and pull request templates,
- automation and checks,
- documentation linting or policy presence checks,
- label sync according to taxonomy.

These files help automate the procedures.

---

## Further reading

For the full theoretical grounding, case studies, and analysis behind this
structure, see:

[**Diversifying Open Source**  
*An Open Standards Playbook for Inclusive and Equitable Tech Projects*](https://link.springer.com/book/10.1007/979-8-8688-0769-5)
By Paloma Oliveira
Apress / Springer Nature, 2025
DOI: <https://doi.org/10.1007/979-8-8688-0769-5>

