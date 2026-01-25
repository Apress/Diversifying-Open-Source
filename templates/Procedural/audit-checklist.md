# Audit Checklist

This checklist supports periodic review of project practices.

---

## Documentation baseline

- [ ] Contribution paths are documented
- [ ] Security process is defined
- [ ] Accessibility practices are written
- [ ] Funding sources are disclosed
- [ ] Decisions are logged
- [ ] Roles are assigned and rotated

---

## Practice check

- [ ] Procedures are followed in practice
- [ ] Exceptions are documented
- [ ] Non-code work is visible
- [ ] Feedback loops exist

---

## Review notes

{% if audit_frequency %}
This checklist is reviewed {{ audit_frequency }}.
{% endif %}

Date:
Reviewer(s):{% if audit_reviewers %} {{ audit_reviewers }}{% endif %}
Findings:
Follow-up actions:
