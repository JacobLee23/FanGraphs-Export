#! python3
# FanGraphs/exceptions.py

"""
The warnings and exceptions used by modules in the package.
================================================================================
"""


class FilterUpdateIncapabilityWarning(Warning):

    def __init__(self):
        """
        Raised when the filter queries cannot be updated.
        This usually occurs when no filter queries have been configured since the last update.
        """
        self.message = "No filter query configurations to update"
        super().__init__(self.message)


class UnknownBrowserException(Exception):

    def __init__(self, browser):
        """
        Raised when the browser name given is not recognized.

        :param browser: The name of the browser used
        """
        self.browser = browser
        self.message = f"No browser named '{self.browser}' was recognized"
        super().__init__(self.message)


class InvalidFilterQueryException(Exception):

    def __init__(self, query):
        """
        Raised when an invalid filter query is used.

        :param query: The filter query used
        """
        self.query = query
        self.message = f"No filter named '{self.query}' could be found"
        super().__init__(self.message)


class InvalidFilterOptionException(Exception):

    def __init__(self, query, option):
        """
        Raised when a filter query is configured to a nonexistend option

        :param query: The filter query used
        :param option: The option which the filter query was configured to
        """
        self.query, self.option = query, option
        self.message = f"No option '{self.option}' could be found for query '{self.query}'"
        super().__init__(self.message)


class InvalidQuickSplitException(Exception):

    def __init__(self, quick_split):
        """

        :param quick_split:
        """
        self.quick_split = quick_split
        self.message = f"No quick split '{self.quick_split}` could be found"
        super().__init__(self.message)
