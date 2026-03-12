"""File and directory processing logic."""

import sys
from pathlib import Path

import qrcode.exceptions

from ..generator.generator import generate_qr

OUTPUT_DIR = Path("img")


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
    Handle the ``-f`` CLI argument: generate QR codes from a URL or a .txt file.

    If ``input_arg`` is an existing ``.txt`` file, every URL in that file is
    processed via :func:`process_txt_file`.  Otherwise the argument is treated
    as a raw URL and a single QR code is generated.

    Progress and summary information are printed to stdout.

    Args:
        input_arg (str): A raw URL string or a path to a ``.txt`` file of URLs.
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
    Handle the ``-d`` CLI argument: generate QR codes from all .txt files in a directory.

    Scans ``dir_arg`` for ``.txt`` files (using ``**/*.txt`` when ``recursive``
    is ``True``, or ``*.txt`` otherwise) and processes each one via
    :func:`process_txt_file`.  Files are processed in sorted order.

    Exits with code 1 (via :func:`sys.exit`) if ``dir_arg`` is not a valid
    directory or if no ``.txt`` files are found.  Progress and summary
    information are printed to stdout.

    Args:
        dir_arg (str): Path to the directory to scan.
        recursive (bool): When ``True``, also search subdirectories.
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
