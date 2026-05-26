from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QWidget,
    QLabel, QVBoxLayout, QPushButton,
    QFormLayout, QDialog, QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt

from .table import Table


class CustomersTable(Table):
    def load_table(self) -> None:
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)

        data = self.api.customers.get_customers()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Рег. номер", "ФИО", "Адрес", "Тип", "Удалить"
        ])



        for row, c in enumerate(data):
            item = QTableWidgetItem(str(c["register_customer_number"]))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.table.setItem(row, 0, item)
            self.table.setItem(row, 1, QTableWidgetItem(str(c["customer_name"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(c["address"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(c["customer_type"])))
            delete_btn = QPushButton("🗑")
            delete_btn.clicked.connect(
                lambda _, customer_id=c["register_customer_number"]:
                self.delete_customer(customer_id)
            )
            self.table.setCellWidget(row, 4, delete_btn)

        self.table.resizeColumnsToContents()

    def make_table(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.header = self.make_header('Клиенты')

        self.load_table()

        self.details_layout = QVBoxLayout(self.details)
        self.table.itemSelectionChanged.connect(self.show_details)
        self.table.cellChanged.connect(self.update_customer)

        add_btn = QPushButton("Добавить клиента")
        add_btn.clicked.connect(self.add_customer)

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

        register_customer_number = self.table.item(row, 0).text()
        name = self.table.item(row, 1).text()
        address = self.table.item(row, 2).text()
        ctype = self.table.item(row, 3).text()

        info = QLabel(
            f"""
            🧾 ДЕТАЛИ КЛИЕНТА

            Рег. номер: {register_customer_number}
            ФИО: {name}
            Адрес: {address}
            Тип: {ctype}
            """
        )
        info.setAlignment(Qt.AlignmentFlag.AlignTop)
        info.setStyleSheet("font-size: 14px; padding: 10px;")

        self.details_layout.addWidget(info)
        return self.details

    def add_customer(self):
        dialog = QDialog()
        dialog.setWindowTitle("Добавить клиента")

        layout = QFormLayout(dialog)

        reg_input = QLineEdit()
        name_input = QLineEdit()
        address_input = QLineEdit()
        type_input = QLineEdit()

        layout.addRow("Рег. номер:", reg_input)
        layout.addRow("ФИО:", name_input)
        layout.addRow("Адрес:", address_input)
        layout.addRow("Тип:", type_input)

        save_btn = QPushButton("Сохранить")
        layout.addWidget(save_btn)

        def save():
            try:
                data = {
                    "register_customer_number": int(reg_input.text()),
                    "customer_name": name_input.text(),
                    "address": address_input.text(),
                    "customer_type": int(type_input.text())
                }

                self.api.customers.create_customer(**data)

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

    def update_customer(self, row: int, column: int):
        customer_id = int(self.table.item(row, 0).text())

        value = self.table.item(row, column).text()
        field_map = {
            1: 'customer_name',
            2: 'address',
            3: 'customer_type'
        }

        if column not in field_map:
            return

        field_name = field_map[column]
        if field_name == "customer_type":
            value = int(value)

        self.api.customers.update_customer(
            customer_id,
            **{
                field_name: value
            }
        )
        self.show_details()


    def delete_customer(self, customer_id: int):
        reply = QMessageBox.question(
            self.details,
            'Удаление',
            'Вы уверены, что хотите удалить клиента?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        self.api.customers.delete_customer(customer_id)
        self.reload_table()

    def reload_table(self):
        self.table.blockSignals(True)

        self.table.clearContents()
        self.table.setRowCount(0)

        self.load_table()

        self.table.blockSignals(False)