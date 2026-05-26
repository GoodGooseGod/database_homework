from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QWidget,
    QLabel, QVBoxLayout, QPushButton,
    QFormLayout, QDialog, QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt
from datetime import date

from .table import Table


class OrdersTable(Table):
    def load_table(self) -> None:
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)

        data = self.api.orders.get_orders()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Дата", "Номер", "Штрих-код", "Рег. номер", "Количество", "Удалить"
        ])

        for row, c in enumerate(data):
            item = QTableWidgetItem(str(c["order_date"]))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.table.setItem(row, 0, item)

            item = QTableWidgetItem(str(c["order_number"]))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.table.setItem(row, 1, item)

            self.table.setItem(row, 2, QTableWidgetItem(str(c["barcode"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(c["register_customer_number"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(c["amount"])))
            delete_btn = QPushButton("🗑")
            delete_btn.clicked.connect(
                lambda _, order_date=c["order_date"], order_number=c["order_number"]:
                self.delete_order(order_date, order_number)
            )
            self.table.setCellWidget(row, 5, delete_btn)

        self.table.resizeColumnsToContents()

    def make_table(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.header = self.make_header('Заказы')

        self.load_table()

        self.details_layout = QVBoxLayout(self.details)
        self.table.itemSelectionChanged.connect(self.show_details)
        self.table.cellChanged.connect(self.update_order)

        add_btn = QPushButton("Добавить заказ")
        add_btn.clicked.connect(self.add_order)

        layout.addWidget(self.header)
        layout.addWidget(add_btn)
        layout.addWidget(self.table)
        layout.addWidget(self.details)
        return widget

    def show_details(self) -> QWidget:
        row = self.table.currentRow()
        if row < 0:
            return QLabel()

        while self.details_layout.count():
            item = self.details_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        order_date = self.table.item(row, 0).text()
        order_number = self.table.item(row, 1).text()
        barcode = self.table.item(row, 2).text()
        register_customer_number = self.table.item(row, 3).text()
        amount = self.table.item(row, 4).text()

        info = QLabel(
            f"""
            🧾 ДЕТАЛИ ЗАКАЗА

            Дата: {order_date}
            Номер: {order_number}
            Штрих-код: {barcode}
            Рег. номер: {register_customer_number}
            Количество: {amount}
            """
        )
        info.setAlignment(Qt.AlignmentFlag.AlignTop)
        info.setStyleSheet("font-size: 14px; padding: 10px;")

        self.details_layout.addWidget(info)
        return self.details

    def add_order(self):
        dialog = QDialog()
        dialog.setWindowTitle("Добавить заказ")

        layout = QFormLayout(dialog)

        date_input = QLineEdit()
        number_input = QLineEdit()
        barcode_input = QLineEdit()
        reg_num_input = QLineEdit()
        amount_input = QLineEdit()

        layout.addRow("Дата:", date_input)
        layout.addRow("Номер:", number_input)
        layout.addRow("Штрих-код:", barcode_input)
        layout.addRow("Рег. номер:", reg_num_input)
        layout.addRow("Количество:", amount_input)

        save_btn = QPushButton("Сохранить")
        layout.addWidget(save_btn)

        def save():
            try:
                data = {
                    'order_date': date_input.text(),
                    'order_number': int(number_input.text()),
                    'barcode': int(barcode_input.text()),
                    'register_customer_number': int(reg_num_input.text()),
                    'amount': int(amount_input.text()),
                }

                self.api.orders.create_order(**data)

                dialog.accept()

                self.reload_table()

            except Exception as e:
                QMessageBox.critical(
                    self.details,
                    "Ошибка",
                    str(e)
                )

        save_btn.clicked.connect(save)

        dialog.exec()

    def update_order(self, row: int, column: int):
        order_date = self.table.item(row, 0).text()
        order_number = int(self.table.item(row, 1).text())

        value = self.table.item(row, column).text()
        field_map = {
            1: 'barcode',
            2: 'register_customer_number',
            3: 'amount',
        }

        if column not in field_map:
            return

        field_name = field_map[column]
        if field_name == 'barcode':
            value = int(value)
        elif field_name == 'register_customer_number':
            value = int(value)
        elif field_name == 'amount':
            value = int(value)

        self.api.orders.update_order(
            order_date,
            order_number,
            **{
                field_name: value
            }
        )
        self.show_details()


    def delete_order(self, order_date: date, order_number: int):
        reply = QMessageBox.question(
            self.details,
            'Удаление',
            'Вы уверены, что хотите удалить заказ?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        self.api.orders.delete_order(order_date, order_number)
        self.reload_table()