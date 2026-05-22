# Redirect checklist — not required

The site uses **legacy Pascal-Case `.html` filenames at the repo root** (e.g. `BPP-Assignment-Help.html`), matching the live indexed URLs. **No 301 redirect map is needed** for the HTML page migration.

`_redirects` and `.htaccess` are intentionally empty of redirect rules.

If you later change URL shapes again, regenerate rules with:

```bash
python3 scripts/generate-redirect-checklist.py
```

To revert to folder slugs (not recommended if avoiding 301s):

```bash
python3 scripts/migrate-to-slug-folders.py
```

Flatten to Pascal-Case (current layout):

```bash
python3 scripts/migrate-to-pascal-flat.py
```
