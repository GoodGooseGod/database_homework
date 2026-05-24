from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication

from main_window import MainWindow


class App:
    def __init__(self):
        self.app = QApplication([])

        self.window = MainWindow()

    def run(self):
        self.app.exec()