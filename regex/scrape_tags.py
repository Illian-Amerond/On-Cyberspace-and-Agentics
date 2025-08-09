#!/usr/bin/env python3
"""
Scrape \Tag[...] {...} ledger lines from .tex sections and emit
CHANGELOG-ready markdown and/or Engram-ready JSON.

New features:
- Validates tags against a registry (built-in or --tags-reg TAGS.md).
- Adds 'family' classification (Structural, Process, Symbolic, Meta, Epiphany).
- JSON export: --json raw | --json grouped (with --group-by layer|tag|section).
- Recognizes Epiphany Matrix tags: ARC_CLIMAX, GATE_OPEN, GATE_CLOSE,
  CORE_REVEAL, SPIRAL_TURN, FORGE_STRIKE.
"""

import argparse, pathlib, re, sys, json
from collections import defaultdict

# ----------- Tag parsing -----------
TAG_RE = re.compile(
    r"""
    \\Tag
    (?:\[(?P<layer>[A-Za-z]+)\])?          # optional [ONTO] or [EPI]
    \{(?P<tag>[A-Za-z0-9_~∿\-]+)\}         # tag name
    \s+(?P<date>\d{4}-\d{2}-\d{2})         # YYYY-MM-DD
    \s+v(?P<ver>\d+\.\d+\.\d+)             # vX.Y.Z
    \s+—\s+(?P<narr>.+)                    # narrative note
    """, re.VERBOSE
)

HDR_RE = re.compile(r"""\\begin\{SectionHeaderLedger\}\{(?P<title>.+?)\}""")
FTR_RE = re.compile(r"""\\begin\{SectionFooterLedger\}""")
END_RE = re.compile(r"""\\end\{Section(?:Header|Footer)Ledger\}""")
SECTION_RE = re.compile(r"""\\Section(?:\[[^\]]*\])?\{[^}]*\}\{[^}]*\}\{(?P<title>[^}]+)\}""")

# ----------- Built-in registry (fallback) -----------
# Families
STRUCTURAL = "Structural"
PROCESS    = "Process"
SYMBOLIC   = "Symbolic"
META       = "Meta"
EPIPHANY   = "Epiphany"

BUILTIN_REGISTRY = {
    # 1) Structural & Framework
    "GLYPH": STRUCTURAL, "NODE": STRUCTURAL, "ARC": STRUCTURAL, "LATTICE": STRUCTURAL,
    "CORE": STRUCTURAL, "GATE": STRUCTURAL, "BOND": STRUCTURAL, "SEED": STRUCTURAL,
    "SPINE": STRUCTURAL, "KEY": STRUCTURAL,
    # 2) Process & Development
    "DRIFT": PROCESS, "ANCHOR": PROCESS, "FUSE": PROCESS, "REFRACT": PROCESS,
    "SPIRAL": PROCESS, "TEMPER": PROCESS, "CAST": PROCESS, "WARD": PROCESS,
    "TRACE": PROCESS, "FLOW": PROCESS, "BIND": PROCESS,
    # 3) Symbolic & Philosophical
    "LIGHT": SYMBOLIC, "SHDW": SYMBOLIC, "MOTHER": SYMBOLIC, "FATHER": SYMBOLIC,
    "AIR": SYMBOLIC, "FIRE": SYMBOLIC, "WATER": SYMBOLIC, "EARTH": SYMBOLIC,
    "GNOME": SYMBOLIC, "OPAL": SYMBOLIC, "COMPASS": SYMBOLIC, "LAMP": SYMBOLIC, "FORGE": SYMBOLIC,
    # 4) Meta & Operational
    "META": META, "ENGRAM": META, "LEDGER": META, "TEST": META, "PROOF": META,
    "CIPHER": META, "MAP": META, "GLOSS": META, "ARCHIVE": META, "ITER": META,
    # Epiphany Matrix (Appendix A)
    "ARC_CLIMAX": EPIPHANY, "GATE_OPEN": EPIPHANY, "GATE_CLOSE": EPIPHANY,
    "CORE_REVEAL": EPIPHANY, "SPIRAL_TURN": EPIPHANY, "FORGE_STRIKE": EPIPHANY,
}

def load_registry_from_md(path: pathlib.Path):
    """
    Best-effort TAGS.md parser:
    - Collects UPPERCASE tokens at start of table rows or description bullets.
    - Also captures Epiphany Matrix items like ARC_CLIMAX.
    Unknowns default to None family; caller will fall back to BUILTIN_REGISTRY.
    """
    tag_to_family = {}
    current_family = None
    family_map = {
        "Structural": STRUCTURAL, "Framework": STRUCTURAL,
        "Process": PROCESS, "Development": PROCESS,
        "Symbolic": SYMBOLIC, "Philosophical": SYMBOLIC,
        "Meta": META, "Operational": META,
        "Seeded Epiphany Matrix": EPIPHANY, "Epiphany": EPIPHANY
    }
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        sys.stderr.write(f"[warn] could not read TAGS registry {path}: {e}\n")
        return {}

    # Roughly infer which family section we're in from headings
    for line in text.splitlines():
        h = line.strip()
        if h.startswith("## "):  # family header
            for key, fam in family_map.items():
                if key in h:
                    current_family = fam
                    break
            continue

        # Table-style row: | TAG | ...
        m_tbl = re.match(r"^\|\s*([A-Z][A-Z0-9_]+)\s*\|", h)
        if m_tbl and current_family:
            tag = m_tbl.group(1).upper()
            tag_to_family[tag] = current_family
            continue

        # Description-style bullet: \item[TAG]
        m_desc = re.search(r"\[(?P<tag>[A-Z][A-Z0-9_]+)\]", h)
        if m_desc and current_family:
            tag_to_family[m_desc.group("tag").upper()] = current_family
            continue

    return tag_to_family

def get_registry(args):
    reg = dict(BUILTIN_REGISTRY)
    if args.tags_reg:
        md_map = load_registry_from_md(pathlib.Path(args.tags_reg))
        # overlay: prefer MD file entries
        reg.update(md_map)
    return reg

# ----------- Scrape functions -----------
def find_files(root):
    p = pathlib.Path(root)
    if p.is_dir():
        return sorted([x for x in p.rglob("*.tex") if not x.name.startswith(".")])
    elif p.suffix == ".tex":
        return [p]
    return []

def scrape_file(path: pathlib.Path):
    entries = []
    section_title = None
    in_ledger = False
    ledger_title = None

    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        sys.stderr.write(f"[warn] could not read {path}: {e}\n")
        return entries

    msec = SECTION_RE.search(text)
    if msec:
        section_title = msec.group("title")

    for line in text.splitlines():
        if not in_ledger:
            mh = HDR_RE.search(line)
            if mh:
                in_ledger = True
                ledger_title = mh.group("title")
                continue
            if FTR_RE.search(line):
                in_ledger = True
                ledger_title = section_title or "(unknown section)"
                continue
        else:
            if END_RE.search(line):
                in_ledger = False
                ledger_title = None
                continue

        mt = TAG_RE.search(line)
        if mt:
            layer = (mt.group("layer") or "").upper()
            tag   = mt.group("tag").upper()
            date  = mt.group("date")
            ver   = mt.group("ver")
            narr  = mt.group("narr").strip()
            entries.append({
                "file": str(path),
                "section": ledger_title or section_title or "(unknown section)",
                "layer": layer,   # ONTO / EPI / ""
                "tag": tag,       # e.g., SEED, GLYPH, FLOW, ARC_CLIMAX
                "date": date,
                "ver": ver,
                "note": narr
            })
    return entries

# ----------- Formatting -----------
def format_markdown(entries):
    if not entries:
        return "[info] no matching tags found."
    entries.sort(key=lambda e: (e["date"], e["ver"]), reverse=True)
    groups = defaultdict(list)
    for e in entries:
        groups[(e["date"], e["ver"])].append(e)

    chunks = []
    for (date, ver), items in sorted(groups.items(), reverse=True):
        title = items[0]["section"]
        if any(it["section"] != title for it in items):
            header = f"## {date} — v{ver} — Section updates"
        else:
            header = f"## {date} — v{ver} — Section updates: {title}"
        chunks.append(header)
        for it in items:
            layer_tag = f"[{it['layer']}:{it['tag']}]" if it["layer"] else f"[{it['tag']}]"
            chunks.append(f"- **{layer_tag}** ({it['section']}) — {it['note']}")
        chunks.append("\n---\n")
    return "\n".join(chunks).strip()

def enrich_with_family(entries, registry):
    out = []
    for e in entries:
        fam = registry.get(e["tag"])
        e2 = dict(e)
        e2["family"] = fam if fam else "Unknown"
        out.append(e2)
    return out

def json_grouped(entries, by="tag"):
    grouped = defaultdict(list)
    for e in entries:
        key = e.get(by, "")
        grouped[key].append(e)
    return grouped

# ----------- CLI -----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="sections", help="Root .tex folder or single .tex file")
    ap.add_argument("--outfile", default="-", help="CHANGELOG path or '-' for stdout")
    ap.add_argument("--mode", choices=["print","append"], default="print",
                    help="Markdown output mode for CHANGELOG")
    ap.add_argument("--layer", default=None, help="Filter by layer: ONTO or EPI")
    ap.add_argument("--tag", default=None, help="Filter by tag name")
    ap.add_argument("--tags-reg", default=None, help="Path to TAGS.md to validate/classify tags")
    ap.add_argument("--json", choices=["", "raw", "grouped"], default="",
                    help="Emit JSON to stdout instead of markdown")
    ap.add_argument("--group-by", choices=["tag","layer","section"], default="tag",
                    help="Grouping key for --json grouped")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = find_files(args.root)
    all_entries = []
    for f in files:
        all_entries.extend(scrape_file(f))

    # filters
    if args.layer:
        all_entries = [e for e in all_entries if e["layer"] == args.layer.upper()]
    if args.tag:
        all_entries = [e for e in all_entries if e["tag"] == args.tag.upper()]

    # registry + family enrichment
    registry = get_registry(args)
    enriched = enrich_with_family(all_entries, registry)

    # warnings for unknown tags
    unknowns = sorted({e["tag"] for e in enriched if e["family"] == "Unknown"})
    if unknowns:
        sys.stderr.write(f"[warn] unknown tags (consider adding to TAGS.md): {', '.join(unknowns)}\n")

    # JSON modes
    if args.json == "raw":
        print(json.dumps(enriched, indent=2))
        return
    if args.json == "grouped":
        grouped = json_grouped(enriched, by=args.group_by)
        print(json.dumps(grouped, indent=2))
        return

    # Markdown modes (CHANGELOG)
    md = format_markdown(enriched)
    if args.mode == "print" or args.outfile == "-":
        print(md)
        return

    if args.mode == "append":
        if args.dry_run:
            print(f"--- would append to {args.outfile} ---\n{md}")
            return
        try:
            with open(args.outfile, "a", encoding="utf-8") as fh:
                fh.write("\n" + md + "\n")
            print(f"[ok] appended entries to {args.outfile}")
        except Exception as e:
            sys.stderr.write(f"[err] could not append: {e}\n")

if __name__ == "__main__":
    main()
