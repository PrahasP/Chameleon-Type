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
        self.setWindowTitle("Chameleon Type: Encode")
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
        self.name_input.setPlaceholderText("Enter image name here (e.g., encoded_image)")
        self.layout.addWidget(self.name_input)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.openDirectoryScreen)
        self.layout.addWidget(self.next_button)

        self.setCentralWidget(frame)

    def openDirectoryScreen(self):
        image_name = self.name_input.text()
        if self.image and self.password and image_name:
            self.directory_screen = DirectoryScreen(self.image, self.password, image_name)
            self.directory_screen.show()
            self.close()


class DirectoryScreen(QMainWindow):
    def __init__(self, image, password, image_name):
        super().__init__()
        self.setWindowTitle("Select Save Directory")
        self.setMinimumSize(400, 200)

        self.image = image
        self.password = password
        self.image_name = image_name

        frame = QFrame()
        self.layout = QVBoxLayout(frame)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Choose a directory to save the encoded image:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        self.layout.addWidget(self.label)

        self.dir_button = QPushButton("Select Directory")
        self.dir_button.clicked.connect(self.select_directory)
        self.layout.addWidget(self.dir_button)

        self.setCentralWidget(frame)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            try:
                output_path = os.path.join(directory, f"{self.image_name}.png")
                imageEncoder.encode_password_in_image(self.image, self.password, output_path)
                print("Image encoding completed.")

                # Append the full file path (including file name) to "Encoded Passwords/directories.enc"
                enc_dir_file = os.path.join("Encoded Passwords", "directories.enc")
                os.makedirs(os.path.dirname(enc_dir_file), exist_ok=True)
                # Normalize the path to use backslashes on Windows
                normalized_path = os.path.normpath(output_path)
                with open(enc_dir_file, "a", encoding="utf-8") as f:
                    f.write(normalized_path + "\n")

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
