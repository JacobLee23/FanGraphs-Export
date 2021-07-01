#! python3
# FanGraphs/selectors/__init__.py

import datetime
from typing import *

import bs4

import fangraphs.exceptions


class Selectors:
    """

    """
    def __init__(self, page):
        """
        :type page: playwright.sync_api._generated.Page
        """
        self.soup = bs4.BeautifulSoup(page.content(), features="lxml")
        if (d := self.__dict__.get("_selections")) is not None and isinstance(d, dict):
            for attr, kwargs in d.items():
                self.__setattr__(attr, Selection(self.soup, **kwargs))


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


class Selection:
    """

    """
    descendants = (
        "ul > li", "a", "div.button-green.fgButton"
    )

    def __init__(
            self, soup: bs4.BeautifulSoup, /, *,
            css_selector: Optional[str] = None,
            css_selectors: Optional[list[str]] = None,
    ):
        """
        :param soup:
        :param css_selector:
        :param css_selectors:
        """
        if not any((css_selector, css_selectors)):
            raise ValueError
        if all((css_selector, css_selectors)):
            raise ValueError

        self.soup = soup

        self.css_selector = css_selector
        self.css_selectors = css_selectors
        self.desc_selector = ""

        self.options = ()
        self.current = ""

    @property
    def options(self) -> tuple:
        return self._options

    @options.setter
    def options(self, value) -> None:
        """

        """
        options = []
        if self.css_selectors is not None:
            options = [
                e.text for e in [
                    self.soup.select_one(s) for s in self.css_selectors
                ]
            ]
        elif self.css_selector is not None:
            root_elem = self.soup.select_one(self.css_selector)
            for desc in self.descendants:
                if elems := root_elem.select(desc):
                    options = [e.text for e in elems]
                    self.desc_selector = desc
        self._options = tuple(options)

    @property
    def current(self) -> str:
        return self._current

    @current.setter
    def current(self, value) -> None:
        """

        """
        option = ""
        if self.css_selectors is not None:
            for path in self.css_selectors:
                root_elem = self.soup.select_one(path)
                if "active" in root_elem.attrs.get("class"):
                    option = root_elem.text
                    break
        elif self.css_selector is not None:
            root_elem = self.soup.select_one(self.css_selector)
            if self.desc_selector == self.descendants[0]:
                option = e.text if (
                    e := root_elem.select_one(".rtsLink.rtsSelected")
                ) else ""
            elif self.desc_selector == self.descendants[1]:
                elems = self.soup.select(self.css_selector)
                for elem in elems:
                    if "active" in elem.attrs.get("class"):
                        option = elem.text
            elif self.desc_selector == self.descendants[2]:
                elem = root_elem.select_one(
                    "div.button-green.fgButton.active.isActive"
                )
                option = elem.text
        self._current = option

    def configure(self, page, option: str) -> None:
        """

        :type page: playwright.sync_api._generated.Page
        :param option:
        """
        options = [o.lower() for o in self.options]
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption(option) from err

        if self.css_selectors is not None:
            page.click(self.css_selectors[index])
        elif self.css_selector is not None:
            page.query_selector(
                self.css_selector
            ).query_selector_all(self.desc_selector)[index].click()


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
        self.__dd_root = self.page.query_selector(self.dd_options)

    def list_options(self):
        """

        :return:
        :rtype: list[str]
        """
        elems = self.page.query_selector(
            self.dd_options
        ).query_selector_all("ul > li")
        options = [e.text_content() for e in elems]
        return options

    def current_option(self):
        """

        :return:
        :rtype: str
        """
        option = self.page.query_selector(
            self.selector
        ).get_attribute("value")
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
        elem = self.page.query_selector(
            self.selector
        ).query_selector_all("ul > li")[index]
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

    def list_options(self):
        """

        :return:
        :rtype: list[str]
        """
        elems = self.page.query_selector(
            self.selector
        ).query_selector_all("a")
        options = [e.text_content() for e in elems]
        return options

    def current_option(self):
        """

        :return:
        :rtype: str
        """
        elem = self.page.query_selector(
            self.selector
        ).query_selector("span")
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
        elem = self.page.query_selector(
            self.selector
        ).query_selector_all("a")[index]
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

    def list_options(self):
        """

        :return:
        :rtype: list[str]
        """
        elems = self.page.query_selector(
            self.selector
        ).query_selector_all("ul > li")
        options = [e.text_content() for e in elems]
        return options

    def current_option(self, *, multiple=True):
        """

        :param multiple:
        :return:
        :rtype: str or list
        """
        elems = self.page.query_selector(
            self.selector
        ).query_selector_all("ul > li")
        option = [
            e.text_content() for e in elems
            if "highlight" in e.get_attribute("class")
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
        elem = self.page.query_selector(
            self.selector
        ).query_selector_all("ul > li")[index]
        elem.click()


class DropdownsType4(__Selectors):
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

    def list_options(self):
        """

        :return:
        :rtype: list[str]
        """
        elems = self.page.query_selector(
            self.selector
        ).query_selector_all("option")
        options = [e.text_content() for e in elems]
        return options

    def current_option(self):
        """

        :return:
        :rtype: str
        """
        option = self.page.eval_on_selector(
            self.selector, "el => el.value"
        )
        return option

    def configure(self, option: str):
        """

        :param option:
        :rtype: None
        """
        for opt in self.list_options():
            if opt.lower() == option.lower():
                self.page.select_option(self.selector, label=opt)
                return
        raise fangraphs.exceptions.InvalidFilterOption(option)


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

    def list_options(self):
        """

        :return: list[bool]
        """
        return [True, False]

    def current_option(self):
        """

        :return: bool
        """
        return self.page.query_selector(
            self.selector
        ).is_checked()

    def configure(self, option: bool):
        """

        :param option:
        :return:
        """
        if option is not self.current_option():
            self.page.click(self.selector)


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
        option = "isActive" in self.page.query_selector(
            self.selector
        ).get_attribute("class")
        return option

    def configure(self, option: bool):
        """

        :param option:
        :rtype: None
        """
        if option is not self.current_option():
            self.page.click(self.selector)


class Calendars(__Selectors):
    """

    """

    def __init__(self, page, btn_selector: str, calendar: str, selector: str):
        """
        :param page: A Playwright ``Page`` object
        :type page: playwright.sync_api._generated.Page
        :param btn_selector:
        :param calendar:
        :param selector:
        """
        super().__init__()
        self.page = page
        self.btn_selector = btn_selector
        self.calendar = calendar
        self.selector = selector

        self.fast_prev = f"{self.calendar} > a.rcFastPrev"
        self.prev = f"{self.calendar} > a.rcPrev"
        self.next = f"{self.calendar} > a.rcNext"
        self.fast_next = f"{self.calendar} > a.rcFastNext"

    def list_options(self):
        """

        :return:
        :rtype: list[datetime.datetime]
        """
        self.page.click(self.btn_selector)
        self.page.click(self.fast_prev)

        options = []

        def get_current_month():
            return self.page.query_selector(
                f"{self.calendar} > span.rcTitle"
            ).text_content()

        while True:
            curr_month = get_current_month()

            table = self.page.query_selector(self.calendar)
            weeks = table.query_selector_all("tbody > tr.rcRow")
            for week in weeks:
                dates = [
                    d.get_attribute("title") for d in week.query_selector_all(
                        "td[title]"
                    )
                ]
                formatted_dates = [
                    datetime.datetime.strptime(
                        d, "%A, %B %d, %Y"
                    ) for d in dates
                ]
                options.extend(formatted_dates)

            self.page.click(self.next)
            if curr_month == get_current_month():
                return options

    def current_option(self):
        """

        :return:
        :rtype: datetime.datetime
        """
        elem = self.page.query_selector(
            f"{self.selector} > input"
        )
        option = datetime.datetime.strptime(
            elem.get_attribute("value"), "%m/%d/%Y"
        )
        return option

    def configure(self, option):
        """

        :param option:
        :type option: datetime.datetime
        :rtype: None
        """
        curr_date = self.current_option()
        date = option.strftime("%m/%d/%Y")
        self.page.fill(
            f"{self.selector} > input", date
        )
        if self.current_option() == curr_date:
            raise fangraphs.exceptions.InvalidFilterOption(option)
