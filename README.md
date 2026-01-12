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

- [**Daily**](Daily/README.md)
- [**Procedural**](Procedural/README.md)
- [**Long-Term**](Long-Term/README.md)

Each folder represents a different mode of communication in open source projects.

---

## Folders architecture

```
standard-blueprint/
├── README.md
├── .gitignore
├── .gitattributes
├── LICENSE
├── tests/
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
    ├── CODEOWNER
    └── workflows/

```

---

## CLI Tool

This repository includes a **command-line interface (CLI)** tool to help projects adopt and personalize the blueprint documents.

The CLI can:

- inspect existing projects to identify missing documents,
- generate personalized documents from templates using an interactive questionnaire,

For installation, usage, and detailed documentation, see:
[**CLI Documentation**](cli/README.md)

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

