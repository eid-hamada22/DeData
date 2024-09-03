from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.QtCore as QtCore
import sqlite3 as sql, time
import sys, requests, os
import QCustomWidgets
import QTools, QPloting
import pandas as pd
import QTrainingPages
import os 
print(QTemporaryDir)
def get_query(name):
    match name : 
            case "Decision_Tree":
                quary = "INSERT INTO `added_models` (`model_FK`,  `criterion`, `Grid_Search`) VALUES ('Decision_Tree','gini','0')"
            case "Regressor_Tree":
                quary = "INSERT INTO `added_models` (`model_FK`,  `Grid_Search`) VALUES ('Regressor_Tree','0')"
            case "Linear_Regression":
                quary = "INSERT INTO `added_models` (`model_FK`,  `Grid_Search`) VALUES ('Linear_Regression','0')"
            case "Logistic_Regression":
                quary = "INSERT INTO `added_models` (`model_FK`,  `Grid_Search`) VALUES ('Logistic_Regression','0')"
            case "Elastic_Net":
                quary = "INSERT INTO `added_models` (`model_FK`,  `alpha`, `Grid_Search`) VALUES ('Elastic_Net','1','0')"
            case "Polynomial_Regression":
                quary = "INSERT INTO `added_models` (`model_FK`,  `degree`, `Grid_Search`) VALUES ('Polynomial_Regression','2','0')"
            case "Random_Forest_Classifier":
                quary = "INSERT INTO `added_models` (`model_FK`,  `n_estimators`, `Grid_Search`) VALUES ('Random_Forest_Classifier','100','0')"
            case "Random_Forest_Regressor":
                quary = "INSERT INTO `added_models` (`model_FK`,  `n_estimators`, `Grid_Search`) VALUES ('Random_Forest_Regressor','100','0')"
            case "Extra_Trees_Classifier":
                quary = "INSERT INTO `added_models` (`model_FK`,  `n_estimators`, `Grid_Search`) VALUES ('Extra_Trees_Classifier','100','0')"
            case "Extra_Trees_Regressor":
                quary = "INSERT INTO `added_models` (`model_FK`,  `n_estimators`, `Grid_Search`) VALUES ('Extra_Trees_Regressor','100','0')"
            case "Ada_Boost_Classifier":
                quary = "INSERT INTO `added_models` (`model_FK`,  `n_estimators`, `learning_rate`, `Grid_Search`) VALUES ('Ada_Boost_Classifier','50','1','0')"
            case "Ada_Boost_Regressor":
                quary = "INSERT INTO `added_models` (`model_FK`,  `n_estimators`, `learning_rate`, `Grid_Search`) VALUES ('Ada_Boost_Regressor','50','1','0')"
            case "Gradient_Boosting_Classifier":
                quary = "INSERT INTO `added_models` (`model_FK`,  `n_estimators`, `learning_rate`, `Grid_Search`) VALUES ('Gradient_Boosting_Classifier','100','0.1','0')"
            case "Gradient_Boosting_Regressor":
                quary = "INSERT INTO `added_models` (`model_FK`,  `n_estimators`, `learning_rate`, `Grid_Search`) VALUES ('Gradient_Boosting_Regressor','100','0.1','0')"
            case "LinearSVM":
                quary = "INSERT INTO `added_models` (`model_FK`,  `Grid_Search`) VALUES ('LinearSVM','0')"
            case "nonLinearSVM_ploy":
                quary = "INSERT INTO `added_models` (`model_FK`,  `C`, `gamma`, `Grid_Search`) VALUES ('nonLinearSVM_ploy','1','scale','0')"
            case "nonLinearSVM_rbf":
                quary = "INSERT INTO `added_models` (`model_FK`,  `C`, `gamma`, `Grid_Search`) VALUES ('nonLinearSVM_rbf','1','scale','0')"
            case "K_Means":
                quary = "INSERT INTO `added_models` (`model_FK`,  `n_clusters`, `Grid_Search`) VALUES ('K_Means','8','0')"
            case "DB_SCAN":
                quary = "INSERT INTO `added_models` (`model_FK`,  `eps`, `min_samples`, `Grid_Search`) VALUES ('DB_SCAN','0.5','5','0')"
    return quary

class AI_Application_Design(QMainWindow):
    SM_COUNT = -1
    def insert_supervised_model(self, model):
        self.SM_COUNT += 1
        if self.SM_COUNT % 3 == 0:
            self.triple_model_container = QWidget()
            self.triple_model_container.setStyleSheet('border-radius: 10px 0px 0px 0px;')
            self.triple_model_container_layout = QHBoxLayout()
            self.triple_model_container.setLayout(self.triple_model_container_layout)
            self.s_models_sb_layout.addWidget(self.triple_model_container)
        id, family, alg_type, name, binary, reg, bio, related, parameters, ploting, import_path, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model
        def reveal_model(model_data):
            layout_ = QHBoxLayout()
            sa__ = QScrollArea()
            widget__ = QWidget()
            sa__.setWidget(widget__)
            sa__.setWidgetResizable(True)
            self.widget__.setCentralWidget(sa__)
            widget__.setLayout(layout_)
            id, family, alg_type, name, binary, reg, bio, related, parameters, ploting, import_path, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model_data
            widget__.setWindowTitle(f'DeData Preview Model - {name.replace("_", " ")}')
            self.widget__.setFixedSize(600, 450)
            sa__.setFixedSize(600, 450)
            # left
            self.widget__L = QWidget()
            self.widget__L_layout = QVBoxLayout()
            self.widget__L.setLayout(self.widget__L_layout)
            layout_.addWidget(self.widget__L)
            # right
            self.widget__R_picker = QWidget()
            self.widget__R_picker_layout = QVBoxLayout()
            self.widget__R_picker.setLayout(self.widget__R_picker_layout)
            
            self.widget__R = QWidget()
            self.widget__R.setFixedHeight(430)
            self.widget__R.setFixedWidth(200)
            self.widget__R.setStyleSheet("background-color:#444; border-radius:17px")
            self.widget__R_layout = QVBoxLayout()
            self.widget__R.setLayout(self.widget__R_layout)
            self.widget__R_picker_layout.addWidget(self.widget__R)
            self.widget__R_picker_layout.addStretch()
            layout_.addWidget(self.widget__R_picker)
            # label_1:
            label_1 = QLabel(name.replace("_", " ")+":")
            f = QFont("Arial", 19);f.setBold(1)
            label_1.setFont(f); self.widget__L_layout.addWidget(label_1)
            # Bio
            Bio = QLabel()
            Bio.setWordWrap(1)
            Bio.setFont(QFont("Arial", 12))
            widget__.setStyleSheet("background-color: #333;")
            Bio.setStyleSheet("background-color: #333; border-color:#333; border-width:2px; border-style:solid;")
            Bio.setText(bio)
            self.widget__L_layout.addWidget(Bio)
            self.widget__.show()
            ##
            label_bin = QLabel()
            label_bin.setStyleSheet("text-align:center;")
            path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\static\\img\\models\\img1\\{name}1.png".replace(' ', '')
            print(path)
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
            label_bin.setFixedHeight(pixmap.height())
            label_bin.setPixmap(pixmap)
            self.widget__L_layout.addWidget(label_bin)
            label_bin.setStyleSheet('color: #FF1F1F;')
            # params
            params = QLabel("Parameters:")
            f = QFont("Arial", 19);f.setBold(1)
            params.setFont(f); self.widget__L_layout.addWidget(params)
            # label_2:
            Param = QLabel()
            Param.setWordWrap(1)
            Param.setFont(QFont("Arial", 12))
            Param.setStyleSheet("background-color: #333; border-color:#333; border-width:2px; border-style:solid;")
            Param.setText(parameters)
            self.widget__L_layout.addWidget(Param)
            ##
            label_bin = QLabel()
            label_bin.setStyleSheet("text-align:center;")
            path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\static\\img\\models\\img2\\{name}2.png".replace(' ', '')
            print(path)
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
            label_bin.setFixedHeight(pixmap.height())
            label_bin.setPixmap(pixmap)
            self.widget__L_layout.addWidget(label_bin)
            label_bin.setStyleSheet('color: #FF1F1F;')
            # Left:
            label_bin = QLabel("Binary:")
            f = QFont("Arial", 17);f.setBold(1)
            label_bin.setFont(f); self.widget__R_layout.addWidget(label_bin)
            if self.current_file.bin == binary: label_bin.setStyleSheet('color: #4FFF1F;')
            else: label_bin.setStyleSheet('color: #FF1F1F;')
            ##
            label_bin = QLabel()
            label_bin.setWordWrap(True)
            f = QFont("Arial", 13);f.setBold(1)
            label_bin.setFont(f); self.widget__R_layout.addWidget(label_bin)
            if self.current_file.bin == binary: label_bin.setText("The structure of your data matches the model's data type.")
            else: label_bin.setText("Your multi-class data is not compatible with this binary model.")
            # Left:
            label_bin = QLabel("Classifier:")
            f = QFont("Arial", 17);f.setBold(1)
            label_bin.setFont(f); self.widget__R_layout.addWidget(label_bin)
            if self.current_file.reg == reg: label_bin.setStyleSheet('color: #4FFF1F;')
            else: label_bin.setStyleSheet('color: #FF1F1F;')
            ##
            label_bin = QLabel()
            label_bin.setWordWrap(True)
            f = QFont("Arial", 13);f.setBold(1)
            label_bin.setFont(f); self.widget__R_layout.addWidget(label_bin)
            if self.current_file.bin == binary: label_bin.setText("The label's data type fits the model you have chosen.")
            else: label_bin.setText("The type of the predicted data contradicts this model's output.")
            
            self.widget__R_layout.addStretch()
            
            def learn_more_button_f(e):
                quary = get_query(self.circle_button.__model_name__)
                print(quary)
                try:
                    cur = self.db.cursor()
                    cur.execute(quary)
                    self.db.commit()
                    cur.close()
                    self.widget__.hide()
                    self.tab_f(self.tab_6)
                except Exception as e:
                    print(e)
                    msg_box = QMessageBox()
                    msg_box.setStyleSheet('background-color:#333; color:#fff;')
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setText("UNEXPECTED ERROR!")
                    msg_box.setWindowTitle("Error")
                    msg_box.addButton("OK", QMessageBox.AcceptRole)
                    msg_box.exec_()
            learn_more_button = QPushButton("Use Model")
            self.circle_button = learn_more_button
            learn_more_button.__model_name__ = name
            learn_more_button.clicked.connect(learn_more_button_f)
            learn_more_button.setCursor(Qt.PointingHandCursor)
            learn_more_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
            self.widget__R_layout.addWidget(learn_more_button)
            
        model_container = QCustomWidgets.ClickableWidget(reveal_model)
        model_container.setFixedWidth(260)
        model_container.data_ = model
        model_container_layout = QVBoxLayout()
        model_container.setLayout(model_container_layout)
        model_container.setFixedHeight(260)
        l_1 = QLabel()
        l_1.setAlignment(Qt.AlignCenter)
        l_1.setFixedHeight(180)
        path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\database\\archive\\static\\img\\models\\img1\\{name}1.png".replace(' ', '')
        print(path)
        pixmap = QPixmap(path).scaled(250, 180)
        l_1.setPixmap(pixmap)
        l_1.setStyleSheet('border-radius: 0px;')
        model_container_layout.addWidget(l_1)
        model_container_layout.setSpacing(0)
        l_2 = QLabel(name.replace("_", " "))
        l_2.setFont(QFont("arial", 15))
        l_2.setAlignment(Qt.AlignCenter)
        l_2.setStyleSheet('border-radius: 0px;')
        model_container_layout.addWidget(l_2)
        self.triple_model_container_layout.addWidget(model_container)
    def insert_dir_in_project_files(self, dir_, file_full_path=None):
        if 'nothing_to_show_2' in dir(self): self.nothing_to_show_2.setParent(None)
        file_id = dir_[:dir_.find(".")]
        if not file_full_path:
            cur = self.db.cursor()
            cur.execute("SELECT file_full_path FROM files WHERE file_id=?", (file_id,))
            file_full_path = cur.fetchall()[0][0]; cur.close()
        def start_file(e):
            os.startfile(f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\projects\\{self.project_id}\\{self.focusWidget().path_}")
        label_widget = QWidget()
        label_layout = QHBoxLayout()
        label_layout.setContentsMargins(0,0,0,0)
        label_widget.setLayout(label_layout)
        label = QPushButton(file_full_path)
        label_layout.addWidget(label)
        label.setFixedWidth(600)
        label.setFixedHeight(30)
        label.setStyleSheet("""
        QPushButton {
            background-color:#333; color:#fff;
            text-align:left; border-radius:5px;
            padding:5px;
            border-width:1px;
            border-color: #555;
            border-style: solid;
        }
        QPushButton:hover {
            background-color:#444; color:#fff;
        }
        QPushButton:pressed {
            background-color: #007ACC; color:#fff;
            color: white;
        }""")
        label.path_ = dir_
        label.clicked.connect(start_file)
        label.setFont(QFont('arial', 15))
        def label_combo_f(e):
            combo = self.focusWidget()
            label = combo.getOption()
            column_data = QTools.read_file(combo.path_)[label]
            cur = self.db.cursor()
            reg = 0; bin = 0; len_ = len(set(column_data))
            if len_ == 2: bin = 1
            if len_ >= 20 and pd.api.types.is_numeric_dtype(column_data): reg = 1
            cur.execute("UPDATE files SET label = ?, reg = ?, binary = ? WHERE file_id=?", (label, reg, bin, combo.file_id))
            self.db.commit()
            cur.close()
        label_combo = QCustomWidgets.DarkComboBox()
        label_combo.setFixedWidth(189)
        label_combo.label_combo_f = label_combo_f
        cur = self.db.cursor()
        cur.execute("SELECT label FROM files WHERE file_id = ?", (file_id,))
        label = cur.fetchone()[0]
        cur.close()
        List = ['None'] + list(QTools.read_file(f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\projects\\{self.project_id}\\{dir_}").columns)
        label_combo.setItems(List)
        label_combo.setCurrentIndex(List.index(label.__str__()))
        label_combo.path_ = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\projects\\{self.project_id}\\{dir_}"
        label_combo.file_id = file_id
        label_combo.activated.connect(label_combo.label_combo_f)
        label_layout.addWidget(label_combo)
        self.project_files_layout.insertWidget(0, label_widget)
        self.file_combo.addItem(file_full_path)
    def insert_un_supervised_model(self, model):
        self.SM_COUNT += 1
        if self.SM_COUNT % 3 == 0:
            self.triple_model_container = QWidget()
            self.triple_model_container.setStyleSheet('border-radius: 10px 0px 0px 0px;')
            self.triple_model_container_layout = QHBoxLayout()
            self.triple_model_container.setLayout(self.triple_model_container_layout)
            self.s_models_sb_layout.addWidget(self.triple_model_container)
        def reveal_model(model_data):
            layout_ = QHBoxLayout()
            sa__ = QScrollArea()
            widget__ = QWidget()
            sa__.setWidget(widget__)
            sa__.setWidgetResizable(True)
            self.widget__.setCentralWidget(sa__)
            widget__.setLayout(layout_)
            id, family, alg_type, name, binary, reg, bio, related, parameters, ploting, import_path, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model_data
            widget__.setWindowTitle(f'AI Algorithms Preview Model - {name.replace("_", " ")}')
            self.widget__.setFixedSize(600, 450)
            sa__.setFixedSize(600, 450)
            # left
            self.widget__L = QWidget()
            self.widget__L_layout = QVBoxLayout()
            self.widget__L.setLayout(self.widget__L_layout)
            layout_.addWidget(self.widget__L)
            # right
            self.widget__R_picker = QWidget()
            self.widget__R_picker_layout = QVBoxLayout()
            self.widget__R_picker.setLayout(self.widget__R_picker_layout)
            
            self.widget__R = QWidget()
            self.widget__R.setFixedHeight(430)
            self.widget__R.setFixedWidth(200)
            self.widget__R.setStyleSheet("background-color:#444; border-radius:17px")
            self.widget__R_layout = QVBoxLayout()
            self.widget__R.setLayout(self.widget__R_layout)
            self.widget__R_picker_layout.addWidget(self.widget__R)
            self.widget__R_picker_layout.addStretch()
            layout_.addWidget(self.widget__R_picker)
            # label_1:
            label_1 = QLabel(name.replace("_", " ")+":")
            f = QFont("Arial", 19);f.setBold(1)
            label_1.setFont(f); self.widget__L_layout.addWidget(label_1)
            # Bio
            Bio = QLabel()
            Bio.setWordWrap(1)
            Bio.setFont(QFont("Arial", 12))
            widget__.setStyleSheet("background-color: #333;")
            Bio.setStyleSheet("background-color: #333; border-color:#333; border-width:2px; border-style:solid;")
            Bio.setText(bio)
            self.widget__L_layout.addWidget(Bio)
            self.widget__.show()
            ##
            label_bin = QLabel()
            label_bin.setStyleSheet("text-align:center;")
            path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\static\\img\\models\\img1\\{name}1.png".replace(' ', '')
            print(path)
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
            label_bin.setFixedHeight(pixmap.height())
            label_bin.setPixmap(pixmap)
            self.widget__L_layout.addWidget(label_bin)
            label_bin.setStyleSheet('color: #FF1F1F;')
            # params
            params = QLabel("Parameters:")
            f = QFont("Arial", 19);f.setBold(1)
            params.setFont(f); self.widget__L_layout.addWidget(params)
            # label_2:
            Param = QLabel()
            Param.setWordWrap(1)
            Param.setFont(QFont("Arial", 12))
            Param.setStyleSheet("background-color: #333; border-color:#333; border-width:2px; border-style:solid;")
            Param.setText(parameters)
            self.widget__L_layout.addWidget(Param)
            ##
            label_bin = QLabel()
            label_bin.setStyleSheet("text-align:center;")
            path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\static\\img\\models\\img2\\{name}2.png".replace(' ', '')
            print(path)
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
            label_bin.setFixedHeight(pixmap.height())
            label_bin.setPixmap(pixmap)
            self.widget__L_layout.addWidget(label_bin)
            label_bin.setStyleSheet('color: #FF1F1F;')
            # Left:
            label_bin = QLabel("Binary:")
            f = QFont("Arial", 17);f.setBold(1)
            label_bin.setFont(f); self.widget__R_layout.addWidget(label_bin)
            if self.current_file.bin == binary: label_bin.setStyleSheet('color: #4FFF1F;')
            else: label_bin.setStyleSheet('color: #FF1F1F;')
            ##
            label_bin = QLabel()
            label_bin.setWordWrap(True)
            f = QFont("Arial", 13);f.setBold(1)
            label_bin.setFont(f); self.widget__R_layout.addWidget(label_bin)
            if self.current_file.bin == binary: label_bin.setText("The structure of your data matches the model's data type.")
            else: label_bin.setText("Your multi-class data is not compatible with this binary model.")
            # Left:
            label_bin = QLabel("Classifier:")
            f = QFont("Arial", 17);f.setBold(1)
            label_bin.setFont(f); self.widget__R_layout.addWidget(label_bin)
            if self.current_file.reg == reg: label_bin.setStyleSheet('color: #4FFF1F;')
            else: label_bin.setStyleSheet('color: #FF1F1F;')
            ##
            label_bin = QLabel()
            label_bin.setWordWrap(True)
            f = QFont("Arial", 13);f.setBold(1)
            label_bin.setFont(f); self.widget__R_layout.addWidget(label_bin)
            if self.current_file.bin == binary: label_bin.setText("The label's data type fits the model you have chosen.")
            else: label_bin.setText("The type of the predicted data contradicts this model's output.")
            
            self.widget__R_layout.addStretch()
            
            def learn_more_button_f(e):
                quary = get_query(self.circle_button.__model_name__)
                print(quary)
                try:
                    cur = self.db.cursor()
                    cur.execute(quary)
                    self.db.commit()
                    cur.close()
                    self.widget__.hide()
                    self.tab_f(self.tab_6)
                    cur= self.db.cursor()
                    cur.execute("SELECT * FROM added_models")
                    added_models = cur.fetchall()
                    cur.close()
                    self.triple_model_container = QWidget()
                    self.triple_model_container.setStyleSheet('border-radius: 10px 0px 0px 0px;')
                    self.triple_model_container_layout = QHBoxLayout()
                    self.triple_model_container.setLayout(self.triple_model_container_layout)
                    self.s_models_sb_layout.addWidget(self.triple_model_container)
                    for model in added_models:
                        self.SM_COUNT = -1
                        self.insert_un_supervised_model(model)
                except Exception as e:
                    print(e)
                    msg_box = QMessageBox()
                    msg_box.setStyleSheet('background-color:#333; color:#fff;')
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setText("UNEXPECTED ERROR!")
                    msg_box.setWindowTitle("Error")
                    msg_box.addButton("OK", QMessageBox.AcceptRole)
                    msg_box.exec_()
            learn_more_button = QPushButton("Use Model")
            self.circle_button = learn_more_button
            learn_more_button.__model_name__ = name
            learn_more_button.clicked.connect(learn_more_button_f)
            learn_more_button.setCursor(Qt.PointingHandCursor)
            learn_more_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
            self.widget__R_layout.addWidget(learn_more_button)
            
        model_container = QCustomWidgets.ClickableWidget(reveal_model)
        model_container.setFixedWidth(260)
        model_container.data_ = model
        model_container_layout = QVBoxLayout()
        model_container.setLayout(model_container_layout)
        model_container.setFixedHeight(260)
        l_1 = QLabel()
        l_1.setAlignment(Qt.AlignCenter)
        l_1.setFixedHeight(180)
        path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\database\\archive\\static\\img\\models\\img1\\{name}1.png".replace(' ', '')
        print(path)
        pixmap = QPixmap(path).scaled(250, 180)
        l_1.setPixmap(pixmap)
        l_1.setStyleSheet('border-radius: 0px;')
        model_container_layout.addWidget(l_1)
        model_container_layout.setSpacing(0)
        l_2 = QLabel(name.replace("_", " "))
        l_2.setFont(QFont("arial", 15))
        l_2.setAlignment(Qt.AlignCenter)
        l_2.setStyleSheet('border-radius: 0px;')
        model_container_layout.addWidget(l_2)
        self.triple_model_container_layout.addWidget(model_container)
    def insert_dir_in_project_files(self, dir_, file_full_path=None):
        if 'nothing_to_show_2' in dir(self): self.nothing_to_show_2.setParent(None)
        file_id = dir_[:dir_.find(".")]
        if not file_full_path:
            cur = self.db.cursor()
            cur.execute("SELECT file_full_path FROM files WHERE file_id=?", (file_id,))
            file_full_path = cur.fetchall()[0][0]; cur.close()
        def start_file(e):
            os.startfile(f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\projects\\{self.project_id}\\{self.focusWidget().path_}")
        label_widget = QWidget()
        label_layout = QHBoxLayout()
        label_layout.setContentsMargins(0,0,0,0)
        label_widget.setLayout(label_layout)
        label = QPushButton(file_full_path)
        label_layout.addWidget(label)
        label.setFixedWidth(600)
        label.setFixedHeight(30)
        label.setStyleSheet("""
        QPushButton {
            background-color:#333; color:#fff;
            text-align:left; border-radius:5px;
            padding:5px;
            border-width:1px;
            border-color: #555;
            border-style: solid;
        }
        QPushButton:hover {
            background-color:#444; color:#fff;
        }
        QPushButton:pressed {
            background-color: #007ACC; color:#fff;
            color: white;
        }""")
        label.path_ = dir_
        label.clicked.connect(start_file)
        label.setFont(QFont('arial', 15))
        def label_combo_f(e):
            combo = self.focusWidget()
            label = combo.getOption()
            column_data = QTools.read_file(combo.path_)[label]
            cur = self.db.cursor()
            reg = 0; bin = 0; len_ = len(set(column_data))
            if len_ == 2: bin = 1
            if len_ >= 20 and pd.api.types.is_numeric_dtype(column_data): reg = 1
            cur.execute("UPDATE files SET label = ?, reg = ?, binary = ? WHERE file_id=?", (label, reg, bin, combo.file_id))
            self.db.commit()
            cur.close()
        label_combo = QCustomWidgets.DarkComboBox()
        label_combo.setFixedWidth(189)
        label_combo.label_combo_f = label_combo_f
        cur = self.db.cursor()
        cur.execute("SELECT label FROM files WHERE file_id = ?", (file_id,))
        label = cur.fetchone()[0]
        cur.close()
        List = ['None'] + list(QTools.read_file(f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\projects\\{self.project_id}\\{dir_}").columns)
        label_combo.setItems(List)
        label_combo.setCurrentIndex(List.index(label.__str__()))
        label_combo.path_ = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\projects\\{self.project_id}\\{dir_}"
        label_combo.file_id = file_id
        label_combo.activated.connect(label_combo.label_combo_f)
        label_layout.addWidget(label_combo)
        self.project_files_layout.insertWidget(0, label_widget)
        self.file_combo.addItem(file_full_path)
    def insert_file_in_project(self, file_full_path, project_id, url=False):
        try:
            if not url:
                f = open(file_full_path, 'rb')
                data = f.read(); f.close()
            else:
                response = requests.get(file_full_path)
                data = response.content
                response.close()
            cur = self.db.cursor()
            cur.execute("INSERT INTO files (file_full_path, project_id) VALUES(?, ?)", (file_full_path, self.project_id))
            file_id = cur.lastrowid
            self.db.commit()
            cur.close()
            file = open(f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\projects\\{project_id}\\{file_id}.{file_full_path.split('.')[-1]}", 'wb')
            file.write(data)
            file.close()
            self.insert_dir_in_project_files(f"{file_id}.{file_full_path.split('.')[-1]}", file_full_path)
        except Exception as e:
            print(e)
            msg_box = QMessageBox()
            msg_box.setStyleSheet('background-color:#333; color:#fff;')
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("unable to import the file!")
            msg_box.setWindowTitle("Error")
            msg_box.addButton("OK", QMessageBox.AcceptRole)
            msg_box.exec_()
    def seek_files_in_project(self, id_):
        dirs = os.listdir(f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\projects\\{id_}")
        if dirs:
            for dir_ in dirs:
                self.insert_dir_in_project_files(dir_)
        else:
            self.nothing_to_show_2 = QLabel()
            self.nothing_to_show_2.setAlignment(Qt.AlignCenter)
            self.nothing_to_show_2.setAlignment(Qt.AlignCenter)
            self.nothing_to_show_2.setFixedHeight(145)
            pixmap = QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\static\\img\\nothing_here_to_show_2.png")
            self.nothing_to_show_2.setPixmap(pixmap)
            self.project_files_layout.addWidget(self.nothing_to_show_2)
    
    class FileRepresentation:
        def __init__(self, file_full_path, file_archive_path, file_df, file_label, reg, bin, file_id):
            self.file_full_path = file_full_path
            self.file_archive_path = file_archive_path
            self.file_df = file_df
            self.file_label = file_label
            self.reg = reg; self.bin = bin
            self.file_id = file_id
    
    def workbench_page(self, creation_date, project_description, project_name, id_):
        self.project_id = id_
        self.workbench_widget = QWidget()
        self.workbench_layout = QVBoxLayout()
        self.workbench_widget.setLayout(self.workbench_layout)
        self.setCentralWidget(self.workbench_widget)
        self.setWindowTitle("AI Algorithms - Workbench:")
        self.workbench_main = QWidget()
        self.workbench_main_layout = QVBoxLayout()
        self.workbench_main.setLayout(self.workbench_main_layout)
        self.file_combo = QCustomWidgets.DarkComboBox()
        # tabs
        self.arbtrary_widget = QWidget()
        self.tabs_widget = QWidget()
        self.tabs_layout = QHBoxLayout()
        self.tabs_widget.setLayout(self.tabs_layout)
        
        def tab_f(tab=None):
            if not tab: Tab = self.focusWidget()
            else: Tab = tab
            for tab in [tab_1, tab_2, tab_3, tab_4, tab_5, tab_6]:
                if tab == Tab: tab.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                else: tab.setStyleSheet("background-color: #333333; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
            for i in range(self.workbench_layout.count()):
                item = self.workbench_layout.itemAt(i)
                if item: 
                    if item.widget() != self.tabs_widget:item.widget().setParent(None)
            Tab.layout_.setStyleSheet('background-color:#333; border-radius:10px')
            self.workbench_layout.insertWidget(1, Tab.layout_)

        self.tab_f = tab_f

        tab_1 = QPushButton("Import Data")
        self.id_widget = QWidget()
        self.id_layout = QVBoxLayout()
        self.id_widget.setLayout(self.id_layout)
        tab_1.layout_ = self.id_widget
        tab_1.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        tab_1.setCursor(Qt.PointingHandCursor)
        tab_1.clicked.connect(tab_f)

        tab_2 = QPushButton("Data Visualization")
        self.dv_widget = QWidget()
        self.dv_layout = QVBoxLayout()
        self.dv_widget.setLayout(self.dv_layout)
        tab_2.layout_ = self.dv_widget
        tab_2.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        tab_2.setCursor(Qt.PointingHandCursor)
        tab_2.clicked.connect(tab_f)
        
        tab_3 = QPushButton("Supervised Models")
        self.s_models_widget = QWidget()
        self.s_models_layout = QVBoxLayout()
        self.s_models_widget.setLayout(self.s_models_layout)
        tab_3.layout_ = self.s_models_widget
        tab_3.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        tab_3.setCursor(Qt.PointingHandCursor)
        tab_3.clicked.connect(tab_f)
        
        tab_4 = QPushButton("Unsupervised Models")
        self.u_models_widget = QWidget()
        self.u_models_layout = QVBoxLayout()
        self.u_models_widget.setLayout(self.u_models_layout)
        tab_4.layout_ = self.u_models_widget
        tab_4.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        tab_4.setCursor(Qt.PointingHandCursor)
        tab_4.clicked.connect(tab_f)
        
        tab_5 = QPushButton("Deep Learning")
        self.settings_layout = QVBoxLayout()
        self.settings_widget = QWidget()
        self.settings_widget.setLayout(self.settings_layout)
        tab_5.layout_ = self.settings_widget
        tab_5.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        tab_5.setCursor(Qt.PointingHandCursor)
        tab_5.clicked.connect(tab_f)
        
        tab_6 = QPushButton("Workspace")
        self.tab_6 = tab_6
        self.workspace_layout = QVBoxLayout()
        self.workspace_widget = QWidget()
        self.workspace_widget.setLayout(self.workspace_layout)
        tab_6.layout_ = self.workspace_widget
        tab_6.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        tab_6.setCursor(Qt.PointingHandCursor)
        tab_6.clicked.connect(tab_f)
        
        self.tabs_widget.setFixedHeight(64)
        
        self.tabs_layout.addWidget(tab_1)
        self.tabs_layout.addWidget(tab_2)
        self.tabs_layout.addWidget(tab_6)
        self.tabs_layout.addWidget(tab_3)
        self.tabs_layout.addWidget(tab_4)
        self.tabs_layout.addWidget(tab_5)

        self.workbench_layout.addWidget(self.tabs_widget)
        self.workbench_layout.addWidget(self.id_widget)
        self.id_widget.setStyleSheet('background-color:#333; border-radius:10px')
        # Import Data:
        def import_1_f(e):
            file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "All Files (*)")
            if file_path:
                if file_path.split('.')[-1] in ['csv', 'json', 'xlsx', 'data']:
                    self.import_1_input.setText(file_path)
                else:
                    msg_box = QMessageBox()
                    msg_box.setStyleSheet('background-color:#333; color:#fff;')
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setText("Unsupported file type!")
                    msg_box.setWindowTitle("Error")
                    msg_box.addButton("OK", QMessageBox.AcceptRole)
                    msg_box.exec_()
        import_1 = QPushButton("Import file from your local machine:")
        import_1.clicked.connect(import_1_f)
        import_1.setCursor(Qt.PointingHandCursor)
        import_1.setStyleSheet("""
            QPushButton {
                color: #fff; font-size: 16px; text-align: left;
            } 
            QPushButton:hover {
                color: #007ACC;
            }""")
        self.import_1_input = QLineEdit()
        self.import_1_input.setPlaceholderText(r"C:\Directory\Datasets\file_data.csv")
        self.import_1_input.setStyleSheet("background-color: #222; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
        
        import_2 = QLabel("Import file from the cloud:")
        import_2.setStyleSheet("color: #fff; font-size: 16px;")
        
        self.import_2_input = QLineEdit()
        self.import_2_input.setPlaceholderText(r"https://www.example.com/file_data.csv")
        self.import_2_input.setStyleSheet("background-color: #222; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
        
        files_in_use_label = QLabel("Files in use:")
        files_in_use_label.setStyleSheet("color: #fff; font-size: 24px;")
        
        self.project_files_scrollarea = QScrollArea()
        self.project_files_scrollarea.setStyleSheet("background-color: #222; color: #fff; font-size: 14px;")
        self.project_files_widget = QWidget()
        self.project_files_layout = QVBoxLayout()
        self.project_files_layout.addStretch()
        self.project_files_scrollarea.setWidget(self.project_files_widget)
        self.project_files_widget.setLayout(self.project_files_layout)
        self.project_files_scrollarea.setWidgetResizable(True)
        self.seek_files_in_project(id_)
        def import_button_f():
            if self.import_1_input.text():
                self.insert_file_in_project(self.import_1_input.text(), id_)
                self.import_1_input.setText('')
            if self.import_2_input.text():
                self.insert_file_in_project(self.import_2_input.text(), id_, url=True)
                self.import_2_input.setText('')
        import_button = QPushButton("Import File")
        import_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        import_button.setCursor(QtCore.Qt.PointingHandCursor)
        import_button.clicked.connect(import_button_f)
        
        for element in [import_1, self.import_1_input, import_2, self.import_2_input, files_in_use_label, self.project_files_scrollarea, import_button]:
            if element == 0:
                self.id_layout.addStretch()
            else:
                self.id_layout.addWidget(element)
        # Data Visualization tab:
        self.dv_scrollarea = QScrollArea()
        self.dv_sa_widget = QWidget()
        self.dv_sa_layout = QVBoxLayout()
        self.dv_scrollarea.setWidget(self.dv_sa_widget)
        self.dv_sa_widget.setLayout(self.dv_sa_layout)
        self.dv_scrollarea.setWidgetResizable(True)
        self.dv_layout.addWidget(self.dv_scrollarea)
        self.dv_scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        set_file_label = QLabel("Load a file to the workbench:")
        set_file_label.setStyleSheet("color: #fff; font-size: 16px;")
        self.dv_sa_layout.addWidget(set_file_label)
        self.dv_sa_layout.addWidget(self.file_combo)
        def file_combo_f(e):
            file_full_path = self.file_combo.getOption()
            extension = file_full_path.split('.')[-1]
            cur = self.db.cursor()
            cur.execute("SELECT file_id, label FROM files WHERE file_full_path = ? AND project_id = ?", (file_full_path,id_))
            file_id, label = cur.fetchall()[0]; cur.close()
            path = fr"Database\archive\projects\{id_}\{file_id}.{extension}"
            df = QTools.read_file(path)
            self.sheet.load_pandas_dataframe(df, label, file_path=path, file_id=file_id)
        self.file_combo.activated.connect(file_combo_f)
        self.file_combo.setSizePolicy(self.dv_sa_widget.sizePolicy())
        # Sheet:
        self.sheet_place = QWidget()
        self.sheet_place.setMaximumHeight(300)
        self.sheet_place.setStyleSheet("border-radius:10px; background-color:#000; background-image:url(C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\static\\img\\sheet.png); background-repeat:no-repeat; background-position: center;")
        self.sheet_place_layout = QVBoxLayout()
        self.sheet_place_layout.setContentsMargins(1,1,1,1)
        self.sheet_place.setLayout(self.sheet_place_layout)
        self.sheet = QCustomWidgets.QSheet()
        self.sheet.mainclass = self
        self.sheet.setMinimumHeight(300)
        self.sheet_place_layout.addWidget(self.sheet)
        self.dv_sa_layout.addWidget(self.sheet_place)
        self.file_combo.setFixedWidth(780)
        def retrive_sheet_button_f(e):
            self.retrive_sheet_button.setParent(None)
            self.sheet.show()
            self.sheet_place_layout.addWidget(self.sheet)
        self.retrive_sheet_button = QPushButton("Retrive Sheet")
        self.retrive_sheet_button.clicked.connect(retrive_sheet_button_f)
        self.retrive_sheet_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 14px; border-radius: 8px; padding: 10px 15px;")
        self.ploting_combo = QCustomWidgets.DarkComboBox()
        self.ploting_combo.setItems([
            'Pie Chart', 'Scatter Chart', 'Line Chart', 'Histogram'
        ])
        
        self.pie_window = QPloting.PieChartGeneratorWindow(); self.pie_window.mainclass = self
        self.scatter_window = QPloting.ScatterPlotGeneratorWindow(); self.scatter_window.mainclass = self
        self.histogram_window = QPloting.HistogramGeneratorWindow(); self.histogram_window.mainclass = self
        self.line_window = QPloting.LinePlotGeneratorWindow(); self.line_window.mainclass = self
        
        self.ploting_combo.setFixedWidth(780)
        def ploting_combo_f(e):
            option = self.ploting_combo.getOption()
            if option == 'Pie Chart':
                self.pie_window.initui()
            elif option == 'Scatter Chart':
                self.scatter_window.initui()
            elif option == 'Histogram':
                self.histogram_window.initui()
            elif option == 'Line Chart':
                self.line_window.initui()
        self.ploting_combo.activated.connect(ploting_combo_f)
        self.dv_sa_layout.addWidget(self.ploting_combo)
        self.plots_picker = QWidget()
        self.plots_picker_layout = QVBoxLayout()
        self.plots_picker.setLayout(self.plots_picker_layout)
        self.plots_picker.setStyleSheet("border-radius:10px; background-color:#000;")
        self.plots_img = QLabel()
        self.plots_img.setAlignment(Qt.AlignCenter)
        self.plots_img.setPixmap(QPixmap("Database\\Archive\\static\\img\\ploting.png"))
        self.plots_picker_layout.addWidget(self.plots_img)
        self.dv_sa_layout.addWidget(self.plots_picker)
        self.dv_sa_layout.addStretch()
        # settings:
        stay_tuned_label = QLabel()
        stay_tuned_label.setAlignment(Qt.AlignCenter)
        stay_tuned_pixmap = QPixmap(r"Database\archive\static\img\stay_tuned.png")
        stay_tuned_label.setPixmap(stay_tuned_pixmap)
        self.settings_layout.addWidget(stay_tuned_label)
        # Supercised Models:
        self.s_models_sb = QScrollArea()
        self.s_models_sb_widget = QWidget()
        self.s_models_sb_widget.setFixedWidth(810)
        self.s_models_sb_layout = QVBoxLayout()
        self.s_models_sb_widget.setLayout(self.s_models_sb_layout)
        self.s_models_sb.setWidget(self.s_models_sb_widget)
        self.s_models_sb.setWidgetResizable(True)
        self.s_models_layout.addWidget(self.s_models_sb)
        # Unsupercised Models:
        self.workspace_sa = QScrollArea()
        self.workspace_sa_widget = QWidget()
        self.workspace_sa_widget.setFixedWidth(810)
        self.workspace_sa_layout = QVBoxLayout()
        self.workspace_sa_widget.setLayout(self.workspace_sa_layout)
        self.workspace_sa.setWidget(self.workspace_sa_widget)
        self.workspace_sa.setWidgetResizable(True)
        self.workspace_layout.addWidget(self.s_models_sb)
        # DB stuff:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM models WHERE alg_type = 'supervised'")
        self.models = cur.fetchall()
        print(len(self.models), 'LEN')
        cur.close()
        def choose_file_combo_f(e):
            file_id = self.choose_file_structure[self.choose_file_combo.currentIndex()][0]
            extension = self.choose_file_combo.getOption().split('.')[-1]
            path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\projects\\{self.project_id}\\{file_id}.{extension}"
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
        self.s_models_sb_layout.addWidget(self.choose_file_combo)
        ##
        choose_file_combo_f(0)
        self.triple_model_container = QWidget()
        self.triple_model_container_layout = QHBoxLayout()
        self.triple_model_container.setLayout(self.triple_model_container_layout)
        self.s_models_sb_layout.addWidget(self.triple_model_container)
        for model in self.models:
            print(model)
            self.insert_supervised_model(model)
            
    def connect_database(self):
        self.db = sql.connect('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\database.sqlite3')
    
    def navbar(self):
        self.navbar_layout = QHBoxLayout()
        
    def seek_projects_in_database(self):
        cur = self.db.cursor()
        cur.execute("SELECT project_name, project_description, creation_date, project_id FROM projects;")
        data = cur.fetchall()
        cur.close()
        if data:
            for project in data:
                self.insert_into_scroll(*project)
        else:
            self.nothing_to_show = QLabel()
            self.nothing_to_show.setAlignment(Qt.AlignCenter)
            self.nothing_to_show.setMinimumHeight(400)
            pixmap = QPixmap('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\archive\static\img\nothing_here_to_show.png')
            self.nothing_to_show.setPixmap(pixmap)
            self.projects_scrollarea_layout.insertWidget(0, self.nothing_to_show)
    def project_widget_clicked(self):
        button = self.focusWidget()
        id_ = button._id
        self.project_id = id_
        project_name = button.project_name
        project_description = button.project_description
        creation_date = button.creation_date
        self.workbench_page(creation_date, project_description, project_name, id_)
    def insert_into_scroll(self, project_name, project_description, creation_date, _id):
        if 'nothing_to_show' in dir(self): self.nothing_to_show.setParent(None)
        project_widget = QWidget()
        project_widget_layout = QVBoxLayout()
        project_widget.setLayout(project_widget_layout)
        project_widget.setFixedHeight(150)
        project_widget.setStyleSheet('background-color:#444; border-radius:10px; color:#fff')
        project_widget_name = QPushButton(project_name)
        project_widget_name.setCursor(Qt.PointingHandCursor)
        project_widget_name.setStyleSheet("text-align: left;")
        project_widget_name.project_name = project_name
        project_widget_name.project_description = project_description
        project_widget_name.creation_date = creation_date
        project_widget_name._id = _id
        project_widget_name.clicked.connect(self.project_widget_clicked)
        f = QFont('Arial', 17); f.setBold(True)
        project_widget_name.setFont(f)
        project_widget_layout.addWidget(project_widget_name)
        project_widget_date = QLabel(creation_date)
        project_widget_layout.addWidget(project_widget_date)
        project_widget_date.setFont(QFont('Arial', 9))
        project_widget_description = QLabel(project_description)
        project_widget_description.setFont(QFont('Arial', 12))
        project_widget_layout.addWidget(project_widget_description)
        self.projects_scrollarea_layout.insertWidget(0, project_widget)
        
    def main_page(self):
        self.connect_database()
        self.main_widget_2 = QWidget()
        self.setWindowTitle('AI Algorithms: Control Panel:')
        self.main_widget_2.setFixedSize(850, 500)
        self.setFixedSize(self.main_widget_2.size())
        self.main_layout_2 = QHBoxLayout()
        self.main_layout_2.setContentsMargins(0,0,0,0)
        self.main_widget_2.setStyleSheet("background-color: #222;")
        self.main_widget_2.setLayout(self.main_layout_2)
        self.setCentralWidget(self.main_widget_2)
        # welcome + create project
        self.side_1_control_panel = QWidget()
        self.side_1_control_panel_layout = QVBoxLayout()
        self.side_1_control_panel.setLayout(self.side_1_control_panel_layout)
        self.side_1_control_panel.setFixedWidth(300)
        self.side_1_control_panel.setStyleSheet("background-color: #333;")
        self.main_layout_2.addWidget(self.side_1_control_panel)
        ## welcome:
        self.welcome_label = QLabel(f"Welcome {self.username_input.text()}!")
        self.welcome_label.setFont(QFont('arial', 18))
        self.welcome_label.setMaximumHeight(50)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("color:#fff; background-color: #333; border-radius:10px")
        self.side_1_control_panel_layout.addWidget(self.welcome_label)
        ## create project form:
        self.create_project_form = QWidget()
        self.create_project_form_layout = QVBoxLayout()
        self.create_project_form.setLayout(self.create_project_form_layout)
        self.create_project_form.setStyleSheet("color:#fff; background-color: #444; border-radius:10px")
        ### form components:
        self.create_project_form_label = QLabel("Create Project")
        self.create_project_form_label.setAlignment(Qt.AlignCenter)
        self.create_project_form_label.setFont(QFont('arial', 15))
        self.project_name_label = QLabel('Project Name:')
        self.project_name_label.setStyleSheet("color: #fff; font-size: 16px;")
        self.project_name_input = QLineEdit()
        self.project_name_input.setStyleSheet("background-color: #555; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
        self.project_description_label = QLabel('Project description: (OPTIONAL)')
        self.project_description_label.setStyleSheet("color: #fff; font-size: 16px;")
        self.project_description_text = QPlainTextEdit()
        self.project_description_text.setStyleSheet("background-color: #555; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
        
        def create_project_button_f(e):
            project_name = self.project_name_input.text()
            project_description = self.project_description_text.toPlainText()
            creation_date = time.ctime()
            if project_name:
                cur = self.db.cursor()
                cur.execute(f"INSERT INTO projects (project_name, project_description, creation_date) VALUES(?,?,?)", (project_name, project_description, creation_date))
                id_ = cur.lastrowid
                cur.close()
                self.db.commit()
                self.project_name_input.setText('')
                self.project_description_text.setPlainText('')
                self.insert_into_scroll(project_name, project_description, creation_date, id_)
                os.mkdir(f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\projects\\{id_}")
            else:
                msg_box = QMessageBox()
                msg_box.setStyleSheet('background-color:#333; color:#fff;')
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("Invalid project name!")
                msg_box.setWindowTitle("Error")
                msg_box.addButton("OK", QMessageBox.AcceptRole)
                msg_box.exec_()
        
        self.create_project_button = QPushButton("Create")
        self.create_project_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        self.create_project_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.create_project_button.clicked.connect(create_project_button_f)
        for element in [
            self.create_project_form_label,
            self.project_name_label,
            self.project_name_input,
            self.project_description_label,
            self.project_description_text,
            self.create_project_button
        ]: self.create_project_form_layout.addWidget(element)
        self.side_1_control_panel_layout.addWidget(self.create_project_form)
        # existing projects:
        self.side_2_control_panel = QWidget()
        self.side_2_control_panel_layout = QVBoxLayout()
        self.side_2_control_panel.setLayout(self.side_2_control_panel_layout)
        self.side_2_control_panel.setStyleSheet("background-color: #222;")
        self.main_layout_2.addWidget(self.side_2_control_panel)
        ## label
        self.existing_projects_label = QLabel('Your Recent Projects')
        self.existing_projects_label.setAlignment(Qt.AlignCenter)
        self.existing_projects_label.setStyleSheet("color:#fff; background-color: #333; border-radius:10px; padding:4px")
        self.existing_projects_label.setFont(QFont('arial', 20))
        self.side_2_control_panel_layout.addWidget(self.existing_projects_label)
        ## projects scrollarea
        self.projects_scrollarea = QScrollArea()
        self.projects_scrollarea.setStyleSheet('background-color:#333; border-radius:10px;')
        self.projects_scrollarea_widget = QWidget()
        self.projects_scrollarea.setWidget(self.projects_scrollarea_widget)
        self.projects_scrollarea.setWidgetResizable(True)
        self.projects_scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.projects_scrollarea_layout = QVBoxLayout()
        self.projects_scrollarea_layout.addStretch()
        self.projects_scrollarea_widget.setLayout(self.projects_scrollarea_layout)
        self.side_2_control_panel_layout.addWidget(self.projects_scrollarea)
        self.seek_projects_in_database()

    def initui(self):
        self.widget__ = QMainWindow()
        self.use_widget = QWidget()
        self.setStyleSheet("background-color: #222;")
        self.mian_widget_1 = QWidget()
        self.setCentralWidget(self.mian_widget_1)
        self.mian_widget_1.setStyleSheet("background-color: #222;")

        main_layout = QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.mian_widget_1.setLayout(main_layout)

        title_label = QLabel("AI Algorithms - Regerster Form")
        title_label.setStyleSheet("color: #fff; font-size: 24px; font-weight: bold;")
        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)

        title_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.addLayout(title_layout)

        form_layout = QVBoxLayout()
        form_layout.setAlignment(QtCore.Qt.AlignCenter)

        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #fff; font-size: 16px;")

        self.username_input = QLineEdit()
        self.username_input.setText('Atiya Alkhodari')
        self.username_input.setStyleSheet("background-color: #333; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")

        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #fff; font-size: 16px;")

        self.password_input = QLineEdit()
        self.password_input.setStyleSheet("background-color: #333; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.USERNAME = ''
        
        def login_button_f(e):
            self.main_page()

        login_button = QPushButton("Login")
        login_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        login_button.setCursor(QtCore.Qt.PointingHandCursor)
        login_button.clicked.connect(login_button_f)

        def sign_up_button_f(e):
            login_button_f(0)

        sign_up_button = QPushButton("Sign Up")
        sign_up_button.setStyleSheet("background-color: #555; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
        sign_up_button.setCursor(QtCore.Qt.PointingHandCursor)
        sign_up_button.clicked.connect(sign_up_button_f)

        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(login_button)
        form_layout.addWidget(sign_up_button)
        
        self.main_widget_2 = QWidget()
        self.main_widget_2.setStyleSheet("background-color: #222;")
        
        main_layout.addLayout(form_layout)
        
        self.setWindowTitle("AI Algorithms - regester form:")

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        self.main_widget_2.setLayout(main_layout)
    def __init__(self):
        super().__init__()
        print(self.focusWidget())
        self.initui()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
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
    ai = AI_Application_Design()
    sys.exit(app.exec_())
