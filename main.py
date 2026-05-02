import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from database import db_manager
from ui.main_window import MainWindow

def load_stylesheet(app: QApplication) -> None:
    qss_path = os.path.join(os.path.dirname(__file__), "styles", "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"[PERINGATAN] File style.qss tidak ditemukan di: {qss_path}")

def main():
    db_manager.init_db()

    app = QApplication(sys.argv)
    app.setApplicationName("Buku Kontak Digital")

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    load_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()