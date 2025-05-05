from PyQt5.QtWidgets import QMainWindow, QLineEdit, QToolBar, QAction, QMenu, QMessageBox, QStatusBar, QDialog, QVBoxLayout, QListWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from urllib.parse import urlparse
from . import settings
from .bookmarks import BookmarkManager
from .tabs import TabManager

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(settings.WINDOW_TITLE)
        self.resize(*settings.WINDOW_SIZE)

        self.tabs = TabManager()  # Use TabManager for tabs
        self.setCentralWidget(self.tabs)

        self.bookmark_manager = BookmarkManager("bookmarks.json")  # Initialize BookmarkManager

        self.init_ui()
        self.init_status_bar()

        # Connect the TabManager's url_changed signal to update the URL bar
        self.tabs.url_changed.connect(self.update_url_bar)

    def init_ui(self):
        # Toolbar
        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)

        # Back Button
        back_action = QAction("Back", self)
        back_action.triggered.connect(lambda: self.current_browser().back())
        toolbar.addAction(back_action)

        # Forward Button
        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(lambda: self.current_browser().forward())
        toolbar.addAction(forward_action)

        # Reload Button
        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(lambda: self.current_browser().reload())
        toolbar.addAction(reload_action)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)

        # Go Button
        go_action = QAction("Go", self)
        go_action.triggered.connect(self.navigate_to_url)
        toolbar.addAction(go_action)

        # Bookmark Button
        bookmark_action = QAction("Bookmark", self)
        bookmark_action.triggered.connect(self.add_bookmark)
        toolbar.addAction(bookmark_action)

        # View Bookmarks Button
        view_bookmarks_action = QAction("View Bookmarks", self)
        view_bookmarks_action.triggered.connect(self.view_bookmarks)
        toolbar.addAction(view_bookmarks_action)

        # Bookmarks Menu
        bookmarks_menu = QMenu("Bookmarks", self)
        self.menuBar().addMenu(bookmarks_menu)
        self.update_bookmarks_menu(bookmarks_menu)

        # Update URL Bar when URL changes
        self.tabs.currentChanged.connect(self.update_url_bar_on_tab_change)

    def init_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Update status bar on load events
        self.tabs.currentChanged.connect(self.update_status_bar_on_tab_change)

    def current_browser(self):
        return self.tabs.currentWidget()

    def navigate_to_url(self):
        input_text = self.url_bar.text()
        url = QUrl(input_text)

        # Function to check if the input is a valid URL
        def is_valid_url(string):
            try:
                QUrl(string).isValid()
                return True
            except:
                return False

        if is_valid_url(input_text):
            # If it's a valid URL, navigate directly to the site
            if url.scheme() == "":
                url.setScheme("http")
            self.current_browser().setUrl(url)
        else:
            # Otherwise, treat it as a search query
            query = input_text
            self.open_results_page(query)

    def open_results_page(self, query):
        try:
            # Redirect to the search results page
            results_url = f"http://127.0.0.1:5000/results.html?q={query}"
            self.tabs.new_tab(results_url)
        except Exception as e:
            print(f"Error opening results page: {e}")

    def update_url_bar(self, url):
        """Update the URL bar with the current URL."""
        self.url_bar.setText(url.toString())

    def update_url_bar_on_tab_change(self, index):
        browser = self.current_browser()
        if browser:
            self.url_bar.setText(browser.url().toString())

    def update_status_bar_on_tab_change(self, index):
        browser = self.current_browser()
        if browser:
            browser.loadStarted.connect(lambda: self.status_bar.showMessage("Loading..."))
            browser.loadProgress.connect(lambda p: self.status_bar.showMessage(f"Loading... {p}%"))
            browser.loadFinished.connect(lambda: self.status_bar.showMessage("Done"))

    def add_bookmark(self):
        current_url = self.current_browser().url().toString()
        current_title = self.current_browser().title()
        self.bookmark_manager.add_bookmark(current_title, current_url)
        QMessageBox.information(self, "Bookmark Added", f"Added bookmark: {current_title}")

    def update_bookmarks_menu(self, menu):
        menu.clear()
        for bookmark in self.bookmark_manager.get_bookmarks():
            action = QAction(bookmark['title'], self)
            action.triggered.connect(lambda checked, url=bookmark['url']: self.current_browser().setUrl(QUrl(url)))
            menu.addAction(action)

    def view_bookmarks(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Bookmarks")
        dialog.resize(400, 300)

        layout = QVBoxLayout(dialog)

        # List Widget to display bookmarks
        bookmark_list = QListWidget(dialog)
        for bookmark in self.bookmark_manager.get_bookmarks():
            bookmark_list.addItem(f"{bookmark['title']} - {bookmark['url']}")
        layout.addWidget(bookmark_list)

        # Open Button
        open_button = QPushButton("Open", dialog)
        open_button.clicked.connect(lambda: self.open_selected_bookmark(bookmark_list, dialog))
        layout.addWidget(open_button)

        # Close Button
        close_button = QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def open_selected_bookmark(self, bookmark_list, dialog):
        selected_item = bookmark_list.currentItem()
        if selected_item:
            url = selected_item.text().split(" - ")[1]
            self.current_browser().setUrl(QUrl(url))
            dialog.close()
