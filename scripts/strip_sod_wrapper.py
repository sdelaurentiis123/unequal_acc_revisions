#!/usr/bin/env python3
"""Pre-process a v2-style .tex file before running latexdiff against v3.

Two fixes:
  1. Strip the multi-line \\sod{ ... } wrapper around the Bondi-Hoyle paragraph
     in §3.1.1. v3 has no wrapper but identical inner text, so without this
     pre-processing latexdiff renders a giant '[SOD: ...]' green/bold strikethrough
     that overflows the margin.

  2. Neutralize the \\sod and \\mss macro definitions so they pass content through
     unchanged. Even with (1), if any other \\sod{} or \\mss{} call remains
     anywhere in the diff input, it would render as the formatted '[SOD: ...]'
     style. Making the macros no-ops in the v2 input keeps content visible
     where the diff matters but suppresses the visual styling.

Usage: strip_sod_wrapper.py <input.tex> <output.tex>
"""
import sys
import re
from pathlib import Path

src, dst = sys.argv[1], sys.argv[2]
text = Path(src).read_text()

# --- Fix 1: strip the multi-line \\sod{...} wrapper in §3.1.1 ---
# The wrapper opens at end of "\\sod{" line and closes at "global gas reservoir.}"
text = re.sub(
    r'\\sod\{\s*\n((?:.*\n)*?.*?global gas reservoir\.)\}',
    r'\1',
    text
)

# --- Fix 2: neutralize \\sod and \\mss macro definitions ---
text = re.sub(
    r'\\newcommand\{\\sod\}\[1\]\{[^\n]*\}',
    r'\\newcommand{\\sod}[1]{#1}',
    text
)
text = re.sub(
    r'\\newcommand\{\\mss\}\[1\]\{[^\n]*\}',
    r'\\newcommand{\\mss}[1]{#1}',
    text
)

Path(dst).write_text(text)

# Verify the strip worked
remaining_sod = len(re.findall(r'\\sod\{', text))
remaining_mss = len(re.findall(r'\\mss\{', text))
sod_neutral = '\\newcommand{\\sod}[1]{#1}' in text
mss_neutral = '\\newcommand{\\mss}[1]{#1}' in text
print(f"After preprocessing:")
print(f"  remaining \\sod{{ ... }} calls: {remaining_sod}")
print(f"  remaining \\mss{{ ... }} calls: {remaining_mss}")
print(f"  \\sod neutralized: {sod_neutral}")
print(f"  \\mss neutralized: {mss_neutral}")
print(f"Wrote {dst}")
