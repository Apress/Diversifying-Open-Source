# Maintainers

This document defines who maintains the project and what that role entails.

Maintainers are stewards of continuity, not gatekeepers.

---

## Maintainer responsibilities

Maintainers may:

- review and merge changes
- facilitate discussions
- uphold procedural and long-term commitments
- coordinate releases
- represent the project externally

---

## Current maintainers

{% if maintainer_names %}
Current maintainers: {{ maintainer_names }}

| Name / Handle | Area(s) | Contact |
|---------------|---------|---------|
{% for maintainer in maintainers %}
| {{ maintainer.get("name", "") }} | {{ maintainer.get("role", "") }} | {{ maintainer.get("email", "") }} |
{% endfor %}
{% else %}
| Name / Handle | Area(s) | Contact |
|---------------|---------|---------|
|               |         |         |
{% endif %}

---

## Becoming a maintainer

{% if maintainer_selection_process %}
{{ maintainer_selection_process }}
{% else %}
Describe:

- eligibility criteria
- nomination process
- decision mechanism
{% endif %}

---

## Stepping down

{% if maintainer_stepdown_process %}
{{ maintainer_stepdown_process }}
{% else %}
Maintainers may step down at any time.
Transitions should prioritize continuity and care.
{% endif %}
