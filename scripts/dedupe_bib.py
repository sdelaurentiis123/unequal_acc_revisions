#!/usr/bin/env python3
"""Dedupe main.bib entries by case-sensitive key (keep first occurrence).
Writes cleaned bib in-place. Reports deletions."""
import re
import sys
import shutil
from pathlib import Path

BIB = Path(__file__).resolve().parent.parent / "main.bib"
shutil.copy(BIB, BIB.with_suffix(".bib.bak"))

text = BIB.read_text()

# Find all @TYPE{KEY,...} entries with their full block (until next @ at column 0)
# Strategy: split text into entries by lines starting with "@", track each entry's key, line range
lines = text.split("\n")
entries = []  # list of (start_line, end_line_exclusive, key, type, raw_block)
i = 0
while i < len(lines):
    m = re.match(r"^@([A-Za-z]+)\s*\{\s*([^,\s]+)", lines[i])
    if m:
        etype, key = m.group(1), m.group(2)
        # Find the end of this entry: next line starting with @ or EOF
        j = i + 1
        while j < len(lines) and not re.match(r"^@", lines[j]):
            j += 1
        entries.append((i, j, key, etype, "\n".join(lines[i:j])))
        i = j
    else:
        i += 1

print(f"Total entries found: {len(entries)}")

# Track first occurrence of each key (case-sensitive)
seen = {}
keep = []
deleted = []
for entry in entries:
    start, end, key, etype, block = entry
    if key in seen:
        deleted.append((key, start + 1, end))  # 1-indexed
        print(f"  DELETING {key} at lines {start+1}-{end} (first kept at line {seen[key]+1})")
    else:
        seen[key] = start
        keep.append(entry)

# Reconstruct: take the lines NOT in any deleted block
deleted_line_set = set()
for key, start_1indexed, end_exclusive in deleted:
    # Convert to 0-indexed range
    for ln in range(start_1indexed - 1, end_exclusive):
        deleted_line_set.add(ln)

new_lines = [lines[i] for i in range(len(lines)) if i not in deleted_line_set]
new_text = "\n".join(new_lines)

BIB.write_text(new_text)

print(f"\nKept {len(keep)} unique entries; deleted {len(deleted)} duplicates.")
print(f"Backup: {BIB.with_suffix('.bib.bak')}")
print(f"Wrote: {BIB}")
