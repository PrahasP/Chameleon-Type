import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
import imageEncoder


class EncodeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Lion: Encode")
        self.setMinimumSize(400, 300)

        self.image = None  # Image that we're gonna encode
        self.encoded_password = None  # Placeholder for the encoded password

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

        self.encode_button = None  # Placeholder for the encode button

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

                    # Add the "Encode this image" button if it doesn't exist
                    if not self.encode_button:
                        self.encode_button = QPushButton("Encode this image")
                        self.encode_button.clicked.connect(self.go_to_password_screen)
                        self.layout.addWidget(self.encode_button)
                except Exception as e:
                    print("Failed to load image:", e)

    def go_to_password_screen(self):
        if self.image:
            self.password_screen = PasswordScreen(self.image)
            self.password_screen.show()
            self.close()


class PasswordScreen(QMainWindow):
    def __init__(self, image):
        super().__init__()
        self.setWindowTitle("Enter Password")
        self.setMinimumSize(400, 300)

        self.image = image  # Store the image passed from the previous screen

        frame = QFrame()
        self.layout = QVBoxLayout(frame)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Enter a password to encode:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password here")
        self.layout.addWidget(self.password_input)

        self.encode_button = QPushButton("Encode Image")
        self.encode_button.clicked.connect(self.encode_image)
        self.layout.addWidget(self.encode_button)

        self.setCentralWidget(frame)

    def encode_image(self):
        password = self.password_input.text()
        if self.image and password:
            try:
                # Call the imageEncoder function with the provided password
                imageEncoder.encode_password_in_image(self.image, password, "Encoded Passwords/encoded_image.png")
                print("Image encoding completed.")
                self.close()
            except Exception as e:
                print("Failed to encode image:", e)


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
    QLineEdit {
        padding: 5px;
        font-size: 14px;
    }
    """)
    window = EncodeScreen()
    window.show()
    sys.exit(app.exec_())
