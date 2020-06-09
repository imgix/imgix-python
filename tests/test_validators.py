import unittest

from imgix.constants import IMAGE_MIN_WIDTH, IMAGE_MAX_WIDTH, \
    IMAGE_ZERO_WIDTH, SRCSET_MIN_WIDTH_TOLERANCE

from imgix.validators import validate_min_width, validate_max_width, \
    validate_range, validate_min_max_tol, validate_widths

from imgix.errors import WidthRangeError, WidthToleranceError

LESS_THAN_ZERO = IMAGE_ZERO_WIDTH - 1


class TestValidators(unittest.TestCase):
    def test_validate_min_raises(self):
        with self.assertRaises(WidthRangeError):
            validate_min_width(-1)

        with self.assertRaises(WidthRangeError):
            validate_min_width("1")

        with self.assertRaises(WidthRangeError):
            validate_min_width(LESS_THAN_ZERO)

        with self.assertRaises(WidthRangeError):
            validate_min_width([-1])

    def test_validate_max_raises(self):
        with self.assertRaises(WidthRangeError):
            validate_max_width(-1)

        with self.assertRaises(WidthRangeError):
            validate_max_width("1")

        with self.assertRaises(WidthRangeError):
            validate_max_width(LESS_THAN_ZERO)

        with self.assertRaises(WidthRangeError):
            validate_max_width([-1])

    def test_validate_range_raises(self):

        with self.assertRaises(WidthRangeError):
            validate_range(IMAGE_ZERO_WIDTH, IMAGE_ZERO_WIDTH)

        with self.assertRaises(WidthRangeError):
            validate_range(IMAGE_ZERO_WIDTH, IMAGE_MAX_WIDTH)

        with self.assertRaises(WidthRangeError):
            validate_range(IMAGE_MAX_WIDTH, IMAGE_MIN_WIDTH)

    def test_validate_min_max_tol_raises(self):

        with self.assertRaises(WidthToleranceError):
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

    def test_start_equals_stop(self):
        # Due to the assertive nature of this validator
        # if this test does not raise, it passes.
        for x, y in enumerate([x for x in range(1, 10)], start=1):
            assert x == y
            validate_range(x, y)

    def test_validate_widths_raise(self):
        with self.assertRaises(WidthRangeError):
            validate_widths([2, 3, 4, 5, 6, -7])
