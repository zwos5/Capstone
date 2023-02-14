import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class ZetaBrowser(QMainWindow):
	def __init__(self):
		super(ZetaBrowser, self).__init__()
		self.browser = QWebEngineView()
		self.browser.setUrl(QUrl('http://nsuok.edu'))
		self.setCentralWidget(self.browser)
		self.showMaximized()

		#navigation bar
		navbar = QToolBar()
		self.addToolBar(navbar)

		back_button = QAction('Back', self)
		back_button.triggered.connect(self.browser.back)
		navbar.addAction(back_button)

		forward_button = QAction('Forward', self)
		forward_button.triggered.connect(self.browser.forward)
		navbar.addAction(forward_button)

		self.url_bar = QLineEdit()
		self.url_bar.returnPressed.connect(self.navigate_to_url)
		navbar.addWidget(self.url_bar)

		self.browser.urlChanged.connect(self.update_url)

	def navigate_to_url(self):
		url = self.url_bar.text()
		self.browser.setUrl(QUrl(url))

	def update_url(self, x):
		self.url_bar.setText(x.toString())

app = QApplication(sys.argv)
QApplication.setApplicationName('Zeta Browser')
window = ZetaBrowser()
app.exec_()
