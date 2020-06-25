from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
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
    chrome_options.add_argument("--silent")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe", options=chrome_options
    )
    driver.implicitly_wait(0.5)
    return driver


def get_campaign_urls(driver, search_term):
    """
        Retrieve all campaign urls based on search term
    """
    driver.get(f"https://www.patreon.com/search?q={search_term}")

    campaigns = driver.find_elements_by_xpath("//a[@data-tag='campaign-result-avatar']")
    return list(map(lambda x: x.get_attribute("href"), campaigns))


def get_campaign_info(driver, campaign_url):
    campaign_info = {
        "creator_id": campaign_url.split("/")[-1],
        "reward_tiers": [],
        "patron_count": 0,
        "monthly_income": 0,
    }
    driver.get(campaign_url)

    try:
        campaign_info["reward_tiers"] = list(
            map(
                lambda x: x.text,
                driver.find_elements_by_xpath(
                    "//div[@data-tag='reward-tier-card']//div[starts-with(text(), '$')]"
                ),
            )
        )
    except NoSuchElementException:
        print(f"Could not find reward tiers in url {campaign_url}")

    try:
        campaign_info["patron_count"] = driver.find_element_by_xpath(
            "//div[@data-tag='CampaignPatronEarningStats-patron-count']/h2"
        ).text
    except NoSuchElementException:
        print(f"Could not find patron count in url {campaign_url}")

    try:
        campaign_info["monthly_income"] = driver.find_element_by_xpath(
            "//div[@data-tag='CampaignPatronEarningStats-earnings']/h2"
        ).text
    except NoSuchElementException:
        print(f"Could not find monthly income in url {campaign_url}")

    return campaign_info


def scrape():
    driver = setup_driver()
    terms = generate_terms()
    for term in terms:
        campaign_urls = get_campaign_urls(driver, term)
        for url in campaign_urls:
            print(get_campaign_info(driver, url))


scrape()
