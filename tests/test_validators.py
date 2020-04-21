import unittest

from imgix.constants import IMAGE_MIN_WIDTH, IMAGE_MAX_WIDTH, \
    IMAGE_ZERO_WIDTH, SRCSET_MIN_WIDTH_TOLERANCE

from imgix.constants import OUTPUT_QUALITY_MIN, \
    OUTPUT_QUALITY_DEFAULT, OUTPUT_QUALITY_MAX

from imgix.validators import validate_min_width, validate_max_width, \
    validate_range, validate_min_max_tol, validate_output_quality


class TestValidators(unittest.TestCase):

    def test_validate_min_raises(self):
        with self.assertRaises(AssertionError):
            validate_min_width(-1)

        with self.assertRaises(AssertionError):
            validate_min_width("1")

        with self.assertRaises(AssertionError):
            validate_min_width(IMAGE_ZERO_WIDTH)

        with self.assertRaises(AssertionError):
            validate_min_width([-1])

    def test_validate_max_raises(self):
        with self.assertRaises(AssertionError):
            validate_max_width(-1)

        with self.assertRaises(AssertionError):
            validate_max_width("1")

        with self.assertRaises(AssertionError):
            validate_max_width(IMAGE_ZERO_WIDTH)

        with self.assertRaises(AssertionError):
            validate_max_width([-1])

        with self.assertRaises(AssertionError):
            validate_max_width(IMAGE_MAX_WIDTH+1)

    def test_validate_range_raises(self):
        # Each x, y or <min, max> pair should fail in
        # because they are equal in every case.
        for x, y in enumerate([x for x in range(10)]):
            with self.assertRaises(AssertionError):
                validate_range(x, y)

        with self.assertRaises(AssertionError):
            validate_range(IMAGE_ZERO_WIDTH, IMAGE_ZERO_WIDTH)

        with self.assertRaises(AssertionError):
            validate_range(IMAGE_MIN_WIDTH, IMAGE_MIN_WIDTH)

        with self.assertRaises(AssertionError):
            validate_range(IMAGE_ZERO_WIDTH, IMAGE_MAX_WIDTH)

        with self.assertRaises(AssertionError):
            validate_range(IMAGE_MAX_WIDTH, IMAGE_MAX_WIDTH)

    def test_validate_min_max_tol_raises(self):

        with self.assertRaises(AssertionError):
            # `IMAGE_ZERO_WIDTH` is being used to
            # simulate a `tol` < ONE_PERCENT.
            validate_min_max_tol(
                IMAGE_MIN_WIDTH,
                IMAGE_MAX_WIDTH,
                IMAGE_ZERO_WIDTH)

    def test_validate_min_max_tol(self):
        # Due to the assertive nature of this validator
        # if this test does not raise, it passes.
        validate_min_max_tol(
            IMAGE_MIN_WIDTH,
            IMAGE_MAX_WIDTH,
            SRCSET_MIN_WIDTH_TOLERANCE)

    def test_validate_min_output_quality(self):
        validate_output_quality(OUTPUT_QUALITY_MIN)

    def test_validate_max_output_quality(self):
        validate_output_quality(OUTPUT_QUALITY_MAX)

    def test_validate_default_output_quality(self):
        validate_output_quality(OUTPUT_QUALITY_DEFAULT)

    def test_validate_output_quality_raises(self):
        # Assert values below the minimum raise.
        with self.assertRaises(AssertionError):
            validate_output_quality(-1)

        # Assert values above the maximum raise.
        with self.assertRaises(AssertionError):
            validate_output_quality(101)
