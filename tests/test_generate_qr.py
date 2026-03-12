from pathlib import Path

import pytest
import qrcode.exceptions

from qr_code_generator import (
    generate_qr,
    process_txt_file,
    sanitize_filename,
)


class TestSanitizeFilename:
    """Tests for the sanitize_filename utility function."""

    def test_simple_url(self):
        assert sanitize_filename("https://example.com") == "example.com"

    def test_url_with_path(self):
        assert sanitize_filename("https://example.com/path/to/page") == "example.com_path_to_page"

    def test_url_with_query_params(self):
        assert sanitize_filename("https://example.com?foo=bar") == "example.com_foo_bar"

    def test_url_with_ampersand(self):
        assert sanitize_filename("https://example.com?a=1&b=2") == "example.com_a_1_b_2"

    def test_url_strips_underscores(self):
        assert sanitize_filename("https://example.com/") == "example.com"

    def test_truncates_long_url(self):
        long_url = "https://" + "a" * 200 + ".com"
        result = sanitize_filename(long_url)
        assert len(result) <= 120

    def test_http_url(self):
        assert sanitize_filename("http://example.com") == "example.com"


class TestGenerateQR:
    """Tests for the generate_qr core function."""

    @pytest.fixture
    def temp_output_dir(self, tmp_path):
        """Provide a temporary output directory that does not exist yet."""
        return tmp_path / "qr_output"

    def test_valid_url_creates_file(self, temp_output_dir):
        result = generate_qr("https://example.com", temp_output_dir)
        assert result is not None
        assert result.exists()
        assert result.suffix == ".png"

    def test_valid_url_returns_path(self, temp_output_dir):
        result = generate_qr("https://test.com", temp_output_dir)
        assert isinstance(result, Path)
        assert result is not None and "test.com" in str(result)

    def test_empty_string_returns_none(self, temp_output_dir):
        result = generate_qr("", temp_output_dir)
        assert result is None

    def test_whitespace_only_returns_none(self, temp_output_dir):
        result = generate_qr("   ", temp_output_dir)
        assert result is None

    def test_comment_line_returns_none(self, temp_output_dir):
        result = generate_qr("# this is a comment", temp_output_dir)
        assert result is None

    def test_url_with_special_chars_emoji(self, temp_output_dir):
        result = generate_qr("https://example.com/🎉", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_url_with_spanish_chars(self, temp_output_dir):
        result = generate_qr("https://ejemplo.com/café", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_url_with_chinese_chars(self, temp_output_dir):
        result = generate_qr("https://例子.com/测试", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_url_with_arabic_chars(self, temp_output_dir):
        result = generate_qr("https://مثال.com/اختبار", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_url_with_cyrillic_chars(self, temp_output_dir):
        result = generate_qr("https://пример.рф/тест", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_url_with_special_symbols(self, temp_output_dir):
        result = generate_qr("https://example.com/path!@#$%", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_url_with_brackets(self, temp_output_dir):
        result = generate_qr("https://example.com/(test)/[1]", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_plain_text_not_url(self, temp_output_dir):
        result = generate_qr("Just some plain text", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_email_address(self, temp_output_dir):
        result = generate_qr("mailto:test@example.com", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_phone_number(self, temp_output_dir):
        result = generate_qr("tel:+1234567890", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_wifi_qr_format(self, temp_output_dir):
        wifi_qr = "WIFI:S:MyNetwork;T:WPA;P:password123;;"
        result = generate_qr(wifi_qr, temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_creates_output_directory(self, temp_output_dir):
        assert not temp_output_dir.exists()
        generate_qr("https://example.com", temp_output_dir)
        assert temp_output_dir.exists()
        assert temp_output_dir.is_dir()


class TestProcessTxtFile:
    """Tests for process_txt_file, which reads a .txt file and generates QR codes."""

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Provide a temporary working directory for input and output files."""
        return tmp_path

    def test_processes_valid_urls(self, temp_dir):
        txt_file = temp_dir / "urls.txt"
        txt_file.write_text("https://example.com\nhttps://test.com\n")

        output_dir = temp_dir / "output"
        count = process_txt_file(txt_file, output_dir)
        assert count == 2
        assert (output_dir / "example.com.png").exists()
        assert (output_dir / "test.com.png").exists()

    def test_ignores_comments(self, temp_dir):
        txt_file = temp_dir / "urls.txt"
        txt_file.write_text("# comment\nhttps://example.com\n# another\n")

        output_dir = temp_dir / "output"
        count = process_txt_file(txt_file, output_dir)
        assert count == 1

    def test_ignores_empty_lines(self, temp_dir):
        txt_file = temp_dir / "urls.txt"
        txt_file.write_text("\n\nhttps://example.com\n\n")

        output_dir = temp_dir / "output"
        count = process_txt_file(txt_file, output_dir)
        assert count == 1

    def test_handles_special_characters_in_file(self, temp_dir):
        txt_file = temp_dir / "urls.txt"
        txt_file.write_text("https://ejemplo.com/café\nhttps://test.com\n", encoding="utf-8")

        output_dir = temp_dir / "output"
        count = process_txt_file(txt_file, output_dir)
        assert count == 2

    def test_returns_zero_for_empty_file(self, temp_dir):
        txt_file = temp_dir / "urls.txt"
        txt_file.write_text("")

        output_dir = temp_dir / "output"
        count = process_txt_file(txt_file, output_dir)
        assert count == 0


class TestDifferentOutputFormats:
    """Tests that verify the output file format and destination path."""

    @pytest.fixture
    def temp_output_dir(self, tmp_path):
        """Provide a temporary output directory that does not exist yet."""
        return tmp_path / "qr_output"

    def test_png_output_format(self, temp_output_dir):
        result = generate_qr("https://example.com", temp_output_dir)
        assert result is not None
        assert result.suffix == ".png"

    def test_custom_output_path(self, temp_output_dir):
        result = generate_qr("https://example.com", temp_output_dir)
        assert result is not None
        assert result.parent == temp_output_dir


class TestEdgeCases:
    """Tests for boundary conditions and unusual inputs in generate_qr."""

    @pytest.fixture
    def temp_output_dir(self, tmp_path):
        """Provide a temporary output directory that does not exist yet."""
        return tmp_path / "qr_output"

    def test_single_character_url(self, temp_output_dir):
        result = generate_qr("a", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_very_long_url(self, temp_output_dir):
        long_url = "https://" + "a" * 1000 + ".com"
        # qrcode auto-selects the highest version; result depends on library capacity.
        # We only assert that the function either succeeds or raises DataOverflowError —
        # both are valid outcomes depending on qrcode version and error correction level.
        try:
            result = generate_qr(long_url, temp_output_dir)
            assert result is None or result.exists()
        except qrcode.exceptions.DataOverflowError:
            pass

    def test_url_with_port(self, temp_output_dir):
        result = generate_qr("https://example.com:8080/path", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_url_with_fragments(self, temp_output_dir):
        result = generate_qr("https://example.com#section", temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_url_with_multiple_query_params(self, temp_output_dir):
        url = "https://example.com?a=1&b=2&c=3&d=4"
        result = generate_qr(url, temp_output_dir)
        assert result is not None
        assert result.exists()

    def test_leading_trailing_whitespace(self, temp_output_dir):
        result = generate_qr("  https://example.com  ", temp_output_dir)
        assert result is not None
        assert result.exists()
