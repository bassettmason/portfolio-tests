from pylenium.driver import Pylenium


def test_bassettmason(py: Pylenium):
    py.visit('https://www.bassettmason.com/')
    assert py.get('h2.elementor-heading-title.elementor-size-default').should().contain_text('Mason Bassett')