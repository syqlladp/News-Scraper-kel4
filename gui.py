from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QProgressBar,
    QSpinBox, QFileDialog, QDateEdit, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFormLayout
)

from worker import ScraperWorker
from utils import export_excel, export_csv

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("News Scraper Application")
        self.setGeometry(200,200,1300,700)

        main_layout = QVBoxLayout()

        title = QLabel("News Scraper Application")
        title.setStyleSheet("font-size:20px;font-weight:bold;")
        main_layout.addWidget(title)

        form = QFormLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.cnnindonesia.com/nasional")
        form.addRow("URL Berita", self.url_input)

        self.limit_spin = QSpinBox()
        self.limit_spin.setValue(20)
        form.addRow("Limit Artikel", self.limit_spin)

        self.delay_spin = QSpinBox()
        self.delay_spin.setValue(2)
        form.addRow("Delay (detik)", self.delay_spin)

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        form.addRow("Start Date", self.start_date)

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        form.addRow("End Date", self.end_date)

        main_layout.addLayout(form)

        btn_layout = QHBoxLayout()

        self.start_btn = QPushButton("Start Scraping")
        self.start_btn.clicked.connect(self.start_scraping)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_scraping)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)

        main_layout.addLayout(btn_layout)

        self.progress = QProgressBar()
        main_layout.addWidget(self.progress)

        split_layout = QHBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Judul","Tanggal","Isi","URL"])

        self.table.setColumnWidth(0,300)
        self.table.setColumnWidth(1,120)
        self.table.setColumnWidth(2,500)
        self.table.setColumnWidth(3,300)

        split_layout.addWidget(self.table)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        split_layout.addWidget(self.log_box)

        main_layout.addLayout(split_layout)

        export_layout = QHBoxLayout()

        self.export_excel_btn = QPushButton("Export Excel")
        self.export_excel_btn.clicked.connect(self.export_excel)

        self.export_csv_btn = QPushButton("Export CSV")
        self.export_csv_btn.clicked.connect(self.export_csv)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_table)

        export_layout.addWidget(self.export_excel_btn)
        export_layout.addWidget(self.export_csv_btn)
        export_layout.addWidget(self.clear_btn)

        main_layout.addLayout(export_layout)

        self.setLayout(main_layout)

        self.data = []

    def log(self,msg):

        self.log_box.append(msg)

        with open("logs.txt","a",encoding="utf-8") as f:
            f.write(msg+"\n")

    def start_scraping(self):

        url = self.url_input.text()
        limit = self.limit_spin.value()
        delay = self.delay_spin.value()

        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()

        self.worker = ScraperWorker(url,limit,delay,start_date,end_date)

        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.show_results)
        self.worker.log.connect(self.log)

        self.worker.start()

        self.log("Scraping dimulai")

    def stop_scraping(self):

        if hasattr(self,"worker"):
            self.worker.running = False
            self.log("Scraping dihentikan")

    def show_results(self,results):

        self.data = results

        self.table.setRowCount(len(results))

        for row,item in enumerate(results):

            self.table.setItem(row,0,QTableWidgetItem(item["title"]))
            self.table.setItem(row,1,QTableWidgetItem(item["date"]))
            self.table.setItem(row,2,QTableWidgetItem(item["content"][:200]))
            self.table.setItem(row,3,QTableWidgetItem(item["url"]))

        self.log(f"{len(results)} artikel ditemukan")

    def export_excel(self):

        if not self.data:
            self.log("Tidak ada data")
            return

        path,_ = QFileDialog.getSaveFileName(self,"Save","","Excel (*.xlsx)")

        if path:
            export_excel(self.data,path)
            self.log("Export Excel berhasil")

    def export_csv(self):

        if not self.data:
            return

        path,_ = QFileDialog.getSaveFileName(self,"Save","","CSV (*.csv)")

        if path:
            export_csv(self.data,path)
            self.log("Export CSV berhasil")

    def clear_table(self):

        self.table.setRowCount(0)
        self.data = []
        self.log("Data dibersihkan")