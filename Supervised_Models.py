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
            case "Decision_Tree":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `criterion`, `Grid_Search`,  `data_set`) VALUES ('Decision_Tree','{project_id}','gini','0', '{data_set}')"
            case "Regressor_Tree":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `Grid_Search`,   `data_set`) VALUES ('Regressor_Tree','{project_id}','0', '{data_set}')"
            case "Linear_Regression":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `Grid_Search`,   `data_set`) VALUES ('Linear_Regression','{project_id}','0', '{data_set}')"
            case "Logistic_Regression":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `Grid_Search`,   `data_set`) VALUES ('Logistic_Regression','{project_id}','0', '{data_set}')"
            case "Elastic_Net":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `alpha`, `Grid_Search`,  `data_set`) VALUES ('Elastic_Net','{project_id}','1','0', '{data_set}')"
            case "Polynomial_Regression":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `degree`, `Grid_Search`, `data_set`) VALUES ('Polynomial_Regression','{project_id}','2','0', '{data_set}')"
            case "Random_Forest_Classifier":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `n_estimators`, `Grid_Search`,   `data_set`) VALUES ('Random_Forest_Classifier','{project_id}','100','0', '{data_set}')"
            case "Random_Forest_Regressor":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `n_estimators`, `Grid_Search`,   `data_set`) VALUES ('Random_Forest_Regressor','{project_id}','100','0', '{data_set}')"
            case "Extra_Trees_Classifier":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `n_estimators`, `Grid_Search`,   `data_set`) VALUES ('Extra_Trees_Classifier','{project_id}','100','0', '{data_set}')"
            case "Extra_Trees_Regressor":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `n_estimators`, `Grid_Search`,   `data_set`) VALUES ('Extra_Trees_Regressor','{project_id}','100','0', '{data_set}')"
            case "Ada_Boost_Classifier":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `n_estimators`, `learning_rate`, `Grid_Search`,  `data_set`) VALUES ('Ada_Boost_Classifier','{project_id}','50','1','0', '{data_set}')"
            case "Ada_Boost_Regressor":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `n_estimators`, `learning_rate`, `Grid_Search`,  `data_set`) VALUES ('Ada_Boost_Regressor','{project_id}','50','1','0', '{data_set}')"
            case "Gradient_Boosting_Classifier":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `n_estimators`, `learning_rate`, `Grid_Search`,  `data_set`) VALUES ('Gradient_Boosting_Classifier','{project_id}','100','0.1','0', '{data_set}')"
            case "Gradient_Boosting_Regressor":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `n_estimators`, `learning_rate`, `Grid_Search`,  `data_set`) VALUES ('Gradient_Boosting_Regressor','{project_id}','100','0.1','0', '{data_set}')"
            case "LinearSVM":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `Grid_Search`,   `data_set`) VALUES ('LinearSVM','{project_id}','0', '{data_set}')"
            case "nonLinearSVM_ploy":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `C`, `gamma`, `Grid_Search`, `data_set`) VALUES ('nonLinearSVM_ploy','{project_id}','1','scale','0', '{data_set}')"
            case "nonLinearSVM_rbf":
                quary = f"INSERT INTO `added_models` (`model_FK`, `project`, `C`, `gamma`, `Grid_Search`, `data_set`) VALUES ('nonLinearSVM_rbf','{project_id}','1','scale','0', '{data_set}')"
    return quary

class Supervised_Models(QWidget):
    use_btn_clicked = pyqtSignal(str)  

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
        self.s_models_layout = QVBoxLayout()
        self.project_id = id_


        # DB stuff:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM models WHERE alg_type = 'supervised'")
        self.models = cur.fetchall()
        cur.close()
        file_combo_and_btns = QWidget()
        file_combo_and_btns_layout = QHBoxLayout();file_combo_and_btns.setLayout(file_combo_and_btns_layout)
        def file_combo_f(e):
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
        self.file_combo.activated.connect(file_combo_f)

        btns = QWidget()
        btns.setMaximumWidth(int(file_combo_and_btns.size().width() * 0.185))
        btns.setMaximumHeight(int(self.file_combo.size().height()))
        btns_layout = QHBoxLayout();btns.setLayout(btns_layout)
        btn1 = QLabel();btns_layout.addWidget(btn1)
        btn1.setCursor(Qt.PointingHandCursor)
        btn1.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\menu.png").scaled(30,30))
        btn2 = QLabel();btns_layout.addWidget(btn2)
        btn2.setCursor(Qt.PointingHandCursor)
        btn2.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\rows.png").scaled(30,30))
        
        
        file_combo_and_btns_layout.addWidget(self.file_combo)
        file_combo_and_btns_layout.addWidget(btns)
        self.s_models_layout.addWidget(file_combo_and_btns)

        cur = self.db.cursor()
        cur.execute(
            f"SELECT file_id, label, header FROM files WHERE  project_id = {id_}", )
        if cur.fetchone() :
            self.current_file = 1
            file_combo_f(0)
        else :
            self.current_file = 0
        cur.close()
        ###
        
        vert_and_grid = QWidget()
        self.vert_and_grid_layout = QStackedLayout();vert_and_grid.setLayout(self.vert_and_grid_layout)
        self.s_models_layout.addWidget(vert_and_grid)

        ScrollArea_1 = QScrollArea()
        # ScrollArea_1.setFixedHeight(2000)
        w = QWidget();ScrollArea_1.setWidget(w)
        self.models_container_layout = QGridLayout()
        w.setLayout(self.models_container_layout)
        self.vert_and_grid_layout.addWidget(ScrollArea_1)
        ScrollArea_1.setWidgetResizable(True)

        ScrollArea_2 = QScrollArea()
        # ScrollArea_1.setFixedHeight(2000)
        w2 = QWidget();ScrollArea_2.setWidget(w2)
        self.models_container_vert_layout = QVBoxLayout()
        w2.setLayout(self.models_container_vert_layout)
        self.vert_and_grid_layout.addWidget(ScrollArea_2)
        ScrollArea_2.setWidgetResizable(True)
        
        self.max_containers_per_row = 4  # Maximum number of buttons in one row
        self.models_containers = []
        self.vert_and_grid_layout.setCurrentIndex(0)
        
        update_models = {}
        self.EN = 1
        def change_lang(EN) :
            self.EN = EN
        self.change_lang = change_lang
        for i,model in enumerate(self.models):
            id, family, alg_type, name, binary, reg, bio, bio_ar, related, parameters, parameters_ar, ploting, import_path, playground, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model
            update_models[i] = {}
            update_models[i]['model'] = model
            def reveal_model(model_data):
                id, family, alg_type, name, binary, reg, bio, bio_ar, related, parameters, parameters_ar, ploting, import_path, playground, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model_data
                # print(f"{i}",self.current_file.reg)
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
                    # print(path)
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
                    # print(path)
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
                            # print(quary)
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
                
            update_models[i]['model_container'] = QCustomWidgets.ClickableWidget(reveal_model)
            update_models[i]['model_container'].setMaximumWidth(260)
            update_models[i]['model_container'].data_ = update_models[i]['model']
            update_models[i]['model_container_layout'] = QVBoxLayout()
            update_models[i]['model_container'].setLayout(update_models[i]['model_container_layout'])
            update_models[i]['model_container'].setMinimumHeight(260)
            size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            update_models[i]['model_container'].setSizePolicy(size_policy)
            l_1 = QLabel()
            l_1.setAlignment(Qt.AlignCenter)
            l_1.setFixedHeight(180)
            path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\database\\archive\\static\\img\\models\\img1\\{name}1.png".replace(' ', '')
            # print(path)
            pixmap = QPixmap(path).scaled(250, 180)
            l_1.setPixmap(pixmap)
            l_1.setStyleSheet('border-radius: 0px;')
            update_models[i]['model_container_layout'].addWidget(l_1)
            update_models[i]['model_container_layout'].setSpacing(0)
            l_2 = QLabel(name.replace("_", " "))
            l_2.setFont(QFont("arial", 15))
            l_2.setAlignment(Qt.AlignCenter)
            l_2.setStyleSheet('border-radius: 0px;')
            # l_1.setFixedHeight(180)
            update_models[i]['model_container_layout'].addWidget(l_2)


            update_models[i]['model_container2'] = QCustomWidgets.ClickableWidget(reveal_model)
            update_models[i]['model_container2'].setStyleSheet('background-color:#444; border-width:1.5px; border-color:#555; border-style:solid;')

            # update_models[i]['model_container']2.setMaximumWidth(260)
            update_models[i]['model_container2'].data_ = model
            update_models[i]['model_container2_layout'] = QVBoxLayout()
            update_models[i]['model_container2'].setLayout(update_models[i]['model_container2_layout'])
            update_models[i]['model_container2'].setMinimumHeight(260)
            size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            update_models[i]['model_container2'].setSizePolicy(size_policy)
            top = QWidget()
            update_models[i]['top_layout'] = QHBoxLayout();top.setLayout(update_models[i]['top_layout'])
            update_models[i]['model_container2_layout'].addWidget(top)
            if True : # update_models[i]['top_layout']
                img_label = QLabel()
                # img_label.setAlignment(Qt.AlignLeft)
                img_label.setFixedHeight(180)
                img_label.setFixedWidth(250)
                path = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\database\\archive\\static\\img\\models\\img1\\{name}1.png".replace(' ', '')
                # print(path)
                pixmap = QPixmap(path).scaled(250, 180)
                img_label.setPixmap(pixmap)
                update_models[i]['top_layout'].addWidget(img_label)

                # name and bio
                name_and_bio = QWidget();update_models[i]['top_layout'].addWidget(name_and_bio)
                name_and_bio_layout = QVBoxLayout();name_and_bio.setLayout(name_and_bio_layout)
                name_ = QLabel(name.replace("_", " "));name_and_bio_layout.addWidget(name_)
                f = QFont("Arial", 17);f.setBold(1)
                name_.setFont(f)
                name_.setStyleSheet('border:none;')
                
                bio_ = QLabel(bio)
                bio_.setStyleSheet('border:none;')
                bio_.setWordWrap(True)
                name_and_bio_layout.addWidget(bio_)

                # rag and bin
                if self.current_file :
                    rag_and_bin = QVBoxLayout();update_models[i]['top_layout'].addLayout(rag_and_bin)
                    bin_w = QWidget(); rag_and_bin.addWidget(bin_w)
                    bin_l = QVBoxLayout();bin_w.setLayout(bin_l)
                    update_models[i]['label_bin_vert'] = QLabel("Binary:")
                    update_models[i]['label_bin_vert'].setStyleSheet('border:none;')
                    f = QFont("Arial", 17);f.setBold(1)
                    update_models[i]['label_bin_vert'].setFont(f); bin_l.addWidget(update_models[i]['label_bin_vert'])
                    if self.current_file.bin == binary: update_models[i]['label_bin_vert'].setStyleSheet('border:none;color: #43e882;')
                    else: update_models[i]['label_bin_vert'].setStyleSheet('border:none;color: #ff5639;')
                    ##
                    update_models[i]['bio_bin_vert'] = QLabel()
                    update_models[i]['bio_bin_vert'].setStyleSheet('border:none;')
                    update_models[i]['bio_bin_vert'].setWordWrap(True)
                    f = QFont("Arial", 13);f.setBold(1)
                    update_models[i]['bio_bin_vert'].setFont(f); bin_l.addWidget(update_models[i]['bio_bin_vert'])
                    
                    if self.current_file.bin == binary: update_models[i]['bio_bin_vert'].setText("The structure of your data matches the model's data type.")
                    else: update_models[i]['bio_bin_vert'].setText("Your multi-class data is not compatible with this binary model.")
                    
                    # Left:
                    reg_w = QWidget(); rag_and_bin.addWidget(reg_w)
                    reg_l = QVBoxLayout();reg_w.setLayout(reg_l)

                    if reg :
                        update_models[i]['label_reg_vert'] = QLabel("Regressor:")
                    else :
                        update_models[i]['label_reg_vert'] = QLabel("Classifier:")

                    update_models[i]['label_reg_vert'].setStyleSheet('border:none;')
                    f = QFont("Arial", 17);f.setBold(1)
                    update_models[i]['label_reg_vert'].setFont(f); reg_l.addWidget(update_models[i]['label_reg_vert'])
                    if self.current_file.reg == reg:
                        update_models[i]['label_reg_vert'].setStyleSheet('border:none;color: #43e882;')
                    else: update_models[i]['label_reg_vert'].setStyleSheet('border:none;color: #ff5639;')
                    ##
                    update_models[i]['bio_reg_vert'] = QLabel()
                    update_models[i]['bio_reg_vert'].setStyleSheet('border:none;')
                    update_models[i]['bio_reg_vert'].setWordWrap(True)
                    f = QFont("Arial", 13);f.setBold(1)
                    update_models[i]['bio_reg_vert'].setFont(f); reg_l.addWidget(update_models[i]['bio_reg_vert'])

                    if self.current_file.reg == reg:
                        update_models[i]['bio_reg_vert'].setText("The label's data type fits the model you have chosen.")
                    else:
                        if reg :
                            update_models[i]['bio_reg_vert'].setText("The type of the predicted data contradicts this model's output, This model output is a numaric output but your chosen dataset deeling with text-form output.")
                        else :
                            update_models[i]['bio_reg_vert'].setText("The type of the predicted data contradicts this model's output, This model output is a text-form output but your chosen dataset deeling with numaric output.")
                    

            # l_1.setStyleSheet('border-radius: 0px;')
            # update_models[i]['model_container2_layout'].addWidget(l_1)
            update_models[i]['model_container2_layout'].setSpacing(0)

            l_2 = QLabel("Show more")
            l_2.setFont(QFont("arial", 15))
            l_2.setAlignment(Qt.AlignCenter)
            l_2.setStyleSheet('border-radius: 0px;background-color: #007ACC; color: #fff;')
            update_models[i]['model_container2_layout'].addWidget(l_2)
            l_2.setCursor(Qt.PointingHandCursor)


            self.models_containers.append(update_models[i]['model_container'])
            row, col = divmod(i, self.max_containers_per_row)
            self.models_container_layout.addWidget(update_models[i]['model_container'], row, col)
            self.models_container_vert_layout.addWidget(update_models[i]['model_container2'])
       

        def update_reg_and_bin(e):
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
                for i,model in enumerate(self.models):
                    try :
                        id, family, alg_type, name, binary, reg, bio, bio_ar, related, parameters, parameters_ar, ploting, import_path, playground, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model
                        if self.current_file.bin == binary:
                            update_models[i]['label_bin_vert'].setStyleSheet('border:none;color: #43e882;')
                            update_models[i]['bio_bin_vert'].setText("The structure of your data matches the model's data type.")

                        else:
                            update_models[i]['label_bin_vert'].setStyleSheet('border:none;color: #ff5639;')
                            update_models[i]['bio_bin_vert'].setText("Your multi-class data is not compatible with this binary model.")



                        if self.current_file.reg == reg:
                            update_models[i]['label_reg_vert'].setStyleSheet('border:none;color: #43e882;')
                            update_models[i]['bio_reg_vert'].setText("The label's data type fits the model you have chosen.")
                        else:
                            update_models[i]['label_reg_vert'].setStyleSheet('border:none;color: #ff5639;')
                            if reg :
                                update_models[i]['bio_reg_vert'].setText("The type of the predicted data contradicts this model's output, This model output is a numaric output but your chosen dataset deeling with text-form output.")
                            else :
                                update_models[i]['bio_reg_vert'].setText("The type of the predicted data contradicts this model's output, This model output is a text-form output but your chosen dataset deeling with numaric output.")
                    except :
                        rag_and_bin = QVBoxLayout();update_models[i]['top_layout'].addLayout(rag_and_bin)
                        bin_w = QWidget(); rag_and_bin.addWidget(bin_w)
                        bin_l = QVBoxLayout();bin_w.setLayout(bin_l)
                        update_models[i]['label_bin_vert'] = QLabel("Binary:")
                        update_models[i]['label_bin_vert'].setStyleSheet('border:none;')
                        f = QFont("Arial", 17);f.setBold(1)
                        update_models[i]['label_bin_vert'].setFont(f); bin_l.addWidget(update_models[i]['label_bin_vert'])
                        if self.current_file.bin == binary: update_models[i]['label_bin_vert'].setStyleSheet('border:none;color: #43e882;')
                        else: update_models[i]['label_bin_vert'].setStyleSheet('border:none;color: #ff5639;')
                        ##
                        update_models[i]['bio_bin_vert'] = QLabel()
                        update_models[i]['bio_bin_vert'].setStyleSheet('border:none;')
                        update_models[i]['bio_bin_vert'].setWordWrap(True)
                        f = QFont("Arial", 13);f.setBold(1)
                        update_models[i]['bio_bin_vert'].setFont(f); bin_l.addWidget(update_models[i]['bio_bin_vert'])
                        
                        if self.current_file.bin == binary: update_models[i]['bio_bin_vert'].setText("The structure of your data matches the model's data type.")
                        else: update_models[i]['bio_bin_vert'].setText("Your multi-class data is not compatible with this binary model.")
                        
                        # Left:
                        reg_w = QWidget(); rag_and_bin.addWidget(reg_w)
                        reg_l = QVBoxLayout();reg_w.setLayout(reg_l)

                        if reg :
                            update_models[i]['label_reg_vert'] = QLabel("Regressor:")
                        else :
                            update_models[i]['label_reg_vert'] = QLabel("Classifier:")

                        update_models[i]['label_reg_vert'].setStyleSheet('border:none;')
                        f = QFont("Arial", 17);f.setBold(1)
                        update_models[i]['label_reg_vert'].setFont(f); reg_l.addWidget(update_models[i]['label_reg_vert'])
                        if self.current_file.reg == reg:
                            update_models[i]['label_reg_vert'].setStyleSheet('border:none;color: #43e882;')
                        else: update_models[i]['label_reg_vert'].setStyleSheet('border:none;color: #ff5639;')
                        ##
                        update_models[i]['bio_reg_vert'] = QLabel()
                        update_models[i]['bio_reg_vert'].setStyleSheet('border:none;')
                        update_models[i]['bio_reg_vert'].setWordWrap(True)
                        f = QFont("Arial", 13);f.setBold(1)
                        update_models[i]['bio_reg_vert'].setFont(f); reg_l.addWidget(update_models[i]['bio_reg_vert'])

                        if self.current_file.reg == reg:
                            update_models[i]['bio_reg_vert'].setText("The label's data type fits the model you have chosen.")
                        else:
                            if reg :
                                update_models[i]['bio_reg_vert'].setText("The type of the predicted data contradicts this model's output, This model output is a numaric output but your chosen dataset deeling with text-form output.")
                            else :
                                update_models[i]['bio_reg_vert'].setText("The type of the predicted data contradicts this model's output, This model output is a text-form output but your chosen dataset deeling with numaric output.")
                        
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
                        for i,model in enumerate(self.models):
                            try :
                                id, family, alg_type, name, binary, reg, bio, bio_ar, related, parameters, parameters_ar, ploting, import_path, playground, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model
                                if self.current_file.bin == binary:
                                    update_models[i]['label_bin_vert'].setStyleSheet('border:none;color: #43e882;')
                                    update_models[i]['bio_bin_vert'].setText("The structure of your data matches the model's data type.")

                                else:
                                    update_models[i]['label_bin_vert'].setStyleSheet('border:none;color: #ff5639;')
                                    update_models[i]['bio_bin_vert'].setText("Your multi-class data is not compatible with this binary model.")



                                if self.current_file.reg == reg:
                                    update_models[i]['label_reg_vert'].setStyleSheet('border:none;color: #43e882;')
                                    update_models[i]['bio_reg_vert'].setText("The label's data type fits the model you have chosen.")
                                else:
                                    update_models[i]['label_reg_vert'].setStyleSheet('border:none;color: #ff5639;')
                                    if reg :
                                        update_models[i]['bio_reg_vert'].setText("The type of the predicted data contradicts this model's output, This model output is a numaric output but your chosen dataset deeling with text-form output.")
                                    else :
                                        update_models[i]['bio_reg_vert'].setText("The type of the predicted data contradicts this model's output, This model output is a text-form output but your chosen dataset deeling with numaric output.")
                            except :
                                rag_and_bin = QVBoxLayout();update_models[i]['top_layout'].addLayout(rag_and_bin)
                                bin_w = QWidget(); rag_and_bin.addWidget(bin_w)
                                bin_l = QVBoxLayout();bin_w.setLayout(bin_l)
                                update_models[i]['label_bin_vert'] = QLabel("Binary:")
                                update_models[i]['label_bin_vert'].setStyleSheet('border:none;')
                                f = QFont("Arial", 17);f.setBold(1)
                                update_models[i]['label_bin_vert'].setFont(f); bin_l.addWidget(update_models[i]['label_bin_vert'])
                                if self.current_file.bin == binary: update_models[i]['label_bin_vert'].setStyleSheet('border:none;color: #43e882;')
                                else: update_models[i]['label_bin_vert'].setStyleSheet('border:none;color: #ff5639;')
                                ##
                                update_models[i]['bio_bin_vert'] = QLabel()
                                update_models[i]['bio_bin_vert'].setStyleSheet('border:none;')
                                update_models[i]['bio_bin_vert'].setWordWrap(True)
                                f = QFont("Arial", 13);f.setBold(1)
                                update_models[i]['bio_bin_vert'].setFont(f); bin_l.addWidget(update_models[i]['bio_bin_vert'])
                                
                                if self.current_file.bin == binary: update_models[i]['bio_bin_vert'].setText("The structure of your data matches the model's data type.")
                                else: update_models[i]['bio_bin_vert'].setText("Your multi-class data is not compatible with this binary model.")
                                
                                # Left:
                                reg_w = QWidget(); rag_and_bin.addWidget(reg_w)
                                reg_l = QVBoxLayout();reg_w.setLayout(reg_l)

                                if reg :
                                    update_models[i]['label_reg_vert'] = QLabel("Regressor:")
                                else :
                                    update_models[i]['label_reg_vert'] = QLabel("Classifier:")

                                update_models[i]['label_reg_vert'].setStyleSheet('border:none;')
                                f = QFont("Arial", 17);f.setBold(1)
                                update_models[i]['label_reg_vert'].setFont(f); reg_l.addWidget(update_models[i]['label_reg_vert'])
                                if self.current_file.reg == reg:
                                    update_models[i]['label_reg_vert'].setStyleSheet('border:none;color: #43e882;')
                                else: update_models[i]['label_reg_vert'].setStyleSheet('border:none;color: #ff5639;')
                                ##
                                update_models[i]['bio_reg_vert'] = QLabel()
                                update_models[i]['bio_reg_vert'].setStyleSheet('border:none;')
                                update_models[i]['bio_reg_vert'].setWordWrap(True)
                                f = QFont("Arial", 13);f.setBold(1)
                                update_models[i]['bio_reg_vert'].setFont(f); reg_l.addWidget(update_models[i]['bio_reg_vert'])

                                if self.current_file.reg == reg:
                                    update_models[i]['bio_reg_vert'].setText("The label's data type fits the model you have chosen.")
                                else:
                                    if reg :
                                        update_models[i]['bio_reg_vert'].setText("The type of the predicted data contradicts this model's output, This model output is a numaric output but your chosen dataset deeling with text-form output.")
                                    else :
                                        update_models[i]['bio_reg_vert'].setText("The type of the predicted data contradicts this model's output, This model output is a text-form output but your chosen dataset deeling with numaric output.")
                                
                    else:
                        msg_box = QMessageBox()
                        msg_box.setStyleSheet('background-color:#333; color:#fff;')
                        msg_box.setIcon(QMessageBox.Warning)
                        msg_box.setText("You fotgot to set the label to your file!")
                        msg_box.setWindowTitle("Error")
                        msg_box.addButton("OK", QMessageBox.AcceptRole)
                        msg_box.exec_()
        self.file_combo.activated.connect(update_reg_and_bin)

        self.file_combo.fun1 = file_combo_f
        self.file_combo.fun2 = update_reg_and_bin

        btn1.mousePressEvent = lambda X : self.vert_and_grid_layout.setCurrentIndex(0)
        btn2.mousePressEvent = lambda X : self.vert_and_grid_layout.setCurrentIndex(1)

    # def resizeEvent(self, event):
    #     # Calcul2ate the number of models_container in one row based on the window width
    #     new_models_container_per_row = max(1, event.size().width() // 250)  # Adjust based on the button width

    #     if new_models_container_per_row != self.max_containers_per_row:
    #         # Clear the layout
    #         reveal_model_layouttemp = self.models_container_layout
    #         for container in self.models_containers:
    #             reveal_model_layouttemp.removeWidget(container)
    #             container.deleteLater()
                    
    #         # Recreate models_container and arrange them in rows based on the new count
    #         self.max_containers_per_row = new_models_container_per_row
    #         for i, button in enumerate(self.models_containers):
    #             row, col = divmod(i, self.max_containers_per_row)
    #             reveal_model_layouttemp.addWidget(button, row, col)

        # super().resizeEvent(event)
        layout = QVBoxLayout()  # Add a layout to center the button
        layout.addLayout(self.s_models_layout)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
