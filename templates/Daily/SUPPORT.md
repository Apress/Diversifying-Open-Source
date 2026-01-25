# Support

Support is treated as shared infrastructure, not as an individual burden.

This document explains **where to ask what**, so questions do not get lost or misplaced.

---

## Where to get help

{% if support_channels %}
You can get help through:
{% for channel in support_channels %}
- {{ channel }}{% if channel == "Email" and support_email %} ({{ support_email }}){% endif %}
{% endfor %}
{% else %}
- Questions and discussions: [link]
- Bug reports: Issues
- Feature ideas: Issues
{% endif %}
- Security concerns: see [Procedural/SECURITY.md](Procedural/SECURITY.md){% if security_email %} or contact {{ security_email }}{% endif %}

{% if support_channels %}
If you are unsure where your question belongs, start with the discussion channel.
{% else %}
If you are unsure where your question belongs, start with the discussion channel.
{% endif %}

---

## What to include

When asking for help, try to include:

- what you are trying to do
- what you expected to happen
- what actually happened
- any relevant context (version, environment, screenshots)

Incomplete questions are still welcome.

---

## Response expectations

This is a best-effort, volunteer-driven project.

- Typical response time: {% if support_response_time %}{{ support_response_time }}{% else %}a few days{% endif %}
- No response does not mean your question is unwelcome
- You are encouraged to follow up politely

---

## Accessibility and language

- Plain-language questions are welcome.
- You may ask for clarification, summaries, or slower explanations.
- Accessibility-related questions should be clearly marked.
