from PIL import Image as PILImage, ImageChops
from byu_pytest_utils import run_python_script, test_files, ensure_missing, this_folder, with_import, tier
import functools
from pytest import approx, fail
from pathlib import Path


core = tier('Core', 1)
advanced = tier('Advanced', 2)
excellent = tier('Excellent', 3)


def compare_images(obs: Path | PILImage.Image, exp: Path | PILImage.Image, *, min_pixel_match_ratio: float = 1.0):
    assert 0 <= min_pixel_match_ratio <= 1, "min_pixel_match_ratio must be between 0 and 1."

    if not isinstance(obs, PILImage.Image):
        observed = PILImage.open(obs).convert('RGB')
    else:
        observed = obs
    if not isinstance(exp, PILImage.Image):
        expected = PILImage.open(exp).convert('RGB')
    else:
        expected = exp

    obs_stem = obs.stem if isinstance(obs, Path) else "image"

    try:
        assert observed.size == expected.size, f"Image sizes don't match. Expected `{expected.size}`, but got `{observed.size}`."

        diff = ImageChops.difference(observed, expected)
        bbox = diff.getbbox()
        if not bbox:
            return

        if min_pixel_match_ratio == 1.0:
            for y in range(bbox[1], bbox[3]):
                for x in range(bbox[0], bbox[2]):
                    observed_pixel = observed.getpixel((x, y))
                    expected_pixel = expected.getpixel((x, y))
                    if not observed_pixel or not expected_pixel:
                        assert False, f"Failed to get pixels at ({x}, {y})!"

                    if isinstance(observed_pixel, (float, int)) or isinstance(expected_pixel, (float, int)):
                        assert False, "Failed to get correct pixel type!"

                    try:
                        assert observed_pixel[0] == approx(expected_pixel[0], abs=2), f"The pixels' red values at ({x}, {y}) don't match. Expected `{expected_pixel[0]}`, but got `{observed_pixel[0]}`. Check the diff image ({obs_stem}.diff.png) for details."
                        assert observed_pixel[1] == approx(expected_pixel[1], abs=2), f"The pixels' green values at ({x}, {y}) don't match. Expected `{expected_pixel[1]}`, but got `{observed_pixel[1]}`. Check the diff image ({obs_stem}.diff.png) for details."
                        assert observed_pixel[2] == approx(expected_pixel[2], abs=2), f"The pixels' blue values at ({x}, {y}) don't match. Expected `{expected_pixel[2]}`, but got `{observed_pixel[2]}`. Check the diff image ({obs_stem}.diff.png) for details."
                    except AssertionError as e:
                        if isinstance(obs, Path):
                            diff.save(this_folder / f'{obs_stem}.diff.png')
                        raise e
            return

        total_pixels = observed.width * observed.height
        matching_pixels = 0
        first_mismatch = None
        for y in range(observed.height):
            for x in range(observed.width):
                observed_pixel = observed.getpixel((x, y))
                expected_pixel = expected.getpixel((x, y))
                if not observed_pixel or not expected_pixel:
                    assert False, f"Failed to get pixels at ({x}, {y})!"

                if isinstance(observed_pixel, (float, int)) or isinstance(expected_pixel, (float, int)):
                    assert False, "Failed to get correct pixel type!"

                red_matches = observed_pixel[0] == approx(expected_pixel[0], abs=2)
                green_matches = observed_pixel[1] == approx(expected_pixel[1], abs=2)
                blue_matches = observed_pixel[2] == approx(expected_pixel[2], abs=2)
                if red_matches and green_matches and blue_matches:
                    matching_pixels += 1
                elif first_mismatch is None:
                    first_mismatch = (x, y, observed_pixel, expected_pixel)

        match_ratio = matching_pixels / total_pixels
        if match_ratio < min_pixel_match_ratio:
            if isinstance(obs, Path):
                diff.save(this_folder / f'{obs_stem}.diff.png')

            mismatch_message = ""
            if first_mismatch is not None:
                x, y, observed_pixel, expected_pixel = first_mismatch
                mismatch_message = f" First mismatch at ({x}, {y}): expected `{expected_pixel}`, got `{observed_pixel}`."
            assert False, (
                f"Only {match_ratio * 100:.2f}% of pixels matched, but at least "
                f"{min_pixel_match_ratio * 100:.2f}% is required.{mismatch_message} "
                f"Check the diff image ({obs_stem}.diff.png) for details."
            )
    finally:
        if isinstance(obs, Path):
            obs.unlink(missing_ok=True)


@core
@with_import('byuimage', 'Image')
def test_CORE_display_image(Image, monkeypatch):
    observed = None

    @functools.wraps(Image.show)
    def patched_Image_show(self):
        nonlocal observed
        observed = self.image
    monkeypatch.setattr(Image, 'show', patched_Image_show)

    run_python_script('image_processing.py', '-d',
                      test_files / 'explosion.input.jpg')

    if observed is None:
        fail('No Image was shown')

    compare_images(observed, test_files / 'explosion.input.jpg')


def make_filter_tester(observed_file: Path, key_file: Path, *script_args, min_pixel_match_ratio: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def inner_func():
            run_python_script('image_processing.py', *script_args)
            compare_images(observed_file, key_file, min_pixel_match_ratio=min_pixel_match_ratio)
            observed_file.unlink(missing_ok=True)
        return inner_func
    return decorator


@core
@ensure_missing(this_folder / "darkened-explosion.output.png")
@make_filter_tester(
    this_folder / 'darkened-explosion.output.png', test_files / 'darkened-explosion.key.png',
    '-k', test_files / 'explosion.input.jpg', this_folder / 'darkened-explosion.output.png', 0.3)
def test_CORE_darken_filter():
    ...


@core
@ensure_missing(this_folder / "sepia-explosion.output.png")
@make_filter_tester(
    this_folder / 'sepia-explosion.output.png', test_files / 'sepia-explosion.key.png',
    '-s', test_files / 'explosion.input.jpg', this_folder / 'sepia-explosion.output.png')
def test_CORE_sepia_filter():
    ...


@core
@ensure_missing(this_folder / "grayscale-explosion.output.png")
@make_filter_tester(
    this_folder / 'grayscale-explosion.output.png', test_files / 'grayscale-explosion.key.png',
    '-g', test_files / 'explosion.input.jpg', this_folder / 'grayscale-explosion.output.png')
def test_CORE_grayscale_filter():
    ...


@advanced
@ensure_missing(this_folder / "flipped-explosion.output.png")
@make_filter_tester(
    this_folder / 'flipped-explosion.output.png', test_files / 'flipped-explosion.key.png',
    '-f', test_files / 'explosion.input.jpg', this_folder / 'flipped-explosion.output.png')
def test_ADVANCED_flip_filter():
    ...


@advanced
@ensure_missing(this_folder / "mirrored-explosion.output.png")
@make_filter_tester(
    this_folder / 'mirrored-explosion.output.png', test_files / 'mirrored-explosion.key.png',
    '-m', test_files / 'explosion.input.jpg', this_folder / 'mirrored-explosion.output.png')
def test_ADVANCED_mirror_filter():
    ...


@excellent
@ensure_missing(this_folder / "bordered-explosion.output.png")
@make_filter_tester(
    this_folder / 'bordered-explosion.output.png', test_files / 'bordered-explosion.key.png',
    '-b', test_files / 'explosion.input.jpg', this_folder / 'bordered-explosion.output.png', 10, 120, 20, 14)
def test_EXCELLENT_border_filter():
    ...


@excellent
@ensure_missing(this_folder / "collage.output.png")
@make_filter_tester(
    this_folder / 'collage.output.png', test_files / 'collage.key.png',
    '-c', test_files / 'beach1.input.jpg', test_files / 'beach2.input.jpg',
    test_files / 'beach3.input.jpg', test_files / 'beach4.input.jpg',
    this_folder / 'collage.output.png', 10)
def test_EXCELLENT_collage_filter():
    ...


@excellent
@ensure_missing(this_folder / "greenscreen.output.png")
@make_filter_tester(
    this_folder / 'greenscreen.output.png', test_files / 'greenscreen.key.png',
    '-y', test_files / 'man.input.jpg', test_files / 'explosion.input.jpg',
    this_folder / 'greenscreen.output.png', 90, 1.3, min_pixel_match_ratio=0.95)
def test_EXCELLENT_greenscreen_filter():
    ...


def class_docstring_test(cls):
    owner = getattr(cls, '__module__', None) or getattr(cls, '__name__', None)
    for func in dir(cls):
        attr = getattr(cls, func)
        if callable(attr) and getattr(attr, '__module__', None) == owner:
            if func.startswith('__') or func == 'main':
                continue
            assert getattr(cls, func).__doc__ is not None, f"{func}() is missing a docstring"


@excellent
def test_EXCELLENT_image_docstrings():
    import image_processing
    class_docstring_test(image_processing)
