from selenium import webdriver
from selenium.webdriver.common.by import By


class BBCCralwer:
    def __init__(self, url):
        self.url = url
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        self.driver = webdriver.Chrome("../chromedriver", chrome_options=options)

    def get(self):
        self._get_links()
        self._get_details()

    def _get_links(self):
        self.driver.get(self.url)
        return [e.get_attribute('href') for e in self.driver.find_elements(by=By.CLASS_NAME, value="btn_detail")[:10]]

    def _get_details(self, urls):
        for url in urls:
            self.driver.get(url)

            title = self.driver.find_element(by=By.CLASS_NAME, value="title").text
            body = self.driver.find_element(by=By.ID, value="articleBody").get_attribute('innerHtml')
            attachment_list = [e.find_element(By.TAG_NAME, "a").text
                               for e in self.driver.find_elements(by=By.CLASS_NAME, value="file-anchor")]
