# pdf_to_images.py

import fitz  # PyMuPDF
import argparse
import sys
from pathlib import Path


def convert_pdf_to_images(pdf_path_str: str, output_folder_str: str, dpi: int = 300, img_format: str = "png"):
    """
    Converts each page of a PDF file into a high-resolution image.

    Args:
        pdf_path_str: The file path to the master template PDF.
        output_folder_str: The folder path to save the output images.
        dpi: The Dots Per Inch (resolution) for the output images.
        img_format: The output image format (e.g., "png", "jpg").
    """

    pdf_path = Path(pdf_path_str)
    output_folder = Path(output_folder_str)

    # 1. Validate PDF files
    if not pdf_path.is_file() or pdf_path.suffix.lower() != '.pdf':
        print(f"❌ ERROR: The file '{pdf_path}' is not a valid PDF file.")
        sys.exit(1)

    # 2. Create the output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # 3. Open the PDF document
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"❌ ERROR: Could not open PDF file '{pdf_path}'. Error: {e}")
        sys.exit(1)

    print(f"🚀 Starting conversion of '{pdf_path}' ({doc.page_count} pages)...")

    # 4. Define the transformation matrix for scaling (DPI)
    # PyMuPDF's default is 72 DPI. We need to scale this.
    # A scale factor of 2 gives 144 DPI (72 * 2).
    # So, for 300 DPI, the scale factor is 300 / 72.
    scale_factor = dpi / 72.0
    mat = fitz.Matrix(scale_factor, scale_factor)

    # 5. Iterate through each page and save as an image
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)

        # Apply the transformation matrix to get the high-res pixmap
        pix = page.get_pixmap(matrix=mat)

        # Create a user-friendly 1-based filename
        output_filename = output_folder / f"master_page_{page_num + 1}.{img_format}"

        try:
            pix.save(str(output_filename))
            print(f"  ✅ Saved page {page_num + 1} to '{output_filename}'")
        except Exception as e:
            print(f"  ❌ ERROR saving page {page_num + 1}: {e}")

    doc.close()
    print(f"\n✨ All pages converted. Output is in '{output_folder}'.")


def main():
    """
    Main function to parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Convert all pages of a PDF to high-quality images."
    )
    parser.add_argument(
        "--pdf",
        required=True,
        help="Path to the master template PDF file (e.g., 'Upitnik Blanko.pdf')."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the folder where images will be saved (e.g., './master_templates')."
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Dots Per Inch (DPI) for image quality. Default is 300."
    )
    parser.add_argument(
        "--format",
        type=str,
        default="png",
        help="Output image format (e.g., 'png', 'jpg'). 'png' is recommended for lossless quality."
    )

    args = parser.parse_args()

    convert_pdf_to_images(args.pdf, args.output, args.dpi, args.format)


if __name__ == "__main__":
    main()