# Funding and Financial Transparency

{% if has_funding %}
This document defines how funding is disclosed and handled.

Its purpose is to make financial influence visible and reviewable.

---

## Funding sources

{% if funding_sources %}
{{ funding_sources }}
{% else %}
List current sources:

- Grants: [...]
- Sponsorships: [...]
- Donations: [...]
- In-kind support: [...]
{% endif %}

---

## Use of funds

Funds may be used for:

- maintenance work
- infrastructure costs
- accessibility improvements
- community activities
- security or audit work

---

## Decision process

Funding decisions follow established governance procedures.
Significant allocations are documented.

---

## Conflicts of interest

- Conflicts must be disclosed
- Recusal procedures: [...]

---

## Updates

This document is updated when funding sources or policies change.
{% else %}
This project does not currently receive external funding.

All work is contributed voluntarily by community members.
{% endif %}
