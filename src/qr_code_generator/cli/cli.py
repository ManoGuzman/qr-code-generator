"""CLI entry point for the QR code generator."""

import argparse

from ..processor.processor import handle_directory, handle_file


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
  generate-qr -f https://example.com
  generate-qr -f urls.txt
  generate-qr -d ./links
  generate-qr -d ./links --recursive
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
