"""QR code generation logic."""

from pathlib import Path

import qrcode
import qrcode.constants

from ..sanitizer.sanitize import sanitize_filename


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
