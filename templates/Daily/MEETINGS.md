# Meetings

{% if has_meetings %}
Meetings are optional coordination tools.
Participation is not required to have a voice in decisions.

---

## Meeting schedule

{% if meeting_frequency %}
We hold regular meetings with the following frequency: {{ meeting_frequency }}
{% else %}
We hold regular meetings as needed for coordination.
{% endif %}

---

## Meeting types

- contributor syncs
- maintainer syncs
- working sessions
- community discussions

---

## Accessibility

- agendas are shared in advance
- notes are published after meetings
- asynchronous input is welcome
- recordings or summaries are provided when possible

---

## Roles (rotated)

Each meeting should have:

- facilitator
- note-taker
- time-keeper (optional)

Role rotation helps distribute responsibility and visibility.

---

## Where notes live

Meeting notes are stored in:

- [link or folder]

Decisions are recorded separately in the decision log.
{% else %}
This project does not hold regular meetings. All coordination happens
asynchronously through issues, pull requests, and discussions.

If you need to discuss something synchronously, you can:
- Open an issue for discussion
- Request a one-on-one conversation with maintainers
- Use the project's communication channels
{% endif %}
