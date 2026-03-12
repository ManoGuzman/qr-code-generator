"""
QR Code Generator

Usage:
  generate-qr -f <url_or_file.txt>
  generate-qr -d <directory> [--recursive]

  # Single URL → img/example.com.png
  generate-qr -f https://example.com

  # .txt file (one URL per line, # comments ignored)
  generate-qr -f urls.txt

  # All .txt files in a folder
  generate-qr -d ./links

  # Recursive across nested folders
  generate-qr -d ./links --recursive

Output is always written to ./img/
"""

from .cli import main
from .generator import generate_qr
from .processor import process_txt_file
from .sanitizer import sanitize_filename

__all__ = ["main", "generate_qr", "process_txt_file", "sanitize_filename"]
