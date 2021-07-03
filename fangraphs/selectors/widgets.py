#! usr/bin/env python
# fangraphs/selectors/__init__.py

from typing import *

import bs4

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


WIDGET_TYPES = {
    "_selections": Selection,
    "_dropdowns": Dropdown,
    "_checkboxes": Checkbox,
    "_switches": Switch
}


class Selectors:
    """

    """

    def __init__(self, page):
        """
        :type page: playwright.sync_api._generated.Page
        """
        self.page = page
        self.soup = bs4.BeautifulSoup(page.content(), features="lxml")

        for wname, wclass in WIDGET_TYPES.items():
            if (d := self.__class__.__dict__.get(wname)) is not None:
                if not isinstance(d, dict):
                    raise TypeError
                for attr, kwargs in d.items():
                    self.__setattr__(attr, wclass(self.page, self.soup, **kwargs))

        self.widgets = {}

    @property
    def widgets(self) -> dict[str, Any]:
        """

        """
        return self._widgets

    @widgets.setter
    def widgets(self, value) -> None:
        """

        """
        def get_widgets_by_type(w_type: str) -> Generator[tuple[str, Any], None, None]:
            if (w_names := self.__class__.__dict__.get(w_type)) is not None:
                for name in w_names:
                    yield name, self.__dict__.get(name)

        widgets = {}
        for wtype in list(WIDGET_TYPES):
            widgets.update(dict(get_widgets_by_type(wtype)))

        self._widgets = widgets

    def configure(self, **kwargs) -> None:
        """

        :param kwargs:
        """
        for wname, option in kwargs.items():
            widget = self.widgets.get(wname)
            widget.configure(option)
