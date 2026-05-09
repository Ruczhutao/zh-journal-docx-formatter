from pathlib import Path

import yaml

from chinese_paper_formatter.format_spec import FormatSpec
from chinese_paper_formatter.templates import TemplateRegistry
from chinese_paper_formatter.validation import validate_config


ROOT = Path(__file__).resolve().parents[1]


def test_preset_template_validates_without_errors_or_unresolved_items():
    registry = TemplateRegistry(ROOT / "templates")
    spec, result = registry.load_with_validation("gb7714-in-text")

    assert spec.meta.name == "GB/T 7714 文中注"
    assert result.ok
    assert result.unresolved_items == []


def test_missing_non_default_fields_become_unresolved_items():
    data = yaml.safe_load((ROOT / "templates/presets/gb7714-in-text.yaml").read_text(encoding="utf-8"))
    del data["paragraph"]["align"]
    del data["paragraph"]["font"]["family"]
    del data["paragraph"]["font"]["size"]
    del data["paragraph"]["line_height"]
    del data["citations"]["position"]

    result = validate_config(data)
    paths = {item.path for item in result.unresolved_items}

    assert result.ok
    assert "paragraph.align" not in paths
    assert "paragraph.font.family" not in paths
    assert "paragraph.font.size" not in paths
    assert "paragraph.line_height" not in paths
    assert "references.hanging_indent" not in paths
    assert "citations.position" in paths


def test_advanced_word_fields_are_warnings_not_errors():
    data = yaml.safe_load((ROOT / "templates/presets/gb7714-in-text.yaml").read_text(encoding="utf-8"))
    data["advanced_word"]["east_asian_line_break"] = True
    data["advanced_word"]["character_spacing"] = "0.5pt"

    result = validate_config(data)
    warning_paths = {item.path for item in result.warnings}

    assert result.ok
    assert "advanced_word.east_asian_line_break" in warning_paths
    assert "advanced_word.character_spacing" in warning_paths
    assert "advanced_word.use_document_grid" not in warning_paths


def test_default_spacing_only_applies_to_title_like_blocks():
    registry = TemplateRegistry(ROOT / "templates")
    spec = registry.load("gb7714-in-text")

    assert spec.paragraph.space_before is None
    assert spec.paragraph.space_after is None
    assert spec.front_matter.abstract.space_before is None
    assert spec.front_matter.abstract.space_after is None
    assert spec.references.entry.space_before is None
    assert spec.references.entry.space_after is None
    assert spec.figures_tables.figure_caption.space_before is None
    assert spec.figures_tables.figure_caption.space_after is None
    assert spec.headings[1].space_after is not None
    assert spec.references.title.space_after is not None


def test_format_spec_round_trips_headings_as_string_keys():
    registry = TemplateRegistry(ROOT / "templates")
    spec = registry.load("circled-in-text")
    data = spec.to_dict()

    assert "1" in data["headings"]
    assert FormatSpec.from_dict(data).headings[1].numbering == "chinese"
