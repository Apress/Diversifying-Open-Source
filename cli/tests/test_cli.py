"""Basic tests for CLI functionality."""

import tempfile
from pathlib import Path

import pytest

from diversity_standard.config import ProjectConfig
from diversity_standard.inspector import ProjectInspector


def test_config_auto_detect():
    """Test configuration auto-detection."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        
        # Create a simple package.json
        package_json = project_root / "package.json"
        package_json.write_text('{"name": "test-project", "description": "A test project"}')
        
        config = ProjectConfig(project_root)
        config.auto_detect()
        
        assert config.get("project.name") == "test-project"
        assert config.get("project.description") == "A test project"


def test_inspector_find_documents():
    """Test document inspection."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        
        # Create a CONTRIBUTING.md file
        contributing = project_root / "CONTRIBUTING.md"
        contributing.write_text("# Contributing\n\nHow to contribute to this project.")
        
        inspector = ProjectInspector()
        result = inspector.inspect(project_root)
        
        # Should find CONTRIBUTING.md
        found_names = [doc.blueprint_name for doc in result.found_documents]
        assert "CONTRIBUTING.md" in found_names


def test_inspector_missing_documents():
    """Test detection of missing documents."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        
        inspector = ProjectInspector()
        result = inspector.inspect(project_root)
        
        # Should report missing documents
        assert len(result.missing_documents) > 0


def test_config_get_set():
    """Test configuration get/set methods."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        config = ProjectConfig(project_root)
        
        config.set("project.name", "Test Project")
        assert config.get("project.name") == "Test Project"
        
        assert config.get("project.nonexistent", "default") == "default"

