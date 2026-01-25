"""Utility functions for the diversity standard CLI."""

import json
import re
from pathlib import Path
from typing import Any, Dict, Optional


def find_file_by_name(
    root: Path, filename: str, case_sensitive: bool = False
) -> Optional[Path]:
    """Find a file by name in the directory tree.

    Args:
        root: Root directory to search
        filename: Filename to search for
        case_sensitive: Whether to do case-sensitive matching

    Returns:
        Path to the file if found, None otherwise
    """
    pattern = filename if case_sensitive else filename.lower()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if case_sensitive:
            if path.name == filename:
                return path
        else:
            if path.name.lower() == pattern:
                return path
    return None


def find_files_by_patterns(
    root: Path, patterns: list[str], case_sensitive: bool = False
) -> list[Path]:
    """Find files matching any of the given patterns.

    Args:
        root: Root directory to search
        patterns: List of filename patterns to match
        case_sensitive: Whether to do case-sensitive matching

    Returns:
        List of matching file paths
    """
    matches = []
    patterns_lower = [p.lower() for p in patterns] if not case_sensitive else patterns

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        name = path.name if case_sensitive else path.name.lower()
        for pattern in patterns_lower:
            if pattern in name or name == pattern:
                matches.append(path)
                break
    return matches


def read_json_file(path: Path) -> Optional[Dict[str, Any]]:
    """Read and parse a JSON file.

    Args:
        path: Path to JSON file

    Returns:
        Parsed JSON data or None if file doesn't exist or is invalid
    """
    try:
        if path.exists():
            return json.loads(path.read_text())
    except (json.JSONDecodeError, IOError):
        pass
    return None


def read_file_content(path: Path) -> Optional[str]:
    """Read file content safely.

    Args:
        path: Path to file

    Returns:
        File content or None if file doesn't exist
    """
    try:
        if path.exists():
            return path.read_text(encoding="utf-8")
    except IOError:
        pass
    return None


def contains_keywords(content: str, keywords: list[str], case_sensitive: bool = False) -> bool:
    """Check if content contains any of the given keywords.

    Args:
        content: Text content to search
        keywords: List of keywords to search for
        case_sensitive: Whether to do case-sensitive matching

    Returns:
        True if any keyword is found
    """
    if not case_sensitive:
        content = content.lower()
        keywords = [k.lower() for k in keywords]

    for keyword in keywords:
        if keyword in content:
            return True
    return False


def extract_project_name(root: Path) -> Optional[str]:
    """Extract project name from various sources.

    Args:
        root: Project root directory

    Returns:
        Project name or None
    """
    # Try package.json
    package_json = root / "package.json"
    if package_json.exists():
        data = read_json_file(package_json)
        if data and "name" in data:
            return data["name"]

    # Try setup.py (basic parsing)
    setup_py = root / "setup.py"
    if setup_py.exists():
        content = read_file_content(setup_py)
        if content:
            match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)

    # Try pyproject.toml
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        content = read_file_content(pyproject)
        if content:
            match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)

    # Fall back to directory name
    return root.name


def extract_repository_url(root: Path) -> Optional[str]:
    """Extract repository URL from various sources.

    Args:
        root: Project root directory

    Returns:
        Repository URL or None
    """
    # Try package.json
    package_json = root / "package.json"
    if package_json.exists():
        data = read_json_file(package_json)
        if data:
            repo = data.get("repository")
            if isinstance(repo, str):
                return repo
            elif isinstance(repo, dict) and "url" in repo:
                return repo["url"]

    # Try .git/config
    git_config = root / ".git" / "config"
    if git_config.exists():
        content = read_file_content(git_config)
        if content:
            match = re.search(r'url\s*=\s*(.+)', content)
            if match:
                return match.group(1).strip()

    # Try README for GitHub links
    readme = find_file_by_name(root, "README.md")
    if readme:
        content = read_file_content(readme)
        if content:
            # Look for GitHub URLs
            match = re.search(
                r'https?://github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+', content
            )
            if match:
                return match.group(0)

    return None

