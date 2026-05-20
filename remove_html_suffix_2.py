#!/usr/bin/env python3
"""Remove -2 suffix from HTML page filenames and internal links (-2.html -> .html)."""

from __future__ import annotations

import argparse
from pathlib import Path

SUFFIX = "-2.html"
REPLACEMENT = ".html"


def iter_html_files(root: Path, exclude_dirs: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.html"):
        if any(part in exclude_dirs for part in path.relative_to(root).parts):
            continue
        files.append(path)
    return sorted(files)


def update_contents(path: Path, dry_run: bool) -> int:
    text = path.read_text(encoding="utf-8")
    if SUFFIX not in text:
        return 0
    updated = text.replace(SUFFIX, REPLACEMENT)
    if not dry_run:
        path.write_text(updated, encoding="utf-8")
    return text.count(SUFFIX)


def rename_minus_two_pages(root: Path, dry_run: bool) -> list[tuple[Path, Path]]:
    renames: list[tuple[Path, Path]] = []
    for path in sorted(root.glob(f"*{SUFFIX}")):
        target = path.with_name(path.name.replace(SUFFIX, REPLACEMENT))
        if target.exists():
            raise FileExistsError(f"Cannot rename {path.name}: {target.name} already exists")
        renames.append((path, target))
        if not dry_run:
            path.rename(target)
    return renames


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Site root directory (default: script directory)",
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=["old"],
        help="Directory names to skip when scanning HTML (default: old)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print changes without writing or renaming",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    exclude_dirs = set(args.exclude)

    content_hits = 0
    files_touched = 0
    for html_path in iter_html_files(root, exclude_dirs):
        count = update_contents(html_path, args.dry_run)
        if count:
            files_touched += 1
            content_hits += count
            action = "would update" if args.dry_run else "updated"
            print(f"{action} {html_path.relative_to(root)} ({count} replacements)")

    renames = rename_minus_two_pages(root, args.dry_run)
    for src, dst in renames:
        action = "would rename" if args.dry_run else "renamed"
        print(f"{action} {src.name} -> {dst.name}")

    print(
        f"\nDone: {content_hits} link replacements in {files_touched} files, "
        f"{len(renames)} file renames"
        + (" (dry run)" if args.dry_run else "")
    )


if __name__ == "__main__":
    main()
