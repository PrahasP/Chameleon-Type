import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame, QPushButton, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image

class EncodeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Lion: Encode")
        self.setMinimumSize(400, 300)

        self.image = None  # Image that we're gonna encode

        frame = QFrame()
        self.layout = QVBoxLayout(frame)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Encode Screen")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.layout.addWidget(self.label)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.file_button = QPushButton("Open File Explorer")
        self.file_button.clicked.connect(self.open_file_explorer)
        self.layout.addWidget(self.file_button)

        self.setCentralWidget(frame)

    def open_file_explorer(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilters(["PNG Files (*.png)"])
        file_dialog.setViewMode(QFileDialog.Detail)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                print("Selected file:", file_path)
                try:
                    # Use Pillow to open the image and store in self.image
                    self.image = Image.open(file_path)
                    print("Image loaded successfully.")

                    # Show image preview
                    pixmap = QPixmap(file_path)
                    self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
                except Exception as e:
                    print("Failed to load image:", e)


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
    """)
    window = EncodeScreen()
    window.show()
    sys.exit(app.exec_())
