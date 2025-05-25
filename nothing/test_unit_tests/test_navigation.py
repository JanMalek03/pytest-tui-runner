import pytest


@pytest.mark.navigation
@pytest.mark.menu
def test_navigation_bar_visible():
    print("Navigation bar visible")
    assert True


@pytest.mark.navigation
@pytest.mark.test
def test_navigation_bar_clickable():
    print("Navigation bar clickable")
    assert True
