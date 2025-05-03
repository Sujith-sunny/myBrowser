import sys
from PyQt5.QtWidgets import QApplication
from browser.window import BrowserWindow


def main():
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
