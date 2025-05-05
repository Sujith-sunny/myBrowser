from PyQt5.QtWidgets import QTabWidget, QTabBar, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSignal
import os

class TabManager(QTabWidget):
    url_changed = pyqtSignal(QUrl)  # Signal to notify when the URL changes

    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.tabBarDoubleClicked.connect(self.new_tab)

        # Add the first tab
        self.new_tab()

    def new_tab(self, url=None):
        try:
            browser = QWebEngineView()
            if url:
                browser.setUrl(QUrl(url))
            else:
                homepage_path = os.path.abspath("ui/homepage.html")
                browser.setUrl(QUrl.fromLocalFile(homepage_path))

            browser.urlChanged.connect(self.url_changed)
            self.addTab(browser, "New Tab")
            self.setCurrentWidget(browser)
        except Exception as e:
            print(f"Error creating new tab: {e}")

    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)


# TODO: Add a method that allows the user to open a new tab with a specific URL
# TODO: Add a method to open a new tab with clicking on "open Link in New Tab"