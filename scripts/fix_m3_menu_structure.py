#!/usr/bin/env python3
"""Remove legacy menu wrappers and apply M3 navigation drawer markup."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fix_menu_html(html: str) -> str:
    if 'id="menu"' not in html:
        return html

    html = re.sub(
        r'<div class="viamagus-menu-top-row">\s*</div>\s*',
        '',
        html,
        flags=re.IGNORECASE,
    )

    html = re.sub(
        r'class="viamagus-component-content navbar navbar-inverse"',
        'class="viamagus-component-content navbar navbar-inverse wr-m3-app-bar"',
        html,
        count=1,
    )

    html = re.sub(
        r'class="container menu-center"',
        'class="container menu-center wr-m3-app-bar__row"',
        html,
        count=1,
    )

    html = re.sub(
        r'(</a>\s*</div>\s*)<div class="collapse-center">\s*<div class="nav-collapse collapse">',
        r'\1</div>\n                <nav class="nav-collapse collapse wr-m3-navigation-drawer" aria-label="Site navigation">',
        html,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # Close drawer: </ul> then nav-collapse div + collapse-center div -> </nav> only
    html = re.sub(
        r'(</ul>)\s*</div>\s*</div>(\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>)',
        r'\1\n                </nav>\2',
        html,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )

    return html


def main() -> None:
    updated = 0
    for path in sorted(ROOT.rglob('*.html')):
        if 'old' in path.parts or path.parts[-2] == 'partials':
            continue
        text = path.read_text(encoding='utf-8')
        new_text = fix_menu_html(text)
        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
            updated += 1
            print(path.relative_to(ROOT))
    print(f'\nDone: {updated} file(s)')


if __name__ == '__main__':
    main()
