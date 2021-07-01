#! usr/bin/env python
# fangraphs/selectors/__init__.py

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
        self.page = page
        self.soup = bs4.BeautifulSoup(page.content(), features="lxml")

        if (d := self.__dict__.get("_selections")) is not None and isinstance(d, dict):
            for attr, kwargs in d.items():
                self.__setattr__(attr, Selection(self.page, self.soup, **kwargs))
        if (d := self.__dict__.get("_dropdowns")) is not None and isinstance(d, dict):
            for attr, kwargs in d.items():
                self.__setattr__(attr, Dropdown(self.page, self.soup, **kwargs))
        if (d := self.__dict__.get("_checkboxes")) is not None and isinstance(d, dict):
            for attr, kwargs in d.items():
                self.__setattr__(attr, Checkbox(self.page, self.soup, **kwargs))
        if (d := self.__dict__.get("_switches")) is not None and isinstance(d, dict):
            for attr, kwargs in d.items():
                self.__setattr__(attr, Switch(self.page, self.soup, **kwargs))


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
            self, page, soup: bs4.BeautifulSoup, /, *,
            root_selector: Optional[str] = None,
            root_selectors: Optional[list[str]] = None,
    ):
        """
        :param page:
        :type page: playwright.sync_api._generated.Page
        :param soup:
        :param root_selector:
        :param root_selectors:
        """
        if not any((root_selector, root_selectors)):
            raise ValueError
        if all((root_selector, root_selectors)):
            raise ValueError

        self.page = page
        self.soup = soup

        self.root_selector = root_selector
        self.root_selectors = root_selectors
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
        options = ()

        if self.root_selectors is not None:
            # Get options from texts of listed elements
            options = [
                e.text for e in [
                    self.soup.select_one(s) for s in self.root_selectors
                ]
            ]

        elif self.root_selector is not None:
            root_elem = self.soup.select_one(self.root_selector)
            # Iterate through possible descendant elements
            for desc in self.descendants:
                if elems := root_elem.select(desc):
                    # Get options from texts of descendant elements
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

        if self.root_selectors is not None:
            # Iterate through elements and select current option
            for path in self.root_selectors:
                elem = self.soup.select_one(path)
                if "active" in elem.attrs.get("class"):
                    option = elem.text
                    break

        elif self.root_selector is not None:
            root_elem = self.soup.select_one(self.root_selector)

            if self.desc_selector == self.descendants[0]:
                # Get current option from text of descendant element
                option = e.text if (
                    e := root_elem.select_one(".rtsLink.rtsSelected")
                ) else ""
            elif self.desc_selector == self.descendants[1]:
                # Get current option from text of active option element
                elems = root_elem.select(self.desc_selector)
                for elem in elems:
                    if "active" in elem.attrs.get("class"):
                        option = elem.text
            elif self.desc_selector == self.descendants[2]:
                # Get current option from text of descendant element
                elem = root_elem.select_one(
                    "div.button-green.fgButton.active.isActive"
                )
                option = elem.text

        self._current = option

    def configure(self, option: str) -> None:
        """

        :param option:
        """
        # Get index of appropriate option, if applicable
        options = [o.lower() for o in self.options]
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption(option) from err

        if self.root_selectors is not None:
            # Click appropriate selection option
            self.page.click(self.root_selectors[index])

        elif self.root_selector is not None:
            # Click appropriate selection option
            root_elem = self.page.query_selector(self.root_selector)
            opt_elem = root_elem.query_selector_all(self.desc_selector)[index]
            opt_elem.click()


class Dropdown:
    """

    """
    descendants = (
        "ul > li", "a", "option"
    )

    def __init__(self, page, soup: bs4.BeautifulSoup, /, *,
                 root_selector: str,
                 dropdown_selector: Optional[str] = None,
                 button_selector: Optional[str] = None
                 ):
        """
        :type page: playwright.sync_api._generated.Page
        :param soup:
        :param root_selector:
        """
        self.page = page
        self.soup = soup

        self.root_selector = root_selector
        self.dropdown_selector = dropdown_selector
        self.button_selector = button_selector
        self.desc_selector = ""

        self.options = ()
        self.current = ""
        self.currents = ()

    @property
    def options(self) -> tuple[str]:
        """

        :return:
        """
        return self._options

    @options.setter
    def options(self, value) -> None:
        """

        """
        options = ()

        if self.dropdown_selector is not None:
            # Get options from texts of descendant elements
            root_elem = self.soup.select_one(self.dropdown_selector)
            self.desc_selector = self.descendants[0]
            options = [e.text for e in root_elem.select(self.desc_selector)]

        else:
            root_elem = self.soup.select_one(self.root_selector)
            # Iterate through possible descendant elements
            for desc in self.descendants:
                if elems := root_elem.select(desc):
                    # Get options from texts of descendant elements
                    options = [e.text_content() for e in elems]
                    self.desc_selector = desc

        self._options = tuple(options)

    @property
    def current(self) -> str:
        """

        :return:
        """
        return self._current

    @current.setter
    def current(self, value) -> None:
        """

        """
        option = ""
        root_elem = self.soup.select_one(self.root_selector)

        if self.desc_selector in (self.descendants[0], self.descendants[2]):
            if self.dropdown_selector is not None:
                # Get current option from element 'value' attribute
                option = root_elem.attrs.get("value")
            else:
                # Get current options from element text (multi-select widget)
                options = [
                    e.text for e in root_elem.select("ul > li")
                    if "highlight" in e.attrs.get("class")
                ]
                option = options[0]
                self.currents = tuple(options)
        elif self.desc_selector == self.descendants[1]:
            # Get current option from text of descendant element
            option = root_elem.select_one("span").text

        elif self.desc_selector == self.descendants[3]:
            # Evaluate JavaScript on element to get current option
            option = self.page.eval_on_selector(
                self.root_selector, "el => el.value"
            )

        self._current = option

    def configure(self, option: str) -> None:
        """

        :param option:
        """
        if self.desc_selector in self.descendants[:3]:
            # Get index of appropriate option, if applicable
            options = [o.lower() for o in self.options]
            try:
                index = options.index(option.lower())
            except ValueError as err:
                raise fangraphs.exceptions.InvalidFilterOption(option) from err

            # Click dropdown menu to display options
            self.page.click(self.root_selector)

            # Click appropriate dropdown option
            root_elem = self.page.query_selector(self.root_selector)
            opt_elem = root_elem.query_selector_all(self.desc_selector)[index]
            opt_elem.click()

            if self.button_selector is not None:
                # Submit form with button, if necessary
                self.page.click(self.button_selector)

        elif self.desc_selector == self.descendants[3]:
            # Iterate through options and find appropriate option
            for opt in self.options:
                if opt.lower() == option.lower():
                    # Select corresponding option
                    self.page.select_option(self.root_selector, label=opt)
                    return

            raise fangraphs.exceptions.InvalidFilterOption(option)


class Checkbox:
    """

    """
    def __init__(self, page, soup: bs4.BeautifulSoup, /, *,
                 root_selector: str):
        """
        :type page: playwright.sync_api._generated.Page
        :param soup:
        :param root_selector:
        """
        self.page = page
        self.soup = soup

        self.root_selector = root_selector

        self.options = ()
        self.current = None

    @property
    def options(self) -> tuple:
        """

        """
        return self._options

    @options.setter
    def options(self, value) -> None:
        """

        """
        options = (True, False)
        self._options = options

    @property
    def current(self) -> bool:
        """

        """
        return self._current

    @current.setter
    def current(self, value) -> None:
        """

        """
        option = self.page.query_selector(
            self.root_selector
        ).is_checked()
        self._current = option

    def configure(self, option: bool) -> None:
        """

        :param option:
        """
        if option is not self.current:
            self.page.click(self.root_selector)


class Switch:
    """

    """
    def __init__(self, page, soup: bs4.BeautifulSoup, /, *,
                 root_selector: str):
        """
        :type page: playwright.sync_api._generated.Page
        :param soup:
        :param root_selector:
        """
        self.page = page
        self.soup = soup

        self.root_selector = root_selector

        self.options = ()
        self.current = None

    @property
    def options(self) -> tuple:
        """

        """
        return self._options

    @options.setter
    def options(self, value) -> None:
        """

        """
        options = (True, False)
        self._options = options

    @property
    def current(self) -> bool:
        """

        """
        return self._current

    @current.setter
    def current(self, value) -> None:
        """

        """
        root_elem = self.soup.select_one(self.root_selector)
        option = "isActive" in root_elem.attrs.get("class")
        self._current = option

    def configure(self, option: bool) -> None:
        """

        :param option:
        """
        if option is not self.current:
            self.page.click(self.root_selector)


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
