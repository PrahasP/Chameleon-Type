import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QFrame, QPushButton, QLabel,
    QFileDialog, QListWidget, QListWidgetItem, QHBoxLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image
import imageDecoder

class DecodeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chameleopn Type: Decode")
        self.setMinimumSize(600, 400)

        self.image = None  # Image that we're gonna decode

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

        # Decode button
        self.decode_button = QPushButton("Decode Image")
        self.decode_button.setEnabled(False)
        self.decode_button.clicked.connect(self.decode_image)
        self.right_layout.addWidget(self.decode_button)

        # Back to main screen button
        self.back_button = QPushButton("Back to Main Screen")
        self.back_button.clicked.connect(self.return_to_main)
        self.right_layout.addWidget(self.back_button)

        self.layout.addLayout(self.right_layout)
        self.setCentralWidget(frame)

        # Load images from the folder
        self.load_images_from_folder("Encoded Passwords")

    def load_images_from_folder(self, folder_path):
        enc_file = os.path.join(folder_path, "directories.enc")
        if not os.path.exists(enc_file):
            return

        with open(enc_file, "r") as f:
            for line in f:
                file_name = line.strip()
                if not file_name:
                    continue
                file_path = os.path.join(folder_path, file_name)
                if file_name.lower().endswith('.png') and os.path.isfile(file_path):
                    pixmap = QPixmap(file_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    item = QListWidgetItem(QIcon(pixmap), file_name)
                    item.setData(Qt.UserRole, file_path)
                    self.image_list.addItem(item)

    def display_image(self, item):
        file_path = item.data(Qt.UserRole)
        pixmap = QPixmap(file_path).scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image = Image.open(file_path)
        self.decode_button.setEnabled(True)

    def decode_image(self):
        if self.image is not None:
            password = imageDecoder.decode_password_from_image(self.image)

            # Show the password on a new screen
            self.show_password_screen(password)

    def show_password_screen(self, password):
        self.password_window = QMainWindow(self)
        self.password_window.setWindowTitle("Decoded Password")
        self.password_window.setMinimumSize(400, 200)

        layout = QVBoxLayout()

        # Password label with hidden text
        self.password_label = QLabel("Decoded Password: ********")
        self.password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(self.password_label)

        # Show password on hover
        self.password_label.setToolTip(password)
        self.password_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: white;
        """)
        self.password_label.setToolTipDuration(0)  # Ensures the tooltip stays visible
        self.password_label.setToolTip(password)
        self.setStyleSheet("""
            QToolTip { 
            background-color: black; 
            color: white; 
            border: 1px solid white; 
            font-size: 14px; 
            }
        """)

        # Copy to clipboard button
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setStyleSheet("""
            font-size: 14px; 
            font-weight: bold; 
            color: white; 
            background-color: rgb(60, 90, 255;
            QPushButton:pressed {
                background-color: rgb(30, 60, 200);
            }
        """)
        self.copy_button.clicked.connect(lambda: self.copy_to_clipboard(password))
        layout.addWidget(self.copy_button)

        frame = QFrame()
        frame.setLayout(layout)
        self.password_window.setCentralWidget(frame)
        self.password_window.show()

    def copy_to_clipboard(self, password):
        clipboard = QApplication.clipboard()
        clipboard.setText(password)

    def return_to_main(self):
        from gui_main import MainScreen  # Import here to avoid circular imports
        self.main_screen = MainScreen()
        self.main_screen.show()
        self.close()


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
    window = DecodeScreen()
    window.show()
    sys.exit(app.exec_())
