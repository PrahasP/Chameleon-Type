import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QFrame, QPushButton, QLabel,
    QFileDialog, QListWidget, QListWidgetItem, QHBoxLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image


class DecodeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Lion: Encode")
        self.setMinimumSize(600, 400)

        self.image = None  # Image that we're gonna encode

        # Main layout
        frame = QFrame()
        self.layout = QHBoxLayout(frame)

        # Scroll list
        self.image_list = QListWidget()
        self.image_list.setFixedWidth(200)
        self.image_list.itemClicked.connect(self.display_image)
        self.layout.addWidget(self.image_list)

        # Right-side layout
        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Decode Screen")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.right_layout.addWidget(self.label)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(self.image_label)

        self.layout.addLayout(self.right_layout)
        self.setCentralWidget(frame)

        # Load images from the folder
        self.load_images_from_folder("Encoded Passwords")

    def load_images_from_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(('.png')):
                file_path = os.path.join(folder_path, file_name)
                pixmap = QPixmap(file_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                item = QListWidgetItem(QIcon(pixmap), file_name)
                item.setData(Qt.UserRole, file_path)
                self.image_list.addItem(item)

    def display_image(self, item):
        file_path = item.data(Qt.UserRole)
        pixmap = QPixmap(file_path).scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def open_file_explorer(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "PNG Files (*.png)")
        if file_path:
            pixmap = QPixmap(file_path).scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QFrame {
        background-color: #3f3f3f;
    }
    QPushButton {
        border-radius: 5px;
        background-color: rgb(60, 90, 255);
        padding: 10px;
        color: white;
        font-weight: bold;
        font-family: Arial;
        font-size: 12px;
    }
    QPushButton::hover {
        background-color: rgb(60, 20, 255);
    }
    QListWidget {
        background-color: #2f2f2f;
        color: white;
        border: none;
    }
    QListWidget::item {
        padding: 5px;
    }
    QListWidget::item:selected {
        background-color: rgb(60, 90, 255);
        color: white;
    }
    """)
    window = EncodeScreen()
    window.show()
    sys.exit(app.exec_())
