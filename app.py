import sys
from os import environ
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QTabWidget, QLabel, QLineEdit, QPushButton,
                              QTableWidget, QTableWidgetItem, QMessageBox, QAbstractItemView)
from PySide6.QtCore import Qt
import mysql.connector
from datetime import datetime

class BillingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing System")
        self.setGeometry(100, 100, 800, 600)
        self.db = mysql.connector.connect(
            host=environ.get("HOST"),
            user=environ.get("USER"),
            port=environ.get("PORT"),
            password=environ.get("PASSWORD"),
            database="billing_db"
        )
        self.cursor = self.db.cursor()

        self.create_tables()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.create_bill_tab = QWidget()
        self.view_bills_tab = QWidget()
        self.view_customers_tab = QWidget()

        self.tabs.addTab(self.create_bill_tab, "Create Bill")
        self.tabs.addTab(self.view_bills_tab, "View Bills")
        self.tabs.addTab(self.view_customers_tab, "View Customers")

        self.setup_create_bill_tab()
        self.setup_view_bills_tab()
        self.setup_view_customers_tab()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(20)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                amount FLOAT,
                description TEXT,
                date DATETIME,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
        self.db.commit()

    def setup_create_bill_tab(self):
        layout = QVBoxLayout(self.create_bill_tab)

        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Customer Name")
        layout.addWidget(QLabel("Customer Name"))
        layout.addWidget(self.customer_name)

        self.customer_email = QLineEdit()
        self.customer_email.setPlaceholderText("Customer Email")
        layout.addWidget(QLabel("Customer Email"))
        layout.addWidget(self.customer_email)

        self.customer_phone = QLineEdit()
        self.customer_phone.setPlaceholderText("Customer Phone")
        layout.addWidget(QLabel("Customer Phone"))
        layout.addWidget(self.customer_phone)

        self.bill_amount = QLineEdit()
        self.bill_amount.setPlaceholderText("Bill Amount")
        layout.addWidget(QLabel("Bill Amount"))
        layout.addWidget(self.bill_amount)

        self.bill_description = QLineEdit()
        self.bill_description.setPlaceholderText("Description")
        layout.addWidget(QLabel("Description"))
        layout.addWidget(self.bill_description)

        submit_btn = QPushButton("Create Bill")
        submit_btn.clicked.connect(self.create_bill)
        layout.addWidget(submit_btn)
        layout.addStretch()

    def setup_view_bills_tab(self):
        layout = QVBoxLayout(self.view_bills_tab)

        self.bills_table = QTableWidget()
        self.bills_table.setColumnCount(5)
        self.bills_table.setHorizontalHeaderLabels(["ID", "Customer ID", "Amount", "Description", "Date"])
        self.bills_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.bills_table)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_bills)
        layout.addWidget(refresh_btn)

        self.load_bills()

    def setup_view_customers_tab(self):
        layout = QVBoxLayout(self.view_customers_tab)

        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(4)
        self.customers_table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone"])
        self.customers_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.customers_table)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_customers)
        layout.addWidget(refresh_btn)

        self.load_customers()

    def create_bill(self):
        try:
            name = self.customer_name.text()
            email = self.customer_email.text()
            phone = self.customer_phone.text()
            amount = float(self.bill_amount.text())
            description = self.bill_description.text()
            if name is None or name == "":
                raise Exception("You can't submit without name.")
            if email is None or email == "":
                raise Exception("You can't submit without email.")
            if amount is None or amount == "":
                raise Exception("You can't submit without amount.")
            self.cursor.execute("""
                INSERT INTO customers (name, email, phone)
                VALUES (%s, %s, %s)
            """, (name, email, phone))
            customer_id = self.cursor.lastrowid

            self.cursor.execute("""
                INSERT INTO bills (customer_id, amount, description, date)
                VALUES (%s, %s, %s, %s)
            """, (customer_id, amount, description, datetime.now()))

            self.db.commit()

            self.customer_name.clear()
            self.customer_email.clear()
            self.customer_phone.clear()
            self.bill_amount.clear()
            self.bill_description.clear()

            QMessageBox.information(self, "Success", "Bill created successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error creating bill:", f"{str(e)}")

    def load_bills(self):
        self.cursor.execute("SELECT * FROM bills")
        bills = self.cursor.fetchall()

        self.bills_table.setRowCount(len(bills))
        for row, bill in enumerate(bills):
            for col, value in enumerate(bill):
                self.bills_table.setItem(row, col, QTableWidgetItem(str(value)))

    def load_customers(self):
        self.cursor.execute("SELECT * FROM customers")
        customers = self.cursor.fetchall()

        self.customers_table.setRowCount(len(customers))
        for row, customer in enumerate(customers):
            for col, value in enumerate(customer):
                self.customers_table.setItem(row, col, QTableWidgetItem(str(value)))

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == '__main__':
    # Create database if it doesn't exist
    db = mysql.connector.connect(
        host=environ.get("HOST"),
        user=environ.get("USER"),
        port=environ.get("PORT"),
        password=environ.get("DB_PASSWORD")
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS billing_db")
    db.commit()
    db.close()

    app = QApplication(sys.argv)
    window = BillingApp()
    window.show()
    sys.exit(app.exec())
