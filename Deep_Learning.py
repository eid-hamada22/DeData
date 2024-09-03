from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.QtCore as QtCore
import sqlite3 as sql, time
import sys, requests, os
import QCustomWidgets
import QTools, QPloting
import pandas as pd
import os
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Deep_Learning(QWidget):


    class FileRepresentation:
        def __init__(self, file_full_path, file_archive_path, file_df, file_label, reg, bin, file_id):
            self.file_full_path = file_full_path
            self.file_archive_path = file_archive_path
            self.file_df = file_df
            self.file_label = file_label
            self.reg = reg; self.bin = bin
            self.file_id = file_id

    def connect_database(self):
        self.db = sql.connect('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\database.sqlite3')
    
    def __init__(self, id_,file_combo):
        super().__init__()
        self.connect_database()
        self.widget__ = QMainWindow()
        self.Deep_Learning_layout = QVBoxLayout()
        self.project_id = id_

        self.Deep_Learning_sb = QScrollArea()
        self.Deep_Learning_sb_widget = QWidget()
        self.Deep_Learning_sb_layout = QVBoxLayout()
        self.Deep_Learning_sb_widget.setLayout(self.Deep_Learning_sb_layout)
        self.Deep_Learning_sb.setWidget(self.Deep_Learning_sb_widget)
        self.Deep_Learning_sb.setWidgetResizable(True)
        self.Deep_Learning_layout.addWidget(self.Deep_Learning_sb)

        # DB stuff:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM models WHERE alg_type = 'un_supervised'")
        self.models = cur.fetchall()
        cur.close()
        def choose_file_combo_f(e):
            file_id = self.choose_file_structure[self.choose_file_combo.currentIndex()][0]
            extension = self.choose_file_combo.getOption().split('.')[-1]
            path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\projects\\{id_}\\{file_id}.{extension}"
            cur = self.db.cursor()
            cur.execute("SELECT label, reg, binary FROM files WHERE file_id = ?", (file_id,))
            label, reg, bin = cur.fetchall()[0]
            file_df = QTools.read_file(path)
            cur.close()
            if label:
                self.current_file = self.FileRepresentation(
                    file_full_path=self.choose_file_combo.getOption(),
                    file_archive_path=path,
                    file_label=label,
                    reg=reg, bin=bin,
                    file_id=file_id,
                    file_df=file_df
                )
            else:
                msg_box = QMessageBox()
                msg_box.setStyleSheet('background-color:#333; color:#fff;')
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("You fotgot to set the label to your file!")
                msg_box.setWindowTitle("Error")
                msg_box.addButton("OK", QMessageBox.AcceptRole)
                msg_box.exec_()
        self.choose_file_combo = QCustomWidgets.DarkComboBox()
        self.choose_file_combo.activated.connect(choose_file_combo_f)
        cur = self.db.cursor()
        cur.execute("SELECT file_id, file_full_path FROM files")
        self.choose_file_structure = cur.fetchall()
        cur.close()
        for i in self.choose_file_structure:
            self.choose_file_combo.addItem(i[1])
        # self.Deep_Learning_sb_layout.addWidget(self.choose_file_combo)
        ##
        cur = self.db.cursor()
        cur.execute(
            f"SELECT file_id, label, header FROM files WHERE  project_id = {id_}", )
        if cur.fetchone() :
            choose_file_combo_f(0)
        cur.close()
        ###


        web_Eng = QWebEngineView()
        web_Eng.setUrl(QUrl("https://playground.tensorflow.org/"))
        web_Eng.setMinimumHeight(600)
        self.Deep_Learning_sb_layout.addWidget(web_Eng)


        work_space = QWidget();self.Deep_Learning_sb_layout.addWidget(work_space)
        work_space_layout = QHBoxLayout();work_space.setLayout(work_space_layout)

        self.Deep_Learning_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.Deep_Learning_layout)
