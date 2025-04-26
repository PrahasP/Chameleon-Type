import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
import imageEncoder
import os


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

        self.name_button = QPushButton("Next")
        self.name_button.clicked.connect(self.openNamingScreen)
        self.layout.addWidget(self.name_button)

        self.setCentralWidget(frame)

    def openNamingScreen(self):
        password = self.password_input.text()
        if self.image and password:
            # Call the naming screen with the image and password
            self.naming_screen = NamingScreen(self.image, password)
            self.naming_screen.show()
            self.close()


class NamingScreen(QMainWindow):
    def __init__(self, image, password):
        super().__init__()
        self.setWindowTitle("Set Image Name")
        self.setMinimumSize(400, 300)

        self.image = image  # Store the image passed from the previous screen
        self.password = password  # Store the password passed from the previous screen

        frame = QFrame()
        self.layout = QVBoxLayout(frame)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Enter a name for the encoded image:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.layout.addWidget(self.label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter image name here (e.g., encoded_image.png)")
        self.layout.addWidget(self.name_input)

        self.encode_button = QPushButton("Save Encoded Image")
        self.encode_button.clicked.connect(self.encode_image)
        self.layout.addWidget(self.encode_button)

        self.setCentralWidget(frame)

    def encode_image(self):
        image_name = self.name_input.text()
        if self.image and self.password and image_name:
            try:
                # Call the imageEncoder function with the provided password and image name
                # Check if the "Encoded Passwords" folder exists, create it if not
                output_folder = "Encoded Passwords"
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                    print(f"Created folder: {output_folder}")

                # Encode the password in the image and save it
                imageEncoder.encode_password_in_image(self.image, self.password, f"{output_folder}/{image_name}.png")
                print("Image encoding completed.")

                # Show the success screen
                self.success_screen = SuccessScreen()
                self.success_screen.show()
                self.close()
            except Exception as e:
                print("Failed to encode image:", e)


class SuccessScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Encoded!")
        self.setMinimumSize(400, 300)

        frame = QFrame()
        self.layout = QVBoxLayout(frame)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Encoded!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.layout.addWidget(self.label)

        self.return_button = QPushButton("Return to Main Screen")
        self.return_button.clicked.connect(self.return_to_main)
        self.layout.addWidget(self.return_button)

        self.setCentralWidget(frame)

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
    QLineEdit {
        padding: 5px;
        font-size: 14px;
    }
    """)
    window = EncodeScreen()
    window.show()
    sys.exit(app.exec_())
