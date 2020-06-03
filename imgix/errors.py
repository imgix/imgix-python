class Error(Exception):
    """Base class for exceptions in the imgix module."""

    def __init__(self, message):
        """Initialize the `Error` with a `message` explaining why the
        exception occurred.

        Parameters
        ----------
        message : str
            A brief description explaining why the exception occurred.
        """
        self.message = message


class DomainError(Error):
    """Exception raised for an invalid domain string."""


class WidthRangeError(Error):
    """Exception raised for an invalid width range."""


class WidthToleranceError(Error):
    """Exception raised for an invalid width `tol`erance."""
