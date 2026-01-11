"""Project inspection logic for finding and mapping documents."""

import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from diversity_standard.utils import (
    contains_keywords,
    find_files_by_patterns,
    read_file_content,
)


@dataclass
class DocumentMatch:
    """Represents a found document and its mapping."""

    blueprint_name: str
    actual_path: Path
    category: str
    confidence: float  # 0.0 to 1.0
    match_type: str  # "filename" or "content"


@dataclass
class InspectionResult:
    """Results of project inspection."""

    found_documents: List[DocumentMatch]
    missing_documents: List[str]
    project_root: Path


class ProjectInspector:
    """Inspects projects to find existing documents."""

    def __init__(self, blueprint_root: Optional[Path] = None):
        """Initialize inspector.

        Args:
            blueprint_root: Root directory of blueprint repository.
                          If None, tries to find it relative to this file.
        """
        if blueprint_root is None:
            # Assume we're in cli/diversity_standard/, go up to repo root
            blueprint_root = Path(__file__).parent.parent.parent
        self.blueprint_root = blueprint_root
        self.mapping = self._load_document_mapping()

    def _load_document_mapping(self) -> Dict:
        """Load document mapping configuration.

        Returns:
            Document mapping dictionary
        """
        mapping_file = Path(__file__).parent / "document_mapping.yml"
        if mapping_file.exists():
            with open(mapping_file) as f:
                return yaml.safe_load(f)
        return {"documents": {}}

    def inspect(self, project_root: Path) -> InspectionResult:
        """Inspect a project for existing documents.

        Args:
            project_root: Root directory of the project to inspect

        Returns:
            InspectionResult with found and missing documents
        """
        found_documents: List[DocumentMatch] = []
        found_blueprint_names = set()

        # Search for each blueprint document
        for blueprint_name, config in self.mapping.get("documents", {}).items():
            matches = self._find_document(
                project_root, blueprint_name, config
            )
            if matches:
                found_documents.extend(matches)
                found_blueprint_names.add(blueprint_name)

        # Determine missing documents
        all_blueprint_docs = set(self.mapping.get("documents", {}).keys())
        missing_documents = sorted(all_blueprint_docs - found_blueprint_names)

        return InspectionResult(
            found_documents=found_documents,
            missing_documents=missing_documents,
            project_root=project_root,
        )

    def _find_document(
        self, project_root: Path, blueprint_name: str, config: Dict
    ) -> List[DocumentMatch]:
        """Find a specific document in the project.

        Args:
            project_root: Project root directory
            blueprint_name: Name of the blueprint document
            config: Document mapping configuration

        Returns:
            List of DocumentMatch objects (may be empty)
        """
        matches: List[DocumentMatch] = []
        filenames = config.get("filenames", [])
        content_keywords = config.get("content_keywords", [])
        category = config.get("category", "Unknown")

        # Search by filename
        filename_matches = find_files_by_patterns(project_root, filenames)
        for path in filename_matches:
            matches.append(
                DocumentMatch(
                    blueprint_name=blueprint_name,
                    actual_path=path,
                    category=category,
                    confidence=0.9,  # High confidence for filename match
                    match_type="filename",
                )
            )

        # If no filename match, try content-based search
        if not matches:
            # Search all markdown files for content keywords
            for md_file in project_root.rglob("*.md"):
                if md_file in [m.actual_path for m in matches]:
                    continue  # Already matched by filename

                content = read_file_content(md_file)
                if content and contains_keywords(content, content_keywords):
                    matches.append(
                        DocumentMatch(
                            blueprint_name=blueprint_name,
                            actual_path=md_file,
                            category=category,
                            confidence=0.6,  # Lower confidence for content match
                            match_type="content",
                        )
                    )
                    break  # Only take first content match

        return matches

    def get_document_location_preference(self, project_root: Path) -> Dict[str, Path]:
        """Determine preferred document locations based on existing structure.

        Args:
            project_root: Project root directory

        Returns:
            Dictionary mapping categories to preferred base paths
        """
        preferences: Dict[str, Path] = {}

        # Check for existing blueprint structure
        daily_dir = project_root / "Daily"
        procedural_dir = project_root / "Procedural"
        long_term_dir = project_root / "Long-Term"

        if daily_dir.exists() or procedural_dir.exists() or long_term_dir.exists():
            # Use blueprint structure
            preferences["Daily"] = daily_dir if daily_dir.exists() else project_root / "Daily"
            preferences["Procedural"] = (
                procedural_dir if procedural_dir.exists() else project_root / "Procedural"
            )
            preferences["Long-Term"] = (
                long_term_dir if long_term_dir.exists() else project_root / "Long-Term"
            )
        else:
            # Check for docs/ directory
            docs_dir = project_root / "docs"
            if docs_dir.exists():
                # Use docs/ with subdirectories
                preferences["Daily"] = docs_dir / "daily"
                preferences["Procedural"] = docs_dir / "procedural"
                preferences["Long-Term"] = docs_dir / "long-term"
            else:
                # Default to root
                preferences["Daily"] = project_root
                preferences["Procedural"] = project_root
                preferences["Long-Term"] = project_root

        return preferences

