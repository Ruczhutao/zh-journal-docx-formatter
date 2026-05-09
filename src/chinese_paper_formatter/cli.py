"""Command line wrappers used by the Codex skill."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

from .docx_format import apply_docx_format, md_to_docx, save_report
from .format_spec import FormatSpec
from .templates import TemplateRegistry
from .validation import validate_config


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(prog="cpf")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list-templates")
    p_list.add_argument("--category", choices=TemplateRegistry.CATEGORIES)

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("spec")

    p_md = sub.add_parser("md-to-docx")
    p_md.add_argument("input")
    p_md.add_argument("output")
    _add_spec_args(p_md)
    p_md.add_argument("--report")

    p_apply = sub.add_parser("apply-docx")
    p_apply.add_argument("input")
    p_apply.add_argument("output")
    _add_spec_args(p_apply)
    p_apply.add_argument("--report")

    p_save = sub.add_parser("save-template")
    p_save.add_argument("spec")
    p_save.add_argument("--name")
    p_save.add_argument("--category", default="custom", choices=TemplateRegistry.CATEGORIES)

    args = parser.parse_args(argv)
    registry = TemplateRegistry(create=args.command == "save-template")

    if args.command == "list-templates":
        print(json.dumps(registry.list_templates(args.category), ensure_ascii=False, indent=2))
        return 0
    if args.command == "validate":
        import yaml

        data = yaml.safe_load(Path(args.spec).read_text(encoding="utf-8")) or {}
        result = validate_config(data)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        return 0 if result.ok else 1
    if args.command in {"md-to-docx", "apply-docx"}:
        spec = _load_spec(args, registry)
        if args.command == "md-to-docx":
            report = md_to_docx(Path(args.input), Path(args.output), spec)
        else:
            report = apply_docx_format(Path(args.input), Path(args.output), spec)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if args.report:
            save_report(report, Path(args.report))
        return 0
    if args.command == "save-template":
        import yaml

        data = yaml.safe_load(Path(args.spec).read_text(encoding="utf-8")) or {}
        spec = FormatSpec.from_dict(data)
        path = registry.save(spec, name=args.name, category=args.category)
        print(str(path))
        return 0
    return 1


def _add_spec_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--spec", help="Path to a FormatSpec YAML file")
    group.add_argument("--template", help="Template name from templates/{defaults,presets,journals,custom}")


def _load_spec(args, registry: TemplateRegistry) -> FormatSpec:
    if args.template:
        return registry.load(args.template)
    import yaml

    data = yaml.safe_load(Path(args.spec).read_text(encoding="utf-8")) or {}
    return FormatSpec.from_dict(data)


if __name__ == "__main__":
    raise SystemExit(main())
