# Localization

Localization defines how this project adapts to **different contexts of use**, not only to different languages.

It exists to avoid treating one cultural, linguistic, or institutional context as the default,
and to reduce the need for ad-hoc decisions when the project is used elsewhere.

---

## What localization includes

Localization may involve:
- language and translation
- regional terminology and conventions
- legal or regulatory context
- accessibility expectations
- cultural references and assumptions
- documentation examples and defaults
- workflows shaped by local infrastructure

Not all localization work involves translating text.

---

## Supported contexts

This project documents which contexts it actively supports.

- Primary context(s): [e.g. language, region, institutional setting]
- Additional contexts: [list]

Unsupported contexts may still use the project, but without guarantees.

---

## How localization work is proposed

Localization changes can be proposed by:
- opening an issue labeled `localization`
- submitting a pull request with context notes

Proposals should describe:
- the context being addressed
- what assumptions are being changed
- potential impact on other contexts

---

## Review process

Localization changes are reviewed for:
- clarity and necessity
- impact on existing users
- maintainability across contexts
- consistency with project goals

Reviews may involve contributors familiar with the affected context.

---

## Documentation structure

Where possible:
- context-specific content should be clearly marked
- defaults should be explicit
- alternatives should be documented, not hidden

Avoid silently overwriting one context with another.

---

## Language-specific notes (when applicable)

When translation is involved:
- prefer plain, non-idiomatic language
- flag terms that do not translate cleanly
- document translation choices when meaning shifts

---

## Credit

Localization work is credited in [`Long-Term/CREDIT.md`](Long-Term/CREDIT.md),
including contextual research, adaptation, and review.

---

## Review and updates

Localization practices are reviewed periodically and updated
as the project’s user base and contexts evolve.