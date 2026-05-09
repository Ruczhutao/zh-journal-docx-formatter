"""Template registry for FormatSpec YAML files."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml

from .format_spec import FormatSpec
from .validation import ValidationResult, validate_config


class TemplateNotFoundError(FileNotFoundError):
    """Raised when a named template cannot be found."""


class TemplateRegistry:
    """Load, list, validate, and save FormatSpec YAML templates."""

    CATEGORIES = ("defaults", "presets", "journals", "custom")

    def __init__(self, templates_dir: Optional[os.PathLike] = None, create: bool = False):
        if templates_dir is None:
            templates_dir = Path(__file__).resolve().parents[2] / "templates"
        self.templates_dir = Path(templates_dir)
        if create:
            for category in self.CATEGORIES:
                (self.templates_dir / category).mkdir(parents=True, exist_ok=True)

    def list_templates(self, category: Optional[str] = None) -> List[Dict[str, str]]:
        categories = [category] if category else list(self.CATEGORIES)
        items: List[Dict[str, str]] = []
        for cat in categories:
            for path in sorted((self.templates_dir / cat).glob("*.yaml")):
                data = self._read_yaml(path)
                meta = data.get("meta", {}) if isinstance(data, dict) else {}
                items.append(
                    {
                        "name": str(meta.get("name", path.stem)),
                        "description": str(meta.get("description", "")),
                        "source": str(meta.get("source", cat)),
                        "category": cat,
                        "filename": path.name,
                        "path": str(path),
                    }
                )
        return items

    def load(self, name: str, category: Optional[str] = None) -> FormatSpec:
        path = self.find(name, category=category)
        data = self._read_yaml(path)
        return FormatSpec.from_dict(data)

    def load_with_validation(self, name: str, category: Optional[str] = None) -> Tuple[FormatSpec, ValidationResult]:
        path = self.find(name, category=category)
        data = self._read_yaml(path)
        return FormatSpec.from_dict(data), validate_config(data)

    def validate_file(self, path: os.PathLike) -> ValidationResult:
        return validate_config(self._read_yaml(Path(path)))

    def save(self, spec: FormatSpec, name: Optional[str] = None, category: str = "custom") -> Path:
        if category not in self.CATEGORIES:
            raise ValueError(f"unknown template category: {category}")
        target_dir = self.templates_dir / category
        target_dir.mkdir(parents=True, exist_ok=True)
        filename_base = name or (spec.meta.journal if category == "journals" and spec.meta.journal else spec.meta.name)
        filename = f"{_template_filename(filename_base)}.yaml"
        path = target_dir / filename
        with path.open("w", encoding="utf-8") as stream:
            yaml.safe_dump(spec.to_dict(), stream, allow_unicode=True, sort_keys=False)
        return path

    def find(self, name: str, category: Optional[str] = None) -> Path:
        categories = [category] if category else list(self.CATEGORIES)
        normalized = name.lower()
        exact_candidates: List[Path] = []
        fuzzy_candidates: List[Path] = []

        for cat in categories:
            directory = self.templates_dir / cat
            for path in sorted(directory.glob("*.yaml")):
                stem = path.stem.lower()
                data = self._read_yaml(path)
                meta_name = str((data.get("meta") or {}).get("name", "")).lower() if isinstance(data, dict) else ""
                if normalized in {stem, meta_name}:
                    exact_candidates.append(path)
                elif normalized in stem or (meta_name and normalized in meta_name):
                    fuzzy_candidates.append(path)

        if exact_candidates:
            return exact_candidates[0]
        if fuzzy_candidates:
            return fuzzy_candidates[0]
        raise TemplateNotFoundError(f"未找到模板: {name}")

    def _read_yaml(self, path: Path) -> Dict[str, Any]:
        with path.open("r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream) or {}
        if not isinstance(data, dict):
            raise ValueError(f"模板必须是 YAML mapping: {path}")
        return data


def _template_filename(value: str) -> str:
    """Preserve journal names in filenames while avoiding path separators."""

    filename = value.strip().replace("/", "／").replace("\\", "＼")
    filename = re.sub(r"\s+", " ", filename).strip(" .")
    return filename or "未命名模板"
