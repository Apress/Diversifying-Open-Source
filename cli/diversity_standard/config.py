"""Configuration management for the diversity standard CLI."""

import json
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from diversity_standard.utils import (
    extract_project_name,
    extract_repository_url,
    read_file_content,
    read_json_file,
)


class ProjectConfig:
    """Manages project configuration for document generation."""

    def __init__(self, project_root: Path):
        """Initialize configuration.

        Args:
            project_root: Root directory of the target project
        """
        self.project_root = project_root
        self.config: Dict[str, Any] = {}

    def load_from_file(self, config_path: Optional[Path] = None) -> bool:
        """Load configuration from YAML file.

        Args:
            config_path: Path to config file. If None, searches for
                        .diversity-standard.yml or .diversity-standard.yaml

        Returns:
            True if config file was found and loaded
        """
        if config_path is None:
            config_path = self.project_root / ".diversity-standard.yml"
            if not config_path.exists():
                config_path = self.project_root / ".diversity-standard.yaml"

        if config_path and config_path.exists():
            try:
                content = read_file_content(config_path)
                if content:
                    self.config = yaml.safe_load(content) or {}
                    return True
            except Exception:
                pass
        return False

    def auto_detect(self) -> None:
        """Auto-detect project information from existing files."""
        # Project name
        if "project" not in self.config:
            self.config["project"] = {}
        if "name" not in self.config["project"]:
            name = extract_project_name(self.project_root)
            if name:
                self.config["project"]["name"] = name

        # Repository
        if "repository" not in self.config["project"]:
            repo = extract_repository_url(self.project_root)
            if repo:
                self.config["project"]["repository"] = repo

        # License
        if "license" not in self.config:
            self.config["license"] = {}
        if "type" not in self.config["license"]:
            license_type = self._detect_license()
            if license_type:
                self.config["license"]["type"] = license_type

        # Maintainers
        if "maintainers" not in self.config:
            self.config["maintainers"] = self._detect_maintainers()

        # Description
        if "description" not in self.config["project"]:
            desc = self._detect_description()
            if desc:
                self.config["project"]["description"] = desc

    def _detect_license(self) -> Optional[str]:
        """Detect license type from project files."""
        # Check LICENSE file
        license_file = self.project_root / "LICENSE"
        if not license_file.exists():
            license_file = self.project_root / "LICENSE.txt"
        if not license_file.exists():
            license_file = self.project_root / "LICENSE.md"

        if license_file.exists():
            content = read_file_content(license_file)
            if content:
                content_upper = content.upper()
                if "GNU GENERAL PUBLIC LICENSE" in content_upper or "GPL" in content_upper:
                    if "VERSION 3" in content_upper or "v3" in content_upper:
                        return "GPL-3.0"
                    elif "VERSION 2" in content_upper or "v2" in content_upper:
                        return "GPL-2.0"
                elif "MIT" in content_upper:
                    return "MIT"
                elif "APACHE" in content_upper:
                    if "2.0" in content_upper:
                        return "Apache-2.0"
                elif "BSD" in content_upper:
                    return "BSD"

        # Check package.json
        package_json = self.project_root / "package.json"
        if package_json.exists():
            data = read_json_file(package_json)
            if data and "license" in data:
                return str(data["license"])

        # Check setup.py
        setup_py = self.project_root / "setup.py"
        if setup_py.exists():
            content = read_file_content(setup_py)
            if content:
                match = __import__("re").search(
                    r'license\s*=\s*["\']([^"\']+)["\']', content
                )
                if match:
                    return match.group(1)

        return None

    def _detect_maintainers(self) -> list[Dict[str, str]]:
        """Detect maintainers from project files."""
        maintainers = []

        # Check package.json
        package_json = self.project_root / "package.json"
        if package_json.exists():
            data = read_json_file(package_json)
            if data:
                # Check author field
                author = data.get("author")
                if isinstance(author, str):
                    maintainers.append({"name": author})
                elif isinstance(author, dict):
                    maintainers.append(author)

                # Check maintainers field
                if "maintainers" in data:
                    if isinstance(data["maintainers"], list):
                        maintainers.extend(data["maintainers"])

        # Check MAINTAINERS.md
        maintainers_file = self.project_root / "MAINTAINERS.md"
        if not maintainers_file.exists():
            maintainers_file = self.project_root / "Long-Term" / "MAINTAINERS.md"
        if not maintainers_file.exists():
            maintainers_file = self.project_root / "docs" / "MAINTAINERS.md"

        if maintainers_file.exists():
            content = read_file_content(maintainers_file)
            if content:
                # Simple parsing - look for markdown table or list
                lines = content.split("\n")
                for line in lines:
                    if "|" in line and "Name" in line:
                        # Table format - skip header
                        continue
                    if "|" in line:
                        parts = [p.strip() for p in line.split("|")]
                        if len(parts) >= 2:
                            maintainers.append({"name": parts[1]})

        return maintainers

    def _detect_description(self) -> Optional[str]:
        """Detect project description from README."""
        readme = self.project_root / "README.md"
        if readme.exists():
            content = read_file_content(readme)
            if content:
                # Get first paragraph (non-empty lines before first heading)
                lines = content.split("\n")
                desc_lines = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        if desc_lines:
                            break
                        continue
                    if line.startswith("#"):
                        break
                    desc_lines.append(line)
                if desc_lines:
                    return " ".join(desc_lines[:3])  # First few lines

        # Check package.json
        package_json = self.project_root / "package.json"
        if package_json.exists():
            data = read_json_file(package_json)
            if data and "description" in data:
                return data["description"]

        return None

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.

        Args:
            key: Configuration key (e.g., "project.name")
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation.

        Args:
            key: Configuration key (e.g., "project.name")
            value: Value to set
        """
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    def save(self, config_path: Optional[Path] = None) -> None:
        """Save configuration to YAML file.

        Args:
            config_path: Path to save config. If None, uses
                        .diversity-standard.yml in project root
        """
        if config_path is None:
            config_path = self.project_root / ".diversity-standard.yml"

        with open(config_path, "w") as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)

