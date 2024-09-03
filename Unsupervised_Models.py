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
from demo_fils import get_df
def get_query(name,project_id,data_set):
    match name : 
            case "K_Means":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `n_clusters`, `Grid_Search`, `data_set`) VALUES ('K_Means','{project_id}','8','0', '{data_set}')"
            case "DBSCAN":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `eps`, `min_samples`, `Grid_Search`, `data_set`) VALUES ('DBSCAN','{project_id}','0.5','5','0', '{data_set}')"
    return quary

class Unsupervised_Models(QWidget):
    use_btn_clicked = pyqtSignal(str)  

    SM_COUNT = -1
    def insert_unsupervised_model(self, model):
        self.SM_COUNT += 1
        if self.SM_COUNT % 3 == 0:
            self.triple_model_container = QWidget()
            self.triple_model_container.setStyleSheet('border-radius: 10px 0px 0px 0px;')
            self.triple_model_container_layout = QHBoxLayout()
            self.triple_model_container.setLayout(self.triple_model_container_layout)
            self.un_s_models_sb_layout.addWidget(self.triple_model_container)
        id, family, alg_type, name, binary, reg, bio, bio_ar, related, parameters, parameters_ar, ploting, import_path, playground, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model
        def reveal_model(model_data):
            id, family, alg_type, name, binary, reg, bio, bio_ar, related, parameters, parameters_ar, ploting, import_path, playground, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model_data
            reveal_model_layout = QHBoxLayout()
            reveal_model_widget = QWidget()
            reveal_model_widget.show()
            # reveal_model_widget.setWidgetResizable(True)
            reveal_model_widget.setLayout(reveal_model_layout)
            reveal_model_widget.setWindowTitle(f'DeData Preview Model - {name.replace("_", " ")}')
            self.widget__.setWindowTitle(f'DeData Preview Model - {name.replace("_", " ")}')
            reveal_model_widget.setMinimumSize(800, 600)
            reveal_model_widget.setStyleSheet("background-color: #333;")
            self.widget__.setCentralWidget(reveal_model_widget)
            self.widget__.show()

            # left
            if True :
                left_sa = QScrollArea()
                widget__L = QWidget()
                left_sa.setWidget(widget__L)
                widget__L_layout = QVBoxLayout()
                widget__L.setLayout(widget__L_layout)
                reveal_model_layout.addWidget(left_sa)
                left_sa.setWidgetResizable(True)
                # label_1:
                label_1 = QLabel(name.replace("_", " ")+":")
                f = QFont("Arial", 19);f.setBold(1)
                label_1.setFont(f); widget__L_layout.addWidget(label_1)
                # Bio
                Bio = QLabel()
                Bio.setWordWrap(1)
                Bio.setFont(QFont("Arial", 12))
                Bio.setStyleSheet("background-color: #333; border-color:#333; border-width:2px; border-style:solid;")
                if self.EN :
                    Bio.setText(bio)
                else : 
                    Bio.setText(bio_ar)
                widget__L_layout.addWidget(Bio)
                ##
                label_bin = QLabel()
                label_bin.setStyleSheet("text-align:center;")
                path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\static\\img\\models\\img1\\{name}1.png".replace(' ', '')
                pixmap = QPixmap(path)
                pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
                label_bin.setFixedHeight(pixmap.height())
                label_bin.setPixmap(pixmap)
                widget__L_layout.addWidget(label_bin)
                label_bin.setStyleSheet('color: #ff5639;')
                # params
                if self.EN :
                    params = QLabel("Parameters:")
                else :
                    params = QLabel("المتغيرات:")

                f = QFont("Arial", 19);f.setBold(1)
                params.setFont(f); widget__L_layout.addWidget(params)
                # label_2:
                Param = QLabel()
                Param.setWordWrap(1)
                Param.setFont(QFont("Arial", 12))
                Param.setStyleSheet("background-color: #333; border-color:#333; border-width:2px; border-style:solid;")
                if self.EN :
                    Param.setText(parameters)
                else :
                    Param.setText(parameters_ar)
                widget__L_layout.addWidget(Param)
                ##
                label_bin = QLabel()
                label_bin.setStyleSheet("text-align:center;")
                path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\static\\img\\models\\img2\\{name}2.png".replace(' ', '')
                pixmap = QPixmap(path)
                pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
                label_bin.setFixedHeight(pixmap.height())
                label_bin.setPixmap(pixmap)
                widget__L_layout.addWidget(label_bin)
                label_bin.setStyleSheet('color: #ff5639;')
            # right
            if True :
                widget__R_picker = QWidget()
                widget__R_picker_layout = QVBoxLayout()
                widget__R_picker.setLayout(widget__R_picker_layout)
                
                widget__R = QWidget()
                widget__R.setMinimumHeight(430)
                widget__R.setMinimumWidth(250)
                widget__R.setMaximumWidth(300)
                widget__R.setStyleSheet("background-color:#444; border-radius:10px")
                widget__R_layout = QVBoxLayout()
                widget__R.setLayout(widget__R_layout)
                widget__R_picker_layout.addWidget(widget__R)
                widget__R_picker_layout.addStretch()
                reveal_model_layout.addWidget(widget__R_picker)

                if self.current_file :
                    if self.EN :
                        label_bin = QLabel("Binary:")
                    else :
                        label_bin = QLabel("ثنائي الإخراج:")

                    f = QFont("Arial", 17);f.setBold(1)
                    label_bin.setFont(f); widget__R_layout.addWidget(label_bin)
                    if self.current_file.bin == binary: label_bin.setStyleSheet('color: #43e882;')
                    else: label_bin.setStyleSheet('color: #ff5639;')
                    ##
                    label_bin = QLabel()
                    label_bin.setWordWrap(True)
                    f = QFont("Arial", 13);f.setBold(1)
                    label_bin.setFont(f); widget__R_layout.addWidget(label_bin)
                    if self.current_file.bin == binary:
                        if self.EN :
                            label_bin.setText("The structure of your data matches the model's data type.")
                        else :
                            label_bin.setText("نوع مخرج بياناتك يتطابق مع مخرج الخورزمية")

                    else:
                        if self.EN :
                            label_bin.setText("Your multi-class data is not compatible with this binary model.")
                        else :
                            label_bin.setText("بياناتك متعددة المخرجات لا تتطابق مع هذا الخوزمية ثنائية الاخراج")
                    # Left:
                    if reg :
                        if self.EN :
                            label_bin = QLabel("Regressor:")
                        else :
                            label_bin = QLabel("عددي :")
                    else :
                        if self.EN :
                            label_bin = QLabel("Classifier:")
                        else :
                            label_bin = QLabel("تصنيفي :")
                    f = QFont("Arial", 17);f.setBold(1)
                    label_bin.setFont(f); widget__R_layout.addWidget(label_bin)
                    if self.current_file.reg == reg: label_bin.setStyleSheet('color: #43e882;')
                    else: label_bin.setStyleSheet('color: #ff5639;')
                    ##
                    label_bin = QLabel()
                    label_bin.setWordWrap(True)
                    f = QFont("Arial", 13);f.setBold(1)
                    label_bin.setFont(f); widget__R_layout.addWidget(label_bin)
                    if self.current_file.reg == reg:
                        if self.EN :
                            label_bin.setText("The label's data type fits the model you have chosen.")
                        else :
                            label_bin.setText("نوع البيانات يتتطابق مع الخورزمية التي اخترتها")

                    else:
                        if reg :
                            if self.EN :
                                label_bin.setText("The type of the predicted data contradicts this model's output, This model output is a numaric output but your chosen dataset deeling with text-form output.")
                            else :
                                label_bin.setText("نوع البيانات المتطلب تخمينها يناقض نوع البيانات التي تخمنها الخورزمية, هذه الخورزمية تتوقع ارقام لاكن قاعدة بياناتك تحتوي على بيانات نصية")
                        else :
                            if self.EN :
                                label_bin.setText("The type of the predicted data contradicts this model's output, This model output is a text-form output but your chosen dataset deeling with numaric output.")
                            else :
                                label_bin.setText("نوع البيانات المتطلب تخمينها يناقض نوع البيانات التي تخمنها الخورزمية, هذه الخورزمية تتوقع نصوص لاكن قاعدة بياناتك تحتوي على بيانات رقمية")

                    if  self.current_file.bin != binary or self.current_file.reg != reg :
                        if related != "0" :
                            widget__R_layout.addSpacing(10)
                            if self.EN :
                                relate_model = QLabel(f'• see {related.replace("_", " ")} as a possable alternative ');widget__R_layout.addWidget(relate_model)
                            else :
                                relate_model = QLabel(f'• انظر ل {related.replace("_", " ")} كخيار بديل ');widget__R_layout.addWidget(relate_model)
                            relate_model.setStyleSheet("color:yellow;  font-size:12px")

                            f = QFont("Arial", 15);f.setBold(1)
                            relate_model.setFont(f)
                            relate_model.setWordWrap(True)
                    
                        
                    widget__R_layout.addStretch()
                    
                    def use_model_button_f(e):
                        quary = get_query(self.circle_button.__model_name__,self.project_id,self.file_combo.getOption())
                        try:
                            cur = self.db.cursor()
                            cur.execute(quary)
                            self.db.commit()
                            cur.close()
                            self.widget__.hide()

                            self.use_btn_clicked.emit(name)  
                            # self.tab_f(self.tab_6)
                        except Exception as e:
                            print(e)
                            msg_box = QMessageBox()
                            msg_box.setStyleSheet('background-color:#333; color:#fff;')
                            msg_box.setIcon(QMessageBox.Warning)
                            msg_box.setText("UNEXPECTED ERROR!")
                            msg_box.setWindowTitle("Error")
                            msg_box.addButton("OK", QMessageBox.AcceptRole)
                            msg_box.exec_()
                    if self.EN :
                        use_model_button = QPushButton("Use Model")
                    else :
                        use_model_button = QPushButton("استخدم الخورزمية")
                    self.circle_button = use_model_button
                    use_model_button.__model_name__ = name
                    if  self.current_file.bin != binary or self.current_file.reg != reg:
                        if self.EN :
                            use_model_button.setText("can't use with the chosen dataset")
                        else :
                            use_model_button.setText("لا يمكن الاستخدام مع قاعدةالبيانات")
                        use_model_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    else :
                        use_model_button.clicked.connect(use_model_button_f)
                        use_model_button.setCursor(Qt.PointingHandCursor)
                        use_model_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    widget__R_layout.addWidget(use_model_button)
                else :
                    widget__R_layout.addStretch()
                    use_model_button = QPushButton("insert files to use")
                    use_model_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    widget__R_layout.addWidget(use_model_button)
            
        
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
        self.un_s_models_layout = QVBoxLayout()
        self.project_id = id_
        # Supercised Models:
        self.un_s_models_sb = QScrollArea()
        self.un_s_models_sb_widget = QWidget()
        self.un_s_models_sb_layout = QVBoxLayout()
        self.un_s_models_sb_widget.setLayout(self.un_s_models_sb_layout)
        self.un_s_models_sb.setWidget(self.un_s_models_sb_widget)
        self.un_s_models_sb.setWidgetResizable(True)
        self.un_s_models_layout.addWidget(self.un_s_models_sb)

        # DB stuff:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM models WHERE alg_type = 'un_supervised'")
        self.models = cur.fetchall()
        cur.close()
        def choose_file_combo_f(e):
            if self.current_file :
                # file_id = self.choose_file_structure[self.file_combo.currentIndex()][0]
                # extension = self.file_combo.getOption().split('.')[-1]
                # path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\projects\\{id_}\\{file_id}.{extension}"
                file_full_path = self.file_combo.getOption()
                cur = self.db.cursor()
                cur.execute(f"SELECT name, binary, reg FROM demo_datasets")
                data = cur.fetchall()
                cur.close()
                data_names = [i[0]  for i in data]
                if file_full_path in data_names :
                    bin = data[data_names.index(file_full_path)][1]
                    reg = data[data_names.index(file_full_path)][2]

                    df,label = get_df(file_full_path)
                    path = None
                    file_id = None
                    header = 1
                    self.current_file = self.FileRepresentation(
                        file_full_path=self.file_combo.getOption(),
                        file_archive_path=path,
                        file_label=label,
                        reg=reg, bin=bin,
                        file_id=file_id,
                        file_df=df
                    )
                else :
                    extension = file_full_path.split('.')[-1]
                    cur = self.db.cursor()
                    cur.execute(
                        "SELECT file_id, label FROM files WHERE file_full_path = ? AND project_id = ?", (file_full_path, id_))
                    file_id, label = cur.fetchone()
                    cur.close()
                    path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\projects\\{id_}\\{file_id}.{extension}"

                    cur = self.db.cursor()
                    cur.execute("SELECT label, reg, binary FROM files WHERE file_id = ?", (file_id,))
                    label, reg, bin = cur.fetchall()[0]
                    file_df = QTools.read_file(path)
                    cur.close()
                    if label:
                        self.current_file = self.FileRepresentation(
                            file_full_path=self.file_combo.getOption(),
                            file_archive_path=path,
                            file_label=label,
                            reg=reg, bin=bin,
                            file_id=file_id,
                            file_df=file_df
                        )
                    else:
                        self.current_file = 0
                        msg_box = QMessageBox()
                        msg_box.setStyleSheet('background-color:#333; color:#fff;')
                        msg_box.setIcon(QMessageBox.Warning)
                        msg_box.setText("You fotgot to set the label to your file!")
                        msg_box.setWindowTitle("Error")
                        msg_box.addButton("OK", QMessageBox.AcceptRole)
                        msg_box.exec_()
        self.file_combo = file_combo
        self.file_combo.activated.connect(choose_file_combo_f)
        # cur = self.db.cursor()
        # cur.execute("SELECT file_id, file_full_path FROM files")
        # self.choose_file_structure = cur.fetchall()
        # cur.close()
        # for i in self.choose_file_structure:
        #     self.file_combo.addItem(i[1])
        self.un_s_models_sb_layout.addWidget(self.file_combo)
        self.file_combo.setSizePolicy(self.un_s_models_sb_widget.sizePolicy())
        ##
        cur = self.db.cursor()
        cur.execute(
            f"SELECT file_id, label, header FROM files WHERE  project_id = {id_}", )
        if cur.fetchone() :
            self.current_file = 1
            choose_file_combo_f(0)
        else :
            self.current_file = 0

        cur.close()
        self.EN = 1
        def change_lang(EN) :
            self.EN = EN
        self.change_lang = change_lang
        self.triple_model_container = QWidget()
        self.triple_model_container_layout = QHBoxLayout()
        self.triple_model_container.setLayout(self.triple_model_container_layout)
        self.un_s_models_sb_layout.addWidget(self.triple_model_container)
        for model in self.models:
            self.insert_unsupervised_model(model)

        self.un_s_models_sb_layout.addStretch()

        def check_fun(e):
            file_full_path = self.file_combo.getOption()
            cur = self.db.cursor()
            cur.execute(f"SELECT name, binary, reg FROM demo_datasets")
            data = cur.fetchall()
            cur.close()
            data_names = [i[0]  for i in data]
            if file_full_path in data_names :
                bin = data[data_names.index(file_full_path)][1]
                reg = data[data_names.index(file_full_path)][2]
                df,label = get_df(file_full_path)
                path = None
                file_id = None
                header = 1
                self.current_file = self.FileRepresentation(
                    file_full_path=self.file_combo.getOption(),
                    file_archive_path=path,
                    file_label=label,
                    reg=reg, bin=bin,
                    file_id=file_id,
                    file_df=df
                )
            else :
                extension = file_full_path.split('.')[-1]
                cur = self.db.cursor()
                cur.execute(
                    "SELECT file_id, label FROM files WHERE file_full_path = ? AND project_id = ?", (file_full_path, id_))
                f = cur.fetchone()
                if f and f[1] :
                    file_id, label = f
                    cur.close()
                    path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\projects\\{id_}\\{file_id}.{extension}"

                    cur = self.db.cursor()
                    cur.execute("SELECT label, reg, binary FROM files WHERE file_id = ?", (file_id,))
                    label, reg, bin = cur.fetchall()[0]
                    file_df = QTools.read_file(path)
                    cur.close()
                    if label:
                        self.current_file = self.FileRepresentation(
                            file_full_path=self.file_combo.getOption(),
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
        self.file_combo.activated.connect(check_fun)

        self.file_combo.fun1 = choose_file_combo_f
        self.file_combo.fun2 = check_fun


        layout = QVBoxLayout()  # Add a layout to center the button
        layout.addLayout(self.un_s_models_layout)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
