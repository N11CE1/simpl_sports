from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem


class OrderList(QListWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.user_preferences_updated = None
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.data_dict = {}
        self.setFixedSize(300, 500)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 5px solid #D9D9D9;
                border-radius: 20px;
                font-size: 30px;
            }
            QListWidget::item {
                color: black;
                background-color: #F5F5F5;
                border: 2px solid #D9D9D9;
                border-radius: 15px;
                padding: 10px;    
            }
            QListWidget::item:selected {
                border: 2px solid #007AFF;
                border-radius: 15px;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 12px;
                margin: 0px 0px 0px 0px;
                padding: 0px;
            }
            QScrollBar::handle:vertical {
                background: #888;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar::handle:vertical:hover {
                background: #666;
            }
        """)
        self.set_items(items)

    def set_items(self, items):
        self.clear()
        for item in items:
            list_item = QListWidgetItem(item["display_text"])
            list_item.setData(Qt.UserRole, item["unique_key"])
            list_item.setTextAlignment(Qt.AlignCenter)
            list_item.setSizeHint(QSize(30, 100))
            self.addItem(list_item)
        self.update_data()

    def dropEvent(self, event):
        super().dropEvent(event)
        self.update_data()
        event.accept()

    def update_data(self):
        self.data_dict = {}
        for index in range(self.count()):
            item = self.item(index)
            unique_key = item.data(Qt.UserRole)
            self.data_dict[index] = unique_key
        print("dictionary:", self.data_dict)


    def get_order_list(self):
        return self.data_dict

    def update_user_preferences(self):
        self.user_preferences_updated.emit()