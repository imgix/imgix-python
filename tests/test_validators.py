import unittest

from imgix.constants import IMAGE_MIN_WIDTH, IMAGE_MAX_WIDTH, \
    IMAGE_ZERO_WIDTH

from imgix.validators import validate_min_width, validate_max_width, \
    validate_range

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