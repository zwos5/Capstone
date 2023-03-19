import sys, os
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import ( QApplication, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QGridLayout, QLabel, QTabWidget,
    QPushButton, QDialogButtonBox )
from file_validate import *

def _fromUtf8(s):
    return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class UrlBox(QLineEdit):
    def __init__(self, parent):
        QLineEdit.__init__(self, parent)
        font = self.font()
        font.setPointSize(9)
        self.setFont(font)
    def setText(self, text):
        super(UrlBox, self).setText(text)
        self.setCursorPosition(0)


class BookmarksTable(QTableWidget):
    doubleclicked = QtCore.pyqtSignal(str)
    urlSelected = QtCore.pyqtSignal(str)
    def __init__(self, parent, item_list, use_icons=False):
        QTableWidget.__init__(self, len(item_list), 1, parent)
        self.itemSelectionChanged.connect(self.on_select)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(1) # Select Rows
        #self.setHorizontalHeaderLabels(["Title", "Address"])
        #self.horizontalHeader().setDefaultSectionSize(240)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        #self.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)
        self.horizontalHeader().setHidden(True)
        self.verticalHeader().setHidden(True)
        self.use_icons = use_icons
        self.data_changed = False
        self.data = item_list[:]
        self.set_user_data()

    def set_user_data(self):
        for row, item in enumerate (self.data):
            title_item = QTableWidgetItem(item[0])
            font = title_item.font()
            font.setBold(True)
            title_item.setFont(font)
            if self.use_icons:
                icon = QIcon(dir_icons + QtCore.QUrl(item[1]).host() + '.jpg')
                if icon.pixmap(16, 16).isNull(): icon = QIcon(os.path.join('Icons', 'browseremblem.jpg'))
                title_item.setIcon(icon)
            
            self.setItem(row, 0, title_item)
    
    def event_dbl_click(self, e):
        url = self.data[self.rowAt(e.pos().y())][1]
        self.doubleclicked.emit(url)

    def on_select(self):
        rows = self.selectionModel().selectedRows()
        if len(rows) == 1:
            item = rows[0]
            url = self.data[item.row()][1]
            self.urlSelected.emit(url)
        else:
            self.urlSelected.emit('')

    def item_up(self):
        row = self.selectionModel().selectedRows()[0].row()
        if row == 0: return
        self.data[row-1], self.data[row] = self.data[row], self.data[row-1]
        lower, upper = self.takeItem(row, 0), self.takeItem(row-1, 0)
        self.setItem(row, 0, upper)
        self.setItem(row-1, 0, lower)
        self.row_select(row-1)
        self.data_changed = True

    def item_down(self):
        row = self.selectionModel().selectedRows()[0].row()
        if row == len(self.data) - 1 : return
        self.data[row+1], self.data[row] = self.data[row], self.data[row+1]
        upper, lower = self.takeItem(row, 0), self.takeItem(row+1, 0)
        self.setItem(row, 0, lower)
        self.setItem(row+1, 0, upper)
        self.row_select(row+1)
        self.data_changed = True

    def copy_site_link(self):
        row = self.selectionModel().selectedRows()[0].row()
        addr = self.data[row][1]
        QApplication.clipboard().setText(addr)

    def edit_item(self):
        row = self.selectionModel().selectedRows()[0].row()
        title, addr = self.data[row][0], self.data[row][1]
        dialog = QDialog(self)
        edit_dialog = Add_Bookmark_Dialog()
        edit_dialog.set_ui(dialog)
        edit_dialog.titleEdit.setText(title)
        edit_dialog.addressEdit.setText(addr)
        dialog.setWindowTitle('Edit Item')
        if (dialog.exec_() == QDialog.Accepted):
            title = str(edit_dialog.titleEdit.text())
            self.data[row][0], self.data[row][1] = title, str(edit_dialog.addressEdit.text())
            self.item(row, 0).setText(title)
            self.data_changed = True

    def delete_item(self):
        rows = self.selectionModel().selectedRows()
        self.clearSelection()
        selected_rows = [item.row() for item in rows]
        selected_rows.sort()
        for row in selected_rows:
            del self.data[row - selected_rows.index(row)]
            self.removeRow(row - selected_rows.index(row))
        self.data_changed = True

    def row_select(self, row):
        index = self.indexFromItem(self.item(row, 0))
        self.selectionModel().select(index, QItemSelectionModel.ClearAndSelect)

class Bookmarks_Dialog(object):
    def set_ui(self, Dialog, bookmark_data, favorites):
        Dialog.resize(740, 450)
        Dialog.setWindowTitle('Bookmarks Manager')
        self.layout = QGridLayout(Dialog)
        self.urlLabel = QLabel('URL :', Dialog)
        self.layout.addWidget(self.urlLabel, 0, 0, 1, 1)
        self.urlBox = UrlBox(Dialog)
        self.layout.addWidget(self.urlBox, 0, 1, 1, 5)

        # Create Tab Widget
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.tabBar().setExpanding(True)

        # Add Bookmarks Table
        self.bookmarks_table = BookmarksTable(Dialog, bookmark_data, True)
        self.tabWidget.addTab(self.bookmarks_table, 'Bookmarks') 
        
        # Add Favorites table
        self.layout.addWidget(self.tabWidget, 1, 0, 1, 6)
        
        # Add Buttons
        self.move_up_button = QPushButton(QIcon(os.path.join('Icons', 'defaulttext.jpg')), 'Up', Dialog) # DefaultText.png is a placeholder since I can't get the icons to load correctly
        self.move_up_button.clicked.connect(self.item_up)
        self.layout.addWidget(self.move_up_button, 2, 0, 1, 1)

        self.move_dwn_button = QPushButton(QIcon(os.path.join('Icons', 'defaulttext.jpg')), 'Down', Dialog)
        self.move_dwn_button.clicked.connect(self.item_down)
        self.layout.addWidget(self.move_dwn_button, 2, 1, 1, 1)

        self.copy_link = QPushButton(QIcon(os.path.join('Icons', 'defaulttext.jpg')), 'Copy', Dialog)
        self.copy_link.clicked.connect(self.copy_site_link)
        self.layout.addWidget(self.copy_link, 2, 2, 1, 1)

        self.edit_button = QPushButton(QIcon(os.path.join('Icons', 'defaulttext.jpg')), 'Edit', Dialog)
        self.edit_button.clicked.connect(self.edit_item)
        self.layout.addWidget(self.edit_button, 2, 3, 1, 1)

        self.delete_button = QPushButton(QIcon(os.path.join('Icons', 'defaulttext.jpg')), 'Delete', Dialog)
        self.delete_button.clicked.connect(self.delete_item)
        self.layout.addWidget(self.delete_button, 2, 4, 1, 1)

        # Add ButtonBox
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
        self.layout.addWidget(self.buttonBox, 2, 5, 1, 1)

        self.bookmarks_table.urlSelected.connect(self.urlBox.setText)
        self.bookmarks_table.doubleclicked.connect(Dialog.accept)
        self.bookmarks_table.itemSelectionChanged.connect(self.toggle_access)

        self.tabWidget.currentChanged.connect(self.toggle_access)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.bookmarks_table.row_select(0)
        self.bookmarks_table.setFocus()

    def toggle_access(self):
        selection_count = len(self.tabWidget.currentWidget().selectedIndexes())
        if selection_count == 1:
            self.enabled_button(True, True, True, True, True)
        elif selection_count > 1:
            self.enabled_button(False, False, False, False, True)
        else:
            self.enabled_button(False, False, False, False, False)

    def enabled_button(self, state1, state2, state3, state4, state5):
        self.move_up_button.setEnabled(state1)
        self.move_dwn_button.setEnabled(state2)
        self.copy_link.setEnabled(state3)
        self.edit_button.setEnabled(state4)
        self.delete_button.setEnabled(state5)

    def item_up(self):
        self.tabWidget.currentWidget().item_up()
        self.tabWidget.currentWidget().setFocus()

    def item_down(self):
        self.tabWidget.currentWidget().item_down()
        self.tabWidget.currentWidget().setFocus()

    def copy_site_link(self):
        self.tabWidget.currentWidget().copy_site_link()
        self.tabWidget.currentWidget().setFocus()

    def edit_item(self):
        self.tabWidget.currentWidget().edit_item()
        self.tabWidget.currentWidget().setFocus()

    def delete_item(self):
        self.tabWidget.currentWidget().delete_item()


class Add_Bookmark_Dialog(object):
    def set_ui(self, Dialog):
        Dialog.resize(640, 165)
        Dialog.setWindowTitle("Add Bookmark")
        self.gridLayout = QGridLayout(Dialog)
        self.label = QLabel(Dialog)
        self.label.setText("Title :")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.titleEdit = QLineEdit(Dialog)
        self.gridLayout.addWidget(self.titleEdit, 0, 1, 1, 1)
        self.label_2 = QLabel(Dialog)
        self.label_2.setText("Address :")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.addressEdit = QLineEdit(Dialog)
        self.gridLayout.addWidget(self.addressEdit, 1, 1, 1, 1)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)