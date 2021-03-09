#! python3
# FanGraphs/exceptions.py


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
