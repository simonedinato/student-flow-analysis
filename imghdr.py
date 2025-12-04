"""
Minimal drop-in replacement for the deprecated stdlib imghdr module.

Implements the small subset of functionality required by Sphinx when
building our Jupyter Book. The public API mirrors the original module's
`what` function and exposes the `tests` list so that downstream code can
append additional detection hooks (for example, SVG support).
"""

from __future__ import annotations

from typing import BinaryIO, List, Optional

tests: List[callable] = []


def what(file: BinaryIO | str, h: Optional[bytes] = None) -> Optional[str]:
    """
    Return the detected image format name (e.g. 'png', 'jpeg') or None.
    """
    header = h if h is not None else _read_header(file)
    if not header:
        return None
    for test in tests:
        res = test(header, file)
        if res:
            return res
    return None


def _read_header(file: BinaryIO | str, length: int = 32) -> bytes:
    """
    Read and return the first `length` bytes from a file or file-like object.
    """
    if hasattr(file, "read"):
        fp = file  # type: ignore[assignment]
        pos = fp.tell()
        header = fp.read(length)
        fp.seek(pos)
        return header
    with open(file, "rb") as fp:
        return fp.read(length)


def test_png(header: bytes, file: BinaryIO | str) -> Optional[str]:
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    return None


def test_jpeg(header: bytes, file: BinaryIO | str) -> Optional[str]:
    if header[:3] == b"\xff\xd8\xff":
        return "jpeg"
    return None


def test_gif(header: bytes, file: BinaryIO | str) -> Optional[str]:
    if header.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    return None


def test_webp(header: bytes, file: BinaryIO | str) -> Optional[str]:
    if header.startswith(b"RIFF") and header[8:12] == b"WEBP":
        return "webp"
    return None


def test_bmp(header: bytes, file: BinaryIO | str) -> Optional[str]:
    if header.startswith(b"BM"):
        return "bmp"
    return None


def test_tiff(header: bytes, file: BinaryIO | str) -> Optional[str]:
    if header.startswith((b"MM\x00*", b"II*\x00")):
        return "tiff"
    return None


def test_pnm(header: bytes, file: BinaryIO | str) -> Optional[str]:
    if header.startswith((b"P1", b"P4")):
        return "pbm"
    if header.startswith((b"P2", b"P5")):
        return "pgm"
    if header.startswith((b"P3", b"P6")):
        return "ppm"
    return None


tests.extend(
    [
        test_png,
        test_jpeg,
        test_gif,
        test_webp,
        test_bmp,
        test_tiff,
        test_pnm,
    ]
)


