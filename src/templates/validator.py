"""Compatibility wrapper around FormatSpec validation."""

from typing import Dict, List

from chinese_paper_formatter.validation import ValidationResult, validate_config


class ValidationError(Exception):
    """Template validation error."""


class TemplateValidator:
    """Validate FormatSpec configuration."""

    def validate_result(self, config: Dict) -> ValidationResult:
        return validate_config(config)

    def validate(self, config: Dict) -> List[str]:
        result = validate_config(config)
        messages = [issue.message for issue in result.errors]
        messages.extend(issue.message for issue in result.unresolved_items)
        return messages

    def is_valid(self, config: Dict) -> bool:
        return validate_config(config).ok


def validate_template(config: Dict) -> List[str]:
    return TemplateValidator().validate(config)
