"""Main CLI interface for diversity standard tool."""

from pathlib import Path

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
def inspect(path: Path):
    """Inspect a project for existing diversity documentation."""
    inspector = ProjectInspector()
    result = inspector.inspect(path)

    # Load config to check for intentionally skipped documents
    project_config = ProjectConfig(path)
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
@click.option("--backup", is_flag=True, help="Backup existing files before overwriting")
@click.option("--force", is_flag=True, help="Overwrite existing files without backup")
def init(path: Path, backup: bool, force: bool):
    """Initialize project with diversity documentation using interactive questionnaire."""
    # Load configuration
    project_config = ProjectConfig(path)
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
    config_path = path / ".diversity-standard.yml"
    project_config.save(config_path)

    if not selected_documents:
        console.print("[yellow]No documents selected for generation.[/yellow]")
        return

    # Get output preferences (check config first)
    output_preferences = inspector.get_document_location_preference(path, project_config)

    # Generate documents
    generator = DocumentGenerator()
    generated = generator.generate_missing_documents(
        result,
        project_config,
        output_preferences,
        backup=backup,
        force=force,
    )

    console.print("\n[bold]Generated documents:[/bold]\n")

    for file_path in generated:
        rel_path = file_path.relative_to(path)
        console.print(f"  [green]✓[/green] {rel_path}")

    console.print(f"\n[bold]Generated {len(generated)} document(s)[/bold]\n")
    console.print(f"[dim]Configuration saved to {config_path}[/dim]\n")




if __name__ == "__main__":
    main()

