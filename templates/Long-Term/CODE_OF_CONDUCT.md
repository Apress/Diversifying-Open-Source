# Code of Conduct

This Code of Conduct defines the behavioral expectations for participation
and how harm is addressed when it occurs.

It exists to protect people, not to police disagreement.

---

## Expected behavior

- respectful and attentive communication
- openness to feedback
- awareness of impact, not only intent
- care for shared spaces

---

## Unacceptable behavior

- harassment or discrimination
- intimidation or threats
- sustained disruption
- retaliation against reporting

---

## Reporting

Reports can be made via:

- Email: {% if coc_reporting_contact %}{{ coc_reporting_contact }}{% else %}[...]{% endif %}
- Backup contact: [...]

Reports are handled confidentially.

---

## Response process

Responses prioritize:

- safety
- accountability
- repair when possible

{% if code_of_conduct_enforcement == "Restorative process (preferred)" %}
Details are documented in the restorative process.
{% elif code_of_conduct_enforcement == "Traditional enforcement" %}
This project uses traditional enforcement mechanisms for Code of Conduct violations.
{% elif code_of_conduct_enforcement == "Hybrid approach" %}
This project uses a hybrid approach combining restorative processes with traditional enforcement as needed.
{% else %}
Details are documented in the restorative process.
{% endif %}

---

## Scope

This Code applies to all project spaces.
