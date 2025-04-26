import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame, QPushButton, QLabel
from PyQt5.QtCore import Qt
from gui_encode import EncodeScreen  # Import the screen from gui_encode.py
from gui_decode import DecodeScreen  # Import the screen from gui_decode.py

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Lion")
        self.setMinimumSize(400, 300)

        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("The Lion")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(self.label)

        self.button1 = QPushButton("Encode")
        self.button1.clicked.connect(self.open_encode_screen)  # Connect to the encode screen
        layout.addWidget(self.button1)

        self.button2 = QPushButton("Decode")
        self.button2.clicked.connect(self.open_decode_screen)  # Connect to the decode screen
        layout.addWidget(self.button2)

        self.setCentralWidget(frame)

    def open_encode_screen(self):
        self.encode_screen = EncodeScreen()  # Create an instance of the EncodeScreen
        self.setCentralWidget(self.encode_screen) # Set it to be the main widget of the window

    def open_decode_screen(self):
        self.decode_screen = DecodeScreen()  # Create an instance of the DecodeScreen
        self.setCentralWidget(self.decode_screen)

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
    window = MainScreen()
    window.show()
    sys.exit(app.exec_())