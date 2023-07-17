from typing import List
from pylenium.driver import Pylenium
import pytest
import requests
class Portfolio:
    def __init__(self, py: Pylenium):
        self.py = py

    def goto(self) -> 'Portfolio':
        self.py.visit('https://www.bassettmason.com/portfolio')
        return self

    def get_heading(self):
        return self.py.get('h2.elementor-heading-title.elementor-size-default')

    def get_nav_items(self):
        # Locate all nav items
        nav_items = self.py.find('.elementor-icon-list-item .elementor-icon-list-text')
        return nav_items

    def click_nav_item(self, index: int):
        self.get_nav_items()[index].click()

    def get_all_links(self):
        return self.py.find('a')
    

@pytest.fixture
def portfolio(py: Pylenium):
    return Portfolio(py).goto()

def test_nav_items(portfolio: Portfolio, py: Pylenium):
    nav_items = portfolio.get_nav_items()

    assert nav_items[0].text() == 'Home'
    portfolio.click_nav_item(0)
    assert py.should().contain_url('https://www.bassettmason.com/')

    portfolio.goto()  # navigate back to the portfoliopage
    nav_items = portfolio.get_nav_items()  # re-fetch nav items

    assert nav_items[1].text() == 'Portfolio'
    portfolio.click_nav_item(1)
    assert py.should().contain_url('https://www.bassettmason.com/portfolio')

    portfolio.goto()  # navigate back to the portfoliopage
    nav_items = portfolio.get_nav_items()  # re-fetch nav items

    assert nav_items[2].text() == 'Contact'
    portfolio.click_nav_item(2)
    assert py.should().contain_url('https://www.bassettmason.com/contact')


def test_no_broken_links(portfolio: Portfolio):
    links = portfolio.get_all_links()

    for link in links:
        url = link.get_attribute('href')

        # If the href attribute is None, skip this link
        if url is None:
            continue

        response = requests.get(url)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f"Broken link found: {url}")
            raise SystemExit(err)

