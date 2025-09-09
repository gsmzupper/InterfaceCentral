import sys
from PyQt6.QtWidgets import QApplication
from show_windows import ShowWindows

def main():
    app = QApplication(sys.argv)
    window = ShowWindows()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()