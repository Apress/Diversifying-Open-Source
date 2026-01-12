# Template Conditional Examples

This document shows how to use conditional logic in templates to personalize documents based on questionnaire answers.

## Basic Conditional Sections

```jinja2
{% if has_funding %}
## Funding Sources

{{ funding_sources }}

{% else %}
This project does not currently receive external funding.
{% endif %}
```

## Multiple Choice Conditionals

```jinja2
{% if governance_model == "consensus-seeking" %}
Our project uses a consensus-seeking governance model where decisions
are made through discussion and agreement among participants.

{% elif governance_model == "council-based" %}
Our project is governed by a council of maintainers who make decisions
through discussion and voting.

{% elif governance_model == "custom" %}
{{ governance_custom }}

{% else %}
Our project uses a {{ governance_model }} governance model.
{% endif %}
```

## Yes/No Questions

```jinja2
{% if has_meetings %}
## Meeting Schedule

We hold regular meetings with the following frequency:
{{ meeting_frequency }}

{% else %}
This project does not hold regular meetings. All coordination happens
asynchronously through issues, pull requests, and discussions.
{% endif %}
```

## Custom Text Injection

```jinja2
## Code Review Philosophy

{% if code_review_philosophy %}
{{ code_review_philosophy }}

{% else %}
Code review is treated as a collaborative practice, not as a quality gate.
The goal is shared understanding and long-term maintainability.
{% endif %}
```

## Support Channels

```jinja2
## Where to get help

{% if support_channels %}
You can get help through:
{% for channel in support_channels %}
- {{ channel }}
{% endfor %}

{% else %}
- GitHub Issues
- GitHub Discussions
{% endif %}

{% if support_response_time %}
Typical response time: {{ support_response_time }}
{% endif %}
```

## Accessibility

```jinja2
{% if has_accessibility_commitment %}
## Our Commitment

{% if accessibility_approach %}
{{ accessibility_approach }}

{% else %}
We are committed to making this project accessible to all users.
{% endif %}

{% else %}
Accessibility considerations are documented as they arise.
{% endif %}
```

## Localization

```jinja2
{% if supports_multiple_languages %}
## Supported Languages

We support the following languages:
{{ supported_languages }}

{% else %}
This project currently supports English only.
{% endif %}
```

## License Rationale

```jinja2
## Rationale

{% if license_rationale %}
{{ license_rationale }}

{% else %}
This license was chosen to [provide your rationale here].
{% endif %}
```

## Maintainer Information

```jinja2
{% if maintainer_names %}
Current maintainers: {{ maintainer_names }}

{% if maintainer_selection_process %}
## Becoming a Maintainer

{{ maintainer_selection_process }}

{% endif %}

{% if maintainer_stepdown_process %}
## Stepping Down

{{ maintainer_stepdown_process }}

{% endif %}
{% endif %}
```

## Available Variables

All questionnaire answers are available as template variables:

- `has_funding` - Boolean
- `has_meetings` - Boolean
- `has_accessibility_commitment` - Boolean
- `supports_multiple_languages` - Boolean
- `emphasize_non_code` - Boolean
- `governance_model` - String
- `governance_custom` - String (if custom model)
- `funding_sources` - String
- `code_review_philosophy` - String
- `accessibility_approach` - String
- `supported_languages` - String
- `meeting_frequency` - String
- `support_channels` - List
- `support_response_time` - String
- `security_reporting_method` - String
- `security_disclosure_policy` - String
- `versioning_scheme` - String
- `code_of_conduct_enforcement` - String
- `coc_reporting_contact` - String
- `ownership_structure` - String
- `maintainer_selection_process` - String
- `maintainer_stepdown_process` - String
- `contribution_types` - String
- And all core project variables (project_name, etc.)

