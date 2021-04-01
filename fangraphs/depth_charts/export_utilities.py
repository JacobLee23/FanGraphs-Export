#! python3
# fangraphs/depth_charts/export_utilities.py

import csv
import os


def _write_table_headers(writer: csv.writer, node, headers_sel):
    elems = node.select(headers_sel)
    headers = [e.getText() for e in elems]
    writer.writerow(headers)


def _write_table_rows(writer: csv.writer, node, rows_sel):
    elems = node.select(rows_sel)
    rows = [[e.getText() for e in row.select("td")] for row in elems]
    writer.writerows(rows)


class Export:
    """
    Exports the **Depth Charts** data tables.
    """
    headers = "thead > tr > th"
    rows = "tr[class*='depth']"
    tables = "#content > div > table"
    table_names = "#content > div > a"

    def __init__(self, ttype, soup, path):
        ttype = ttype.lower()
        if ttype in ["standings", "baseruns"]:
            self.__insertat = 0
        elif ttype in ["depth charts", "position"]:
            self.__insertat = -1
        else:
            raise Exception
        self.soup = soup
        self.path = os.path.normpath(path)

    def get_tables(self):
        tables_sel = self.soup.select(self.tables)
        tnames_sel = self.soup.select(self.table_names)
        tnames = [e.getText() for e in tnames_sel]
        tnames.insert(self.__insertat, "General")
        tables = dict(zip(tnames, tables_sel))
        return tables

    def export(self):
        tables = self.get_tables()
        for tname, telem in tables.items():
            filepath = os.path.join(self.path, f"{tname}.csv")
            with open(filepath, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                _write_table_headers(writer, telem, self.headers)
                _write_table_rows(writer, telem, self.rows)
