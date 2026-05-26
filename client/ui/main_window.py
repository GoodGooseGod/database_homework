from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QListWidget, QStackedWidget, QHBoxLayout,
    QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt

from .tabs.customers_tab import CustomersTable
from .tabs.products_tab import ProductsTable
from .tabs.orders_tab import OrdersTable


class MainWindow(QMainWindow):
    def __init__(self, api):
        super().__init__()
        self.api = api

        self.central = QWidget()
        self.root = QVBoxLayout(self.central)
        body = QWidget()
        self.root.addWidget(body)
        self.body_layout = QHBoxLayout(body)

        self.customers_table = CustomersTable(self.api)
        self.products_table = ProductsTable(self.api)
        self.orders_table = OrdersTable(self.api)

        self.add_left_menu()

        self.configure()

    def configure(self):
        self.setCentralWidget(self.central)
        self.setWindowTitle("Приложуха")
        self.setMinimumSize(800, 400)

    def make_tabs_content(self) -> QStackedWidget:
        content = QStackedWidget()

        content.addWidget(self.customers_table.make_table())
        content.addWidget(self.products_table.make_table())
        content.addWidget(self.orders_table.make_table())
        return content

    def add_left_menu(self):
        menu = QListWidget()
        menu.addItems(["Клиенты", "Продукты", "Заказы"])
        menu.setFixedWidth(150)
        menu.setSpacing(10)
        menu.setStyleSheet('''
            font-size: 16px;
            font-family: Impact;
            border: 2px solid black;
            padding: 8px;
        ''')

        content = self.make_tabs_content()

        menu.currentRowChanged.connect(content.setCurrentIndex)
        menu.setCurrentRow(0)
        self.body_layout.addWidget(menu)
        self.body_layout.addWidget(content)



