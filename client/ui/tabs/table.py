from PyQt6.QtWidgets import QWidget, QLabel, QTableWidget, QVBoxLayout
from PyQt6.QtCore import Qt


class Table:
    def __init__(self, api):
        self.api = api
        self.header: QLabel = QLabel()
        self.details: QWidget = QWidget()
        self.details_layout: QVBoxLayout = QVBoxLayout()
        self.table: QTableWidget = QTableWidget()

    @staticmethod
    def make_header(header: str) -> QLabel:
        header = QLabel(header)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet('''
                    font-size: 22px;
                    font-family: Impact;
                 ''')
        return header

    def reload_table(self):
        self.table.blockSignals(True)

        self.table.clearContents()
        self.table.setRowCount(0)

        self.load_table()

        self.table.blockSignals(False)

    def load_table(self) -> None:
        raise NotImplemented("Method load_table wasn't defined")

    def make_table(self) -> QWidget:
        raise NotImplemented("Method make_table wasn't defined")

    def show_details(self) -> QWidget:
        raise NotImplemented("Method show_details wasn't defined")


