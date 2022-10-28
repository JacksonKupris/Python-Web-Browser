import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.showMaximized()

        navbar = QToolBar()
        self.addToolBar(navbar)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        back_btn = QAction('Back', self)
        back_btn.setStatusTip('Go back a page')
        back_btn.triggered.connect(
            lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.setStatusTip('Go forward a page')
        forward_btn.triggered.connect(
            lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.setStatusTip('Refresh')
        reload_btn.triggered.connect(
            lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.setStatusTip('Home')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.add_new_tab(QUrl('https://www.google.com'), 'New Tab')

        self.show()

    def add_new_tab(self, qurl=None, label='Blank'):
        if qurl is None:
            qurl = QUrl('https://www.google.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)

        tab_index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(tab_index)

        browser.urlChanged.connect(
            lambda qurl, tab_index=tab_index, browser=browser: self.update_url_bar(qurl, browser))

        browser.loadFinished.connect(lambda _, tab_index=tab_index, browser=browser: self.tabs.setTabText(
            tab_index, browser.page().title()))

    def tab_open_doubleclick(self, tab_index):
        if tab_index == -1:
            self.add_new_tab()

    def current_tab_changed(self, tab_index):
        qurl = self.tabs.currentWidget().url()
        self.update_url(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, tab_index):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(tab_index)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s" % title)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl('https://www.google.com'))

    def navigate_to_url(self):
        qurl = QUrl(self.url_bar.text())

        if qurl.scheme() == "":
            qurl.setScheme('http')

        self.tabs.currentWidget().setUrl(qurl)

    def update_url(self, q, *args):
        self.url_bar.setText(q.toString())

    def update_url_bar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(q.toString())


app = QApplication(sys.argv)
QApplication.setApplicationName('Python-Browser')
window = MainWindow()
app.exec_()
