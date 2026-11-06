"""Keep where Dan lives, and whose machine built this, out of a public repo.

    uv run scripts/privacy.py check
        fail, naming each file, when a file git would commit is an image carrying any metadata
        but a colour profile, is a photo or video format this check can't read inside, or holds
        a home-folder path (/Users/<name>/ or /home/<name>/)
    uv run scripts/privacy.py strip FILE ...
        rewrite each JPEG, PNG or WebP upright, with no metadata but its colour profile

A photo's location hides in EXIF's GPS block, in XMP text (plain or compressed), in IPTC and in
PNG text chunks; a camera's serial number and its owner's name hide beside it. Rather than hunt
for each, the check allows nothing but a colour profile and the format's own housekeeping, and
refuses the formats it can't read inside (HEIC, AVIF, RAW, video). What a photo shows (a window's
view, a street, a face) no check can see: Dan looks at each before it's staged.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
READABLE = {".jpg", ".jpeg", ".png", ".webp"}
UNREADABLE = {
    ".heic", ".heif", ".avif", ".jxl", ".gif", ".tif", ".tiff", ".bmp", ".jfif", ".mpo",
    ".dng", ".raw", ".cr2", ".cr3", ".nef", ".arw", ".orf", ".rw2",
    ".mov", ".mp4", ".m4v", ".3gp",
}  # fmt: skip
HOUSEKEEPING = {
    "icc_profile", "dpi", "jfif", "jfif_version", "jfif_unit", "jfif_density", "adobe",
    "adobe_transform", "progressive", "progression", "gamma", "srgb", "chromaticity",
    "transparency", "aspect", "interlace", "loop", "background", "timestamp", "duration",
}  # fmt: skip
JPEG_HOUSEKEEPING = {"APP0", "APP2", "APP14"}  # JFIF, the colour profile, Adobe's colour flag
HOME = re.compile(rb"/(?:Users|home)/[^/\s\"'<>()]+/")


def committable(root: Path) -> list[Path]:
    """Every file git would commit: tracked, or untracked and not ignored."""
    listed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root, capture_output=True, check=True,
    ).stdout.decode("utf-8").split("\0")  # fmt: skip
    return sorted({root / name for name in listed if name and (root / name).is_file()})


def image_problem(path: Path) -> str | None:
    """Why this image can't be committed, or None when it carries nothing but a colour profile."""
    suffix = path.suffix.lower()
    if suffix in UNREADABLE:
        return f"a {suffix} file, which this check can't read inside; convert it to JPEG first"
    try:
        with Image.open(path) as image:
            image.load()
            if getattr(image, "n_frames", 1) > 1:
                return "more than one frame"
            if len(image.getexif()):
                return "EXIF metadata"
            extra = sorted(set(image.info) - HOUSEKEEPING)
            markers = {marker for marker, _ in getattr(image, "applist", [])}
    except (OSError, ValueError, Image.DecompressionBombError) as error:
        return f"unreadable as an image ({error})"
    if extra:
        return f"metadata: {', '.join(extra)}"
    if markers - JPEG_HOUSEKEEPING:
        return f"metadata segments: {', '.join(sorted(markers - JPEG_HOUSEKEEPING))}"
    return None


def path_problem(path: Path) -> str | None:
    """Where this file holds a home-folder path, or None. The path itself is never printed."""
    data = path.read_bytes()
    if not HOME.search(data):
        return None
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return "a home-folder path inside it"
    numbers = [str(n) for n, line in enumerate(lines, 1) if HOME.search(line.encode("utf-8"))]
    return f"a home-folder path on line {', '.join(numbers)}"


def problems(root: Path) -> list[tuple[Path, str]]:
    found = []
    for path in committable(root):
        if path.suffix.lower() in READABLE | UNREADABLE:
            reason = image_problem(path)
            if reason:
                found.append((path, reason))
        reason = path_problem(path)
        if reason:
            found.append((path, reason))
    return found


def strip(path: Path) -> None:
    with Image.open(path) as opened:
        image_format = opened.format
        icc = opened.info.get("icc_profile")
        transparency = opened.info.get("transparency")
        image = ImageOps.exif_transpose(opened)
        image.load()
    image.info = {}  # Pillow writes a JPEG's comment, and EXIF or XMP, from info unless cleared
    options = {"icc_profile": icc} if icc else {}
    if transparency is not None and image_format in {"PNG", "WEBP"}:
        options["transparency"] = transparency
    if image_format == "JPEG":
        options |= {"quality": 95, "subsampling": 0}
    handle, temp = tempfile.mkstemp(dir=path.parent, suffix=path.suffix)
    os.close(handle)
    try:
        image.save(temp, format=image_format, **options)
        shutil.copymode(path, temp)
        os.replace(temp, path)
    finally:
        Path(temp).unlink(missing_ok=True)


def command_check(root: Path) -> int:
    found = problems(root)
    for path, reason in found:
        print(f"privacy: {path.relative_to(root)}: {reason}", file=sys.stderr)
    if found:
        return 1
    print("privacy: no image metadata, unreadable photo format or home-folder path")
    return 0


def command_strip(files: list[Path]) -> int:
    for path in files:
        if path.suffix.lower() not in READABLE:
            print(f"privacy: {path.name}: strip takes JPEG, PNG or WebP only", file=sys.stderr)
            return 2
    for path in files:
        strip(path)
        print(f"stripped {path.name}")
    return 0


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="fail on image metadata, an unreadable format or a home path")
    strip_parser = sub.add_parser("strip", help="rewrite images without their metadata")
    strip_parser.add_argument("files", nargs="+", type=Path, metavar="FILE")
    args = parser.parse_args(argv)
    if args.command == "strip":
        return command_strip(args.files)
    return command_check(root)


if __name__ == "__main__":
    sys.exit(main())
