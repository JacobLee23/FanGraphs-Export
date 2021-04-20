#! python3
# FanGraphs/selectors/__init__.py

import fangraphs.exceptions


class __Selectors:
    """
    General parent class which all public :py:mod:`fangraphs.selectors` classes inherit.
    """

    def __init__(self):
        pass

    @staticmethod
    def list_options():
        raise NotImplementedError

    @staticmethod
    def current_option():
        raise NotImplementedError

    @staticmethod
    def configure(option: str):
        raise NotImplementedError


class SelectionsType1(__Selectors):
    """

    """

    def __init__(self, page, selector: str):
        """

        :param page:
        :type page: playwright.sync_api._generated.Page
        :param selector:
        """
        super().__init__()
        self.page = page
        self.selector = selector
        self.__root = self.page.query_selector(selector)

    def list_options(self):
        """

        :return:
        :rtype: list[str]
        """
        elems = self.__root.query_selector_all("ul > li")
        options = [e.text_content() for e in elems]
        return options

    def current_option(self):
        """

        :return:
        :rtype: str
        """
        elem = self.__root.query_selector(".rtsLink.rtsSelected")
        option = elem.text_content() if elem else ""
        return option

    def configure(self, option: str):
        """

        :param option:
        :rtype: None
        """
        option = option.lower()
        options = [o.lower() for o in self.list_options()]
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption(option) from err
        elem = self.__root.query_selector_all("ul > li")[index]
        elem.click()


class SelectionsType2(__Selectors):
    """

    """

    def __init__(self, page, selector: list):
        """

        :param page:
        :type page: playwright.sync_api._generated.Page
        :param selector:
        """
        super().__init__()
        self.page = page
        self.selector = selector

    def list_options(self):
        """

        :return:
        :rtype: list[str]
        """
        elems = [self.page.query_selector(s) for s in self.selector]
        options = [e.text_content() for e in elems]
        return options

    def current_option(self):
        """

        :return:
        :rtype: str
        """
        option = ""
        for sel in self.selector:
            elem = self.page.query_selector(sel)
            if "active" in elem.get_attribute("class"):
                option = elem.text_content()
        return option

    def configure(self, option: str):
        """

        :param option:
        :rtype: None
        """
        option = option.lower()
        options = [o.lower() for o in self.list_options()]
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption(option) from err
        self.page.click(self.selector[index])


class DropdownsType1(__Selectors):
    """
    Web scraper utility for a FanGraphs dropdown widget variation.
    The dropdown option elements are separate from the dropdown menu element.
    """

    def __init__(self, page, selector: str, dd_options: str):
        """

        :param page:
        :type page: playwright.sync_api._generated.Page
        :param selector:
        :param dd_options:
        """
        super().__init__()
        self.page = page
        self.selector = selector
        self.dd_options = dd_options
        self.__root = self.page.query_selector(self.selector)
        self.__dd_root = self.page.query_selector(self.dd_options)

    def list_options(self):
        """

        :return:
        :rtype: list[str]
        """
        elems = self.__dd_root.query_selector_all("ul > li")
        options = [e.text_content() for e in elems]
        return options

    def current_option(self):
        """

        :return:
        :rtype: str
        """
        option = self.__root.get_attribute("value")
        return option

    def configure(self, option: str):
        """

        :param option:
        :rtype: None
        """
        options = [o.lower() for o in self.list_options()]
        try:
            index = options.index(option.lower())
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption(option) from err
        self.page.click(self.selector)
        elem = self.__root.query_selector_all("ul > li")[index]
        elem.click()


class DropdownsType2(__Selectors):
    """
    Web scraper utility for a FanGraphs dropdown widget variation.
    The dropdown option elements are descedants of the dropdown menu element.
    """

    def __init__(self, page, selector: str):
        """

        :param page:
        :type page: playwright.sync_api._generated.Page
        :param selector:
        """
        super().__init__()
        self.page = page
        self.selector = selector
        self.__root = self.page.query_selector(selector)

    def list_options(self):
        """

        :return:
        :rtype: list[str]
        """
        elems = self.__root.query_selector_all("div > a")
        options = [e.text_content() for e in elems]
        return options

    def current_option(self):
        """

        :return:
        :rtype: str
        """
        elem = self.__root.query_selector("div > span")
        option = elem.text_content()
        return option

    def configure(self, option: str):
        """

        :param option:
        :rtype: None
        """
        options = [o.lower() for o in self.list_options()]
        try:
            index = options.index(option.lower())
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption(option) from err
        self.page.click(self.selector)
        elem = self.__root.query_selector_all("div > a")[index]
        elem.click()


class DropdownsType3(__Selectors):
    """

    """
    def __init__(self, page, selector: str):
        """

        :param page:
        :type page: playwright.sync_api._generated.Page
        :param selector:
        """
        super().__init__()
        self.page = page
        self.selector = selector
        self.__root = self.page.query_selector(self.selector)

    def list_options(self):
        """

        :return:
        :rtype: list[str]
        """
        elems = self.__root.query_selector_all("ul > li")
        options = [e.text_content() for e in elems]
        return options

    def current_option(self, *, multiple=True):
        """

        :param multiple:
        :return:
        :rtype: str or list
        """
        elems = self.__root.query_selector_all("ul > li")
        option = [
            e.text_content() for e in elems
            if "highlight-selection" in e.get_attribute("class")
        ]
        if not multiple:
            return option[0] if option else ""
        return option

    def configure(self, option: str):
        """

        :param option:
        :rtype: None
        """
        options = [o.lower() for o in self.list_options()]
        try:
            index = options.index(option.lower())
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption(option) from err
        self.page.click(self.selector)
        elem = self.__root.query_selector_all("ul > li")[index]
        elem.click()


class Checkboxes(__Selectors):

    def __init__(self, page, selector: str):
        """

        :param page:
        :type page: playwright.sync_api._generated.Page
        :param selector:
        """
        super().__init__()
        self.page = page
        self.selector = selector
        self.__root = self.page.query_selector(self.selector)

    def list_options(self):
        """

        :return: list[bool]
        """
        return [True, False]

    def current_option(self):
        """

        :return: bool
        """
        return self.__root.is_checked()

    def configure(self, option: bool):
        """

        :param option:
        :return:
        """
        if option is not self.current_option():
            self.__root.click()


class Switches(__Selectors):

    def __init__(self, page, selector: str):
        """

        :param page:
        :type page: playwright.sync_api._generated.Page
        :param selector:
        """
        super().__init__()
        self.page = page
        self.selector = selector
        self.__root = self.page.query_selector(selector)

    def list_options(self):
        """

        :return: list[bool]
        """
        return [True, False]

    def current_option(self):
        """

        :return:
        :rtype: bool
        """
        option = "isActive" in self.__root.get_attribute("class")
        return option

    def configure(self, option: bool):
        """

        :param option:
        :rtype: None
        """
        if option is not self.current_option():
            self.__root.click()
