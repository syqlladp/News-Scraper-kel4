from PyQt5.QtCore import QThread, pyqtSignal
from scraper import NewsScraper
import time
from datetime import datetime
import random

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

        if not text:
            return None

        text = text.replace("WIB","")

        if "," in text:
            text = text.split(",")[1].strip()

        parts = text.split()
        text = " ".join(parts[:3])

        bulan = {
            "Januari":"January",
            "Februari":"February",
            "Maret":"March",
            "April":"April",
            "Mei":"May",
            "Juni":"June",
            "Juli":"July",
            "Agustus":"August",
            "September":"September",
            "Oktober":"October",
            "November":"November",
            "Desember":"December"
        }

        for indo, eng in bulan.items():
            text = text.replace(indo, eng)

        formats = [
            "%Y-%m-%dT%H:%M:%S%z"
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

        for l in links:
            self.log.emit(f"Link ditemukan: {l}")

        results = []

        total = len(links)

        if total == 0:
            self.log.emit("Tidak ada link ditemukan")
            self.finished.emit([])
            return

        for i, link in enumerate(links):

            if not self.running:
                break

            self.log.emit(f"Scraping artikel {i+1}/{total}")

            try:
                data = scraper.scrape_article(link)
            except Exception as e:
                self.log.emit(f"Gagal scrape: {link}")
                continue

            # hanya cek judul
            if data["title"]:
                results.append(data)

            progress = int((i + 1) / total * 100)
            self.progress.emit(progress)

            time.sleep(self.delay + random.uniform(1,2))

        scraper.close()

        self.finished.emit(results)