#! python3
# FanGraphs/exceptions.py


class InvalidFilterQuery(Exception):

    def __init__(self, query):
        """
        Raised when an invalid filter query is used.

        :param query: The filter query used
        """
        self.query = query
        self.message = f"No filter named '{self.query}' could be found"
        super().__init__(self.message)
