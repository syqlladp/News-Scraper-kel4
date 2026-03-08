import time
import random
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NewsScraper:

    def __init__(self, headless=True):

        options = Options()

        if headless:
            options.add_argument("--headless")

        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)


    # ===============================
    # Collect article links
    # ===============================
    def collect_links(self, url, limit=10):

        domain = urlparse(url).netloc
        links = set()
        page = 1

        while len(links) < limit:

            page_url = f"{url}?page={page}"

            self.driver.get(page_url)

            time.sleep(random.uniform(2,4))

            elements = self.driver.find_elements(By.TAG_NAME, "a")

            for el in elements:

                href = el.get_attribute("href")

                if not href:
                    continue

                if urlparse(href).netloc != domain:
                    continue

                if "#" in href:
                    continue

                # hindari kategori
                if "/video/" in href or "/foto/" in href or "/tag/" in href:
                    continue

                parts = href.split("/")

                # hanya ambil link yang punya angka (biasanya tanggal artikel)
                if not any(part.isdigit() and len(part) >= 6 for part in parts):
                    continue

                links.add(href)

                if len(links) >= limit:
                    break

            page += 1

            if page > 10:
                break

        return list(links)[:limit]


    # ===============================
    # Extract article
    # ===============================
    def scrape_article(self, url):

        self.driver.get(url)

        title = ""
        date = ""
        content = ""

        # =====================
        # TITLE
        # =====================
        try:
            title = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            ).text.strip()
        except:
            try:
                title = self.driver.find_element(By.TAG_NAME, "h2").text.strip()
            except:
                pass


        # =====================
        # DATE
        # =====================

        date = ""

        # ambil dari atribut datetime
        time_selectors = [
            "time[datetime]",
            "[data-date]",
            "[data-timestamp]",
            "[data-publish-date]",
            "[data-created]",
            "[itemprop='datePublished']",
            "[property='article:published_time']",
        ]

        for selector in time_selectors:
            try:
                el = self.driver.find_element(By.CSS_SELECTOR, selector)

                # coba ambil dari atribut dulu
                for attr in ["datetime", "data-date", "data-timestamp",
                            "data-publish-date", "data-created", "content"]:
                    val = el.get_attribute(attr)
                    if val and val.strip():
                        date = val.strip()
                        break

                if date:
                    break
            except:
                continue

        # Fallback
        if not date:
            meta_selectors = [
                "meta[property='article:published_time']",
                "meta[name='publish-date']",
                "meta[name='date']",
                "meta[itemprop='datePublished']",
                "meta[name='pubdate']",
            ]
            for selector in meta_selectors:
                try:
                    el = self.driver.find_element(By.CSS_SELECTOR, selector)
                    val = el.get_attribute("content")
                    if val and val.strip():
                        date = val.strip()
                        break
                except:
                    continue


        # Fallback terakhir
        if not date:
            text_selectors = [
                "[class*='date']",
                "[class*='publish']",
                "[class*='posted']",
                "[class*='created']",
            ]

            # menyeleksi kata kata yang berhubungan dengan tanggal
            relative_keywords = ["lalu", "yang lalu", "ago", "menit", "jam",
                                "hari", "minggu", "bulan", "tadi", "baru"]

            for selector in text_selectors:
                try:
                    el = self.driver.find_element(By.CSS_SELECTOR, selector)
                    txt = el.text.strip()

                    if not txt:
                        continue

                    # skip kalau teks relatif
                    if any(kw in txt.lower() for kw in relative_keywords):
                        continue

                    date = txt
                    break
                except:
                    continue

        paragraphs = []

        # coba dengan article tag
        try:
            article = self.driver.find_element(By.TAG_NAME, "article")
            paragraphs = article.find_elements(By.TAG_NAME, "p")
        except:
            pass

        # fallback cari container besar
        if not paragraphs:
            try:
                containers = self.driver.find_elements(By.CSS_SELECTOR, "div")
                for c in containers:
                    ps = c.find_elements(By.TAG_NAME, "p")
                    if len(ps) > 5:
                        paragraphs = ps
                        break
            except:
                pass

        # fallback terakhir
        if not paragraphs:
            paragraphs = self.driver.find_elements(By.TAG_NAME, "p")

        text = []

        for p in paragraphs:

            t = p.text.strip()

            if len(t) < 40:
                continue

            t_lower = t.lower()

            if "copyright" in t_lower:
                continue

            if "share" in t_lower:
                continue

            if "baca juga" in t_lower:
                continue

            text.append(t)

        content = " ".join(text)

        return {
            "title": title,
            "date": date,
            "content": content,
            "url": url
        }


    # ===============================
    # Main scraping
    # ===============================
    def scrape(self, url, limit=10):

        links = self.collect_links(url, limit)

        results = []

        for link in links:

            try:

                data = self.scrape_article(link)

                if data["title"] and len(data["content"]) > 100:
                    results.append(data)

            except:
                continue

        return results


    def close(self):
        self.driver.quit()