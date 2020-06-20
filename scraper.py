from selenium import webdriver


def setup_driver():
    """
    Configure and return Selenium driver class
    """
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    driver.implicitly_wait(0.5)
    return driver

def get_campaigns(search_term):
    """
        Retrieve all campaign urls based on search term
    """
    driver = setup_driver()
    driver.get(f'https://www.patreon.com/search?q={search_term}')

    campaigns = driver.find_elements_by_xpath("//a[@data-tag='campaign-result-avatar']")
    for campaign in campaigns:
        print(campaign.get_attribute('href'))


def main():
    get_campaigns('ti')

main()