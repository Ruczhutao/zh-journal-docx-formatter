"""Small interactive helper for building a basic FormatSpec."""

from pathlib import Path
from typing import Any, Dict

import yaml

from chinese_paper_formatter.format_spec import FormatSpec
from chinese_paper_formatter.templates import TemplateRegistry


class TemplateWizard:
    """Interactive wizard for creating a minimal custom FormatSpec."""

    def __init__(self):
        self.registry = TemplateRegistry(create=True)

    def run(self) -> Dict[str, Any]:
        print("=== 中文期刊 FormatSpec 配置向导 ===")
        base_name = input("基础模板 [gb7714-in-text]: ").strip() or "gb7714-in-text"
        spec = self.registry.load(base_name)
        spec.meta.name = input(f"模板名称 [{spec.meta.name}]: ").strip() or spec.meta.name
        spec.meta.source = "custom"
        align = input(f"正文对齐 [{spec.paragraph.align}]: ").strip()
        if align:
            spec.paragraph.align = align
        indent = input(f"正文首行缩进 [{spec.paragraph.first_line_indent}]: ").strip()
        if indent:
            spec.paragraph.first_line_indent = indent
        hanging = input(f"参考文献悬挂缩进（默认 0pt，不用）[{spec.references.hanging_indent}]: ").strip()
        if hanging:
            spec.references.hanging_indent = hanging
        return spec.to_dict()

    def save(self, config: Dict[str, Any], filepath: str) -> None:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        Path(filepath).write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(f"配置已保存至: {filepath}")


def interactive_config() -> str:
    wizard = TemplateWizard()
    config = wizard.run()
    name = input("保存模板名称（不含扩展名）[custom]: ").strip() or "custom"
    filepath = Path("templates") / "custom" / f"{name}.yaml"
    wizard.save(config, str(filepath))
    return str(filepath)


if __name__ == "__main__":
    interactive_config()
