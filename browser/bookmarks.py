
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QAction, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QToolBar, QStatusBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from . import settings
from . import bookmarks
import os
import json
import logging
from typing import List, Dict, Any
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Load bookmarks from JSON file
def load_bookmarks(file_path: str) -> List[Dict[str, Any]]:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []
# Save bookmarks to JSON file
def save_bookmarks(file_path: str, bookmarks: List[Dict[str, Any]]):
    with open(file_path, 'w') as f:
        json.dump(bookmarks, f, indent=4)
# Bookmark class to manage individual bookmarks
class Bookmark:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    def to_dict(self) -> Dict[str, Any]:
        return {
            'title': self.title,
            'url': self.url
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Bookmark':
        return cls(data['title'], data['url'])
# BookmarkManager class to manage the list of bookmarks
class BookmarkManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.bookmarks = load_bookmarks(file_path)

    def add_bookmark(self, title: str, url: str):
        new_bookmark = Bookmark(title, url)
        self.bookmarks.append(new_bookmark.to_dict())
        save_bookmarks(self.file_path, self.bookmarks)
        logging.info(f"Added bookmark: {title} - {url}")

    def remove_bookmark(self, title: str):
        self.bookmarks = [b for b in self.bookmarks if b['title'] != title]
        save_bookmarks(self.file_path, self.bookmarks)
        logging.info(f"Removed bookmark: {title}")

    def get_bookmarks(self) -> List[Dict[str, Any]]:
        return self.bookmarks

    def clear_bookmarks(self):
        self.bookmarks = []
        save_bookmarks(self.file_path, self.bookmarks)
        logging.info("Cleared all bookmarks")

    def search_bookmarks(self, query: str) -> List[Dict[str, Any]]:
        return [b for b in self.bookmarks if query.lower() in b['title'].lower()]

    def get_bookmark_by_title(self, title: str) -> Dict[str, Any]:
        for bookmark in self.bookmarks:
            if bookmark['title'] == title:
                return bookmark
        return None

    def get_bookmark_by_url(self, url: str) -> Dict[str, Any]:
        for bookmark in self.bookmarks:
            if bookmark['url'] == url:
                return bookmark
        return None

    def get_bookmark_by_index(self, index: int) -> Dict[str, Any]:
        if 0 <= index < len(self.bookmarks):
            return self.bookmarks[index]
        return None

    def get_bookmark_count(self) -> int:
        return len(self.bookmarks)

    def get_bookmark_titles(self) -> List[str]:
        return [b['title'] for b in self.bookmarks]

    def get_bookmark_urls(self) -> List[str]:
        return [b['url'] for b in self.bookmarks]

    def get_bookmark_titles_and_urls(self) -> List[Dict[str, str]]:
        return [{'title': b['title'], 'url': b['url']} for b in self.bookmarks]

    def find_bookmarks(self, title: str = None, url: str = None, match_all: bool = True) -> List[Dict[str, Any]]:
        """
        Find bookmarks based on title and/or URL.

        Args:
            title (str): The title to search for (optional).
            url (str): The URL to search for (optional).
            match_all (bool): If True, match both title and URL. If False, match either.

        Returns:
            List[Dict[str, Any]]: A list of matching bookmarks.
        """
        results = []
        for bookmark in self.bookmarks:
            title_match = title is None or bookmark['title'] == title
            url_match = url is None or bookmark['url'] == url

            if match_all and title_match and url_match:
                results.append(bookmark)
            elif not match_all and (title_match or url_match):
                results.append(bookmark)
        return results