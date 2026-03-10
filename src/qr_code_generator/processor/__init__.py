"""File and directory processing sub-package."""

from .processor import handle_directory, handle_file, process_txt_file

__all__ = ["process_txt_file", "handle_file", "handle_directory"]
