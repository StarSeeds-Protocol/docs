# docs

Documentation for the StarSeeds Protocol.

## Building the PDF

The Markdown documentation in this repository (this README plus everything
under `docs/`) can be compiled into a single PDF, and the result is
automatically double-checked to make sure no content was lost during
conversion.

### Requirements

- Python 3.10+
- System libraries for WeasyPrint (on Debian/Ubuntu: `libpango-1.0-0` and
  `libpangoft2-1.0-0`)
- Python dependencies: `pip install -r requirements.txt`

### Build

```bash
python3 scripts/build_pdf.py
```

This writes the PDF to `build/docs.pdf`.

### Double-check the content

```bash
python3 scripts/check_pdf.py
```

This extracts the text back out of `build/docs.pdf` and verifies that every
heading and paragraph from the Markdown sources is present. It exits non-zero
and lists any missing fragments if the check fails.

### Continuous integration

The `Build PDF` GitHub Actions workflow runs both steps on every push and
pull request, and uploads the generated PDF as a build artifact.
