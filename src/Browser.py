import os 
import sys 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from managebkmrks import Bookmarks_Dialog, Add_Bookmark_Dialog, dir_icons
from bookmark_ie import *

class MainWindow(QMainWindow): 

	def __init__(self, *args, **kwargs): 
		super(MainWindow, self).__init__(*args, **kwargs) 

		self.tabs = QTabWidget() 
		self.tabs.setDocumentMode(True) 
		self.setWindowIcon(QIcon("Icons/browseremblem.jpg"))

		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick) 
		self.tabs.currentChanged.connect(self.current_tab_changed) 
		self.tabs.setTabsClosable(True) 
		self.tabs.tabCloseRequested.connect(self.close_current_tab) 

		self.setCentralWidget(self.tabs) 

		self.status = QStatusBar() 
		self.setStatusBar(self.status) 

		navtb = QToolBar("Navigation") 

		self.addToolBar(navtb) 

        # Buttons QIcon(os.path.join('icons', 'name.png')), "Back" (icon format insertion for future)
		back_button = QAction(QIcon(os.path.join('Icons', 'Back.jpg')), "Back", self) 
		back_button.setStatusTip("Go back to your previous page")
		back_button.setShortcut("Ctrl+P") 
		back_button.triggered.connect(lambda: self.tabs.currentWidget().back()) 
		navtb.addAction(back_button) 

		next_button = QAction(QIcon(os.path.join('Icons', 'Forward.jpg')),"Forward", self) 
		next_button.setStatusTip("Go forward to your next page")
		next_button.setShortcut("Ctrl+N")  
		next_button.triggered.connect(lambda: self.tabs.currentWidget().forward()) 
		navtb.addAction(next_button) 

		reload_button = QAction(QIcon(os.path.join('Icons', 'Reload.jpg')),"Reload", self) 
		reload_button.setStatusTip("Reload the page")
		reload_button.setShortcut("Ctrl+R")  
		reload_button.triggered.connect(lambda: self.tabs.currentWidget().reload()) 
		navtb.addAction(reload_button) 

		home_button = QAction(QIcon(os.path.join('Icons', 'Home.jpg')),"Home", self) 
		home_button.setStatusTip("Go to your homepage") 
		home_button.setShortcut("Ctrl+H") 
		home_button.triggered.connect(self.navigate_home) 
		navtb.addAction(home_button) 

		navtb.addSeparator() 

		#Loaded URL security icon
		self.httpsicon = QLabel()
		self.httpsicon.setPixmap(QPixmap(os.path.join('Icons', 'lock.jpg')))
		navtb.addWidget(self.httpsicon)

        # URL bar
		self.urlbar = QLineEdit() 
		self.urlbar.returnPressed.connect(self.navigate_to_url) 

		navtb.addWidget(self.urlbar) 

		stop_btn = QAction("Stop", self) 
		stop_btn.setStatusTip("Stop loading current page")
		stop_btn.setShortcut("Ctrl+T")  
		stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop()) 
		navtb.addAction(stop_btn) 
	
		# Initial tab 
		self.add_new_tab(QUrl.fromLocalFile(os.path.abspath(os.path.join(
			os.path.dirname(__file__), "sample_homepage.html")))) 

		self.show() 
		self.setWindowTitle("Zeta Browser") 
		
		darkmode="dark_mode.css"
		with open(darkmode,"r") as dm:
			self.setStyleSheet(dm.read())
		#self.setStyleSheet(os.path.abspath(os.path.join(
		#	os.path.dirname(__file__), "dark_mode.css")))

		self.bookmarks = bkmrk_import("bookmarks.txt")
		self.favorites = fav_import("favorites.txt")

		self.addbookmarkBtn = QToolButton(self)
		self.addbookmarkBtn.setIcon(QIcon(os.path.join('Icons', 'bookmarks.jpg')))
		self.addbookmarkBtn.setToolTip("Add Bookmark")
		self.addbookmarkBtn.setShortcut("Ctrl+B")        
		navtb.addWidget(self.addbookmarkBtn)
		self.addbookmarkBtn.clicked.connect(self.addbookmark)

		self.bookmarkBtn = QPushButton("Bookmarks", self)
		self.bookmarkBtn.setToolTip("Manage Bookmarks\n         [Alt+B]")
		self.bookmarkBtn.setShortcut("Alt+B")
		navtb.addWidget(self.bookmarkBtn)
		self.bookmarkBtn.clicked.connect(self.managebookmarks)

		self.file_menu = self.menuBar().addMenu("&File")
		self.save_file_action = QAction("Save Page As...", self)
		self.save_file_action.setStatusTip("Save current page to file")
		self.save_file_action.triggered.connect(self.save_file)
		self.file_menu.addAction(self.save_file_action)

		self.view_history_action = QAction("History",self)
		self.view_history_action.setStatusTip("View search history")
		self.view_history_action.triggered.connect(self.view_history)
	
	def view_history(self):
		pass #Still being worked on

	def GoTo(self, url):
		URL = QUrl.fromUserInput(url)
		self.browser.load(URL)

	def addbookmark(self):
		dialog = QDialog(self)
		addbmkdialog = Add_Bookmark_Dialog()
		addbmkdialog.set_ui(dialog)
        
		addbmkdialog.titleEdit.setText(QWebEngineView().title())
		addbmkdialog.addressEdit.setText(self.urlbar.text())
          
		if (dialog.exec_() == QDialog.Accepted):
			url = addbmkdialog.addressEdit.text()
			bmk = [addbmkdialog.titleEdit.text(), url] 
			self.bookmarks = bkmrk_import("bookmarks.txt")
			self.bookmarks.insert(0, bmk)
			bkmrk_export("bookmarks.txt", self.bookmarks)
	
	def managebookmarks(self):
		dialog = QDialog(self)
		bmk_dialog = Bookmarks_Dialog()
		bmk_dialog.set_ui(dialog, self.bookmarks, self.favourites)
       
		bmk_dialog.bookmarks_table.doubleclicked.connect(self.GoTo)

		dialog.exec_()

	def add_new_tab(self, qurl = None, label ="Blank"): 
		if qurl is None: 
			qurl = QUrl.fromLocalFile(os.path.abspath(os.path.join(
			os.path.dirname(__file__), "sample_homepage.html"))) 

		browser = QWebEngineView() 
		browser.setUrl(qurl) 

		i = self.tabs.addTab(browser, label) 
		self.tabs.setCurrentIndex(i) 

		browser.urlChanged.connect(lambda qurl, browser = browser: 
								self.update_urlbar(qurl, browser)) 

		browser.loadFinished.connect(lambda _, i = i, browser = browser: 
									self.tabs.setTabText(i, browser.page().title())) 

	def tab_open_doubleclick(self, i): 
		if i == -1: 
			self.add_new_tab() 

	def current_tab_changed(self, i): 
		qurl = self.tabs.currentWidget().url() 
		self.update_urlbar(qurl, self.tabs.currentWidget()) 
		self.update_title(self.tabs.currentWidget()) 

	def close_current_tab(self, i): 
		if self.tabs.count() < 2: 
			return
		self.tabs.removeTab(i) 

	def update_title(self, browser): 
		if browser != self.tabs.currentWidget(): 
			return
		title = self.tabs.currentWidget().page().title() 
		self.setWindowTitle("% s - Zeta Browser" % title) 

	def navigate_home(self): 
		self.tabs.currentWidget().setUrl(QUrl.fromLocalFile(os.path.abspath(os.path.join(
			os.path.dirname(__file__), "sample_homepage.html")))) 

	def navigate_to_url(self): 
		q = QUrl(self.urlbar.text()) 
		if q.scheme() == "": 
			q.setScheme("http") 
		self.tabs.currentWidget().setUrl(q) 

	def update_urlbar(self, q, browser = None): 
		if browser != self.tabs.currentWidget(): 
			return
		if q.scheme() == 'https':
			self.httpsicon.setPixmap(QPixmap(os.path.join('Icons', 'lock.jpg')))
		else:
			self.httpsicon.setPixmap(QPixmap(os.path.join('Icons', 'unlock.jpg')))
		self.urlbar.setText(q.toString()) 
		self.urlbar.setCursorPosition(0) 

	def save_file(self):
		filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")
	    
app = QApplication(sys.argv) 
app.setApplicationName("Zeta Browser") 
window = MainWindow()  
app.exec_() 
