from typing import List
from pylenium.driver import Pylenium
import pytest
import requests
class Home:
    def __init__(self, py: Pylenium):
        self.py = py

    def goto(self) -> 'Home':
        self.py.visit('https://www.bassettmason.com/')
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
def home(py: Pylenium):
    return Home(py).goto()

def test_heading(home: Home):
    assert home.get_heading().should().contain_text('Mason Bassett')

def test_nav_items(home: Home, py: Pylenium):
    nav_items = home.get_nav_items()

    assert nav_items[0].text() == 'Home'
    home.click_nav_item(0)
    assert py.should().contain_url('https://www.bassettmason.com/')

    home.goto()  # navigate back to the homepage
    nav_items = home.get_nav_items()  # re-fetch nav items

    assert nav_items[1].text() == 'Portfolio'
    home.click_nav_item(1)
    assert py.should().contain_url('https://www.bassettmason.com/portfolio')

    home.goto()  # navigate back to the homepage
    nav_items = home.get_nav_items()  # re-fetch nav items

    assert nav_items[2].text() == 'Contact'
    home.click_nav_item(2)
    assert py.should().contain_url('https://www.bassettmason.com/contact')


def test_no_broken_links(home: Home):
    links = home.get_all_links()

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

