# Journal DOCX Formatter

[中文说明](README.md)

Turn journal submission guidelines into reusable, continuously improving Word formatting templates. 📄

Journal formatting rules are often scattered across submission pages, PDF attachments, and style notes: fonts, spacing, heading numbering, footnotes, references, document grids, anonymization requirements, and many small exceptions. The workflow works for both Chinese and English-language journals.

You do not need to build a perfect default template first. The simplest workflow is to find the journal you plan to submit to, send its submission guidelines to an agent, and let the agent turn those requirements into a journal-specific template. Missing or unclear parts can be filled by defaults or surfaced for confirmation.

The default template is optional. You can start directly from a journal submission template, format one manuscript, review the output, and tell the agent what needs to change. Those corrections are written back into the corresponding journal template, so the next run uses the improved rules automatically. 🧠

## Typical Workflow

1. Find the journal submission requirements, whether they are on a web page, in a PDF, in a Word attachment, or in plain text.
2. Send those requirements to an agent.
3. The agent turns them into a journal-specific formatting template and flags anything missing, conflicting, or not fully automatable yet.
4. Provide a Markdown manuscript or an existing Word document.
5. The tool generates a new `.docx` without overwriting the source file, along with a processing report.
6. After reviewing the output, tell the agent what needs to change; those corrections are written back into the journal template.

## What It Helps With

- Avoid manually remembering Word formatting rules for every journal.
- Avoid resetting body text, headings, abstracts, keywords, footnotes, and references from scratch.
- Surface unclear parts of submission guidelines for confirmation.
- Let formatting corrections accumulate automatically after each run.
- Preserve the original manuscript and generate a new submission-ready Word file.

## Supported Inputs

- Markdown manuscripts.
- Existing `.docx` manuscripts.
- Journal submission guidelines from web pages, PDF files, Word attachments, or plain text.
- Saved public journal templates or local custom templates.

## Template Learning

Journal templates keep absorbing your corrections.

For example, after formatting a manuscript with a journal template, you can say:

```text
Do not use hanging indents for references; use a two-character first-line indent by default.
```

That correction is written back into the corresponding template. The next time the agent formats for the same journal, it uses the updated rule directly instead of relying on chat history.

Only update the default template when a rule should apply across journals in general.

## Template Directories

```text
templates/defaults/   # default rules
templates/presets/    # reusable presets
templates/journals/   # confirmed public journal templates
templates/custom/     # local custom templates
```

Journal template filenames should preserve the journal's original name. Do not translate, romanize, or abbreviate journal names.
