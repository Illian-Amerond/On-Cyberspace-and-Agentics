# =========================
# latexmkrc  — Overleaf / LuaLaTeX + biber
# =========================

# Engine & outputs
$pdf_mode      = 1;                            # build PDF
$pdflatex      = 'lualatex -synctex=1 -file-line-error -interaction=nonstopmode %O %S';

# Bibliography (biblatex + biber)
$bibtex        = 'biber %O %B';
$use_biber     = 1;

# Rerun logic
$max_repeat    = 5;                            # extra safety on cross-refs
$recorder      = 1;                            # .fls for dependency tracking

# Log noise
$silence_logfile_warnings = 0;                 # keep important warnings
$diagnostics   = 0;

# Cleanups you want retained between runs (comment out to clean aggressively)
@default_excluded_exts = (
  'synctex.gz', 'synctex', 'nav', 'snm', 'xdv'
);

# --- Optional: glossaries support (uncomment if/when you add glossaries-extra) ---
# add_cus_dep('glo', 'gls', 0, 'makeglossaries');
# sub makeglossaries {
#   my ($base_name, $path) = fileparse( $_[0] );
#   return system("makeglossaries -q '$base_name'");
# }

# --- Optional: index support ---
# $makeindex = 'makeindex %O -o %D %S';

# --- Optional: output dirs (Overleaf usually ignores; local TeX uses these) ---
# $aux_dir = 'build-aux';
# $out_dir = 'build';

# ------------------------------------------------------------
# HOW TO USE THIS FILE
# ------------------------------------------------------------
# 1. What This Is:
#    This file tells 'latexmk' how to compile this document cleanly
#    with LuaLaTeX as the main engine and biber for bibliographies.
#    It’s the build brain of the project.
#
# 2. Where It Lives:
#    Keep it at the ROOT of your Overleaf project (or local repo).
#    Overleaf detects it automatically — no menu toggles needed.
#
# 3. What You Do:
#    • Just hit "Recompile" in Overleaf — this script ensures:
#        - LuaLaTeX runs with good error reporting & SyncTeX.
#        - Bibliography via biber.
#        - Multiple passes for cross-references.
#    • Locally, run:   latexmk -pdf   (or just 'latexmk')
#
# 4. Glossaries & Index:
#    If the project adds glossaries, uncomment the glossaries block above.
#    For an index, uncomment the makeindex line.
#
# 5. Troubleshooting:
#    • Weird references not updating? Delete aux files and recompile.
#    • Bibliography not appearing? Run 'biber <mainfile>' locally or check
#      Overleaf's log for biber errors.
#
# 6. Philosophy:
#    This keeps the build process invisible so authors focus on *writing*.
#    The fewer menu clicks and manual runs, the better.
#
# ------------------------------------------------------------
# End
