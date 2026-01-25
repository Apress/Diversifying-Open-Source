#!/usr/bin/env python3
"""Setup script to copy blueprint templates to CLI templates directory."""

import shutil
from pathlib import Path


def setup_templates():
    """Copy blueprint files to templates directory."""
    # Get paths
    cli_root = Path(__file__).parent
    repo_root = cli_root.parent
    templates_dir = cli_root / "diversity_standard" / "templates"

    # Create templates directory structure
    templates_dir.mkdir(parents=True, exist_ok=True)

    # Directories to copy from (now in templates/)
    source_dirs = {
        "Daily": repo_root / "templates" / "Daily",
        "Procedural": repo_root / "templates" / "Procedural",
        "Long-Term": repo_root / "templates" / "Long-Term",
    }

    copied = 0

    for category, source_dir in source_dirs.items():
        if not source_dir.exists():
            print(f"Warning: {source_dir} does not exist, skipping...")
            continue

        # Copy all markdown files
        for md_file in source_dir.glob("*.md"):
            dest = templates_dir / md_file.name
            shutil.copy2(md_file, dest)
            print(f"Copied {md_file.name} from {category}/")
            copied += 1

        # Handle subdirectories (like metrics/)
        for subdir in source_dir.iterdir():
            if subdir.is_dir():
                subdest = templates_dir / subdir.name
                subdest.mkdir(exist_ok=True)
                for md_file in subdir.glob("*.md"):
                    dest = subdest / md_file.name
                    shutil.copy2(md_file, dest)
                    print(f"Copied {subdir.name}/{md_file.name} from {category}/")
                    copied += 1

    print(f"\n✓ Copied {copied} template file(s) to {templates_dir}")


if __name__ == "__main__":
    setup_templates()

