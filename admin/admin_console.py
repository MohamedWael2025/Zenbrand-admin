"""
Admin Console - Desktop Application using PyQt5
This provides a GUI interface to manage orders, products, and view chat logs.
Run with: python admin_console.py
"""

import sys
import requests
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit,
    QComboBox, QMessageBox, QTabWidget, QDialog, QSpinBox, QDoubleSpinBox,
    QTextEdit, QFormLayout, QStatusBar
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QColor, QFont

# Configuration
API_BASE_URL = "http://localhost:5000"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

class APIWorker(QThread):
    """Worker thread for API calls to prevent UI freezing"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    data_received = pyqtSignal(object)
    
    def __init__(self, method, endpoint, data=None):
        super().__init__()
        self.method = method
        self.endpoint = endpoint
        self.data = data
    
    def run(self):
        try:
            url = f"{API_BASE_URL}{self.endpoint}"
            
            if self.method == 'GET':
                response = requests.get(url)
            elif self.method == 'POST':
                response = requests.post(url, json=self.data)
            elif self.method == 'PUT':
                response = requests.put(url, json=self.data)
            elif self.method == 'DELETE':
                response = requests.delete(url)
            
            if response.status_code in [200, 201]:
                self.data_received.emit(response.json())
            else:
                self.error.emit(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            self.error.emit(f"Connection error: {str(e)}")
        finally:
            self.finished.emit()

class OrdersTab(QWidget):
    """Tab for managing orders"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.refresh_orders()
        
        # Auto-refresh every 30 seconds
        timer = QTimer()
        timer.timeout.connect(self.refresh_orders)
        timer.start(30000)
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Controls
        controls = QHBoxLayout()
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(['All', 'pending', 'confirmed', 'shipped', 'delivered', 'cancelled'])
        self.status_filter.currentTextChanged.connect(self.on_filter_changed)
        controls.addWidget(QLabel("Filter by Status:"))
        controls.addWidget(self.status_filter)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_orders)
        controls.addWidget(refresh_btn)
        
        layout.addLayout(controls)
        
        # Orders table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'Order #', 'Customer', 'Amount', 'Status', 'Date', 'Action'
        ])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 120)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def refresh_orders(self):
        status = self.status_filter.currentText()
        if status == 'All':
            endpoint = '/admin/orders'
        else:
            endpoint = f'/admin/orders?status={status}'
        
        self.worker = APIWorker('GET', endpoint)
        self.worker.data_received.connect(self.populate_orders)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    def populate_orders(self, data):
        self.table.setRowCount(0)
        
        for order in data.get('orders', []):
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(order['order_number']))
            self.table.setItem(row, 1, QTableWidgetItem(str(order.get('customer_id', ''))))
            self.table.setItem(row, 2, QTableWidgetItem(f"${order['total_amount']}"))
            
            status_item = QTableWidgetItem(order['status'].upper())
            status_colors = {
                'pending': QColor(255, 193, 7),
                'confirmed': QColor(33, 150, 243),
                'shipped': QColor(76, 175, 80),
                'delivered': QColor(76, 175, 80),
                'cancelled': QColor(244, 67, 54)
            }
            status_item.setBackground(status_colors.get(order['status'], QColor(158, 158, 158)))
            self.table.setItem(row, 3, status_item)
            
            date_str = order['created_at'][:10] if order['created_at'] else 'N/A'
            self.table.setItem(row, 4, QTableWidgetItem(date_str))
            
            action_btn = QPushButton('Update')
            action_btn.clicked.connect(lambda checked, oid=order['id']: self.update_order(oid, order))
            self.table.setCellWidget(row, 5, action_btn)
    
    def update_order(self, order_id, order):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Update Order {order['order_number']}")
        dialog.setGeometry(100, 100, 400, 300)
        
        form = QFormLayout()
        
        status_combo = QComboBox()
        status_combo.addItems(['pending', 'confirmed', 'shipped', 'delivered', 'cancelled'])
        status_combo.setCurrentText(order['status'])
        
        form.addRow("Status:", status_combo)
        
        ok_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        
        form.addRow(btn_layout)
        
        def save_changes():
            new_status = status_combo.currentText()
            self.worker = APIWorker('PUT', f'/admin/orders/{order_id}/status', {'status': new_status})
            self.worker.data_received.connect(lambda: self.show_success("Order updated successfully"))
            self.worker.error.connect(self.show_error)
            self.worker.finished.connect(dialog.close)
            self.worker.finished.connect(self.refresh_orders)
            self.worker.start()
        
        ok_btn.clicked.connect(save_changes)
        cancel_btn.clicked.connect(dialog.close)
        
        dialog.setLayout(form)
        dialog.exec_()
    
    def on_filter_changed(self):
        self.refresh_orders()
    
    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
    
    def show_success(self, message):
        QMessageBox.information(self, "Success", message)

class ProductsTab(QWidget):
    """Tab for managing products"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.refresh_products()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Add product button
        add_btn = QPushButton("➕ Add New Product")
        add_btn.clicked.connect(self.add_product_dialog)
        layout.addWidget(add_btn)
        
        # Products table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'Name', 'Price', 'Category', 'Stock', 'Active', 'Action'
        ])
        layout.addWidget(self.table)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_products)
        layout.addWidget(refresh_btn)
        
        self.setLayout(layout)
    
    def refresh_products(self):
        self.worker = APIWorker('GET', '/admin/products')
        self.worker.data_received.connect(self.populate_products)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    def populate_products(self, data):
        self.table.setRowCount(0)
        
        for product in data.get('products', []):
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(product['name']))
            self.table.setItem(row, 1, QTableWidgetItem(f"${product['price']}"))
            self.table.setItem(row, 2, QTableWidgetItem(product['category']))
            self.table.setItem(row, 3, QTableWidgetItem(str(product['stock'])))
            
            active_item = QTableWidgetItem("✓" if product['is_active'] else "✗")
            self.table.setItem(row, 4, active_item)
            
            edit_btn = QPushButton('Edit')
            edit_btn.clicked.connect(lambda checked, pid=product['id']: self.edit_product(pid, product))
            self.table.setCellWidget(row, 5, edit_btn)
    
    def add_product_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Product")
        dialog.setGeometry(100, 100, 500, 400)
        
        form = QFormLayout()
        
        name_input = QLineEdit()
        price_input = QDoubleSpinBox()
        category_input = QLineEdit()
        description_input = QTextEdit()
        sizes_input = QLineEdit()
        colors_input = QLineEdit()
        stock_input = QSpinBox()
        
        form.addRow("Name:", name_input)
        form.addRow("Price:", price_input)
        form.addRow("Category:", category_input)
        form.addRow("Description:", description_input)
        form.addRow("Sizes (comma-sep):", sizes_input)
        form.addRow("Colors (comma-sep):", colors_input)
        form.addRow("Stock:", stock_input)
        
        ok_btn = QPushButton("Add Product")
        cancel_btn = QPushButton("Cancel")
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        form.addRow(btn_layout)
        
        def save_product():
            data = {
                'name': name_input.text(),
                'price': price_input.value(),
                'category': category_input.text(),
                'description': description_input.toPlainText(),
                'sizes': sizes_input.text(),
                'colors': colors_input.text(),
                'stock': stock_input.value()
            }
            
            self.worker = APIWorker('POST', '/admin/products', data)
            self.worker.data_received.connect(lambda: self.show_success("Product added successfully"))
            self.worker.error.connect(self.show_error)
            self.worker.finished.connect(dialog.close)
            self.worker.finished.connect(self.refresh_products)
            self.worker.start()
        
        ok_btn.clicked.connect(save_product)
        cancel_btn.clicked.connect(dialog.close)
        
        dialog.setLayout(form)
        dialog.exec_()
    
    def edit_product(self, product_id, product):
        # Similar to add_product_dialog but for editing
        pass
    
    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
    
    def show_success(self, message):
        QMessageBox.information(self, "Success", message)

class ChatLogsTab(QWidget):
    """Tab for viewing chat logs"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.refresh_logs()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Filters
        filters = QHBoxLayout()
        self.customer_filter = QLineEdit()
        self.customer_filter.setPlaceholderText("Filter by customer ID...")
        self.customer_filter.textChanged.connect(self.refresh_logs)
        filters.addWidget(self.customer_filter)
        
        layout.addLayout(filters)
        
        # Chat logs table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'Customer', 'Message', 'Type', 'AI?', 'Model', 'Time'
        ])
        self.table.setColumnWidth(1, 300)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def refresh_logs(self):
        customer_id = self.customer_filter.text()
        if customer_id:
            endpoint = f'/admin/chat-logs?customer_id={customer_id}'
        else:
            endpoint = '/admin/chat-logs'
        
        self.worker = APIWorker('GET', endpoint)
        self.worker.data_received.connect(self.populate_logs)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    def populate_logs(self, data):
        self.table.setRowCount(0)
        
        for log in data.get('logs', []):
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(str(log['customer_id'])))
            message = log['message_content'][:50] + "..." if len(log['message_content']) > 50 else log['message_content']
            self.table.setItem(row, 1, QTableWidgetItem(message))
            self.table.setItem(row, 2, QTableWidgetItem(log['message_type']))
            self.table.setItem(row, 3, QTableWidgetItem("✓" if log['ai_generated'] else ""))
            self.table.setItem(row, 4, QTableWidgetItem(log.get('ai_model_used', '')))
            
            time_str = log['timestamp'][:16] if log['timestamp'] else 'N/A'
            self.table.setItem(row, 5, QTableWidgetItem(time_str))
    
    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

class AdminConsole(QMainWindow):
    """Main admin console window"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("WhatsApp AI - Admin Console")
        self.setGeometry(100, 100, 1200, 700)
        
        # Create central widget and tabs
        tabs = QTabWidget()
        
        tabs.addTab(OrdersTab(), "📦 Orders")
        tabs.addTab(ProductsTab(), "🛍️ Products")
        tabs.addTab(ChatLogsTab(), "💬 Chat Logs")
        
        self.setCentralWidget(tabs)
        
        # Status bar
        self.statusBar().showMessage("Connected to backend")

def main():
    app = QApplication(sys.argv)
    console = AdminConsole()
    console.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
