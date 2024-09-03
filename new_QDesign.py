from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Import_Data import Import_Data
from Data_Visualization import Data_Visualization
from Workspace import Workspace
from Supervised_Models import Supervised_Models
from Unsupervised_Models import Unsupervised_Models
from Deep_Learning import Deep_Learning
import QCustomWidgets
import PyQt5.QtCore as QtCore
import sqlite3 as sql, time
import sys, requests, os
import QCustomWidgets
import QTools, QPloting
import pandas as pd
import os 




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeData")
        app_icon = QIcon()
        app_icon.addFile('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\logo16.png', QtCore.QSize(16,16))
        app_icon.addFile('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\logo24.png', QtCore.QSize(24,24))
        app_icon.addFile('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\logo32.png', QtCore.QSize(32,32))
        app_icon.addFile('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\logo48.png', QtCore.QSize(48,48))
        app_icon.addFile('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\logo256.png', QtCore.QSize(256,256))
        self.setWindowIcon(app_icon)
        # self.setw
        # QMainWindow.setFixedSize(QSize())
        # self.setFullscreen()
        self.main_layout = QVBoxLayout()
        # self.showFullScreen() 
        self.showMaximized()
        # Create a stack of widgets for the workbench sections
        self.workbench_layout = QStackedWidget()
        # Add Color widgets to the workbench_layout3
        self.file_combo_Data_Visualization = QCustomWidgets.DarkComboBox()
        self.file_combo_Workspace = QCustomWidgets.DarkComboBox()
        self.file_combo_Supervised_Models = QCustomWidgets.DarkComboBox()
        self.file_combo_Unsupervised_Models = QCustomWidgets.DarkComboBox()
        self.file_combo_Deep_Learning = QCustomWidgets.DarkComboBox()
        c_f = [self.file_combo_Data_Visualization,self.file_combo_Workspace,self.file_combo_Supervised_Models,
               self.file_combo_Unsupervised_Models,self.file_combo_Deep_Learning]
        
        self.Import_Data = Import_Data(5,c_f)
        self.Data_Visualization = Data_Visualization(5,self.file_combo_Data_Visualization)
        self.Workspace = Workspace(5,self.file_combo_Workspace)
        self.Supervised_Models = Supervised_Models(5,self.file_combo_Supervised_Models)
        self.Unsupervised_Models = Unsupervised_Models(5,self.file_combo_Unsupervised_Models)
        self.Deep_Learning = Deep_Learning(5,self.file_combo_Deep_Learning)

        self.workbench_layout.addWidget(self.Import_Data)
        self.workbench_layout.addWidget(self.Data_Visualization)
        self.workbench_layout.addWidget(self.Workspace)
        self.workbench_layout.addWidget(self.Supervised_Models)
        self.workbench_layout.addWidget(self.Unsupervised_Models)
        self.workbench_layout.addWidget(self.Deep_Learning)

        # Set the initial index to green
        self.workbench_layout.setCurrentIndex(0)

        # Define a function to change the tab colors
        def tab_f(tab=None):
            if not tab:
                Tab = self.focusWidget()
            else:
                Tab = tab
            for tab in [tab_1, tab_2, tab_3, tab_4, tab_5, tab_6]:
                if tab == Tab:
                    tab.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 5px; padding: 10px 16px;")
                else:
                    tab.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 5px; padding: 10px 16px;")

        # Create tab buttons
        tab_1 = QPushButton("Import Data")
        tab_1.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 5px; padding: 10px 16px;")
        tab_1.setCursor(Qt.PointingHandCursor)
        tab_1.clicked.connect(lambda: self.workbench_layout.setCurrentIndex(0))
        tab_1.clicked.connect(tab_f)

        tab_2 = QPushButton("Data Visualization")
        tab_2.setStyleSheet("background-color: #555555; color: #ffffff; font-size: 16px; border-radius: 5px; padding: 10px 16px;")
        tab_2.setCursor(Qt.PointingHandCursor)
        tab_2.clicked.connect(lambda: self.workbench_layout.setCurrentIndex(1))
        tab_2.clicked.connect(tab_f)
        self.Import_Data.file_added.connect(lambda: self.Data_Visualization.file_combo.fun2(0))

        tab_3 = QPushButton("Workspace")
        tab_3.setStyleSheet("background-color: #555555; color: #ffffff; font-size: 16px; border-radius: 5px; padding: 10px 16px;")
        tab_3.setCursor(Qt.PointingHandCursor)
        tab_3.clicked.connect(lambda: self.workbench_layout.setCurrentIndex(2))
        tab_3.clicked.connect(tab_f)
        tab_3.clicked.connect(lambda: self.Workspace.file_combo.fun1(0))
        tab_3.clicked.connect(lambda: self.Workspace.file_combo.fun2(0))
        tab_3.clicked.connect(lambda: self.Workspace.file_combo.fun3(0))

        tab_4 = QPushButton("Supervised Models")
        tab_4.setStyleSheet("background-color: #555555; color: #ffffff; font-size: 16px; border-radius: 5px; padding: 10px 16px;")
        tab_4.setCursor(Qt.PointingHandCursor)
        tab_4.clicked.connect(lambda: self.workbench_layout.setCurrentIndex(3))
        tab_4.clicked.connect(tab_f)
        tab_4.clicked.connect(lambda: self.Supervised_Models.file_combo.fun1(0))
        tab_4.clicked.connect(lambda: self.Supervised_Models.file_combo.fun2(0))

        tab_5 = QPushButton("Unsupervised Models")
        tab_5.setStyleSheet("background-color: #555555; color: #ffffff; font-size: 16px; border-radius: 5px; padding: 10px 16px;")
        tab_5.setCursor(Qt.PointingHandCursor)
        tab_5.clicked.connect(lambda: self.workbench_layout.setCurrentIndex(4))
        tab_5.clicked.connect(tab_f)
        tab_5.clicked.connect(lambda: self.Unsupervised_Models.file_combo.fun1(0))
        tab_5.clicked.connect(lambda: self.Unsupervised_Models.file_combo.fun2(0))

        tab_6 = QPushButton("TensorFolw NN Playground")
        tab_6.setStyleSheet("background-color: #555555; color: #ffffff; font-size: 16px; border-radius: 5px; padding: 10px 16px;")
        tab_6.setCursor(Qt.PointingHandCursor)
        tab_6.clicked.connect(lambda: self.workbench_layout.setCurrentIndex(5))
        tab_6.clicked.connect(tab_f)
        
        self.EN = 1
        def change_lang():
            self.EN = 0 if self.EN else 1
            self.Import_Data.change_lang(self.EN)
            self.Data_Visualization.change_lang(self.EN)
            self.Workspace.change_lang(self.EN)
            self.Supervised_Models.change_lang(self.EN)
            self.Unsupervised_Models.change_lang(self.EN)

            if self.EN :
                tab_1.setText("Import Data")
                tab_2.setText("Data Visualization")
                tab_3.setText("Workspace")
                tab_4.setText("Supervised Models")
                tab_5.setText("Unsupervised Models")
                tab_6.setText("TensorFolw NN Playground")
            else :
                tab_1.setText("تحميل بيانات")
                tab_2.setText("عرض البيانات")
                tab_3.setText("مساحة العمل")
                tab_4.setText("Supervised Models")
                tab_5.setText("Unsupervised Models")
                tab_6.setText("TensorFolw NN Playground")
        tab_7 = QPushButton("EN")
        tab_7.setStyleSheet("background-color: #555555; color: #ffffff; font-size: 16px; border-radius: 5px; padding: 10px 16px;")
        tab_7.setCursor(Qt.PointingHandCursor)
        tab_7.clicked.connect(lambda X : change_lang())
        tab_7.clicked.connect(lambda X : tab_7.setText("EN") if self.EN else tab_7.setText("العربية"))

        # Add tab buttons to a layout
        tabs_layout = QHBoxLayout()
        tabs_layout.addWidget(tab_1)
        tabs_layout.addWidget(tab_2)
        tabs_layout.addWidget(tab_3)
        tabs_layout.addWidget(tab_4)
        tabs_layout.addWidget(tab_5)
        tabs_layout.addWidget(tab_6)
        tabs_layout.addWidget(tab_7)

        # Add the tabs layout and the workbench layout to the main layout
        self.main_layout.addLayout(tabs_layout)
        self.main_layout.addWidget(self.workbench_layout)


        # Connect the custom signal to the method that updates the label text
        self.Supervised_Models.use_btn_clicked.connect(self.Workspace.update_models)
        self.Supervised_Models.use_btn_clicked.connect(lambda: self.workbench_layout.setCurrentIndex(2))
        self.Supervised_Models.use_btn_clicked.connect(lambda: tab_f(tab_3))
        self.Supervised_Models.use_btn_clicked.connect(lambda: self.Workspace.file_combo.fun1(0))
        self.Supervised_Models.use_btn_clicked.connect(lambda: self.Workspace.file_combo.fun2(0))
        self.Supervised_Models.use_btn_clicked.connect(lambda: self.Workspace.file_combo.fun3(0))

        self.Unsupervised_Models.use_btn_clicked.connect(self.Workspace.update_models)
        self.Unsupervised_Models.use_btn_clicked.connect(lambda: self.workbench_layout.setCurrentIndex(2))
        self.Unsupervised_Models.use_btn_clicked.connect(lambda: tab_f(tab_3))
        self.Unsupervised_Models.use_btn_clicked.connect(lambda: self.Workspace.file_combo.fun1(0))
        self.Unsupervised_Models.use_btn_clicked.connect(lambda: self.Workspace.file_combo.fun2(0))
        self.Unsupervised_Models.use_btn_clicked.connect(lambda: self.Workspace.file_combo.fun3(0))


        self.Workspace.un_labeled_file.connect(lambda: self.workbench_layout.setCurrentIndex(0))
        self.Workspace.un_labeled_file.connect(lambda: tab_f(tab_1))

        self.Import_Data.label_changed.connect(self.Data_Visualization.label_updated)
        self.Data_Visualization.label_changed.connect(self.Import_Data.label_updated)
        # Create a central widget and set the main layout
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_icon = QIcon()
    app_icon.addFile('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\logo16.png', QtCore.QSize(16,16))
    app_icon.addFile('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\logo24.png', QtCore.QSize(24,24))
    app_icon.addFile('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\logo32.png', QtCore.QSize(32,32))
    app_icon.addFile('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\logo48.png', QtCore.QSize(48,48))
    app_icon.addFile('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\logo256.png', QtCore.QSize(256,256))
    app.setWindowIcon(app_icon)
    app.setStyle("Fusion")
    dark_palette = app.palette()
    dark_palette.setColor(app.palette().Window, QColor(53, 53, 53))
    dark_palette.setColor(app.palette().WindowText, Qt.white)
    dark_palette.setColor(app.palette().Base, QColor(25, 25, 25))
    dark_palette.setColor(app.palette().AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(app.palette().ToolTipBase, Qt.white)
    dark_palette.setColor(app.palette().ToolTipText, Qt.white)
    dark_palette.setColor(app.palette().Text, Qt.white)
    dark_palette.setColor(app.palette().Button, QColor(53, 53, 53))
    dark_palette.setColor(app.palette().ButtonText, Qt.white)
    dark_palette.setColor(app.palette().BrightText, Qt.red)
    dark_palette.setColor(app.palette().Highlight, QColor(142, 45, 197))
    dark_palette.setColor(app.palette().HighlightedText, Qt.white)
    app.setPalette(dark_palette)
    ai = MainWindow()
    ai.show()
    sys.exit(app.exec_())
