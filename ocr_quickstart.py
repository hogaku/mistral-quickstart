"""Process PDFs with Mistral Document AI OCR and save markdown results."""

import os
import json
import base64
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv

from mistralai import Mistral


def ocr_pdf(client: Mistral, pdf_path: Path) -> Dict[str, Any]:
    """Upload a PDF and perform OCR using the Mistral client."""
    upload = client.files.upload(
        file={"file_name": pdf_path.name, "content": pdf_path.open("rb")},
        purpose="ocr",
    )
    signed_url = client.files.retrieve(file_id=upload.id)
    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": signed_url.url},
        include_image_base64=True,
    )
    # The response is an object, convert to dict if possible
    if hasattr(response, "dict"):
        return response.dict()
    if hasattr(response, "model_dump"):
        return response.model_dump()
    return response


def save_result(result: Dict[str, Any], output_dir: Path) -> None:
    """Save OCR result as markdown, JSON and extracted images."""
    text = result.get("text", "")
    images = result.get("images", [])

    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "result.md"
    json_path = output_dir / "result.json"
    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True)

    with md_path.open("w", encoding="utf-8") as md_file:
        md_file.write(text)

    with json_path.open("w", encoding="utf-8") as jf:
        json.dump(result, jf, ensure_ascii=False, indent=2)

    for img in images:
        filename = img.get("filename", "image.png")
        data = img.get("data", "")
        img_path = images_dir / filename
        if data:
            with img_path.open("wb") as f:
                f.write(base64.b64decode(data))
        with md_path.open("a", encoding="utf-8") as md_file:
            rel_path = img_path.relative_to(md_path.parent)
            md_file.write(f"\n\n![{filename}]({rel_path})\n")


def main(input_dir: Path, output_dir: Path, api_key: str) -> None:
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    client = Mistral(api_key=api_key)

    for pdf_file in input_dir.glob("*.pdf"):
        print(f"Processing {pdf_file.name}...")
        result = ocr_pdf(client, pdf_file)
        save_result(result, output_dir / pdf_file.stem)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process PDFs with Mistral OCR")
    parser.add_argument(
        "input_dir",
        type=Path,
        default=Path("input_pdfs"),
        help="Directory containing PDF files",
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        default=Path("results"),
        help="Directory to store results",
    )
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise SystemExit("MISTRAL_API_KEY environment variable not set")

    main(args.input_dir, args.output_dir, api_key)
