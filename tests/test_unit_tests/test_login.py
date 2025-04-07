import pytest
import time


@pytest.mark.login
def test_login_button_visible():
    print("Login button visible")
    time.sleep(3)
    assert True


@pytest.mark.login
@pytest.mark.logout
def test_login_button_clickable():
    print("Login button clickable")
    time.sleep(1)
    assert True


@pytest.mark.login
@pytest.mark.testing
def test_login_button_enabled():
    print("Login button enabled")
    time.sleep(1)
    assert True
