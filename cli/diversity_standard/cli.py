"""Main CLI interface for diversity standard tool."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from diversity_standard.config import ProjectConfig
from diversity_standard.generator import DocumentGenerator
from diversity_standard.inspector import ProjectInspector
from diversity_standard.questionnaire import Questionnaire

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Diversity Standard CLI - Inspect and generate diversity documentation."""
    pass


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
@click.option("--config", type=click.Path(exists=True, path_type=Path), help="Config file path")
def inspect(path: Path, config: Optional[Path]):
    """Inspect a project for existing diversity documentation."""
    inspector = ProjectInspector()
    result = inspector.inspect(path)

    # Load config to check for intentionally skipped documents
    project_config = ProjectConfig(path)
    if config:
        project_config.load_from_file(config)
    else:
        project_config.load_from_file()
    
    answers = project_config.get("answers", {})
    
    # Filter out documents that were intentionally skipped
    from diversity_standard.generator import DocumentGenerator
    generator = DocumentGenerator()
    actually_missing = []
    intentionally_skipped = []
    
    for doc_name in result.missing_documents:
        if generator._should_skip_document(doc_name, answers):
            intentionally_skipped.append(doc_name)
        else:
            actually_missing.append(doc_name)

    console.print(f"\n[bold]Inspecting project:[/bold] {path}\n")

    # Show found documents
    if result.found_documents:
        table = Table(title="Found Documents", show_header=True, header_style="bold magenta")
        table.add_column("Blueprint Document", style="cyan")
        table.add_column("Location", style="green")
        table.add_column("Category", style="yellow")
        table.add_column("Match Type", style="blue")

        for doc in result.found_documents:
            rel_path = doc.actual_path.relative_to(path)
            table.add_row(
                doc.blueprint_name,
                str(rel_path),
                doc.category,
                doc.match_type,
            )
        console.print(table)
        console.print()
    else:
        console.print("[yellow]No matching documents found.[/yellow]\n")

    # Show intentionally skipped documents
    if intentionally_skipped:
        table = Table(title="Intentionally Skipped Documents", show_header=True, header_style="bold yellow")
        table.add_column("Document", style="cyan")
        table.add_column("Category", style="yellow")
        table.add_column("Reason", style="dim")

        # Load mapping to get categories
        import yaml
        mapping_file = Path(__file__).parent / "document_mapping.yml"
        with open(mapping_file) as f:
            mapping = yaml.safe_load(f)

        skip_reasons = {
            "FUNDING.md": "No funding (has_funding: false)",
            "MEETINGS.md": "No meetings (has_meetings: false)",
            "LOCALIZATION.md": "No multi-language support (supports_multiple_languages: false)",
            "ADOPTERS.md": "Not tracking adopters (tracks_adopters: false)",
        }

        for doc_name in intentionally_skipped:
            doc_config = mapping.get("documents", {}).get(doc_name, {})
            category = doc_config.get("category", "Unknown")
            reason = skip_reasons.get(doc_name, "Skipped based on questionnaire")
            table.add_row(doc_name, category, reason)

        console.print(table)
        console.print()

    # Show missing documents
    if actually_missing:
        table = Table(title="Missing Documents", show_header=True, header_style="bold red")
        table.add_column("Document", style="cyan")
        table.add_column("Category", style="yellow")

        # Load mapping to get categories
        import yaml
        mapping_file = Path(__file__).parent / "document_mapping.yml"
        with open(mapping_file) as f:
            mapping = yaml.safe_load(f)

        for doc_name in actually_missing:
            doc_config = mapping.get("documents", {}).get(doc_name, {})
            category = doc_config.get("category", "Unknown")
            table.add_row(doc_name, category)

        console.print(table)
        console.print(f"\n[bold]Total missing:[/bold] {len(actually_missing)}")
        if intentionally_skipped:
            console.print(f"[dim]Note: {len(intentionally_skipped)} document(s) were intentionally skipped based on questionnaire answers[/dim]")
    else:
        if intentionally_skipped:
            console.print(f"[green]✓ All required documents found![/green]")
            console.print(f"[dim]Note: {len(intentionally_skipped)} document(s) were intentionally skipped based on questionnaire answers[/dim]\n")
        else:
            console.print("[green]✓ All documents found![/green]\n")


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
@click.option("--config", type=click.Path(exists=True, path_type=Path), help="Config file path")
@click.option("--dry-run", is_flag=True, help="Show what would be generated without creating files")
@click.option("--backup", is_flag=True, help="Backup existing files before overwriting")
def generate(path: Path, config: Optional[Path], dry_run: bool, backup: bool):
    """Generate missing diversity documentation with interactive questionnaire."""
    # Load configuration
    project_config = ProjectConfig(path)
    if config:
        project_config.load_from_file(config)
    else:
        project_config.load_from_file()

    # Auto-detect missing values
    project_config.auto_detect()

    # Inspect project first
    inspector = ProjectInspector()
    result = inspector.inspect(path)

    if not result.missing_documents:
        console.print("[green]✓ All documents already exist![/green]")
        return

    # Show inspection results
    console.print(f"\n[bold]Found {len(result.missing_documents)} missing document(s)[/bold]\n")

    # Always run full interactive questionnaire
    questionnaire = Questionnaire()
    answers = questionnaire.run(result, project_config)
    questionnaire.update_config(project_config)
    
    # Use selected documents from questionnaire
    selected_documents = answers.get("selected_documents", result.missing_documents)
    
    # Update result to only include selected documents
    result.missing_documents = selected_documents
    
    # Save config with answers
    if not dry_run:
        project_config.save()

    if not selected_documents:
        console.print("[yellow]No documents selected for generation.[/yellow]")
        return

    # Get output preferences
    output_preferences = inspector.get_document_location_preference(path)

    # Generate documents
    generator = DocumentGenerator()
    generated = generator.generate_missing_documents(
        result,
        project_config,
        output_preferences,
        dry_run=dry_run,
        backup=backup,
    )

    if dry_run:
        console.print("\n[bold]Dry run - would generate:[/bold]\n")
    else:
        console.print("\n[bold]Generated documents:[/bold]\n")

    for file_path in generated:
        rel_path = file_path.relative_to(path)
        console.print(f"  [green]✓[/green] {rel_path}")

    if not dry_run:
        console.print(f"\n[bold]Generated {len(generated)} document(s)[/bold]\n")
        console.print("[dim]Answers saved to .diversity-standard.yml[/dim]\n")


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
@click.option("--config", type=click.Path(exists=True, path_type=Path), help="Config file path")
@click.option("--full", is_flag=True, help="Run full questionnaire (not just basic config)")
def init(path: Path, config: Optional[Path], full: bool):
    """Initialize configuration file with interactive prompts."""
    project_config = ProjectConfig(path)

    # Load existing config if present
    if config:
        project_config.load_from_file(config)
    else:
        project_config.load_from_file()

    # Auto-detect what we can
    project_config.auto_detect()

    if full:
        # Run full questionnaire
        inspector = ProjectInspector()
        result = inspector.inspect(path)
        questionnaire = Questionnaire()
        questionnaire.run(result, project_config)
        questionnaire.update_config(project_config)
    else:
        # Simple interactive prompts for missing values
        _interactive_config(project_config)

    # Save config
    config_path = path / ".diversity-standard.yml"
    project_config.save(config_path)
    console.print(f"\n[green]✓ Configuration saved to {config_path}[/green]\n")


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
@click.option("--config", type=click.Path(exists=True, path_type=Path), help="Config file path")
def check(path: Path, config: Optional[Path]):
    """Quick check if project is compliant (exit code 0 if compliant, 1 if not)."""
    inspector = ProjectInspector()
    result = inspector.inspect(path)

    if result.missing_documents:
        console.print(f"[red]✗ Project is missing {len(result.missing_documents)} document(s)[/red]")
        sys.exit(1)
    else:
        console.print("[green]✓ Project is compliant[/green]")
        sys.exit(0)


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
@click.option("--config", type=click.Path(exists=True, path_type=Path), help="Config file path")
def questionnaire(path: Path, config: Optional[Path]):
    """Run interactive questionnaire without generating documents."""
    # Load configuration
    project_config = ProjectConfig(path)
    if config:
        project_config.load_from_file(config)
    else:
        project_config.load_from_file()

    # Auto-detect missing values
    project_config.auto_detect()

    # Inspect project
    inspector = ProjectInspector()
    result = inspector.inspect(path)

    # Run questionnaire
    questionnaire = Questionnaire()
    answers = questionnaire.run(result, project_config)
    questionnaire.update_config(project_config)

    # Save config
    config_path = path / ".diversity-standard.yml"
    project_config.save(config_path)
    console.print(f"\n[green]✓ Configuration saved to {config_path}[/green]\n")
    console.print("[dim]Run 'diversity-standard generate' to create documents[/dim]\n")


def _interactive_config(config: ProjectConfig):
    """Interactive configuration prompts (simple mode)."""
    from rich.prompt import Prompt
    
    # Project name
    if not config.get("project.name"):
        name = Prompt.ask("Project name", default=Path(config.project_root).name)
        config.set("project.name", name)

    # Description
    if not config.get("project.description"):
        desc = Prompt.ask("Project description", default="")
        if desc:
            config.set("project.description", desc)

    # Repository
    if not config.get("project.repository"):
        repo = Prompt.ask("Repository URL", default="")
        if repo:
            config.set("project.repository", repo)

    # License
    if not config.get("license.type"):
        license_type = Prompt.ask("License type", default="MIT")
        config.set("license.type", license_type)

    # Support email
    if not config.get("contact.support_email"):
        email = Prompt.ask("Support email", default="")
        if email:
            config.set("contact.support_email", email)

    # Security email
    if not config.get("contact.security_email"):
        email = Prompt.ask("Security email", default="")
        if email:
            config.set("contact.security_email", email)


if __name__ == "__main__":
    main()

