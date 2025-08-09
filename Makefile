# Makefile — project root
% ------------------------------------------------------------
% \begin{SectionHeaderLedger}
\Tag[META]{LEDGER} 2025-08-09 v1.0.5 — Embedded HOW TO USE block into Makefile.
\Tag[META]{DOCS}   2025-08-09 v1.0.5 — Build instructions and philosophy added inline.
\Tag[ONTO]{CORE}   2025-08-09 v1.0.5 — Consolidated Makefile as central build orchestrator.
% \end{SectionHeaderLedger}
% ------------------------------------------------------------
SHELL := /bin/bash
# ------------------------------------------------------------
# HOW TO USE THIS MAKEFILE
# ------------------------------------------------------------
# Purpose:
#   This Makefile orchestrates building, cleaning, and logging
#   for the LUCID Technologies LaTeX Writing Telemetry workspace.
#   It is both a tool and a teaching artifact—showing the
#   mechanics of a clean, tagged build process.
#
# Common Targets:
#   make pdf             # Compile 'main.tex' to PDF (LuaLaTeX + biber)
#   make changelog       # Append all detected \Tag entries to CHANGELOG.md
#   make changelog-print # Preview \Tag entries without writing to CHANGELOG.md
#   make changelog-onto  # Show ONTO-layer \Tag entries only
#   make changelog-epi   # Show EPI-layer \Tag entries only
#   make ledger          # Print header/footer ledgers from all sections
#   make json            # Export raw tag data to engram.json
#   make json-grouped    # Export tag data grouped by tag type
#   make clean           # Remove all build artifacts
#
# Notes:
#   • Place section `.tex` files in the 'sections' directory.
#   • Tags are scraped from SectionHeaderLedger / SectionFooterLedger blocks.
#   • TAGS.md is the canonical tag registry—scraper validates against it.
#   • Use the changelog targets after each significant change to
#     preserve a complete, tagged build history.
#
# Philosophy:
#   This file is not just a build script—it is a ledger of process.
#   Every command embodies the principle: build with intention,
#   document with care, and leave a trail the next builder can follow.
# ------------------------------------------------------------

PYTHON := python3
SECTIONS_DIR := sections
CHANGELOG := CHANGELOG.md
SCRAPER := regex/scrape_tags.py

# respect latexmkrc, but make lualatex explicit as a fallback
LATEXMK := latexmk -lualatex -shell-escape

.PHONY: all pdf clean help changelog changelog-print changelog-onto changelog-epi \
        json json-grouped ledger validate tags-check watch

# default target
all: pdf

# compile (uses latexmkrc if present)
pdf:
	$(LATEXMK) main.tex

# ----- Changelog / Engram -----
changelog:
	@echo "[info] scanning $(SECTIONS_DIR) for \\Tag entries..."
	@$(PYTHON) $(SCRAPER) --root $(SECTIONS_DIR) --outfile $(CHANGELOG) --mode append --tags-reg TAGS.md

changelog-onto:
	@$(PYTHON) $(SCRAPER) --root $(SECTIONS_DIR) --mode print --layer ONTO --tags-reg TAGS.md

changelog-epi:
	@$(PYTHON) $(SCRAPER) --root $(SECTIONS_DIR) --mode print --layer EPI --tags-reg TAGS.md

changelog-print:
	@$(PYTHON) $(SCRAPER) --root $(SECTIONS_DIR) --mode print --tags-reg TAGS.md

json:
	@$(PYTHON) $(SCRAPER) --root $(SECTIONS_DIR) --json raw --tags-reg TAGS.md > engram.json

json-grouped:
	@$(PYTHON) $(SCRAPER) --root $(SECTIONS_DIR) --json grouped --group-by tag --tags-reg TAGS.md > engram_by_tag.json

# ----- Ledger peek (recursive; handles spaces) -----
ledger:
	@echo "[info] printing SectionHeaderLedger / SectionFooterLedger blocks from $(SECTIONS_DIR)"
	@find "$(SECTIONS_DIR)" -type f -name '*.tex' | while read -r f; do \
	  echo "------------------------------------------------------------"; \
	  echo "$$f — Header Ledger"; \
	  awk '/\\begin{SectionHeaderLedger}/{flag=1;print;next} /\\end{SectionHeaderLedger}/{print;flag=0} flag' "$$f" || true; \
	  echo; \
	  echo "$$f — Footer Ledger"; \
	  awk '/\\begin{SectionFooterLedger}/{flag=1;print;next} /\\end{SectionFooterLedger}/{print;flag=0} flag' "$$f" || true; \
	  echo; \
	done

# ----- Validation for CI (fail on unknown tags) -----
validate: tags-check pdf

tags-check:
	@echo "[info] validating tags against TAGS.md…"
	@set -o pipefail; \
	{ $(PYTHON) $(SCRAPER) --root $(SECTIONS_DIR) --mode print --tags-reg TAGS.md 2>validate.log || true; } ; \
	if grep -q "unknown tags" validate.log; then \
	  echo ""; \
	  echo "[ERROR] Unknown tags found. See validate.log"; \
	  sed -n '1,120p' validate.log; \
	  exit 1; \
	else \
	  echo "[ok] tag validation passed"; \
	  rm -f validate.log; \
	fi

# ----- Developer QoL -----
watch:
	$(LATEXMK) -pvc main.tex

clean:
	latexmk -C
	rm -f *.bbl *.run.xml *.synctex.gz

help:
	@echo "make pdf              # compile to PDF"
	@echo "make watch            # auto-recompile on change"
	@echo "make changelog        # append tag entries to $(CHANGELOG)"
	@echo "make changelog-print  # preview tag entries"
	@echo "make json             # export engram.json"
	@echo "make ledger           # view header/footer ledgers"
	@echo "make validate         # CI-friendly: fail on unknown tags"
	@echo "make clean            # remove build artifacts"

