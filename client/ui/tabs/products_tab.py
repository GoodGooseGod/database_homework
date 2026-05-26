from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QWidget,
    QLabel, QVBoxLayout, QPushButton,
    QFormLayout, QDialog, QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt
from datetime import date

from .table import Table


class ProductsTable(Table):
    def load_table(self) -> None:
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)

        data = self.api.products.get_products()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Штрих-код", "Наименование", "Срок годности", "Тип", "Номер партии", "Цена", "Удалить"
        ])

        for row, c in enumerate(data):
            item = QTableWidgetItem(str(c["barcode"]))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.table.setItem(row, 0, item)
            self.table.setItem(row, 1, QTableWidgetItem(str(c["product_name"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(c["expiration_date"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(c["category"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(c["batch_number"])))
            self.table.setItem(row, 5, QTableWidgetItem(str(c["price"])))
            delete_btn = QPushButton("🗑")
            delete_btn.clicked.connect(
                lambda _, barcode=c["barcode"]:
                self.delete_product(barcode)
            )
            self.table.setCellWidget(row, 6, delete_btn)

        self.table.resizeColumnsToContents()

    def make_table(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.header = self.make_header('Продукты')

        self.load_table()

        self.details_layout = QVBoxLayout(self.details)
        self.table.itemSelectionChanged.connect(self.show_details)
        self.table.cellChanged.connect(self.update_product)

        add_btn = QPushButton("Добавить продукт")
        add_btn.clicked.connect(self.add_product)

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

        barcode = self.table.item(row, 0).text()
        product_name = self.table.item(row, 1).text()
        expiration_date = self.table.item(row, 2).text()
        category = self.table.item(row, 3).text()
        batch_number = self.table.item(row, 4).text()
        price = self.table.item(row, 5).text()

        info = QLabel(
            f"""
            🧾 ДЕТАЛИ ПРОДУКТА

            Штрих-код: {barcode}
            Наименование: {product_name}
            Срок годности: {expiration_date}
            Тип: {category}
            Номер партии: {batch_number}
            Цена: {price}
            """
        )
        info.setAlignment(Qt.AlignmentFlag.AlignTop)
        info.setStyleSheet("font-size: 14px; padding: 10px;")

        self.details_layout.addWidget(info)
        return self.details

    def add_product(self):
        dialog = QDialog()
        dialog.setWindowTitle("Добавить продукт")

        layout = QFormLayout(dialog)

        barcode_input = QLineEdit()
        name_input = QLineEdit()
        date_input = QLineEdit()
        type_input = QLineEdit()
        batch_input = QLineEdit()
        price_input = QLineEdit()

        layout.addRow("Штрих-код:", barcode_input)
        layout.addRow("Наименование:", name_input)
        layout.addRow("Срок годности:", date_input)
        layout.addRow("Тип:", type_input)
        layout.addRow("Номер партии:", batch_input)
        layout.addRow("Цена:", price_input)

        save_btn = QPushButton("Сохранить")
        layout.addWidget(save_btn)

        def save():
            try:
                data = {
                    'barcode': int(barcode_input.text()),
                    'product_name': name_input.text(),
                    'expiration_date': date_input.text(),
                    'category': int(type_input.text()),
                    'batch_number': int(batch_input.text()),
                    'price': float(price_input.text()),
                }

                self.api.products.create_product(**data)

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

    def update_product(self, row: int, column: int):
        product_id = int(self.table.item(row, 0).text())

        value = self.table.item(row, column).text()
        field_map = {
            1: 'product_name',
            2: 'expiration_date',
            3: 'category',
            4: 'batch_number',
            5: 'price',
        }

        if column not in field_map:
            return

        field_name = field_map[column]
        if field_name == 'category':
            value = int(value)
        elif field_name == 'batch_number':
            value = int(value)
        elif field_name == 'price':
            value = float(value)

        self.api.products.update_product(
            product_id,
            **{
                field_name: value
            }
        )
        self.show_details()


    def delete_product(self, product_id: int):
        reply = QMessageBox.question(
            self.details,
            'Удаление',
            'Вы уверены, что хотите удалить продукт?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        self.api.products.delete_product(product_id)
        self.reload_table()

