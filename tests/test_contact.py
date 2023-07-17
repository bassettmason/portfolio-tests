from typing import List
from pylenium.driver import Pylenium
import pytest
import requests
class Contact:
    def __init__(self, py: Pylenium):
        self.py = py

    def goto(self) -> 'Contact':
        self.py.visit('https://www.bassettmason.com/contact')
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
def contact(py: Pylenium):
    return Contact(py).goto()


def test_nav_items(contact: Contact, py: Pylenium):
    nav_items = contact.get_nav_items()

    assert nav_items[0].text() == 'Home'
    contact.click_nav_item(0)
    assert py.should().contain_url('https://www.bassettmason.com/')

    contact.goto()  
    nav_items = contact.get_nav_items()  # re-fetch nav items

    assert nav_items[1].text() == 'Portfolio'
    contact.click_nav_item(1)
    assert py.should().contain_url('https://www.bassettmason.com/portfolio')

    contact.goto()  
    nav_items = contact.get_nav_items()  # re-fetch nav items

    assert nav_items[2].text() == 'Contact'
    contact.click_nav_item(2)
    assert py.should().contain_url('https://www.bassettmason.com/contact')