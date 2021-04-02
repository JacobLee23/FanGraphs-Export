#! python3
# fangraphs/teams/__init__.py

import csv
import os

from fangraphs import ScrapingUtilities
from fangraphs import selectors
import fangraphs.exceptions
from fangraphs.selectors import teams_sel


class DepthCharts(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Depth Charts`_ page.

    .. _Depth Charts: https://fangraphs.com/depthcharts.aspx
    """
    __selections = {}
    __dropdowns = {}

    address = "https://fangraphs.com/depthcharts.aspx"

    def __init__(self):
        super().__init__(
            self.address, selector_mod=teams_sel.DepthCharts
        )
        self.__enter__()

    def __enter__(self):
        self._browser_init()
        self.reset()
        self.__compile_selectors()
        return self

    def __exit__(self, exc_type, value, traceback):
        self.quit()

    def __compile_selectors(self):
        for cat, sel in teams_sel.DepthCharts.selections.items():
            self.__selections.setdefault(
                cat, selectors.Selections(self.soup, sel, "> div > ul > li")
            )
        for cat, sel in teams_sel.DepthCharts.dropdowns.items():
            self.__dropdowns.setdefault(
                cat, selectors.Dropdowns(self.soup, sel, "> ul > a")
            )

    @classmethod
    def list_queries(cls):
        queries = []
        queries.extend(list(cls.__selections))
        return queries

    def list_options(self, query: str):
        query = query.lower()
        if query in self.__selections:
            options = self.__selections[query].list_options()
        elif query in self.__dropdowns:
            options = self.__dropdowns[query].list_options()
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return options

    def current_option(self, query: str):
        query = query.lower()
        if query in self.__selections:
            option = self.__selections[query].current_option()
        elif query in self.__dropdowns:
            option = self.__dropdowns[query].current_option()
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return option

    def configure(self, query: str, option: str):
        query = query.lower()
        if query in self.__selections:
            self.__selections[query].configure(self.page, option)
        elif query in self.__dropdowns:
            self.__selections[query].configure(self.page, option)
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)

    def export(self, *, path):
        self._close_ad()
        current_type = self.current_option("type")
        exp = _Export(
            current_type, self.soup, path
        )
        exp.export()


def _write_table_headers(writer: csv.writer, node, headers_sel):
    elems = node.select(headers_sel)
    headers = [e.getText() for e in elems]
    writer.writerow(headers)


def _write_table_rows(writer: csv.writer, node, rows_sel):
    elems = node.select(rows_sel)
    rows = [[e.getText() for e in row.select("td")] for row in elems]
    writer.writerows(rows)


class _Export:
    """
    Exports the **Depth Charts** data tables.
    """
    headers = "thead > tr > th"
    rows = "tr[class*='depth']"
    tables = "#content > div > table"
    table_names = "#content > div > a"

    def __init__(self, ttype, soup, path):
        self.ttype = ttype.lower()
        self.soup = soup
        if not os.path.isdir(path):
            raise Exception(
                "Argument 'path' must be a valid path to a directory"
            )
        self.path = os.path.normpath(path)

    def _get_tables(self):
        tables_sel = self.soup.select(self.tables)
        tnames_sel = self.soup.select(self.table_names)
        tnames = [e.getText() for e in tnames_sel]
        if self.ttype in ["standings", "baseruns", "totals"]:
            tnames.insert(0, "General")
        elif self.ttype in [
            "depth charts",
            "C", "1B", "2B", "3B", "LF", "CF", "RF", "SP", "RP", "DH"
        ]:
            tnames.append("General")
        else:
            raise Exception
        tables = dict(zip(tnames, tables_sel))
        return tables

    def export(self):
        tables = self._get_tables()
        for tname, telem in tables.items():
            filepath = os.path.join(self.path, f"{tname}.csv")
            with open(filepath, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                _write_table_headers(writer, telem, self.headers)
                _write_table_rows(writer, telem, self.rows)
