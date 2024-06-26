import os

import allure
import pytest
from selene import browser
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import attach

DEFAULT_BROWSER_VERSION = '122.0'


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='122.0'
    )


@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    browser.config.window_width = 1366
    browser.config.window_height = 768

    browser.config.base_url = 'https://demoqa.com'

    browser_version = request.config.getoption('--browser_version') or DEFAULT_BROWSER_VERSION

    with open('allure-results/environment.properties', 'w') as f:
        f.write(f'browserVersion={browser_version}\n')

    options = Options()
    selenoid_capabilities = {
        "browserName": 'chrome',
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
        options=options
    )

    browser.config.driver = driver

    yield browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()
