from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_box = QVBoxLayout()

        self.configure()

        self.add_header()

        self.setLayout(self.main_box)
        self.show()

    def configure(self) -> None:
        self.setMinimumSize(600, 400)
        self.setGeometry(300, 100, 800, 600)
        self.setWindowTitle('Приложуха')

    def add_header(self) -> None:
        header = QLabel('Заголовок', self)
        header.setAlignment(Qt.AlignmentFlag.AlignTop)
        header.setStyleSheet('''
            font-size: 24px;
            font-family: Impact;
            border: 2px solid purple;
        ''')
        self.main_box.addWidget(header)



