"""Compatibility wrapper around the FormatSpec template registry."""

from typing import Dict, List, Optional

from chinese_paper_formatter.templates import TemplateNotFoundError, TemplateRegistry


class TemplateLoader:
    """Load and manage formatting templates."""

    def __init__(self, templates_dir: Optional[str] = None):
        self.registry = TemplateRegistry(templates_dir=templates_dir)

    def list_presets(self) -> List[Dict[str, str]]:
        return self.registry.list_templates("presets")

    def list_journals(self) -> List[Dict[str, str]]:
        return self.registry.list_templates("journals")

    def list_custom(self) -> List[Dict[str, str]]:
        return self.registry.list_templates("custom")

    def get_all_templates(self) -> List[Dict[str, str]]:
        return self.registry.list_templates()

    def load(self, name: str):
        try:
            return self.registry.load(name).to_dict()
        except TemplateNotFoundError:
            return None

    def print_available(self) -> None:
        print("=== 可用模板 ===")
        for item in self.get_all_templates():
            print(f"  - {item['name']} ({item['category']})")


if __name__ == "__main__":
    TemplateLoader().print_available()
