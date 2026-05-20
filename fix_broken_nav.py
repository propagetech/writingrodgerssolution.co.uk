#!/usr/bin/env python3
"""Remove duplicate old nav left after failed regex replace."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ORPHAN_PATTERN = re.compile(
    r'(href="/#wr-contact">Contact</a>\s*</li>)\s*</ul>\s*.*?</ul>(\s*</div>\s*</div>\s*</div>)',
    re.DOTALL,
)

# Also fix index.html home links: #wr-contact stays; broken files only

def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "ASSIGNMENTS BY UNIVERSITY" not in text or 'href="/#wr-contact">Contact' not in text:
        return False
    updated, n = ORPHAN_PATTERN.subn(r"\1\n                    </ul>\2", text, count=1)
    if n:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    fixed = 0
    for path in sorted(ROOT.glob("*.html")):
        if fix_file(path):
            print(f"fixed nav {path.name}")
            fixed += 1
    print(f"Done: {fixed} files")


if __name__ == "__main__":
    main()
