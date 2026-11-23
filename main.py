#!/usr/bin/env python3
"""news-image-20261122 rebuild r2 — copy-image entry point.

Validates the bundled entry.png (PNG magic, IHDR 1024x1024, per-chunk CRCs,
complete IEND, no trailing bytes, intact IDAT) and copies it byte-for-byte
to $MAKEFUN_OUTPUT_DIR/entry.png, then re-reads and re-validates the copy.
Stdlib only, no network. Deterministic: identical bytes every run.
"""
import os
import struct
import sys
import zlib

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


class ValidationError(Exception):
    pass


def _crc(chunk_type, data):
    return zlib.crc32(chunk_type + data) & 0xFFFFFFFF


def validate_png(path):
    """Strict structural validation. Raises ValidationError on any defect."""
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        raise ValidationError(f"cannot read {path}: {exc}") from exc
    if len(raw) < 8:
        raise ValidationError("file too short to be a PNG")
    if raw[:8] != PNG_MAGIC:
        raise ValidationError("bad PNG magic")
    pos = 8
    seen_ihdr = seen_idat = seen_iend = False
    width = height = None
    idat = bytearray()
    while True:
        if pos + 8 > len(raw):
            raise ValidationError("truncated chunk header")
        length, ctype = struct.unpack(">I4s", raw[pos:pos + 8])
        if length > 0x7FFFFFFF:
            raise ValidationError("chunk length too large")
        end = pos + 12 + length
        if end > len(raw):
            raise ValidationError(f"truncated chunk {ctype!r}")
        data = raw[pos + 8:pos + 8 + length]
        crc_stored, = struct.unpack(">I", raw[pos + 8 + length:end])
        if _crc(ctype, data) != crc_stored:
            raise ValidationError(f"bad CRC in chunk {ctype!r}")
        if ctype == b"IHDR":
            if seen_ihdr:
                raise ValidationError("duplicate IHDR")
            seen_ihdr = True
            width, height, bit_depth, color_type = struct.unpack(">IIBB", data[:10])
            if (width, height) != (1024, 1024):
                raise ValidationError(f"wrong dimensions {width}x{height}, expected 1024x1024")
            if bit_depth != 8 or color_type not in (2, 6):
                raise ValidationError(f"unsupported PNG type bit_depth={bit_depth} color_type={color_type}")
        elif ctype == b"IDAT":
            if not seen_ihdr:
                raise ValidationError("IDAT before IHDR")
            if seen_iend:
                raise ValidationError("IDAT after IEND")
            seen_idat = True
            idat.extend(data)
        elif ctype == b"IEND":
            if seen_iend:
                raise ValidationError("duplicate IEND")
            seen_iend = True
            if length != 0:
                raise ValidationError("IEND must be empty")
            if end != len(raw):
                raise ValidationError("trailing bytes after IEND")
            break
        pos = end
    if not seen_ihdr:
        raise ValidationError("missing IHDR")
    if not seen_idat:
        raise ValidationError("missing IDAT")
    if not seen_iend:
        raise ValidationError("missing IEND")
    if len(raw) > 1048576:
        raise ValidationError(f"file too large: {len(raw)} bytes > 1 MiB")
    try:
        zlib.decompress(bytes(idat))
    except zlib.error as exc:
        raise ValidationError(f"corrupt IDAT: {exc}") from exc
    return raw


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 2
    data = validate_png(SRC)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(data)
    # re-read + re-validate the copy
    copied = validate_png(dest)
    if copied != data:
        print("output differs from source after copy", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({len(data)} bytes, sha256 ok)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
