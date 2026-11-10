"""Keep where Dan lives, and whose machine built this, out of a public repo.

    uv run scripts/privacy.py check
        fail, naming each file, when a file git would commit is an image carrying any metadata
        but a colour profile, is a photo or video format this check can't read inside, or holds
        a home-folder path (/Users/<name> or /home/<name>); then the same for every file in
        the history any ref reaches, since a push sends that too (a shallow clone fails: its
        history is only what was fetched)
    uv run scripts/privacy.py strip FILE ...
        rewrite each JPEG, PNG or WebP upright, with no metadata but its colour profile

A photo's location hides in EXIF's GPS block, in XMP text (plain or compressed), in IPTC and in
PNG text chunks; a camera's serial number and its owner's name hide beside it. Rather than hunt
for each, the check allows nothing but a colour profile and the format's own housekeeping, and
refuses the formats it can't read inside (HEIC, AVIF, RAW, video). Since Pillow reads past a
chunk it doesn't know and stops at the image's end, the file's own structure is checked first: a
PNG, JPEG or WebP may hold only the chunks or segments a picture needs, and no image anything
after its end. What a photo shows (a window's view, a street, a face) no check can see: Dan looks
at each before it's staged.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from io import BytesIO
from pathlib import Path, PurePath

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
# the segments a picture needs, by marker: frames and their tables, scans, quantization, restart
# intervals; and the comment and APPn segments, which Pillow reads and the metadata check names
JPEG_SEGMENTS = (
    (set(range(0xC0, 0xD0)) - {0xC8}) | {0xDA, 0xDB, 0xDD, 0xFE} | set(range(0xE0, 0xF0))
)
# the housekeeping APPn segments, by what each must start with and its fixed length (None: any,
# and as many as the colour profile needs); anything else in one of them could be text
JPEG_HOUSEKEEPING_SEGMENTS = {
    0xE0: (b"JFIF\x00", 16),
    0xE2: (b"ICC_PROFILE\x00", None),
    0xEE: (b"Adobe", 14),
}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_CHUNKS = {
    b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"iCCP", b"sRGB", b"gAMA", b"cHRM", b"pHYs",
    b"sBIT", b"bKGD",
}  # fmt: skip
WEBP_CHUNKS = {b"VP8 ", b"VP8L", b"VP8X", b"ALPH", b"ICCP", b"ANIM", b"ANMF"}
AFTER_END = "bytes after the image's end"
CUT_SHORT = "unreadable as an image (cut short or malformed)"
GONE = "unreadable (it went, or can't be opened, while being checked)"
# A home folder, with or without a slash after it: the name runs to the first character a name
# can't hold (/, a space, a quote, <, >, a bracket) or to the end, so /Users/<name>/ doesn't match.
HOME = re.compile(rb"/(?:Users|home)/[^/\s\"'<>()]+")


def committable(root: Path) -> list[Path]:
    """Every file git would commit: tracked, or untracked and not ignored; symlinks included."""
    listed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root, capture_output=True, check=True,
    ).stdout.decode("utf-8").split("\0")  # fmt: skip
    paths = (root / name for name in listed if name)
    return sorted({path for path in paths if path.is_symlink() or path.is_file()})


def committed_bytes(path: Path) -> bytes:
    """What git commits for this file: a symlink's own target path, never what it points at."""
    return os.fsencode(os.readlink(path)) if path.is_symlink() else path.read_bytes()


def png_problem(data: bytes) -> str | None:
    """A chunk outside PNG_CHUNKS, or anything after IEND's CRC. Names the chunk's type only."""
    at = len(PNG_SIGNATURE)
    while at + 8 <= len(data):
        length, kind = int.from_bytes(data[at : at + 4], "big"), data[at + 4 : at + 8]
        if kind not in PNG_CHUNKS:
            return f"a PNG chunk it doesn't allow ({kind.decode('ascii', 'replace')})"
        at += 12 + length  # length, type, data, CRC
        if kind == b"IEND":
            return AFTER_END if at < len(data) else CUT_SHORT if at > len(data) else None
    return CUT_SHORT


def jpeg_walk(data: bytes) -> tuple[int | None, int | None]:
    """Where the JPEG's end-of-image marker (FFD9) ends, walking its segments and scans, so an
    FFD9 inside a segment (a thumbnail's) or a second JPEG appended isn't taken for it; and the
    first segment's marker a picture doesn't need (a DNL or a JPGn), or a JFIF, ICC or Adobe
    segment holding anything but its own data, all of which Pillow reads past. Text inside the scan's coded data, or in a colour profile's
    own text, is out of its reach: make strip re-encodes a photo, and Dan looks at it."""
    stray = None
    seen: set[int] = set()
    at = 2  # past the start-of-image marker
    while at < len(data) and data[at] == 0xFF:
        while at < len(data) and data[at] == 0xFF:  # a marker may follow any number of fill bytes
            at += 1
        if at >= len(data):
            return None, stray
        marker, at = data[at], at + 1
        if marker == 0xD9:
            return at, stray
        if marker not in JPEG_SEGMENTS and not 0xD0 <= marker <= 0xD7 and stray is None:
            stray = marker  # TEM, a DNL, a JPGn, a reserved marker
        if 0xD0 <= marker <= 0xD7 or marker == 0x01:  # restart markers and TEM stand alone
            continue
        length = int.from_bytes(data[at : at + 2], "big")  # the segment's, its length included
        if marker in JPEG_HOUSEKEEPING_SEGMENTS and stray is None:
            magic, fixed = JPEG_HOUSEKEEPING_SEGMENTS[marker]
            again = fixed is not None and marker in seen
            if (
                again
                or not data[at + 2 : at + length].startswith(magic)
                or fixed not in (None, length)
            ):
                stray = marker
            seen.add(marker)
        at += length
        if marker == 0xDA:  # start of scan: its coded data runs to the next marker but a restart
            while (at := data.find(b"\xff", at)) != -1 and at + 1 < len(data):
                if data[at + 1] != 0x00 and not 0xD0 <= data[at + 1] <= 0xD7:
                    break
                at += 2  # a stuffed FF00, or a restart marker inside the scan
            else:
                return None, stray
    return None, stray


def webp_problem(data: bytes) -> str | None:
    """A RIFF size that isn't the file's length, or a chunk outside WEBP_CHUNKS."""
    size = int.from_bytes(data[4:8], "little") + 8
    if size != len(data):
        return AFTER_END if size < len(data) else CUT_SHORT
    at = 12
    while at + 8 <= len(data):
        kind, length = data[at : at + 4], int.from_bytes(data[at + 4 : at + 8], "little")
        if kind not in WEBP_CHUNKS:
            return f"a WebP chunk it doesn't allow ({kind.decode('ascii', 'replace')})"
        at += 8 + length + (length & 1)  # a chunk of odd length has a pad byte
    return None if at == len(data) else CUT_SHORT


def structure_problem(data: bytes) -> str | None:
    """What the file holds that Pillow would read past: checked on the bytes, before Pillow."""
    if data.startswith(PNG_SIGNATURE):
        return png_problem(data)
    if data.startswith(b"\xff\xd8"):
        end, stray = jpeg_walk(data)
        if stray is not None:
            return f"a JPEG segment it doesn't allow (FF{stray:02X})"
        return CUT_SHORT if end is None else AFTER_END if end < len(data) else None
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return webp_problem(data)
    return "unreadable as an image (not a JPEG, PNG or WebP inside)"


def image_problem(path: PurePath, data: bytes | None = None) -> str | None:
    """Why this image can't be committed, or None when it carries nothing but a colour profile.
    data, when given, is the image itself (a blob from the history), read in place of path."""
    suffix = path.suffix.lower()
    if suffix in UNREADABLE:
        return f"a {suffix} file, which this check can't read inside; convert it to JPEG first"
    data = Path(path).read_bytes() if data is None else data
    reason = structure_problem(data)
    if reason:
        return reason
    try:
        with Image.open(BytesIO(data)) as image:
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
    return text_problem(path.read_bytes())


def text_problem(data: bytes) -> str | None:
    """Where these bytes hold a home-folder path, or None. The path itself is never printed."""
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
        try:  # a file can go, or lose its permissions, between the listing and the read
            if path.is_symlink():  # never followed: git commits the target's path, not the file
                linked = HOME.search(committed_bytes(path))
                reasons = ["a symlink to a home-folder path" if linked else None]
            else:
                image = path.suffix.lower() in READABLE | UNREADABLE
                reasons = [image_problem(path) if image else None, path_problem(path)]
        except OSError:
            reasons = [GONE]
        found += [(path, reason) for reason in reasons if reason]
    return found


def history(root: Path) -> list[tuple[str, str, bytes]]:
    """Every file in the history any ref reaches, as (path, blob sha, content); a blob kept
    under several paths is listed once, under the first path git finds it at."""
    listed = subprocess.run(
        ["git", "rev-list", "--objects", "--all"], cwd=root, capture_output=True, check=True
    ).stdout
    batch = subprocess.run(
        ["git", "cat-file", "--batch=%(objectname) %(objecttype) %(objectsize) %(rest)"],
        input=listed, cwd=root, capture_output=True, check=True,
    ).stdout  # fmt: skip
    blobs, at = [], 0
    while at < len(batch):
        end = batch.index(b"\n", at)
        sha, kind, *rest = batch[at:end].split(b" ", 3)
        start = end + 1
        if kind == b"missing":
            raise RuntimeError(f"git cat-file reports object {sha.decode()} missing")
        stop = start + int(rest[0])
        name = rest[1] if len(rest) > 1 else b""
        if kind == b"blob":
            blobs.append((name.decode("utf-8", "replace"), sha.decode(), batch[start:stop]))
        at = stop + 1  # each object's content ends with a newline
    return blobs


def shallow(root: Path) -> bool:
    """Whether this is a shallow clone, whose history pass would see only what was fetched."""
    return subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"],
        cwd=root, capture_output=True, check=True, text=True,
    ).stdout.strip() == "true"  # fmt: skip


def history_problems(root: Path, reported: dict[str, bytes]) -> list[tuple[str, str, str]]:
    """(path, blob sha, reason) for each file in the history that couldn't be committed now,
    leaving out a file the working-tree check already named with this same content."""
    found = []
    for name, sha, data in history(root):
        if reported.get(name) == data:
            continue
        path = PurePath(name)
        name = name or sha[:7]  # a blob a tag points at directly has no path: name it by sha
        if path.suffix.lower() in READABLE | UNREADABLE:
            reason = image_problem(path, data)
            if reason:
                found.append((name, sha, reason))
        reason = text_problem(data)
        if reason:
            found.append((name, sha, reason))
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
    if shallow(root):
        print(
            "privacy: a shallow clone: fetch the whole history (git fetch --unshallow) "
            "so it can be checked",
            file=sys.stderr,
        )
        return 1
    reported = {}
    for path, reason in found:
        try:
            if reason != GONE:
                reported[path.relative_to(root).as_posix()] = committed_bytes(path)
        except OSError:  # gone since: the history pass still checks every blob under its name
            continue
    in_history = history_problems(root, reported)
    for name, sha, reason in in_history:
        print(f"privacy: {name} (in history, {sha[:7]}): {reason}", file=sys.stderr)
    if in_history:
        print(
            "privacy: a push sends the history too; rewriting history to remove it is Dan's call",
            file=sys.stderr,
        )
    if found or in_history:
        return 1
    print("privacy: no image metadata, unreadable photo format or home-folder path, in history too")
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
