from PyQt5.QtCore import QThread, pyqtSignal
from scraper import NewsScraper
import time
from datetime import datetime


class ScraperWorker(QThread):

    progress = pyqtSignal(int)
    finished = pyqtSignal(list)
    log = pyqtSignal(str)

    def __init__(self, url, limit, delay, start_date, end_date):
        super().__init__()

        self.url = url
        self.limit = limit
        self.delay = delay
        self.start_date = start_date
        self.end_date = end_date
        self.running = True

    def parse_date(self, text):

        formats = [
            "%d %B %Y",
            "%d %b %Y",
            "%Y-%m-%d",
            "%d/%m/%Y"
        ]

        for f in formats:
            try:
                return datetime.strptime(text, f)
            except:
                pass

        return None

    def run(self):

        scraper = NewsScraper()

        self.log.emit("Mengambil daftar artikel...")

        links = scraper.collect_links(self.url, self.limit)

        results = []

        total = len(links)

        if total == 0:
            self.log.emit("Tidak ada link ditemukan")
            self.finished.emit([])
            return

        for i, link in enumerate(links):

            if not self.running:
                break

            self.log.emit(f"Scraping artikel {i+1}")

            data = scraper.scrape_article(link)

            # hanya cek judul
            if data["title"]:

                article_date = self.parse_date(data["date"])

                if article_date:

                    if self.start_date <= article_date.date() <= self.end_date:
                        results.append(data)

                else:
                    results.append(data)

            progress = int((i + 1) / total * 100)
            self.progress.emit(progress)

            time.sleep(self.delay)

        scraper.close()

        self.finished.emit(results)