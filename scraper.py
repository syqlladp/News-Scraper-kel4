from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


class NewsScraper:

    def __init__(self):

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")

        self.driver = webdriver.Chrome(options=options)

    # =====================================
    # AMBIL LINK ARTIKEL
    # =====================================

    def collect_links(self, url, limit):

        self.driver.get(url)

        time.sleep(4)

        elements = self.driver.find_elements(By.TAG_NAME, "a")

        links = []
        domain = url.split("/")[2]

        for el in elements:

            href = el.get_attribute("href")

            if not href:
                continue

            if domain not in href:
                continue

            if "#" in href:
                continue

            # kemungkinan artikel
            if href.count("/") < 4:
                continue

            if href in links:
                continue

            links.append(href)

            if len(links) >= limit:
                break

        return links

    # =====================================
    # SCRAPE ARTIKEL
    # =====================================

    def scrape_article(self, url):

        self.driver.get(url)

        time.sleep(2)

        title = ""
        date = ""
        content = ""

        # ===== title =====

        try:
            title = self.driver.find_element(By.TAG_NAME, "h1").text
        except:
            pass

        # ===== date =====

        try:
            date = self.driver.find_element(By.TAG_NAME, "time").text
        except:
            try:
                date = self.driver.find_element(By.CSS_SELECTOR, "[class*=date]").text
            except:
                pass

        # ===== content =====

        paragraphs = []

        try:
            article = self.driver.find_element(By.TAG_NAME, "article")
            paragraphs = article.find_elements(By.TAG_NAME, "p")
        except:
            paragraphs = self.driver.find_elements(By.TAG_NAME, "p")

        text = []

        for p in paragraphs:

            t = p.text.strip()

            if len(t) > 30:
                text.append(t)

        content = " ".join(text)

        return {
            "title": title,
            "date": date,
            "content": content,
            "url": url
        }

    # =====================================

    def close(self):
        self.driver.quit()