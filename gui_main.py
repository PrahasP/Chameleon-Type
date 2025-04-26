import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame, QPushButton
from PyQt5.QtCore import Qt

class SimpleScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Lion")
        self.setMinimumSize(400, 300)

        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button1 = QPushButton("Encode")
        layout.addWidget(self.button1)

        self.button2 = QPushButton("Decode")
        layout.addWidget(self.button2)

        self.setCentralWidget(frame)

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
    window = SimpleScreen()
    window.show()
    sys.exit(app.exec_())