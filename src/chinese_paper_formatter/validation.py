"""Validation for FormatSpec configs."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Union

from .format_spec import FormatSpec


VALID_ALIGN = {"left", "center", "right", "justify"}
VALID_CITATION_STYLES = {"numbered", "circled", "author_year"}
VALID_CITATION_POSITIONS = {"in-text", "footnote", "endnote"}
VALID_NUMBERING = {"chinese", "chinese_paren", "arabic", "arabic_full_stop", "arabic_paren", "none"}
VALID_REF_SORT = {"appearance", "author", "none"}
UNIT_RE = re.compile(r"^-?\d+(\.\d+)?(pt|cm|mm|em)$")


@dataclass
class ValidationIssue:
    severity: str
    path: str
    message: str

    def to_dict(self) -> Dict[str, str]:
        return {"severity": self.severity, "path": self.path, "message": self.message}


@dataclass
class ValidationResult:
    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)
    unresolved_items: List[ValidationIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def extend(self, issues: Iterable[ValidationIssue]) -> None:
        for issue in issues:
            if issue.severity == "error":
                self.errors.append(issue)
            elif issue.severity == "warning":
                self.warnings.append(issue)
            elif issue.severity == "unresolved":
                self.unresolved_items.append(issue)
            else:
                self.warnings.append(issue)

    def to_dict(self) -> Dict[str, List[Dict[str, str]]]:
        return {
            "ok": self.ok,
            "errors": [issue.to_dict() for issue in self.errors],
            "warnings": [issue.to_dict() for issue in self.warnings],
            "unresolved_items": [issue.to_dict() for issue in self.unresolved_items],
        }


def validate_config(config: Dict[str, Any]) -> ValidationResult:
    """Validate raw YAML data and preserve missing-field evidence."""

    result = ValidationResult()
    if not isinstance(config, dict):
        result.errors.append(ValidationIssue("error", "$", "FormatSpec 必须是 YAML mapping"))
        return result

    for section in ["meta", "page", "paragraph", "headings", "citations", "references"]:
        if section not in config:
            result.errors.append(ValidationIssue("error", section, f"缺少必需部分: {section}"))

    meta = config.get("meta", {})
    if isinstance(meta, dict) and not meta.get("name"):
        result.errors.append(ValidationIssue("error", "meta.name", "模板名称是必需的"))

    paragraph = config.get("paragraph", {})
    if isinstance(paragraph, dict):
        _validate_paragraph_dict(result, paragraph, "paragraph")

    citations = config.get("citations", {})
    if isinstance(citations, dict):
        _require_unresolved(result, citations, "position", "citations.position", "引注位置缺失，需确认文中注/脚注/尾注")
        _check_choice(result, citations.get("style"), VALID_CITATION_STYLES, "citations.style")
        _check_choice(result, citations.get("position"), VALID_CITATION_POSITIONS, "citations.position")

    refs = config.get("references", {})
    if isinstance(refs, dict):
        _check_choice(result, refs.get("sort_by"), VALID_REF_SORT, "references.sort_by")
        if "entry" in refs and isinstance(refs["entry"], dict):
            _validate_paragraph_dict(result, refs["entry"], "references.entry")

    headings = config.get("headings", {})
    if isinstance(headings, dict):
        for level, spec in headings.items():
            if isinstance(spec, dict):
                path = f"headings.{level}"
                _validate_paragraph_dict(result, spec, path)
                _check_choice(result, spec.get("align"), VALID_ALIGN, f"{path}.align")
                _check_choice(result, spec.get("numbering"), VALID_NUMBERING, f"{path}.numbering")

    result.extend(_advanced_word_warnings(config.get("advanced_word") or {}))
    for item in config.get("unresolved_items") or []:
        if isinstance(item, dict):
            result.unresolved_items.append(
                ValidationIssue(
                    "unresolved",
                    str(item.get("path", "unresolved_items")),
                    str(item.get("message", item.get("question", "需要用户确认"))),
                )
            )
    return result


def validate_format_spec(spec: Union[FormatSpec, Dict[str, Any]]) -> ValidationResult:
    """Validate a normalized FormatSpec object or dict."""

    if isinstance(spec, FormatSpec):
        config = spec.to_dict()
    else:
        config = spec
    result = validate_config(config)
    if result.errors:
        return result

    normalized = FormatSpec.from_dict(config)
    _check_choice(result, normalized.paragraph.align, VALID_ALIGN, "paragraph.align")
    _check_choice(result, normalized.citations.style, VALID_CITATION_STYLES, "citations.style")
    _check_choice(result, normalized.citations.position, VALID_CITATION_POSITIONS, "citations.position")
    _check_choice(result, normalized.references.sort_by, VALID_REF_SORT, "references.sort_by")
    for level, heading in normalized.headings.items():
        _check_choice(result, heading.align, VALID_ALIGN, f"headings.{level}.align")
        _check_choice(result, heading.numbering, VALID_NUMBERING, f"headings.{level}.numbering")
    return result


def _require_unresolved(result: ValidationResult, data: Dict[str, Any], key: str, path: str, message: str) -> None:
    if key not in data or data.get(key) in ("", None):
        result.unresolved_items.append(ValidationIssue("unresolved", path, message))


def _check_choice(result: ValidationResult, value: Any, valid: set, path: str) -> None:
    if value in ("", None):
        return
    if value not in valid:
        result.errors.append(
            ValidationIssue("error", path, f"无效取值 {value!r}，应为: {', '.join(sorted(valid))}")
        )


def _validate_paragraph_dict(result: ValidationResult, data: Dict[str, Any], path: str) -> None:
    font = data.get("font")
    if isinstance(font, dict):
        if "family" in font and not font.get("family"):
            result.unresolved_items.append(ValidationIssue("unresolved", f"{path}.font.family", "字体缺失，需确认"))
        if "size" in font:
            _check_unit(result, font.get("size"), f"{path}.font.size")
    _check_choice(result, data.get("align"), VALID_ALIGN, f"{path}.align")
    for key in ["first_line_indent", "left_indent", "right_indent", "space_before", "space_after", "character_spacing"]:
        if key in data:
            _check_unit(result, data.get(key), f"{path}.{key}")


def _check_unit(result: ValidationResult, value: Any, path: str) -> None:
    if value in ("", None):
        return
    if not isinstance(value, str) or not UNIT_RE.match(value):
        result.warnings.append(
            ValidationIssue("warning", path, f"单位 {value!r} 未被严格识别，建议使用 pt/cm/mm/em")
        )


def _advanced_word_warnings(advanced: Dict[str, Any]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    weak_fields = {
        "east_asian_line_break",
        "latin_line_break",
        "use_document_grid",
        "character_spacing",
        "raw_ooxml_hints",
    }
    for key, value in advanced.items():
        if value in (None, "", {}, [], False):
            continue
        if key in weak_fields:
            issues.append(
                ValidationIssue(
                    "warning",
                    f"advanced_word.{key}",
                    "该高级 Word 规则会被记录并尽量应用；第一版不保证完全复刻 Word 行为",
                )
            )
    return issues
