#!/usr/bin/env python3
"""
QR Code Generator CLI

Usage:
  python src/generate_qr.py -f <url_or_file.txt>
  python src/generate_qr.py -d <directory> [--recursive]

  # Single URL → img/example.com.png
  python src/generate_qr.py -f https://example.com

  # .txt file (one URL per line, # comments ignored)
  python src/generate_qr.py -f urls.txt

  # All .txt files in a folder
  python src/generate_qr.py -d ./links

  # Recursive across nested folders
  python src/generate_qr.py -d ./links --recursive

Output is always written to ./img/
"""

import argparse
import sys
from pathlib import Path

import qrcode

OUTPUT_DIR = Path("img")


def sanitize_filename(url: str) -> str:
    """Turn a URL into a safe, readable filename."""
    return (
        url.replace("https://", "")
        .replace("http://", "")
        .replace("/", "_")
        .replace(":", "")
        .replace("?", "_")
        .replace("&", "_")
        .replace("=", "_")
        .strip("_")[:120]
    )


def generate_qr(url: str, output_dir: Path) -> Path | None:
    """
    Generate and save a QR code PNG for the given URL.

    Args:
        url (str): The URL to encode in the QR code.
        output_dir (Path): Directory where the PNG will be saved.

    Returns:
        Path | None: The path to the saved PNG file, or None if input is invalid.
    """
    url = url.strip()
    if not url or url.startswith("#"):
        return None

    output_dir.mkdir(parents=True, exist_ok=True)

    qr = qrcode.QRCode(
        version=None,  # auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30% recovery
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    output_path = output_dir / (sanitize_filename(url) + ".png")
    img.save(output_path)

    print(f"  ✓  {url}")
    print(f"     → {output_path}")
    return output_path


def process_txt_file(txt_path: Path, output_dir: Path) -> int:
    """
    Generate QR codes for every URL in a .txt file (one per line).

    Args:
        txt_path (Path): Path to the .txt file.
        output_dir (Path): Directory where PNGs will be saved.

    Returns:
        int: Number of QR codes generated.
    """
    count = 0
    with open(txt_path, encoding="utf-8") as f:
        for line in f:
            try:
                result = generate_qr(line, output_dir)
            except (ValueError, OSError, qrcode.exceptions.DataOverflowError) as exc:
                print(
                    f"Error generating QR for line '{line.strip()}': {exc}",
                    file=sys.stderr,
                )
                continue
            if result:
                count += 1
    return count


def handle_file(input_arg: str) -> None:
    """
    Handle the '-f' argument: accepts a raw URL or a path to a .txt file.

    Args:
        input_arg (str): URL or path to .txt file.
    """
    p = Path(input_arg)

    if p.is_file() and p.suffix == ".txt":
        print(f"\nProcessing file: {p}")
        count = process_txt_file(p, OUTPUT_DIR)
        print(f"\nDone — {count} QR code(s) generated in '{OUTPUT_DIR}/'")
    else:
        print(f"\nGenerating QR for: {input_arg}")
        generate_qr(input_arg, OUTPUT_DIR)
        print(f"\nDone — saved in '{OUTPUT_DIR}/'")


def handle_directory(dir_arg: str, recursive: bool) -> None:
    """
    Handle the '-d' argument: find all .txt files in a directory.

    Args:
        dir_arg (str): Directory path.
        recursive (bool): Whether to search subdirectories.
    """
    d = Path(dir_arg)
    if not d.is_dir():
        print(f"Error: '{dir_arg}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    pattern = "**/*.txt" if recursive else "*.txt"
    txt_files = sorted(d.glob(pattern))

    if not txt_files:
        print(f"No .txt files found in '{dir_arg}'.", file=sys.stderr)
        sys.exit(1)

    total = 0
    flag = "(recursive)" if recursive else ""
    print(f"\nScanning: {d} {flag}")

    for txt_file in txt_files:
        print(f"\n  {txt_file.relative_to(d)}")
        total += process_txt_file(txt_file, OUTPUT_DIR)

    print(f"\nDone — {total} QR code(s) generated in '{OUTPUT_DIR}/'")


def main() -> None:
    """
    Main entry point for the CLI.
    Parses arguments and dispatches to handlers.
    """
    parser = argparse.ArgumentParser(
        description="Generate QR code PNGs from URLs or .txt files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/generate_qr.py -f https://example.com
  python src/generate_qr.py -f urls.txt
  python src/generate_qr.py -d ./links
  python src/generate_qr.py -d ./links --recursive
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f", metavar="URL_OR_FILE", help="A URL string or a .txt file of URLs"
    )
    group.add_argument("-d", metavar="DIRECTORY", help="A directory of .txt files")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recurse into sub-directories (with -d)",
    )

    args = parser.parse_args()

    if args.f:
        handle_file(args.f)
    else:
        handle_directory(args.d, args.recursive)


if __name__ == "__main__":
    main()
