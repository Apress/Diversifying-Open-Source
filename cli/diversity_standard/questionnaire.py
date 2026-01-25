"""Interactive questionnaire system for personalizing documents."""

import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from diversity_standard.config import ProjectConfig
from diversity_standard.inspector import InspectionResult

console = Console()


@dataclass
class Question:
    """Represents a question in the questionnaire."""

    id: str
    type: str
    text: str
    category: str
    options: Optional[List[str]] = None
    default: Any = None
    default_from: Optional[str] = None
    required: bool = False
    multiple: bool = False
    depends_on: Optional[str] = None
    show_if: Optional[Any] = None
    if_yes: Optional[List[Dict]] = None
    if_no: Optional[Dict] = None
    if_custom: Optional[List[Dict]] = None
    auto_detect: bool = False
    affects: Optional[List[str]] = None


class Questionnaire:
    """Manages interactive questionnaire flow."""

    def __init__(self, questions_file: Optional[Path] = None):
        """Initialize questionnaire.

        Args:
            questions_file: Path to questions.yml. If None, uses default location.
        """
        if questions_file is None:
            questions_file = Path(__file__).parent / "questions.yml"
        self.questions_file = questions_file
        self.questions = self._load_questions()
        self.answers: Dict[str, Any] = {}

    def _load_questions(self) -> List[Question]:
        """Load questions from YAML file.

        Returns:
            List of Question objects
        """
        if not self.questions_file.exists():
            return []

        with open(self.questions_file) as f:
            data = yaml.safe_load(f)

        questions = []
        for q_data in data.get("questions", []):
            question = Question(
                id=q_data.get("id"),
                type=q_data.get("type"),
                text=q_data.get("text"),
                category=q_data.get("category", "core"),
                options=q_data.get("options"),
                default=q_data.get("default"),
                default_from=q_data.get("default_from"),
                required=q_data.get("required", False),
                multiple=q_data.get("multiple", False),
                depends_on=q_data.get("depends_on"),
                show_if=q_data.get("show_if"),
                if_yes=q_data.get("if_yes"),
                if_no=q_data.get("if_no"),
                if_custom=q_data.get("if_custom"),
                auto_detect=q_data.get("auto_detect", False),
                affects=q_data.get("affects", []),
            )
            questions.append(question)

        return questions

    def run(
        self, inspection_result: InspectionResult, config: ProjectConfig
    ) -> Dict[str, Any]:
        """Run the full questionnaire.

        Args:
            inspection_result: Results from project inspection
            config: Project configuration (for auto-detection)

        Returns:
            Dictionary of answers
        """
        console.print("\n[bold cyan]Diversity Standard Questionnaire[/bold cyan]\n")
        console.print(
            "This will help personalize your documentation. "
            "You can skip questions by pressing Enter.\n"
        )

        # Phase 1: Core questions
        console.print("[bold]Phase 1: Core Project Information[/bold]\n")
        self._ask_questions_by_category("core", config)

        # Phase 2: Document selection
        console.print("\n[bold]Phase 2: Document Selection[/bold]\n")
        selected_docs = self._select_documents(inspection_result.missing_documents)

        # Phase 3: Category questions (only for selected docs)
        console.print("\n[bold]Phase 3: Category-Specific Questions[/bold]\n")
        for category in ["daily", "procedural", "long_term"]:
            docs_in_category = [
                d
                for d in selected_docs
                if self._get_document_category(d) == category.title()
            ]
            if docs_in_category:
                category_display = category.replace("_", "-").title()
                console.print(f"\n[bold]{category_display} Questions[/bold]\n")
                self._ask_questions_by_category(category, config, selected_docs)

        # Store selected documents
        self.answers["selected_documents"] = selected_docs

        return self.answers

    def _ask_questions_by_category(
        self,
        category: str,
        config: ProjectConfig,
        selected_docs: Optional[List[str]] = None,
    ) -> None:
        """Ask all questions for a specific category.

        Args:
            category: Question category
            config: Project configuration
            selected_docs: List of selected documents (for conditional logic)
        """
        category_questions = [
            q for q in self.questions if q.category == category
        ]

        for question in category_questions:
            # Check dependencies
            if question.depends_on:
                dep_value = self.answers.get(question.depends_on)
                if question.show_if is not None and dep_value != question.show_if:
                    continue

            # Check if question affects selected documents
            if selected_docs:
                # This is a simplified check - in full implementation,
                # we'd check the 'affects' field from questions.yml
                pass

            answer = self._ask_question(question, config)
            if answer is not None:
                self.answers[question.id] = answer

                # Handle maintainer collection
                if question.id == "maintainer_count":
                    maintainers = []
                    count = int(answer) if isinstance(answer, (int, str)) else 1
                    for i in range(count):
                        console.print(f"\n[bold]Maintainer {i+1}:[/bold]")
                        name = Prompt.ask("  Name", default="")
                        email = Prompt.ask("  Email", default="")
                        role = Prompt.ask("  Role", default="Maintainer")
                        if name:
                            maintainers.append({"name": name, "email": email, "role": role})
                    self.answers["maintainers"] = maintainers

                # Handle conditional follow-up questions
                if question.type == "yes_no":
                    if answer is True and question.if_yes:
                        self._ask_followup_questions(question.if_yes, config)
                    elif answer is False and question.if_no:
                        skip_docs = question.if_no.get("skip_documents", [])
                        if skip_docs:
                            # Remove from selected if not already done
                            pass

                elif question.type == "multiple_choice" and answer == "custom":
                    if question.if_custom:
                        self._ask_followup_questions(question.if_custom, config)

    def _ask_question(self, question: Question, config: ProjectConfig) -> Any:
        """Ask a single question.

        Args:
            question: Question to ask
            config: Project configuration

        Returns:
            Answer value
        """
        # Get default value
        default = question.default
        if question.default_from:
            default = self.answers.get(question.default_from, default)

        # Auto-detect if enabled
        if question.auto_detect and default is None:
            config_key_map = {
                "project_name": "project.name",
                "project_description": "project.description",
                "project_repository": "project.repository",
                "license_type": "license.type",
            }
            if question.id in config_key_map:
                default = config.get(config_key_map[question.id])

        # Ask based on question type
        if question.type == "yes_no":
            return Confirm.ask(question.text, default=default if default is not None else False)

        elif question.type == "multiple_choice":
            # Display numbered options for better readability
            console.print(f"[yellow]{question.text}[/yellow]")
            for i, option in enumerate(question.options, 1):
                console.print(f"  {i}. {option}")
            
            if question.multiple:
                # Multi-select
                while True:
                    selected = Prompt.ask(
                        "Enter numbers (comma-separated, e.g., 1,3,5) or press Enter to skip",
                        default="",
                    )
                    if not selected:
                        return []
                    
                    try:
                        indices = [int(x.strip()) - 1 for x in selected.split(",")]
                        # Validate indices are in range
                        valid_indices = [i for i in indices if 0 <= i < len(question.options)]
                        if valid_indices:
                            return [question.options[i] for i in valid_indices]
                        else:
                            console.print("[red]No valid selections. Please enter numbers between 1 and {}[/red]".format(len(question.options)))
                    except ValueError:
                        console.print("[red]Invalid input. Please enter numbers separated by commas (e.g., 1,2,3)[/red]")
            else:
                # Single-select: allow number or option text
                default_idx = default if isinstance(default, int) else (default if default is None else None)
                if default_idx is None and question.options:
                    default_idx = 0
                
                while True:
                    prompt_text = f"Enter number (1-{len(question.options)})"
                    if default_idx is not None:
                        prompt_text += f" [default: {default_idx + 1}]"
                    prompt_text += ": "
                    
                    answer = Prompt.ask(prompt_text, default=str(default_idx + 1) if default_idx is not None else "")
                    
                    # Try to parse as number first
                    try:
                        num = int(answer.strip())
                        if 1 <= num <= len(question.options):
                            return question.options[num - 1]
                        else:
                            console.print(f"[red]Please enter a number between 1 and {len(question.options)}[/red]")
                    except ValueError:
                        # Try to match by option text (case-insensitive, partial match)
                        answer_lower = answer.strip().lower()
                        matches = [opt for opt in question.options if answer_lower in opt.lower()]
                        if len(matches) == 1:
                            return matches[0]
                        elif len(matches) > 1:
                            console.print(f"[red]Ambiguous: '{answer}' matches multiple options. Please enter a number.[/red]")
                        else:
                            console.print(f"[red]Invalid input. Please enter a number (1-{len(question.options)}) or part of an option name.[/red]")

        elif question.type == "text":
            return Prompt.ask(
                question.text,
                default=default or "",
                show_default=bool(default),
            )

        elif question.type == "freeform":
            console.print(f"[yellow]{question.text}[/yellow]")
            if default:
                console.print(f"[dim]Press Enter to use default or type your own text[/dim]")
            console.print("[dim](You can enter multiple lines. Type 'END' on a new line when finished)[/dim]\n")
            
            lines = []
            try:
                while True:
                    line = Prompt.ask("", default="", show_default=False)
                    if line.strip().upper() == "END":
                        break
                    if not line.strip() and not lines:
                        # First empty line - use default if available
                        if default:
                            return default
                        continue
                    if not line.strip() and lines:
                        # Empty line after content - finish
                        break
                    lines.append(line)
            except (KeyboardInterrupt, EOFError):
                pass
            
            result = "\n".join(lines) if lines else (default or "")
            return result

        elif question.type == "number":
            return int(
                Prompt.ask(
                    question.text,
                    default=str(default) if default is not None else "1",
                )
            )

        return None

    def _ask_followup_questions(
        self, followup_questions: List[Dict], config: ProjectConfig
    ) -> None:
        """Ask follow-up questions.

        Args:
            followup_questions: List of follow-up question definitions
            config: Project configuration
        """
        for q_data in followup_questions:
            question = Question(
                id=q_data.get("id"),
                type=q_data.get("type"),
                text=q_data.get("text"),
                category=q_data.get("category", "core"),
                options=q_data.get("options"),
                default=q_data.get("default"),
            )
            answer = self._ask_question(question, config)
            if answer is not None:
                self.answers[question.id] = answer

    def _select_documents(self, missing_documents: List[str]) -> List[str]:
        """Interactive document selection.

        Args:
            missing_documents: List of missing document names

        Returns:
            List of selected document names
        """
        if not missing_documents:
            return []

        # Load document mapping to get categories
        import yaml

        mapping_file = Path(__file__).parent / "document_mapping.yml"
        with open(mapping_file) as f:
            mapping = yaml.safe_load(f)

        # Group by category
        by_category: Dict[str, List[str]] = {}
        for doc_name in missing_documents:
            doc_config = mapping.get("documents", {}).get(doc_name, {})
            category = doc_config.get("category", "Unknown")
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(doc_name)

        # Show selection interface
        console.print("Select which documents to generate:\n")
        selected = []

        for category, docs in by_category.items():
            console.print(f"[bold]{category}:[/bold]")
            for doc in docs:
                if Confirm.ask(f"  Generate {doc}?", default=True):
                    selected.append(doc)
            console.print()

        return selected

    def _get_document_category(self, doc_name: str) -> str:
        """Get category for a document.

        Args:
            doc_name: Document name

        Returns:
            Category name
        """
        import yaml

        mapping_file = Path(__file__).parent / "document_mapping.yml"
        with open(mapping_file) as f:
            mapping = yaml.safe_load(f)

        doc_config = mapping.get("documents", {}).get(doc_name, {})
        return doc_config.get("category", "Unknown")

    def get_answers(self) -> Dict[str, Any]:
        """Get collected answers.

        Returns:
            Dictionary of answers
        """
        return self.answers.copy()

    def update_config(self, config: ProjectConfig) -> None:
        """Update configuration with questionnaire answers.

        Args:
            config: Project configuration to update
        """
        # Map answers to config structure
        if "project_name" in self.answers:
            config.set("project.name", self.answers["project_name"])
        if "project_description" in self.answers:
            config.set("project.description", self.answers["project_description"])
        if "project_repository" in self.answers:
            config.set("project.repository", self.answers["project_repository"])
        if "license_type" in self.answers:
            config.set("license.type", self.answers["license_type"])
        if "license_rationale" in self.answers:
            config.set("license.rationale", self.answers["license_rationale"])
        if "support_email" in self.answers:
            config.set("contact.support_email", self.answers["support_email"])
        if "security_email" in self.answers:
            config.set("contact.security_email", self.answers["security_email"])
        if "document_location" in self.answers:
            config.set("output.location", self.answers["document_location"])
        if "document_location_custom" in self.answers:
            config.set("output.location_custom", self.answers["document_location_custom"])
        if "governance_model" in self.answers:
            config.set("governance.model", self.answers["governance_model"])
        if "governance_custom" in self.answers:
            config.set("governance.custom_description", self.answers["governance_custom"])
        if "maintainers" in self.answers:
            config.set("maintainers", self.answers["maintainers"])
        if "funding_sources" in self.answers:
            config.set("funding.sources", [self.answers["funding_sources"]])
        
        # Map new communication questions
        if "communication_style" in self.answers:
            config.set("communication.style", self.answers["communication_style"])
        if "communication_channels" in self.answers:
            config.set("communication.channels", self.answers["communication_channels"])
        
        # Map new procedural questions
        if "tracks_adopters" in self.answers:
            config.set("adopters.track", self.answers["tracks_adopters"])
        if "adopter_submission_process" in self.answers:
            config.set("adopters.submission_process", self.answers["adopter_submission_process"])
        if "maintains_decision_log" in self.answers:
            config.set("decision_log.maintain", self.answers["maintains_decision_log"])
        if "decision_log_process" in self.answers:
            config.set("decision_log.process", self.answers["decision_log_process"])
        if "has_role_rotation" in self.answers:
            config.set("role_rotation.enabled", self.answers["has_role_rotation"])
        if "role_rotation_frequency" in self.answers:
            config.set("role_rotation.frequency", self.answers["role_rotation_frequency"])
        if "conducts_audits" in self.answers:
            config.set("audit.enabled", self.answers["conducts_audits"])
        if "audit_frequency" in self.answers:
            config.set("audit.frequency", self.answers["audit_frequency"])
        if "audit_reviewers" in self.answers:
            config.set("audit.reviewers", self.answers["audit_reviewers"])
        
        # Map new long-term questions
        if "credit_approach" in self.answers:
            config.set("credit.approach", self.answers["credit_approach"])

        # Store all answers in answers section (this makes them available to templates)
        config.set("answers", self.answers)

