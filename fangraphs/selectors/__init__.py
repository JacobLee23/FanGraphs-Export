#! python3
# FanGraphs/selectors/__init__.py

import fangraphs.exceptions


class Selections:
    """
    Manages selection-class filter queries.
    """
    def __init__(self, soup, selector, descendant=""):
        self.soup = soup
        self.selector = selector
        self.descendant = descendant

    def list_options(self):
        if isinstance(self.selector, str):
            elems = self.soup.select(f"{self.selector} {self.descendant}")
        elif isinstance(self.selector, list):
            elems = [
                self.soup.select(s)[0]
                for s in self.selector
            ]
        else:
            raise Exception
        options = [e.getText() for e in elems]
        return options

    def current_option(self):
        if isinstance(self.selector, str):
            elem = self.soup.select(f"{self.selector} .rtsLink.rtsSelected")[0]
            option = elem.getText() if elem else ""
        elif isinstance(self.selector, list):
            option = ""
            for sel in self.selector:
                elem = self.soup.select(sel)[0]
                if "active" in elem.get("class"):
                    option = elem.getText()
        else:
            raise Exception
        return option

    async def configure(self, page, option: str):
        option = option.lower()
        options = [o.lower() for o in self.list_options()]
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption(option) from err
        if isinstance(self.selector, str):
            elem = await page.query_selector_all(
                f"{self.selector} {self.descendant}"
            )[index]
            await elem.click()
        elif isinstance(self.selector, list):
            await page.click(self.selector[index])
        else:
            raise Exception


class Dropdowns:
    """
    Manage dropdown-class filter queries.
    """
    def __init__(self, soup, selector, descendants="", dd_options=None):
        self.soup = soup
        self.selector = selector
        self.descendants = descendants
        self.dd_options = dd_options

    def list_options(self):
        if self.dd_options:
            elems = self.soup.select(f"{self.dd_options} {self.descendants}")
            options = [e.getText() for e in elems]
        else:
            elems = self.soup.select(f"{self.selector} {self.descendants}")
            options = [e.getText() for e in elems]
        return options

    def current_option(self, opt_type, *, multiple=False):
        if opt_type == 1:
            elem = self.soup.select(self.selector)[0]
            option = elem.get("value")
        elif opt_type == 2:
            elems = self.soup.select(f"{self.selector} {self.descendants}")
            option = [
                e.getText() for e in elems
                if "highlight-selection" in e.get("class")
            ]
            if not multiple:
                option = option[0] if option else ""
        elif opt_type == 3:
            elem = self.soup.select(f"{self.selector} > div > span")[0]
            option = elem.getText()
        else:
            raise Exception
        return option

    async def configure(self, page, option: str):
        options = [o.lower() for o in self.list_options()]
        try:
            index = options.index(option.lower())
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption(option) from err
        await page.click(self.selector)
        elem = await page.query_selector_all(
            f"{self.selector} {self.descendants}"
        )[index]
        await elem.click()


class Switches:
    """
    Manages checkbox-class filter queries.
    """
    def __init__(self, soup, selector):
        self.soup = soup
        self.selector = selector

    def current_option(self, opt_type):
        if opt_type == 1:
            elem = self.soup.select(self.selector)[0]
            option = "True" if elem.get("checked") == "checked" else "False"
        elif opt_type == 2:
            elem = self.soup.select(self.selector)[0]
            option = "True" if "isActive" in elem.get("class") else "False"
        else:
            raise Exception
        return option
