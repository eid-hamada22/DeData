import typing
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.QtCore as QtCore
import sqlite3 as sql, time
import os, sys
from PyQt5.QtWidgets import QWidget
import pandas as pd

class CustomContextMenuButton(QPushButton):
    def __init__(self, create_column_f):
        super().__init__(None)
        self.create_column_f = create_column_f
    def mousePressEvent(self, event):
        if event.button() == 1:  # Left mouse button
            self.showContextMenu(event.globalPos())
        else:
            super().mousePressEvent(event)
            
    def showContextMenu(self, pos):
        context_menu = QMenu(self)
        action1 = QAction("save changes", self)
        action2 = QAction("load the previous page", self)
        action3 = QAction("load the next page", self)
        action4 = QAction("create new column", self)
        action5 = QAction("view in separate window", self)

        context_menu.addAction(action1)
        context_menu.addAction(action2)
        context_menu.addAction(action3)
        context_menu.addAction(action4)
        context_menu.addAction(action5)
        
        selected_action = context_menu.exec_(pos)
        if selected_action == action1:
            print("save changes")
        elif selected_action == action4:
            self.create_column_f()
        elif selected_action == action5:
            print("view")

class QSheet(QScrollArea):
    def __init__(self):
        super(QSheet, self).__init__()
        self.setStyleSheet('background-color: #222;')
        self.sheet_picker_widget = QWidget()
        self.setWidget(self.sheet_picker_widget)
        self.sheet_picker_layout = QVBoxLayout()
        self.sheet_picker_layout.setContentsMargins(0,0,0,0)
        self.sheet_picker_widget.setLayout(self.sheet_picker_layout)
        self.setWidgetResizable(True)
        self.sheet_picker_layout.addStretch()
    def load_pandas_dataframe(self, df: pd.DataFrame):
        self.columns_count = 0; self.rows_count = 0
        if 'sheet_widget' in dir(self): self.sheet_widget.setParent(None)
        self.rows = df.values; headers = df.columns.tolist()
        self.sheet_widget = QWidget()
        self.sheet_layout = QGridLayout()
        self.sheet_widget.setLayout(self.sheet_layout)
        def create_column_f():
            header_input = QLineEdit()
            header_input.setAlignment(Qt.AlignCenter)
            header_input.setStyleSheet("background-color: #333; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
            self.columns_count += 1
            self.sheet_layout.addWidget(header_input, 0, self.columns_count)
            for row in range(1, self.rows_count+1):
                cell_input = QLineEdit()
                cell_input.setStyleSheet("background-color: #444; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
                self.sheet_layout.addWidget(cell_input, row, self.columns_count)
            header_input.setFocus()
        empty_label = CustomContextMenuButton(create_column_f)
        empty_label.setCursor(Qt.PointingHandCursor)
        empty_label.setIcon(QIcon("settings_button.png"))
        empty_label.setIconSize(QSize(20, 20))
        empty_label.setMaximumWidth(65)
        empty_label.setStyleSheet("background-color: #333; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
        self.sheet_layout.addWidget(empty_label, 0, 0)
        for header_index in range(len(headers)):
            header = headers[header_index]
            header_input = QLineEdit(header.__str__())
            header_input.setAlignment(Qt.AlignCenter)
            header_input.setStyleSheet("background-color: #333; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
            self.sheet_layout.addWidget(header_input, 0, header_index+1)
        for y in range(1, 101):
            number_input = QLabel(y.__str__())
            number_input.setMaximumWidth(65)
            number_input.setAlignment(Qt.AlignCenter)
            number_input.setStyleSheet("background-color: #333; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
            self.sheet_layout.addWidget(number_input, y, 0)
            for x in range(len(self.rows[0])):
                try: cell = self.rows[y-1][x]
                except: cell = ''
                cell_input = QLineEdit(cell.__str__())
                cell_input.setStyleSheet("background-color: #444; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
                self.sheet_layout.addWidget(cell_input, y, x+1)
                self.rows_count = y; self.columns_count = x+1
        self.sheet_picker_layout.insertWidget(0, self.sheet_widget)
    def retrive_dataframe(self):
        if 'sheet_widget' in dir(self):
            return 0
        else:
            print("there is no sheet widget load on the picker")

class TestApp(QMainWindow):
    def __init__(self):
        super(TestApp, self).__init__()
        self.setStyleSheet('background-color: #222;')
        self.initui()
    def initui(self):
        sheet = QSheet()
        df = pd.read_csv(r"C:\Users\lenovo\Desktop\file.csv")
        sheet.load_pandas_dataframe(df)
        self.setCentralWidget(sheet)
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_app = TestApp()
    app.exec_()
