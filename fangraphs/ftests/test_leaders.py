#! python3
# fangraphs/ftests/test_leaders.py

"""
Functional tests for :py:mod:`fangraphs.leaders`.
"""

from fangraphs import fangraphs_scraper
from fangraphs import leaders
from fangraphs.selectors import leaders_sel as ls


class TestGameSpan:

    def test_all(self):
        fangraphs_scraper(self.__run_all_tests)(leaders.GameSpan)

    @staticmethod
    def __run_all_tests(scraper):
        TestGameSpan._test_list_queries(scraper)
        TestGameSpan._test_list_options(scraper)
        TestGameSpan._test_current_option(scraper)
        TestGameSpan._test_configure(scraper)

    @staticmethod
    def _test_list_queries(scraper):
        queries = []
        for vals in vars(ls.GameSpan).values():
            if isinstance(vals, dict):
                queries.extend(list(vals))
        assert sorted(queries) == sorted(scraper.list_queries())

    @staticmethod
    def _test_list_options(scraper):
        for qry in scraper.list_queries():
            options = vars(scraper.queries)[qry].list_options()
            assert options == scraper.list_options(qry), qry

    @staticmethod
    def _test_current_option(scraper):
        for qry in scraper.list_queries():
            option = vars(scraper.queries)[qry].current_option()
            assert option == scraper.current_option(qry), qry

    @staticmethod
    def _test_configure(scraper):
        for qry in scraper.list_queries():
            option = vars(scraper.queries)[qry].list_options()[1]
            scraper.configure(qry, option)
            assert option == scraper.current_option(qry), qry
            scraper.reset()
