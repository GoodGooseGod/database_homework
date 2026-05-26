from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow
from api_requests.api_manager import APIManager


class App:
    def __init__(self):
        self.app = QApplication([])
        self.api = APIManager('http://127.0.0.1:8000')

        self.window = MainWindow(self.api)

    def run(self):
        self.window.show()
        self.app.exec()
