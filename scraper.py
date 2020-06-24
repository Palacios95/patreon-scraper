from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from functools import reduce
import string


def generate_terms():
    """
        Generates an array of all 2 character permutations.
    """
    lowercase_list = list(string.ascii_lowercase)
    return reduce(
        lambda x, y: x + list(map(lambda z: f"{y}{z}", lowercase_list)),
        lowercase_list,
        [],
    )


def setup_driver():
    """
    Configure and return Selenium driver class
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe", options=chrome_options
    )
    driver.implicitly_wait(0.5)
    return driver


def get_campaigns(driver, search_term):
    """
        Retrieve all campaign urls based on search term
    """
    driver.get(f"https://www.patreon.com/search?q={search_term}")

    campaigns = driver.find_elements_by_xpath("//a[@data-tag='campaign-result-avatar']")
    for campaign in campaigns:
        print(campaign.get_attribute("href"))


def scrape():
    driver = setup_driver()
    terms = generate_terms()
    for term in terms:
        get_campaigns(driver, term)


scrape()
