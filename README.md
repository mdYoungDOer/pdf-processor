# PDF Extractor (GMS Stocks)

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/mdYoungDOer/pdf-processor/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/downloads/)

A simple, open-source web app for extracting **tables** and **text** from PDF files and converting them to CSV, Excel, TXT, or DOCX. Built with [NiceGUI](https://nicegui.io/) and Python. No data is stored on the server—everything runs in memory.

---

## Features

- **Table extraction** – Pull tables from PDFs into a single spreadsheet (CSV or Excel).
- **Text extraction** – Get plain text from PDFs, optionally as TXT or DOCX.
- **In-browser UI** – Upload, process, preview, and download without leaving the page.
- **Dark mode** – Built-in theme toggle (background #25343F).
- **Custom theme** – Primary (#CD2C58), secondary (#FFC69D); contrast-friendly in light and dark.
- **Self-host or deploy** – Run locally or deploy to [Vercel](https://vercel.com) (or any ASGI host).

---

## Requirements

- **Python 3.11+**
- Dependencies listed in `requirements.txt` (see [Project structure](#project-structure)).

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/mdYoungDOer/pdf-processor.git
cd pdf-processor
pip install -r requirements.txt
```

---

## Usage

### Run locally

```bash
python main.py
```

Then open **http://localhost:8080** in your browser.

### Deploy to Vercel

1. **From Git** – Connect this repo in the [Vercel dashboard](https://vercel.com); it will use the root and `api/` for the Python function.
2. **From CLI** – Install the [Vercel CLI](https://vercel.com/docs/cli) and run:
   ```bash
   vercel
   ```

The app is served at the root via rewrites to `/api`. No environment variables are required for basic use. For large PDFs, consider increasing the function timeout in `vercel.json` (Pro plan allows longer limits).

---

## Project structure

| Path | Description |
|------|-------------|
| `main.py` | NiceGUI UI and FastAPI/ASGI app |
| `processor.py` | PDF extraction (tables/text) and format conversion |
| `api/index.py` | Vercel serverless entrypoint |
| `vercel.json` | Vercel config (rewrites, function settings) |
| `requirements.txt` | Python dependencies |

---

## Versioning and releases

This project follows [Semantic Versioning](https://semver.org/) (SemVer):

- **MAJOR** – Incompatible API or behavior changes.
- **MINOR** – New features, backward compatible.
- **PATCH** – Bug fixes and small improvements.

**Releases** are published as [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github). Each release includes:

- A version tag (e.g. `v0.1.0`).
- Release notes describing changes.
- Optional source code archives (e.g. `pdf-processor-0.1.0.zip`).

To create a new release:

1. Bump the version (e.g. in this README and/or a `VERSION` or `pyproject.toml` file).
2. Commit, push, then create a new release on GitHub with a tag like `v0.1.0` and paste the release notes.

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository.
2. Create a branch (`git checkout -b feature/your-feature` or `fix/your-fix`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request against the default branch.

Please keep changes focused and ensure the app still runs locally and (if applicable) on Vercel.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [NiceGUI](https://nicegui.io/) – Python UI framework.
- [pdfplumber](https://github.com/jsvine/pdfplumber) – PDF table and text extraction.
- [pandas](https://pandas.pydata.org/) – Data handling and export.
