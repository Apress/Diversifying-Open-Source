"""Document generation from templates."""

import shutil
from pathlib import Path
from typing import Dict, List, Optional

from jinja2 import Environment, FileSystemLoader

from diversity_standard.config import ProjectConfig
from diversity_standard.inspector import InspectionResult


class DocumentGenerator:
    """Generates documents from templates."""

    def __init__(self, blueprint_root: Optional[Path] = None, template_dir: Optional[Path] = None):
        """Initialize generator.

        Args:
            blueprint_root: Root directory of blueprint repository
            template_dir: Directory containing templates. If None, uses
                         blueprint_root as template source
        """
        if blueprint_root is None:
            blueprint_root = Path(__file__).parent.parent.parent

        self.blueprint_root = blueprint_root

        if template_dir is None:
            # Try to find templates in blueprint structure
            template_dir = blueprint_root
        self.template_dir = template_dir

        # Setup Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate_document(
        self,
        blueprint_name: str,
        output_path: Path,
        config: ProjectConfig,
        category: str = "Unknown",
    ) -> bool:
        """Generate a single document from template.

        Args:
            blueprint_name: Name of blueprint document to generate
            config: Project configuration
            output_path: Where to write the generated document
            category: Document category (Daily/Procedural/Long-Term)

        Returns:
            True if document was generated successfully
        """
        # Find template file
        template_path = self._find_template(blueprint_name, category)
        if not template_path:
            return False

        # Read template
        try:
            template_content = template_path.read_text(encoding="utf-8")
        except IOError:
            return False

        # Prepare template context
        context = self._build_context(config, blueprint_name, category)

        # Render template with Jinja2 (supports conditionals)
        try:
            template = self.env.from_string(template_content)
            rendered = template.render(**context)
        except Exception as e:
            # Fallback: simple placeholder replacement
            # Log error for debugging (can be enhanced with proper logging later)
            rendered = self._simple_replace(template_content, context)

        # Write output
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
            return True
        except IOError:
            return False

    def _find_template(self, blueprint_name: str, category: str) -> Optional[Path]:
        """Find template file for a blueprint document.

        Args:
            blueprint_name: Name of blueprint document
            category: Document category

        Returns:
            Path to template file or None
        """
        # Try category-specific directory first
        category_dirs = {
            "Daily": ["Daily", "daily"],
            "Procedural": ["Procedural", "procedural"],
            "Long-Term": ["Long-Term", "LongTerm", "long-term", "long_term"],
        }

        for dir_name in category_dirs.get(category, []):
            template_path = self.blueprint_root / dir_name / blueprint_name
            if template_path.exists() and template_path.is_file():
                return template_path

        # Try templates directory (for copied templates)
        template_path = Path(__file__).parent / "templates" / blueprint_name
        if template_path.exists() and template_path.is_file():
            return template_path

        # Try root directory
        template_path = self.blueprint_root / blueprint_name
        if template_path.exists() and template_path.is_file():
            return template_path

        # Try in subdirectories of templates
        templates_dir = Path(__file__).parent / "templates"
        for subdir in templates_dir.iterdir():
            if subdir.is_dir():
                template_path = subdir / blueprint_name
                if template_path.exists() and template_path.is_file():
                    return template_path

        return None

    def _build_context(
        self, config: ProjectConfig, blueprint_name: str, category: str
    ) -> Dict:
        """Build template context from configuration.

        Args:
            config: Project configuration
            blueprint_name: Name of document being generated
            category: Document category

        Returns:
            Dictionary of template variables
        """
        # Get answers from questionnaire if available
        answers = config.get("answers", {})

        context = {
            "project_name": config.get("project.name", "Project Name"),
            "project_description": config.get("project.description", ""),
            "project_repository": config.get("project.repository", ""),
            "license_type": config.get("license.type", ""),
            "license_rationale": config.get("license.rationale", ""),
            "maintainers": config.get("maintainers", []),
            "support_email": config.get("contact.support_email", ""),
            "security_email": config.get("contact.security_email", ""),
            "governance_model": config.get("governance.model", ""),
            "funding_sources": config.get("funding.sources", []),
        }

        # Add questionnaire answers to context (for conditional rendering)
        if answers:
            context.update(answers)
            # Convert yes/no answers to boolean for Jinja2
            for key, value in answers.items():
                if isinstance(value, bool):
                    context[key] = value
                elif isinstance(value, str) and value.lower() in ["true", "false", "yes", "no"]:
                    context[key] = value.lower() in ["true", "yes"]

        # Add maintainer info as formatted strings
        if context["maintainers"]:
            maintainer_names = [m.get("name", "") for m in context["maintainers"] if m.get("name")]
            context["maintainer_names"] = ", ".join(maintainer_names)
            context["maintainer_list"] = maintainer_names
        else:
            context["maintainer_names"] = ""
            context["maintainer_list"] = []

        # Add common conditional flags (convert to boolean if needed)
        context["has_funding"] = bool(answers.get("has_funding", False))
        context["has_meetings"] = bool(answers.get("has_meetings", False))
        context["has_accessibility_commitment"] = bool(answers.get("has_accessibility_commitment", True))
        context["supports_multiple_languages"] = bool(answers.get("supports_multiple_languages", False))
        context["emphasize_non_code"] = bool(answers.get("emphasize_non_code", True))
        context["tracks_adopters"] = bool(answers.get("tracks_adopters", False))
        context["maintains_decision_log"] = bool(answers.get("maintains_decision_log", True))
        context["has_role_rotation"] = bool(answers.get("has_role_rotation", True))
        context["conducts_audits"] = bool(answers.get("conducts_audits", True))

        # Ensure all new question answers are in context with defaults
        new_question_defaults = {
            "communication_style": "",
            "communication_channels": [],
            "adopter_submission_process": "",
            "decision_log_process": "",
            "role_rotation_frequency": "monthly",
            "audit_frequency": "annually",
            "audit_reviewers": "",
            "credit_approach": "",
        }
        
        for key, default_value in new_question_defaults.items():
            if key not in context:
                context[key] = answers.get(key, default_value)

        # Ensure funding_sources is a string if it's a list
        if isinstance(context.get("funding_sources"), list):
            if context["funding_sources"]:
                context["funding_sources"] = "\n".join(f"- {source}" for source in context["funding_sources"])
            else:
                context["funding_sources"] = ""

        return context

    def _simple_replace(self, template: str, context: Dict) -> str:
        """Simple placeholder replacement (fallback).

        Args:
            template: Template content
            context: Template variables

        Returns:
            Rendered content
        """
        result = template
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            result = result.replace(placeholder, str(value))
        return result

    def generate_missing_documents(
        self,
        inspection_result: InspectionResult,
        config: ProjectConfig,
        output_preferences: Optional[Dict[str, Path]] = None,
        dry_run: bool = False,
        backup: bool = False,
    ) -> List[Path]:
        """Generate all missing documents.

        Args:
            inspection_result: Results from project inspection
            config: Project configuration
            output_preferences: Preferred output locations by category
            dry_run: If True, don't actually create files
            backup: If True, backup existing files before overwriting

        Returns:
            List of generated file paths
        """
        generated = []

        if output_preferences is None:
            from diversity_standard.inspector import ProjectInspector

            inspector = ProjectInspector(self.blueprint_root)
            output_preferences = inspector.get_document_location_preference(
                inspection_result.project_root
            )

        # Load document mapping to get categories
        import yaml

        mapping_file = Path(__file__).parent / "document_mapping.yml"
        with open(mapping_file) as f:
            mapping = yaml.safe_load(f)

        # Get answers to check for conditional skipping
        answers = config.get("answers", {})

        for blueprint_name in inspection_result.missing_documents:
            # Check if document should be skipped based on answers
            if self._should_skip_document(blueprint_name, answers):
                continue

            doc_config = mapping.get("documents", {}).get(blueprint_name, {})
            category = doc_config.get("category", "Unknown")

            # Determine output path
            base_path = output_preferences.get(category, inspection_result.project_root)
            output_path = base_path / blueprint_name

            # Check if file already exists
            if output_path.exists() and backup:
                backup_path = output_path.with_suffix(output_path.suffix + ".backup")
                if not dry_run:
                    shutil.copy2(output_path, backup_path)

            if not dry_run:
                success = self.generate_document(blueprint_name, output_path, config, category)
                if success:
                    generated.append(output_path)
            else:
                generated.append(output_path)  # Include in dry-run list

        return generated

    def _should_skip_document(self, doc_name: str, answers: Dict) -> bool:
        """Check if document should be skipped based on questionnaire answers.

        Args:
            doc_name: Document name
            answers: Questionnaire answers

        Returns:
            True if document should be skipped
        """
        # Check for explicit skip conditions
        skip_conditions = {
            "FUNDING.md": not bool(answers.get("has_funding", False)),
            "MEETINGS.md": not bool(answers.get("has_meetings", False)),
            "LOCALIZATION.md": not bool(answers.get("supports_multiple_languages", False)),
            "ADOPTERS.md": not bool(answers.get("tracks_adopters", False)),
        }

        return skip_conditions.get(doc_name, False)

