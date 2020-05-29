from .constants import IMAGE_MAX_WIDTH as MAX_WIDTH
from .constants import IMAGE_ZERO_WIDTH as ZERO_WIDTH
from .constants import SRCSET_MIN_WIDTH_TOLERANCE as ONE_PERCENT


def validate_min_width(value):
    """
    Validate the minimum width value.

    This function ensures that the `value`:
    * is of type `int`, or
    * is of type `float`, and
    * is greater than the `ZERO_WIDTH`

    This function is used to ensure custom minimum widths are within
    a valid range. Here, valid means that the minimum width value must
    an int, or a float, and be greater than zero.

    Raises
    ------
    AssertionError
        This function is designed to fail upon invalid input to
        prevent the propagation of invalid state.

    Parameters
    ----------
    value : float, int
        A valid `value` must be a positive numerical value.
    """
    invalid_width_error = '`min_width` must be a positive ' \
        '`float` or `int`'
    assert isinstance(value, (float, int)), invalid_width_error

    invalid_min_error = '`min_width` must be greater than zero'
    assert value > ZERO_WIDTH, invalid_min_error


def validate_max_width(value):
    """
    Validate the maximum width value.

    This function ensures that the `value`:
    * is of type `int`, or
    * is of type `float`, and
    * is greater than the `ZERO_WIDTH`, and
    * is less than or equal to the `MAX_WIDTH`

    This function is used to ensure custom maximum widths are within
    a valid range. Here, valid means that the maximum width value must
    an int, or a float, be greater than zero, and be less than or equal
    to the maximum value.

    Raises
    ------
    AssertionError
        This function is designed to fail upon invalid input to
        prevent the propagation of invalid state.

    Parameters
    ----------
    value : float, int
        A valid `value` must be a positive numerical value.
    """
    invalid_width_error = '`max_width` must be a positive ' \
        '`float` or `int`'
    assert isinstance(value, (float, int)), invalid_width_error

    invalid_max_error = '`max_width` must be <= 8192.0'
    assert ZERO_WIDTH < value <= MAX_WIDTH, invalid_max_error


def validate_range(min_width, max_width):
    """
    Validate the minimum and maximum width values are in range.

    This function ensures that the values `min_width` and `max_width`:
    * each pass their respective validations, i.e. `validate_min_width`
      for `min_width`
    * represent a valid range, i.e. the minimum value is less than the
      maximum value.

    Raises
    ------
    AssertionError
        This function is designed to fail upon invalid input to
        prevent the propagation of invalid state.

    Parameters
    ----------
    min_width : float, int
        The value representing the lower bound, i.e. in the list [1, 2, 3]
        1 is the lower bound.
    max_width : float, int
        The value representing the upper bound, i.e. in the list [1, 2, 3]
        3 is the upper bound.
    """
    validate_min_width(min_width)
    validate_max_width(max_width)

    invalid_range_error = '`min_width` must be less than `max_width`'
    assert min_width <= max_width, invalid_range_error


def validate_width_tol(value):
    """
    Validate the width tolerance.

    This function ensures that the width tolerance `value` is  greater than or
    equal to 0.01, where 0.01 represents a width tolerance of 1%.

    Note: `value` can be either a float or an int (in the case of 1.0 or 100%),
    but this is only to yield flexibility to the caller.

    Parameters
    ----------
    value : float, int
        Numerical value, typically within the range of [0.01, 1]. It can be
        greater than 1, but no less than 0.01.
    """
    invalid_tol_error = 'tolerance `value` must be >= 0.01'
    assert isinstance(value, (float, int)), invalid_tol_error
    assert ONE_PERCENT <= value, invalid_tol_error


def validate_min_max_tol(min_width, max_width, tol):
    """
    Validate the minimum, maximum, and tolerance values.

    This function is composed of two other validators and exists to provide
    convenience at the call site, i.e. instead of calling three functions to
    validate this triplet, one function can be called.

    Parameters
    ----------
    min_width : float, int
        Minimum renderable image width requested, by default.
    max_width : float, int
        Maximum renderable image width requested, by default.
    tol : float, int
        Tolerable amount of image width variation requested, by default.
    """
    validate_range(min_width, max_width)
    validate_width_tol(tol)
