---
name: chinese-journal-word-formatter
description: Use when formatting Chinese journal manuscripts for submission, including Markdown to Word, existing Word to formatted Word, extracting a reusable FormatSpec from pasted journal requirements, saving templates, or applying saved/custom templates.
---

# Chinese Journal Word Formatter

## Core Rule

Always reduce the request to a `FormatSpec` before formatting. A pasted journal requirement, a saved template, and an on-the-fly custom instruction are only different ways to produce the same YAML spec.

Do not overwrite the user's original document. Always write a new `.docx` and a processing report.

When a Chinese journal guide omits basic page/body formatting, use the repository default rule library without asking: `templates/defaults/中文期刊默认规则.yaml`. Its defaults are A4 page, no page number, default margins, body in 宋体小四 (12pt), Times New Roman for Latin text, justified alignment, 1.25 line spacing, first-line indent of 2 Chinese characters, no document grid alignment, no paragraph spacing unless the journal explicitly requires it, 黑体 not bold unless the guide says 加粗/加黑, and Latin text may break across lines. References also default to one size smaller than body text, first-line indent of 2 Chinese characters, and no hanging indent unless the user or journal style explicitly requires hanging indent.

## Workflow

1. Identify the input mode:
   - Markdown manuscript: use `scripts/md_to_docx.py`.
   - Existing Word manuscript: use `scripts/apply_docx_format.py`.
   - Pasted journal requirements: draft a `FormatSpec`, list only non-default `unresolved_items`, and ask the user to confirm missing or conflicting items before formatting.
   - Saved template: load it from `templates/defaults`, `templates/presets`, `templates/journals`, or `templates/custom`.
   - Journal template: store it under `templates/journals` using the journal's exact name as the filename. Do not translate, romanize, abbreviate, or slugify Chinese or English journal names.
2. Validate the spec:
   - Run `scripts/validate_spec.py <spec.yaml>`.
   - Errors block formatting.
   - `unresolved_items` must be shown to the user before final formatting or template saving.
   - Warnings are allowed; include them in the final report.
3. Apply formatting:
   - Existing Word defaults to template-overwrite behavior: preserve content, replace core styles with the template.
   - Markdown uses the light contract in `references/format-spec.md`.
4. Save reusable templates only after the user confirms unresolved items:
   - Run `scripts/save_template.py <spec.yaml> --category custom` for user templates.
   - Run with `--category journals` for confirmed journal templates. Use the exact journal name for `meta.journal` and `meta.name`.

## Template Learning Policy

During one formatting run, the default rule library is only the baseline for fields the user did not notice or the journal did not mention. If the user reviews an output and gives corrections while using a named journal template, treat those corrections as journal-specific template updates by default.

- Update `templates/journals/<期刊原名>.yaml` when the correction is about the current journal's output.
- Update `templates/defaults/中文期刊默认规则.yaml` only when the user explicitly says it should become a general default for most Chinese journals.
- Record fine-grained corrections in the journal template's structured fields whenever possible. If there is no first-class field yet, record the correction under `rules`.
- Do not rely on remembering the conversation for future runs. After a correction is accepted, the relevant YAML template must carry the rule.
- Keep the default library and journal templates consistent, but journal templates should be self-contained enough that `--template <期刊名>` directly reflects previously confirmed corrections.

## FormatSpec Guidance

Read `references/format-spec.md` when drafting or debugging templates.

First-version coverage:
- Core fields are structured: page, paragraph, headings, front matter, citations, references, figures/tables.
- Advanced Word controls are weakly validated: record them, apply what the scripts support, and report the rest.
- Reference handling is formatting-first. Do not promise full CSL/GB7714 semantic parsing or automatic reference reordering.

Reference formatting rule:
- Reference entries must align element-by-element with the selected journal template. Missing required elements should be added only when they can be inferred from the source; extra elements not allowed by the journal style should be removed.
- Punctuation must be normalized to the selected journal style.
- Repeated works by the same author should use `——` when the journal style uses an author-repeat dash.

## Commands

```bash
python3 scripts/validate_spec.py templates/presets/gb7714-in-text.yaml
python3 scripts/md_to_docx.py input.md output.docx --template gb7714-in-text --report output.report.json
python3 scripts/apply_docx_format.py input.docx output.docx --template gb7714-in-text --report output.report.json
python3 scripts/save_template.py draft-spec.yaml --name "期刊名原文" --category journals
```

## Quality Bar

Report what was applied, what was inferred, what remains unresolved, and which advanced Word rules were only recorded. If rendering tools are available, render and visually inspect the output document before delivery; otherwise call out that visual verification was not run.
