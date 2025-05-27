# Mistral Document AI Quickstart
※codexを用いたコーディングのテストです。

This repository contains a small helper script to process PDF files using the
[Mistral Document AI](https://docs.mistral.ai/capabilities/OCR/document_ai_overview/)
OCR API. The script uploads each PDF to Mistral and stores the OCR output as
Markdown, JSON and any extracted images.

## Requirements

- Python 3.8+
 - The `mistralai` package (see `requirements.txt`)
- A Mistral API key available in the environment as `MISTRAL_API_KEY`

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Place the PDF documents you want to analyse inside the `input_pdfs/` directory
(or specify another one via the command line). The script writes the output
into the `results/` directory. For each input PDF a subdirectory is created
containing `result.md`, `result.json` and an `images/` folder with any
extracted figures.

```bash
export MISTRAL_API_KEY=your-token-here
python ocr_quickstart.py input_pdfs results
```

Each processed PDF will generate a folder under `results/` mirroring the file
name. Inside you will find the extracted text in `result.md`, the full response
as `result.json` and an `images/` subfolder with the image files referenced from
the Markdown.
