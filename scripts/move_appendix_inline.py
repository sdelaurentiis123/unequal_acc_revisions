#!/usr/bin/env python3
"""Bucket D: move Roman's Table 1 + Fig 18 from appendix to inline §3.1 location.

Per Zoltan #1: 'insert a copy of the pertinent figure from your paper with Roman
here, even if it is a duplication.'

In v3:
  - tab:locked_precessing_grid (Roman's Table 1) -> inline at first reference (~line 271)
    Insert immediately after \\end{table} for tab:stable_varying_grid.
  - fig:a_e_cav_heatmap (Roman's Fig 18) -> inline at first reference (~line 288)
    Insert immediately after \\end{figure} for fig:lambda_std_heatmap.
  - Delete the entire \\appendix section.
"""
import re
from pathlib import Path
import shutil

TEX = Path(__file__).resolve().parent.parent / "main.tex"
shutil.copy(TEX, TEX.with_suffix(".tex.bak"))
text = TEX.read_text()
lines = text.split("\n")

# ---- Helpers ----
def find_line(pattern, start=0):
    for i in range(start, len(lines)):
        if re.search(pattern, lines[i]):
            return i
    return -1

def find_block_end(start, end_pattern):
    """Find the next line matching end_pattern starting from start."""
    for i in range(start, len(lines)):
        if re.search(end_pattern, lines[i]):
            return i
    return -1

# ---- 1. Locate the appendix blocks ----
appendix_start = find_line(r"^\\appendix")
print(f"Appendix starts at line {appendix_start+1}")

# Find the tab:locked_precessing_grid block (the Roman table reproduction)
table_lpg_start = -1
for i in range(appendix_start, len(lines)):
    if "\\begin{table}" in lines[i]:
        # Verify this is the right table
        # Look ahead for tab:locked_precessing_grid label
        for j in range(i, min(i+200, len(lines))):
            if "tab:locked_precessing_grid" in lines[j]:
                table_lpg_start = i
                break
        if table_lpg_start >= 0:
            break

table_lpg_end = find_block_end(table_lpg_start, r"\\end\{table\}")
print(f"Roman Table 1 block: lines {table_lpg_start+1} to {table_lpg_end+1}")

# Find the fig:a_e_cav_heatmap block (the Roman fig reproduction)
fig_aec_start = -1
for i in range(table_lpg_end, len(lines)):
    if "\\begin{figure}" in lines[i]:
        for j in range(i, min(i+30, len(lines))):
            if "fig:a_e_cav_heatmap" in lines[j]:
                fig_aec_start = i
                break
        if fig_aec_start >= 0:
            break

fig_aec_end = find_block_end(fig_aec_start, r"\\end\{figure\}")
print(f"Roman Fig 18 block: lines {fig_aec_start+1} to {fig_aec_end+1}")

# Extract the blocks (inclusive)
table_block = lines[table_lpg_start:table_lpg_end+1]
figure_block = lines[fig_aec_start:fig_aec_end+1]

# ---- 2. Update Roman attribution captions to be explicit "in preparation" ----
# The bib entry now says "in preparation" so \citet{DeLaurentiis25} renders correctly,
# but we'll also tighten the figure caption since v2 was confusingly worded.
# (Skip; bibtex output should suffice)

# ---- 3. Locate the inline insertion points ----
# Point A: after \end{table} for tab:stable_varying_grid
svg_start = find_line(r"\\begin\{table\}", 0)
# Find which table comes first
# The first \begin{table} in the file (after the figures, ~line 160)
# We want the one with tab:stable_varying_grid label
svg_block_start = -1
for i in range(0, len(lines)):
    if "\\begin{table}" in lines[i]:
        for j in range(i, min(i+200, len(lines))):
            if "tab:stable_varying_grid" in lines[j]:
                svg_block_start = i
                break
        if svg_block_start >= 0:
            break

svg_block_end = find_block_end(svg_block_start, r"\\end\{table\}")
print(f"V/S table (tab:stable_varying_grid) ends at line {svg_block_end+1}")

# Point B: after \end{figure} for fig:lambda_std_heatmap
lsh_block_start = -1
for i in range(svg_block_end, len(lines)):
    if "\\begin{figure}" in lines[i]:
        for j in range(i, min(i+15, len(lines))):
            if "fig:lambda_std_heatmap" in lines[j]:
                lsh_block_start = i
                break
        if lsh_block_start >= 0:
            break

lsh_block_end = find_block_end(lsh_block_start, r"\\end\{figure\}")
print(f"σ_λ figure (fig:lambda_std_heatmap) ends at line {lsh_block_end+1}")

# ---- 4. Build new file ----
# Strategy:
#   - Up through the V/S table end: keep as-is
#   - Insert: blank line + Roman's Table 1 block + blank line
#   - Continue through the σ_λ figure end: keep
#   - Insert: blank line + Roman's Fig 18 block + blank line
#   - Continue through the appendix start (exclusive): keep
#   - SKIP everything from \appendix to \bibliography (or until last \end{figure} of appendix block)
#   - Resume with \bibliographystyle{...} onwards

# Find the bibliography start to know where the appendix region ends
bib_start = find_line(r"\\bibliographystyle", 0)
print(f"bibliographystyle line: {bib_start+1}")

# Construct new lines list:
new_lines = []
# Part 1: up through V/S table end (inclusive)
new_lines.extend(lines[:svg_block_end+1])
# Insert separator + Roman table
new_lines.append("")
new_lines.append("% Reproduction of Roman's Table 1 (moved from appendix per Zoltan #1)")
new_lines.extend(table_block)
# Continue through to σ_λ figure end (inclusive)
new_lines.extend(lines[svg_block_end+1:lsh_block_end+1])
# Insert separator + Roman figure
new_lines.append("")
new_lines.append("% Reproduction of Roman's Fig 18 (moved from appendix per Zoltan #1)")
new_lines.extend(figure_block)
# Continue from after σ_λ figure end to BEFORE appendix start
new_lines.extend(lines[lsh_block_end+1:appendix_start])
# Skip the appendix entirely. Resume at bibliographystyle.
new_lines.extend(lines[bib_start:])

new_text = "\n".join(new_lines)
TEX.write_text(new_text)
print(f"\nWrote {TEX} ({len(new_lines)} lines, was {len(lines)})")
print(f"Backup: {TEX.with_suffix('.tex.bak')}")
