import pytest


@pytest.mark.login
def test_login_button_visible():
    print("Login button visible")
    assert True


@pytest.mark.login
@pytest.mark.logout
def test_login_button_clickable():
    print("Login button clickable")
    assert True


@pytest.mark.login
@pytest.mark.testing
def test_login_button_enabled():
    print("Login button enabled")
    assert True
