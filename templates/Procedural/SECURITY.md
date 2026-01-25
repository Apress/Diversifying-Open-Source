# Security

This document defines how security issues are handled.

Its purpose is to make security reporting predictable and safe, without
requiring ad-hoc decisions in moments of urgency.

---

## Reporting a security issue

Please report security issues privately.

- Contact email: {% if security_email %}{{ security_email }}{% elif security_reporting_method %}{{ security_reporting_method }}{% else %}[security@example.org]{% endif %}
- Backup contact: [name / role]
- PGP key (optional): [link]

Do not open a public issue for security vulnerabilities.

---

## What happens after reporting

1. Acknowledgement within: [e.g. 72 hours]
2. Initial assessment and triage
3. Development of a fix or mitigation
4. Coordinated disclosure

---

## Disclosure policy

{% if security_disclosure_policy %}
{{ security_disclosure_policy }}
{% else %}
- Default disclosure window: 30–90 days after fix
- Disclosure timing may vary based on risk
- A public advisory will be published when appropriate
{% endif %}

---

## Supported versions

List which versions receive security fixes:

- Supported: [...]
- Unsupported: [...]

---

## Credit

Security reporters are credited when possible and with consent.
