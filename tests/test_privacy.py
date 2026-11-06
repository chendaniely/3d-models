"""scripts/privacy.py: nothing that shows where Dan lives, or whose machine this is, gets in
(S03, S21)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
from PIL import ExifTags, Image, PngImagePlugin

import privacy

HOME = "/" + "Users" + "/someone/"  # joined at runtime, so this file holds no home path itself
XMP = (
    b'<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-'
    b'syntax-ns#"><rdf:Description xmlns:exif="http://ns.adobe.com/exif/1.0/" '
    b'exif:GPSLatitude="0,0.0N" exif:GPSLongitude="0,0.0E"/></rdf:RDF></x:xmpmeta>'
)


def photo(path: Path, *, gps: bool = False, orientation: int | None = None, **save) -> Path:
    """A 40x20 image, optionally with a GPS block, an EXIF orientation or other save options."""
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (40, 20), (200, 180, 150))
    exif = image.getexif()
    if gps:
        block = exif.get_ifd(ExifTags.IFD.GPSInfo)
        block[ExifTags.GPS.GPSLatitudeRef] = "N"
        block[ExifTags.GPS.GPSLatitude] = (0.0, 0.0, 0.0)
    if orientation:
        exif[ExifTags.Base.Orientation] = orientation
    if len(exif) or gps:
        save["exif"] = exif.tobytes()  # an Exif object holding only a GPS block is dropped
    image.save(path, **save)
    return path


def check(repo: Path, capsys) -> tuple[int, str]:
    code = privacy.main(["check"], root=repo)
    return code, capsys.readouterr().err


def commit(repo: Path, *paths: str) -> None:
    """Stage these paths, removals included, and commit them."""
    subprocess.run(["git", "add", "--", *paths], cwd=repo, check=True)
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", "commit", "-qm", "x"],
        cwd=repo, check=True,
    )  # fmt: skip


@pytest.mark.parametrize("name", ["print.jpg", "print.png", "print.webp"])
def test_check_passes_an_image_with_no_metadata(repo: Path, capsys, name: str) -> None:
    photo(repo / "models" / "coupon" / "photos" / name)
    assert check(repo, capsys) == (0, "")


@pytest.mark.parametrize(
    ("name", "reason"),
    [
        ("print.jpg", "EXIF metadata"),
        ("PRINT.JPG", "EXIF metadata"),
        ("print.png", "a PNG chunk it doesn't allow (eXIf)"),
        ("print.webp", "a WebP chunk it doesn't allow (EXIF)"),
    ],
)
def test_check_names_a_photo_with_a_gps_block(repo: Path, capsys, name: str, reason: str) -> None:
    photo(repo / "models" / "coupon" / "photos" / name, gps=True)
    code, err = check(repo, capsys)
    assert code == 1
    assert f"privacy: models/coupon/photos/{name}: {reason}" in err


def test_check_names_a_camera_serial_without_any_gps(repo: Path, capsys) -> None:
    image = Image.new("RGB", (40, 20))
    exif = image.getexif()
    exif[ExifTags.Base.BodySerialNumber] = "12345"
    exif[ExifTags.Base.CameraOwnerName] = "someone"
    image.save(repo / "print.jpg", exif=exif)
    assert check(repo, capsys) == (1, "privacy: print.jpg: EXIF metadata\n")


@pytest.mark.parametrize(
    ("name", "save", "reason"),
    [
        ("xmp.jpg", {"xmp": XMP}, "metadata"),
        ("comment.jpg", {"comment": b"taken at home"}, "metadata"),
        ("xmp.webp", {"xmp": XMP}, "a WebP chunk it doesn't allow (XMP )"),
    ],
)
def test_check_names_xmp_and_comments(
    repo: Path, capsys, name: str, save: dict, reason: str
) -> None:
    photo(repo / name, **save)
    code, err = check(repo, capsys)
    assert code == 1
    assert f"privacy: {name}: {reason}" in err


def test_check_names_xmp_hidden_in_a_compressed_png_chunk(repo: Path, capsys) -> None:
    info = PngImagePlugin.PngInfo()
    info.add_itxt("XML:com.adobe.xmp", XMP.decode(), zip=True)
    photo(repo / "print.png", pnginfo=info)
    assert check(repo, capsys) == (1, "privacy: print.png: a PNG chunk it doesn't allow (iTXt)\n")


def test_check_names_a_png_chunk_it_does_not_allow_without_printing_it(repo: Path, capsys) -> None:
    info = PngImagePlugin.PngInfo()
    info.add(b"prVt", b"taken at home")  # a private chunk Pillow reads past and drops
    photo(repo / "print.png", pnginfo=info)
    assert check(repo, capsys) == (1, "privacy: print.png: a PNG chunk it doesn't allow (prVt)\n")


@pytest.mark.parametrize("name", ["print.jpg", "print.png", "print.webp"])
def test_check_names_bytes_after_the_image_s_end(repo: Path, capsys, name: str) -> None:
    path = photo(repo / name)
    path.write_bytes(path.read_bytes() + b"taken at home")
    assert check(repo, capsys) == (1, f"privacy: {name}: bytes after the image's end\n")


def test_check_names_a_second_jpeg_after_the_first_s_end(repo: Path, capsys) -> None:
    path = photo(repo / "print.jpg")
    hidden = photo(repo.parent / "hidden.jpg", gps=True)  # outside the repo: only its bytes go in
    path.write_bytes(path.read_bytes() + hidden.read_bytes())
    assert check(repo, capsys) == (1, "privacy: print.jpg: bytes after the image's end\n")


def test_check_names_an_image_that_is_not_a_jpeg_png_or_webp_inside(repo: Path, capsys) -> None:
    Image.new("RGB", (40, 20)).save(repo / "print.png", format="PPM")  # Pillow reads it, no info
    assert check(repo, capsys) == (
        1,
        "privacy: print.png: unreadable as an image (not a JPEG, PNG or WebP inside)\n",
    )


def test_check_names_a_second_frame(repo: Path, capsys) -> None:
    frames = [Image.new("RGB", (40, 20), colour) for colour in ("red", "blue")]
    frames[0].save(repo / "turn.webp", save_all=True, append_images=frames[1:])
    assert check(repo, capsys) == (1, "privacy: turn.webp: more than one frame\n")


@pytest.mark.parametrize("name", ["IMG_0001.HEIC", "shot.heif", "clip.mov", "scan.dng", "a.gif"])
def test_check_refuses_a_format_it_cannot_read_inside(repo: Path, capsys, name: str) -> None:
    (repo / "models" / name).write_bytes(b"\x00\x00\x00\x18ftypheic")
    code, err = check(repo, capsys)
    assert code == 1
    assert f"privacy: models/{name}: a {Path(name).suffix.lower()} file" in err


def test_check_names_the_line_of_a_home_folder_path_without_printing_it(repo: Path, capsys) -> None:
    (repo / "notes.md").write_text(f"first\nsaved in {HOME}git/x\n", encoding="utf-8")
    code, err = check(repo, capsys)
    assert code == 1
    assert "privacy: notes.md: a home-folder path on line 2" in err
    assert "someone" not in err


def test_check_finds_a_home_folder_path_inside_a_binary(repo: Path, capsys) -> None:
    (repo / "part.stl").write_bytes(b"\x80\x81 exported from " + HOME.encode() + b"\xff")
    assert check(repo, capsys) == (1, "privacy: part.stl: a home-folder path inside it\n")


def test_check_skips_what_git_ignores(repo: Path, capsys) -> None:
    (repo / ".gitignore").write_text("website/_site/\n.venv/\n", encoding="utf-8")
    photo(repo / "website" / "_site" / "shot.jpg", gps=True)
    (repo / ".venv").mkdir()
    (repo / ".venv" / "paths.txt").write_text(HOME, encoding="utf-8")
    assert check(repo, capsys) == (0, "")


@pytest.mark.parametrize("name", ["print.jpg", "print.png", "print.webp"])
def test_strip_leaves_no_metadata(repo: Path, name: str) -> None:
    path = photo(repo / name, gps=True, **({"xmp": XMP} if name != "print.png" else {}))
    assert privacy.main(["strip", str(path)], root=repo) == 0
    assert privacy.image_problem(path) is None
    with Image.open(path) as image:
        assert image.size == (40, 20)


def test_strip_drops_a_jpeg_comment(repo: Path) -> None:
    path = photo(repo / "print.jpg", comment=b"taken at home")
    privacy.main(["strip", str(path)], root=repo)
    assert privacy.image_problem(path) is None


def test_strip_turns_the_photo_upright_before_dropping_its_orientation(repo: Path) -> None:
    path = photo(repo / "sideways.jpg", orientation=6)
    privacy.main(["strip", str(path)], root=repo)
    with Image.open(path) as image:
        assert image.size == (20, 40)
        assert not len(image.getexif())


def test_strip_keeps_the_colour_profile(repo: Path) -> None:
    icc = b"\x00" * 128  # Pillow keeps the bytes as given; a real profile would be parsed
    path = photo(repo / "print.png", icc_profile=icc)
    privacy.main(["strip", str(path)], root=repo)
    with Image.open(path) as image:
        assert image.info.get("icc_profile") == icc


def test_strip_refuses_a_heic(repo: Path, capsys) -> None:
    path = repo / "IMG_0001.heic"
    path.write_bytes(b"\x00")
    assert privacy.main(["strip", str(path)], root=repo) == 2
    assert "strip takes JPEG, PNG or WebP only" in capsys.readouterr().err


def test_strip_keeps_a_png_s_transparency(repo: Path) -> None:
    image = Image.new("P", (4, 4), 0)
    image.putpalette([0, 0, 0, 255, 0, 0] + [0] * 250 * 3)
    image.putpixel((1, 1), 1)
    path = repo / "alpha.png"
    image.save(path, transparency=0)
    privacy.main(["strip", str(path)], root=repo)
    assert privacy.image_problem(path) is None
    with Image.open(path) as stripped:
        assert stripped.info.get("transparency") is not None
        assert stripped.convert("RGBA").getpixel((0, 0))[3] == 0
        assert stripped.convert("RGBA").getpixel((1, 1))[3] == 255


def test_strip_checks_every_file_before_rewriting_any(repo: Path) -> None:
    good = photo(repo / "good.jpg", comment=b"taken at home")
    bad = repo / "IMG.heic"
    bad.write_bytes(b"\x00")
    before = good.read_bytes()
    assert privacy.main(["strip", str(good), str(bad)], root=repo) == 2
    assert good.read_bytes() == before


def test_strip_prints_file_names_only(repo: Path, capsys) -> None:
    path = photo(repo / "sub" / "print.jpg", comment=b"x")
    privacy.main(["strip", str(path)], root=repo)
    assert capsys.readouterr().out == "stripped print.jpg\n"
    bad = repo / "IMG.heic"
    bad.write_bytes(b"\x00")
    privacy.main(["strip", str(bad)], root=repo)
    assert capsys.readouterr().err == "privacy: IMG.heic: strip takes JPEG, PNG or WebP only\n"


def test_strip_keeps_the_file_mode(repo: Path) -> None:
    path = photo(repo / "print.jpg", comment=b"x")
    path.chmod(0o644)
    privacy.main(["strip", str(path)], root=repo)
    assert path.stat().st_mode & 0o777 == 0o644


def test_check_names_a_file_that_is_not_an_image(repo: Path, capsys) -> None:
    (repo / "fake.jpg").write_text("not an image", encoding="utf-8")
    code, err = check(repo, capsys)
    assert code == 1
    assert "privacy: fake.jpg: unreadable as an image" in err


def test_check_names_a_photo_stripped_after_it_was_committed(repo: Path, capsys) -> None:
    path = photo(repo / "models" / "coupon" / "photos" / "print.jpg", gps=True)
    commit(repo, "models")
    privacy.strip(path)
    commit(repo, "models")
    code, err = check(repo, capsys)
    assert code == 1
    assert "privacy: models/coupon/photos/print.jpg (in history, " in err
    assert "): EXIF metadata" in err
    assert "privacy: models/coupon/photos/print.jpg: " not in err  # the file itself is clean now


def test_check_names_bytes_after_an_image_s_end_in_history(repo: Path, capsys) -> None:
    path = photo(repo / "print.png")
    path.write_bytes(path.read_bytes() + b"taken at home")
    commit(repo, "print.png")
    path.unlink()
    commit(repo, "print.png")
    code, err = check(repo, capsys)
    assert code == 1
    assert "privacy: print.png (in history, " in err
    assert "): bytes after the image's end" in err


def test_check_names_a_home_folder_path_committed_then_removed(repo: Path, capsys) -> None:
    (repo / "notes.md").write_text(f"saved in {HOME}git/x\n", encoding="utf-8")
    commit(repo, "notes.md")
    (repo / "notes.md").unlink()
    commit(repo, "notes.md")
    code, err = check(repo, capsys)
    assert code == 1
    assert "privacy: notes.md (in history, " in err
    assert "): a home-folder path on line 1" in err
    assert "rewriting history to remove it is Dan's call" in err
    assert "someone" not in err


def test_check_passes_a_clean_history(repo: Path, capsys) -> None:
    photo(repo / "models" / "coupon" / "photos" / "print.jpg")
    (repo / "notes.md").write_text("first\n", encoding="utf-8")
    commit(repo, "models", "notes.md")
    (repo / "notes.md").write_text("second\n", encoding="utf-8")
    commit(repo, "notes.md")
    assert check(repo, capsys) == (0, "")


def test_check_names_a_committed_file_once_when_it_is_still_there(repo: Path, capsys) -> None:
    (repo / "notes.md").write_text(f"saved in {HOME}git/x\n", encoding="utf-8")
    commit(repo, "notes.md")
    assert check(repo, capsys) == (1, "privacy: notes.md: a home-folder path on line 1\n")


def test_check_names_a_symlink_to_a_home_folder_path(repo: Path, capsys) -> None:
    os.symlink(f"{HOME}notes.md", repo / "notes.md")  # git commits the target's path as text
    commit(repo, "notes.md")
    assert check(repo, capsys) == (1, "privacy: notes.md: a symlink to a home-folder path\n")


def test_check_passes_a_symlink_to_a_file_in_the_repo(repo: Path, capsys) -> None:
    (repo / "notes.md").write_text("first\n", encoding="utf-8")
    os.symlink("notes.md", repo / "readme.md")
    commit(repo, "notes.md", "readme.md")
    assert check(repo, capsys) == (0, "")


def test_check_names_a_symlink_to_a_home_folder_itself(repo: Path, capsys) -> None:
    os.symlink(HOME.rstrip("/"), repo / "home")
    assert check(repo, capsys) == (1, "privacy: home: a symlink to a home-folder path\n")


def test_check_names_a_line_ending_in_a_home_folder(repo: Path, capsys) -> None:
    (repo / "notes.md").write_text(f"first\ncd {HOME.rstrip('/')}\n", encoding="utf-8")
    assert check(repo, capsys) == (1, "privacy: notes.md: a home-folder path on line 2\n")


def test_check_names_a_blob_a_tag_points_at_directly(repo: Path, capsys) -> None:
    blob = subprocess.run(
        ["git", "hash-object", "-w", "--stdin"], cwd=repo, check=True, capture_output=True,
        input=f"saved in {HOME}git/x\n".encode(),
    ).stdout.decode().strip()  # fmt: skip
    subprocess.run(["git", "tag", "loose", blob], cwd=repo, check=True)
    code, err = check(repo, capsys)
    assert code == 1
    assert f"privacy: {blob[:7]} (in history, {blob[:7]}): a home-folder path on line 1" in err
    assert "someone" not in err


def test_check_refuses_a_shallow_clone(repo: Path, capsys) -> None:
    for text in ("first\n", "second\n"):  # two commits, so a depth of one leaves one out
        (repo / "notes.md").write_text(text, encoding="utf-8")
        commit(repo, "notes.md")
    clone = repo.parent / "clone"
    subprocess.run(
        ["git", "clone", "-q", "--depth", "1", repo.as_uri(), str(clone)], check=True
    )  # fmt: skip
    code, err = check(clone, capsys)
    assert (code, err) == (
        1,
        "privacy: a shallow clone: fetch the whole history (git fetch --unshallow) "
        "so it can be checked\n",
    )
