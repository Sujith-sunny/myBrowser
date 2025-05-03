from PyQt5.QtWidgets import QTabWidget, QTabBar, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from . import settings

class TabManager(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.tabBarDoubleClicked.connect(self.new_tab)

        # Add the first tab
        self.new_tab()

    def new_tab(self, index=None):
        browser = QWebEngineView()
        browser.setUrl(QUrl(settings.HOMEPAGE))
        self.addTab(browser, "New Tab")
        self.setCurrentWidget(browser)

    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)