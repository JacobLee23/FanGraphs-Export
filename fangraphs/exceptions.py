#! python3
# FanGraphs/exceptions.py

"""
The warnings and exceptions used by modules in the package.
"""


class FilterUpdateIncapability(Warning):
    """
    Raised when the filter queries cannot be updated.
    This usually occurs when no filter queries have been configured since the last update.
    """
    def __init__(self):
        self.message = "No filter query configurations to update"
        super().__init__(self.message)


class UnknownBrowser(Exception):
    """
    Raised when the browser name given is not recognized.
    """
    def __init__(self, browser):
        """
        :param browser: The name of the browser used
        """
        self.browser = browser
        self.message = f"No browser named '{self.browser}' was recognized"
        super().__init__(self.message)


class InvalidFilterGroup(Exception):
    """
    Raised when an invalid filter group is used.
    """
    def __init__(self, group):
        """
        :param group: The filter group used
        """
        self.group = group
        self.message = f"No filter group names '{self.group}' could be found"
        super().__init__(self.message)


class InvalidFilterQuery(Exception):
    """
    Raised when an invalid filter query is used.
    """
    def __init__(self, query):
        """
        :param query: The filter query used
        """
        self.query = query
        self.message = f"No filter named '{self.query}' could be found"
        super().__init__(self.message)


class InvalidFilterOption(Exception):
    """
    Raised when a filter query is configured to a nonexistend option.
    """
    def __init__(self, query, option):
        """
        :param query: The filter query used
        :param option: The option which the filter query was configured to
        """
        self.query, self.option = query, option
        self.message = f"No option '{self.option}' could be found for query '{self.query}'"
        super().__init__(self.message)


class InvalidQuickSplit(Exception):
    """
    Raised when an invalid quick split is used.
    """
    def __init__(self, quick_split):
        """
        :param quick_split: The quick split used
        """
        self.quick_split = quick_split
        self.message = f"No quick split '{self.quick_split}` could be found"
        super().__init__(self.message)
