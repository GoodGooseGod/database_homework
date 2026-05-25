from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow


class App:
    def __init__(self):
        self.app = QApplication([])

        self.window = MainWindow()

    def run(self):
        self.app.exec()