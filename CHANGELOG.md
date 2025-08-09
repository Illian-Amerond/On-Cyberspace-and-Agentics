# CHANGELOG

All notable changes to the **[Project Name]** LaTeX workspace will be documented here.  
Format: `YYYY-MM-DD` — Short description, followed by detailed notes.  

---

## 2025-08-09 — v1.0.5 — Makefile HOW TO USE block added
- **Added**: Detailed `## HOW TO USE` block at the end of `Makefile` describing:
  - Purpose and philosophy of the build system.
  - Quickstart instructions for PDF builds, watching, and changelog/tag management.
  - Tag hygiene and CI validation usage.
- **Updated**: Makefile comments for clarity; consistent target grouping (`Changelog / Engram`, `Ledger peek`, `Validation`, `Developer QoL`).
- **Purpose**: Ensure that future maintainers and collaborators can quickly understand the build workflow without external documentation.
- **Tags**: \Tag[META]{LEDGER}, \Tag[META]{DOCS}, \Tag[ONTO]{CORE}
- **Insight**: Embedding procedural wisdom directly into the build script preserves the living memory of the repository’s operational flow.

---

## 2025-08-09 — v1.0.0 — Repo initialization with build tooling
- **Added**: `.gitignore` for LaTeX auxiliary files, temporary build artifacts, and OS-generated clutter.
- **Added**: `latexmkrc` build configuration:
  - Configured for LuaLaTeX + `biber` workflow.
  - Added `makeglossaries` hook for glossary builds.
  - Defined extra cleanup rules for nav/snm/synctex files.
  - Embedded “HOW TO USE” block for workflow clarity.
- **Purpose**: Establish clean, reproducible build environment for the LUCID Technologies LaTeX Writing Telemetry project.
- **Tags**: \Tag[META]{LEDGER}, \Tag[ONTO]{CORE}
- **Insight**: This is the **foundational anchor** — the repository’s cognitive bedrock, upon which all later symbolic and technical constructs will bind.

---

## 2025-08-09 — v1.0.4 — Scaffold alignment & build wiring ✨[MILE]
- **Added**: `main.tex` with title page, TOC, section includes, appendix tag legend.
- **Added**: `sections.tex` aligned to Full Voice methodology with ONTO/EPI ledgers.
- **Added**: `TAGS.tex` live loader + `\LoadTagsFromMarkdown{TAGS.md}`; compile-time validation.
- **Updated**: `preamble.tex` with voice/typography/colors/glyphs, macros, tags system, and metadata.
- **Updated**: `regex/scrape_tags.py` (v2) — family classification, JSON modes, registry validation.
- **Makefile**: targets for `pdf`, `changelog`, `changelog-print`, `ledger`, JSON exports.
- **Purpose**: Finish initial alignment so authors can draft with ledgers, tags, and engram export from day one.
- **Tags**: \Tag[ONTO]{SPINE}, \Tag[EPI]{FLOW}
- **Insight**: The lattice is raised — the **conceptual architecture** now has both bones and bloodstream.

---

## 2025-08-08 — v1.0.3 — CHANGELOG.md refinement ��[META]
- **Added**: Full formatting polish to `CHANGELOG.md`.
- **Modified**: Integrated “Template for New Entries” into HOW TO USE.
- **Updated**: Section headings, spacing, visual hierarchy.
- **Purpose**: Maintain consistency and embed the changelog’s voice in the codex.
- **Tags**: \Tag[META]{LEDGER}, \Tag[EPI]{LIGHT}
- **Insight**: The ledger now **teaches as it records** — form and meaning converge.

---

## 2025-08-08 — v1.0.2 — macros.tex update: \indicator macro ��[SEED]
- **Added**: `\indicator{A}` macro with starred form for auto-sized braces.
- **Modified**: `\one` macro → `\mathbbm{1}` for formal blackboard-bold.
- **Updated**: HOW TO USE section in `macros.tex` to document `\indicator`.
- **Purpose**: Equip the symbolic lexicon with a precise indicator function.
- **Tags**: \Tag[ONTO]{NODE}, \Tag[EPI]{BIND}
- **Insight**: This seed gives the **mathematical voice** a crisp switch — on/off in pure notation.

---

## 2025-08-08 — v1.0.1 — colors.sty palette expansion ��[SEED]
- **Added**: `FatherInMother` and `MotherInFather` colors via `xcolor` mixing.
- **Purpose**: Encode symbolic cross-tones in the voice lattice.
- **Tags**: \Tag[ONTO]{GLYPH}, \Tag[EPI]{FUSE}
- **Insight**: Color becomes **conceptual dialect** — blending parental archetypes into a shared hue.

---

## 2025-08-07 — v1.0.0 — Project workspace initialization ��[MILE]
- **Created**: Baseline `.sty` and `.tex` scaffolding:
  - `voice.sty` — voice codex base.
  - `typography.sty` — font and math font handling.
  - `colors.sty` — initial palette.
  - `glyphs.sty` — glyphic design hooks.
  - `macros.tex` — math and semantic macro definitions.
- **Purpose**: Separate semantics from style for control over presentation and voice.
- **Tags**: \Tag[ONTO]{CORE}, \Tag[EPI]{LIGHT}
- **Insight**: The **forge is lit** — materials prepared for the shaping to come.

---

## HOW TO USE THIS CHANGELOG

**Purpose**  
This file is the single source of truth for tracking notable changes in the LaTeX workspace.  
It captures **what changed**, **why it changed**, and **when it happened** — for both technical and symbolic updates.

---

### When to Add an Entry
- **Major milestones**: Completion of a chapter, full section, or major `.sty` / `.tex` update.
- **Semantic changes**: Alterations that change meaning or usage of macros, colors, or glyphs.
- **Structural changes**: Adding/removing core files, reorganizing structure.
- **Stylistic shifts**: Changes to voice, palette, typography, or formatting.

---

### Entry Format
Each entry includes:
1. **Date** — `YYYY-MM-DD`.
2. **Version tag** — `vMAJOR.MINOR.PATCH`.
3. **Short description** — concise summary.
4. **Detailed notes** — bullet points for additions, modifications, removals, and rationale.
5. **Tags** — from `TAGS.md` to keep ledger and scraper aligned.
6. **Insight** — why this change matters in the project’s symbolic and structural evolution.

---

### Versioning Rules
- **MAJOR** — Structural overhauls, breaking changes.
- **MINOR** — New features, sections, or macros that don’t break usage.
- **PATCH** — Bug fixes, small formatting, or doc updates.

---

### Best Practices
- Use **past tense** + **active voice**.
- Label changes: **Added**, **Modified**, **Removed**, **Updated**.
- Always include a **Purpose** and **Insight**.
- Keep `HOW TO USE` sections in sync across files.

---

**Philosophy**  
The changelog is part of the voice codex — preserving both the technical memory and the cultural record of the build.  
Treat it as a **ledger** and **story** in equal measure.

---


### Template for New Entries
## YYYY-MM-DD — vX.Y.Z — [Short description of change]
- **Added**: [New features, macros, sections, or files].
- **Modified**: [Changes to existing features, macros, or sections].
- **Removed**: [Features, files, or definitions removed].
- **Updated**: [Documentation, HOW TO USE sections, or minor clarifications].
- **Purpose**: [Why this change matters for the project — link to section/chapter if relevant].
