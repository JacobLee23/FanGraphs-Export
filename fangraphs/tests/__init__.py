#! python3
# tests/__init__.py

from urllib.request import urlopen

from playwright.sync_api import sync_playwright
import pytest


class BaseTests:

    address = ""

    def test_address(self):
        res = urlopen(self.address)
        assert res.getcode() == 200


@pytest.fixture(scope="module")
def page(request):
    with sync_playwright() as play:
        try:
            browser = play.chromium.launch()
            webpage = browser.new_page()
            webpage.goto(
                request.getfixturevalue(request.param),
                timeout=0.0
            )
            yield webpage
        finally:
            browser.close()
