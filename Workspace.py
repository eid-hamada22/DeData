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
from supervised import models as s_models
from un_supervised import models as un_s_models
import models_plot 
from sklearn.model_selection import train_test_split
from clean_data import clean_data,get_pipeline
import pickle
from PyQt5.QtWebEngineWidgets import QWebEngineView
from demo_fils import get_df
from sklearn.tree import plot_tree



class Workspace(QWidget):
    un_labeled_file = pyqtSignal()  
    all_models = {}
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
    
    def update_models(self,model_name):
        cur= self.db.cursor()
        cur.execute(f"SELECT * FROM added_models WHERE project=5 and model_FK = '{model_name}'")
        new_model = cur.fetchone()

        organal_model_name = new_model[1]
        cur = self.db.cursor()
        cur.execute(f"SELECT * FROM models WHERE name= '{organal_model_name}'")
        model = cur.fetchall()[0]
        cur.close()
        # self.insert_model(model,added_model)

        id, family, alg_type, name, binary, reg, bio, bio_ar, related, parameters, parameters_ar, ploting, import_path, playground, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model

        def reveal_model(data):
            model = data[0]
            added_model_id = data[1]
            id, family, alg_type, name, binary, reg, bio, bio_ar, related, parameters, parameters_ar, ploting, import_path, playground, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model


            cur = self.db.cursor()
            cur.execute(f"SELECT * FROM added_models WHERE id='{added_model_id}'")
            added_model = cur.fetchone()
            cur.close()
            added_model_dic = {
                "id":	added_model[0],
                "model_FK":	added_model[1],
                "project":	added_model[2],
                "n_estimators":	added_model[3] if n_estimators else False,
                "learning_rate":	added_model[4] if learning_rate else False,
                "criterion":	added_model[5] if criterion else False,
                "C":	added_model[6] if C else False,
                "alpha":	added_model[7] if alpha else False,
                "degree":added_model[8] if degree else False,
                "gamma":	added_model[9] if gamma else False,
                "n_clusters":	added_model[10] if n_clusters else False,
                "eps":	added_model[11] if eps else False,
                "min_samples":	added_model[12] if min_samples else False,
                "saved_file_path":	added_model[13],
                "Grid_Search":added_model[14],
            }

            reveal_model_layout = QVBoxLayout()
            reveal_model_widget = QWidget()
            # reveal_model_widget.setWidgetResizable(True)
            reveal_model_widget.setLayout(reveal_model_layout)
            reveal_model_widget.setWindowTitle(f'DeData Preview Model - {name.replace("_", " ")}')
            self.widget__.setWindowTitle(f'DeData Preview Model - {name.replace("_", " ")}')
            reveal_model_widget.setMinimumSize(880, 660)
            reveal_model_widget.setStyleSheet("background-color: #333;")
            self.widget__.setCentralWidget(reveal_model_widget)
            self.widget__.show()
            reveal_model_widget.show()


            self.model_get_trained = 0 if not added_model_dic['saved_file_path'] else 1
            self.test_data_score = 0
            parameters_adjust = 0

            last_parameters_adjustment = {
                "n_estimators":	added_model[3] if n_estimators else False,
                "learning_rate":	added_model[4] if learning_rate else False,
                "criterion":	added_model[5] if criterion else False,
                "C":	added_model[6] if C else False,
                "alpha":	added_model[7] if alpha else False,
                "degree":added_model[8] if degree else False,
                "gamma":	added_model[9] if gamma else False,
                "n_clusters":	added_model[10] if n_clusters else False,
                "eps":	added_model[11] if eps else False,
                "min_samples":	added_model[12] if min_samples else False,
            }
            to_updata = {}
            def parameters_adjust_fn(parameter,value):
                last_parameters_adjustment[parameter] = value
                added_model_dic[parameter] = value
                to_updata[parameter] = value
            def get_model(parameters_adjust=False,pipeline=False):
                if pipeline:
                    def get_last_filename(base_filename, extension, folder_path):
                        existing_files = [f for f in os.listdir(folder_path) if f.startswith(base_filename) and f.endswith(extension)]
                        latest_file = max(existing_files, key=lambda f: int(f[len(base_filename):-len(extension) - 1]))
                        last_number = int(latest_file[len(base_filename):-len(extension) - 1])
                        next_filename = os.path.join(folder_path, f"{base_filename}{last_number}.{extension}")
                        return next_filename

                    base_name = name + str(added_model_dic['id']) + "_"
                    file_extension = "sav"
                    folder_name = "saved_models"
                    file = get_last_filename(base_name, file_extension, folder_name)
                    from_pickle = pickle.load(open(file, 'rb'))

                    model = from_pickle[0]
                    self.test_data_score = from_pickle[1]
                    # self.test_data_score_label.setText(self.test_data_score)
                else :

                    def get_model_(name, C=False, alpha=False, degree=False, criterion=False, n_estimators=False, learning_rate=False, gamma=False, n_clusters=False, eps=False, min_samples=False):
                        match name : 
                                case "Decision_Tree":
                                    model = s_models.Trees().Decision_Tree(criterion=criterion) if criterion else s_models.Trees().Decision_Tree()
                                case "Regressor_Tree":
                                    model = s_models.Trees().Regressor_Tree()
                                case "Linear_Regression":
                                    model = s_models.Regression().Linear_Regression()
                                case "Logistic_Regression":
                                    model = s_models.Regression().Logistic_Regression()
                                case "Elastic_Net":
                                    model = s_models.Regression().Elastic_Net(alpha=alpha) if alpha else s_models.Regression().Elastic_Net()
                                case "Polynomial_Regression":
                                    model = s_models.Regression().Polynomial_Regression(degree=degree) if degree else s_models.Regression().Polynomial_Regression()
                                case "Random_Forest_Classifier":
                                    model = s_models.Ensemble_Learning().Random_Forest_Classifier(n_estimators=n_estimators) if n_estimators else s_models.Ensemble_Learning().Random_Forest_Classifier()
                                case "Random_Forest_Regressor":
                                    model = s_models.Ensemble_Learning().Random_Forest_Regressor(n_estimators=n_estimators) if n_estimators else s_models.Ensemble_Learning().Random_Forest_Regressor()
                                case "Extra_Trees_Classifier":
                                    model = s_models.Ensemble_Learning().Extra_Trees_Classifier(n_estimators=n_estimators) if n_estimators else s_models.Ensemble_Learning().Extra_Trees_Classifier()
                                case "Extra_Trees_Regressor":
                                    model = s_models.Ensemble_Learning().Extra_Trees_Regressor(n_estimators=n_estimators) if n_estimators else s_models.Ensemble_Learning().Extra_Trees_Regressor()
                                case "Ada_Boost_Classifier":
                                    if n_estimators and learning_rate :
                                        model = s_models.Ensemble_Learning().Ada_Boost_Classifier(n_estimators=n_estimators,learning_rate=learning_rate)
                                    elif n_estimators :
                                        model = s_models.Ensemble_Learning().Ada_Boost_Classifier(n_estimators=n_estimators)
                                    elif learning_rate :
                                        model = s_models.Ensemble_Learning().Ada_Boost_Classifier(learning_rate=learning_rate)
                                    else :
                                        model = s_models.Ensemble_Learning().Ada_Boost_Classifier(learning_rate=learning_rate)
                                case "Ada_Boost_Regressor":
                                    if n_estimators and learning_rate :
                                        model = s_models.Ensemble_Learning().Ada_Boost_Regressor(n_estimators=n_estimators,learning_rate=learning_rate)
                                    elif n_estimators :
                                        model = s_models.Ensemble_Learning().Ada_Boost_Regressor(n_estimators=n_estimators)
                                    elif learning_rate :
                                        model = s_models.Ensemble_Learning().Ada_Boost_Regressor(learning_rate=learning_rate)
                                    else :
                                        model = s_models.Ensemble_Learning().Ada_Boost_Regressor(learning_rate=learning_rate)
                                case "Gradient_Boosting_Classifier":
                                    if n_estimators and learning_rate :
                                        model = s_models.Ensemble_Learning().Gradient_Boosting_Classifier(n_estimators=n_estimators,learning_rate=learning_rate)
                                    elif n_estimators :
                                        model = s_models.Ensemble_Learning().Gradient_Boosting_Classifier(n_estimators=n_estimators)
                                    elif learning_rate :
                                        model = s_models.Ensemble_Learning().Gradient_Boosting_Classifier(learning_rate=learning_rate)
                                    else :
                                        model = s_models.Ensemble_Learning().Gradient_Boosting_Classifier(learning_rate=learning_rate)
                                case "Gradient_Boosting_Regressor":
                                    if n_estimators and learning_rate :
                                        model = s_models.Ensemble_Learning().Gradient_Boosting_Regressor(n_estimators=n_estimators,learning_rate=learning_rate)
                                    elif n_estimators :
                                        model = s_models.Ensemble_Learning().Gradient_Boosting_Regressor(n_estimators=n_estimators)
                                    elif learning_rate :
                                        model = s_models.Ensemble_Learning().Gradient_Boosting_Regressor(learning_rate=learning_rate)
                                    else :
                                        model = s_models.Ensemble_Learning().Gradient_Boosting_Regressor(learning_rate=learning_rate)
                                case "LinearSVM":
                                    model = s_models.SVM().LinearSVM()
                                case "nonLinearSVM_ploy":
                                    if C and gamma :
                                        model = s_models.SVM().nonLinearSVM_ploy(C=C,gamma=gamma)
                                    elif C:
                                        model = s_models.SVM().nonLinearSVM_ploy(C=C,)
                                    elif gamma :
                                        model = s_models.SVM().nonLinearSVM_ploy(gamma=gamma)
                                    else  :
                                        model = s_models.SVM().nonLinearSVM_ploy()

                                case "nonLinearSVM_rbf":
                                    if C and gamma :
                                        model = s_models.SVM().nonLinearSVM_rbf(C=C,gamma=gamma)
                                    elif C:
                                        model = s_models.SVM().nonLinearSVM_rbf(C=C,)
                                    elif gamma :
                                        model = s_models.SVM().nonLinearSVM_rbf(gamma=gamma)
                                    else  :
                                        model = s_models.SVM().nonLinearSVM_rbf()
                                case "K_Means":
                                    model = un_s_models.Clusters().K_Means(n_clusters=n_clusters) if n_clusters else un_s_models.Clusters().K_Means()
                                case "DBSCAN":
                                    model = un_s_models.Clusters().DB_SCAN(eps=eps,min_samples=min_samples)
                                    if eps and min_samples :
                                        model = un_s_models.Clusters().DB_SCAN(eps=eps,min_samples=min_samples)
                                    elif eps:
                                        model = un_s_models.Clusters().DB_SCAN(eps=eps,)
                                    elif min_samples :
                                        model = un_s_models.Clusters().DB_SCAN(min_samples=min_samples)
                                    else  :
                                        model = un_s_models.Clusters().DB_SCAN()
                        return model
                    if parameters_adjust :
                        model = get_model_(name,C=last_parameters_adjustment['C'], alpha=last_parameters_adjustment['alpha'], degree=last_parameters_adjustment['degree'],
                            criterion=last_parameters_adjustment['criterion'], n_estimators=last_parameters_adjustment['n_estimators'], learning_rate=last_parameters_adjustment['learning_rate'],
                                gamma=last_parameters_adjustment['gamma'], n_clusters=last_parameters_adjustment['n_clusters'], eps=last_parameters_adjustment['eps'], min_samples=last_parameters_adjustment['min_samples'])
                        
                    else :
                        model = get_model_(name,C=added_model_dic['C'], alpha=added_model_dic['alpha'], degree=added_model_dic['degree'],
                                        criterion=added_model_dic['criterion'], n_estimators=added_model_dic['n_estimators'], learning_rate=added_model_dic['learning_rate'],
                                            gamma=added_model_dic['gamma'], n_clusters=added_model_dic['n_clusters'], eps=added_model_dic['eps'], min_samples=added_model_dic['min_samples'])

                return model
            def get_code(parameters_adjust=False):
                Grid_Search_code = ""
                criterion_code=""
                C_code = ""
                alpha_code= ""
                degree_code = ""
                n_estimators_code = ""
                learning_rate_code = ""
                gamma_code = ""
                n_clusters_code = ""
                eps_code = ""
                min_samples_code = ""

                if parameters_adjust :
                    if  criterion :
                        criterion_code = f"criterion='{last_parameters_adjustment['criterion']}',"
                    if  C :
                        C_code = f"C={last_parameters_adjustment['C']},"
                    if  alpha :
                        alpha_code = f"alpha={last_parameters_adjustment['alpha']},"
                    if  degree :
                        degree_code = f"degree={last_parameters_adjustment['degree']},"
                    if  n_estimators :
                        n_estimators_code = f"n_estimators={last_parameters_adjustment['n_estimators']},"
                    if  learning_rate :
                        learning_rate_code = f"learning_rate={last_parameters_adjustment['learning_rate']},"
                    if  gamma :
                        gamma_code = f"gamma={last_parameters_adjustment['gamma']},"

                    if  n_clusters :
                        n_clusters_code = f"n_clusters={last_parameters_adjustment['n_clusters']},"
                    if  eps :
                        eps_code = f"eps={last_parameters_adjustment['eps']},"
                    if  min_samples :
                        min_samples_code = f"min_samples={last_parameters_adjustment['min_samples']},"
                else :
                    if  criterion :
                        criterion_code = f"criterion='{added_model_dic['criterion']}',"
                    if  C :
                        C_code = f"C={added_model_dic['C']},"
                    if  alpha :
                        alpha_code = f"alpha={added_model_dic['alpha']},"
                    if  degree :
                        degree_code = f"degree={added_model_dic['degree']},"
                    if  n_estimators :
                        n_estimators_code = f"n_estimators={added_model_dic['n_estimators']},"
                    if  learning_rate :
                        learning_rate_code = f"learning_rate={added_model_dic['learning_rate']},"
                    if  gamma :
                        gamma_code = f"gamma={added_model_dic['gamma']},"

                    if  n_clusters :
                        n_clusters_code = f"n_clusters={added_model_dic['n_clusters']},"
                    if  eps :
                        eps_code = f"eps={added_model_dic['eps']},"
                    if  min_samples :
                        min_samples_code = f"min_samples={added_model_dic['min_samples']},"

                model_name = import_path.split(" ")[3]
                model_code = f"model = {model_name}({criterion_code}{C_code}{alpha_code}{degree_code}{n_estimators_code}{learning_rate_code}{gamma_code}{n_clusters_code}{eps_code}{min_samples_code})"
                return model_code
            def new_model_andmodelCode():
                self.model = get_model(parameters_adjust)
                self.model_code = get_code(parameters_adjust)
                self.code_label.setText(self.model_code)
                self.model_get_trained = 0

                self.test_data_score_label.setText(" ")

                train_button.setEnabled(True)
                train_button.setCursor(Qt.PointingHandCursor)
                train_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                train_button.clicked.connect(train_button_f)

                self.predict_button.setEnabled(False)
                self.predict_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                self.plot_button.setEnabled(False)
                self.plot_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                self.save_button.setEnabled(False)
                self.save_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")

            

            btns_layout = QHBoxLayout();reveal_model_layout.addLayout(btns_layout)
            stacked_layout = QStackedLayout();reveal_model_layout.addLayout(stacked_layout)

            def tab_f(tab=None):
                if not tab:
                    Tab = self.focusWidget()
                else:
                    Tab = tab
                for tab in [btn_1, btn_2]:
                    if tab == Tab:
                        tab.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    else:
                        tab.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        
            if self.EN :
                btn_1 = QPushButton("Your Data")
            else :
                btn_1 = QPushButton("بياناتك")
            btns_layout.addWidget(btn_1)
            btn_1.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
            btn_1.setCursor(Qt.PointingHandCursor)
            btn_1.clicked.connect(lambda: stacked_layout.setCurrentIndex(0))

            
            if playground :
                btn_1.clicked.connect(lambda : tab_f(btn_1))
                if self.EN :
                    btn_2 = QPushButton("Playground");btns_layout.addWidget(btn_2)
                else :
                    btn_2 = QPushButton("ساحة اللعب");btns_layout.addWidget(btn_2)
                btn_2.setStyleSheet("background-color: #555555; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                btn_2.setCursor(Qt.PointingHandCursor)
                btn_2.clicked.connect(lambda: stacked_layout.setCurrentIndex(1))
                btn_2.clicked.connect(lambda : tab_f(btn_2))
            # else :
            #     btn_2.setStyleSheet("background-color: #777777; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
            #     btn_2.setEnabled(False)
            #     # btn_2.setCursor(Qt.PointingHandCursor)
            #     # btn_2.clicked.connect(lambda: stacked_layout.setCurrentIndex(1))
            #     # btn_2.clicked.connect(lambda : tab_f(btn_2))

            first = QWidget();stacked_layout.addWidget(first)
            first_layout = QHBoxLayout();first.setLayout(first_layout)

            if playground :
                secand = QWebEngineView();stacked_layout.addWidget(secand)
                secand.setUrl(QUrl("https://ml-playground.com"))
            # left

            left_sa = QScrollArea()
            widget__L = QWidget()
            left_sa.setWidget(widget__L)
            widget__L_layout = QVBoxLayout()
            widget__L.setLayout(widget__L_layout)
            first_layout.addWidget(left_sa)
            left_sa.setWidgetResizable(True)

            # right
            widget__R_picker = QWidget()
            widget__R_picker_layout = QVBoxLayout()
            widget__R_picker.setLayout(widget__R_picker_layout)
            first_layout.addWidget(widget__R_picker)

            

            model_match = 0

            if True: # R_box1 
                self.R_box1 = QWidget()
                self.R_box1.setFixedHeight(230) # edit
                self.R_box1.setFixedWidth(200)
                self.R_box1.setStyleSheet("background-color:#444; border-radius:10px")
                self.R_box1_layout = QVBoxLayout()
                self.R_box1.setLayout(self.R_box1_layout)
                widget__R_picker_layout.addWidget(self.R_box1)
                # Binary:
                if self.EN :
                    label_bin = QLabel("Binary:")
                else :
                    label_bin = QLabel("ثنائي الإخراج:")
                f = QFont("Arial", 17);f.setBold(1)
                label_bin.setFont(f); self.R_box1_layout.addWidget(label_bin)
                if self.current_file.bin == binary: label_bin.setStyleSheet('color: #43e882;');model_match=1
                else: label_bin.setStyleSheet('color: #ff5639;')
                ##
                label_bin = QLabel()
                label_bin.setWordWrap(True)
                f = QFont("Arial", 13);f.setBold(1)
                label_bin.setFont(f); self.R_box1_layout.addWidget(label_bin)
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
                # Classifier:
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
                label_bin.setFont(f); self.R_box1_layout.addWidget(label_bin)
                if self.current_file.reg == reg: label_bin.setStyleSheet('color: #43e882;');model_match=1 #green
                else: label_bin.setStyleSheet('color: #ff5639;');model_match=0 # red
                ##
                label_bin = QLabel()
                label_bin.setWordWrap(True)
                f = QFont("Arial", 13);f.setBold(1)
                label_bin.setFont(f); self.R_box1_layout.addWidget(label_bin)
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

            if model_match :
                if added_model_dic['saved_file_path'] :
                    self.pipeline = get_model(parameters_adjust,True)
                    self.clean_data = clean_data(self.current_file.file_df )
                    self.X = self.clean_data.drop(columns=[self.current_file.file_label])
                    self.y = self.clean_data[self.current_file.file_label]
                else :
                    self.model = get_model(parameters_adjust)
            self.model_code = get_code(parameters_adjust)
            if True: # R_box2
                ############
                self.R_box2 = QWidget()
                self.R_box2.setFixedHeight(330) # edit
                self.R_box2.setFixedWidth(200)
                self.R_box2.setStyleSheet("background-color:#444; border-radius:10px")
                self.R_box2_layout = QVBoxLayout()
                self.R_box2.setLayout(self.R_box2_layout)
                widget__R_picker_layout.addWidget(self.R_box2)
                widget__R_picker_layout.addStretch()
                def train_button_f():
                    # dubble
                    self.model_get_trained = 1               
                    test_data_size = float(self.size_combo_box.getOption()) / 100
                    pd_data = self.current_file.file_df
                    # self.X_train, X_test, self.y_train, y_test, self.pipeline = clean_data(pd_data,self.current_file.file_label,test_data_size)
                    
                    self.clean_data = clean_data(pd_data)
                    self.X = self.clean_data.drop(columns=[self.current_file.file_label])
                    self.y = self.clean_data[self.current_file.file_label]

                    X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=test_data_size)
                    self.pipeline = get_pipeline(self.X,self.model)

                    if alg_type == "supervised" :
                        self.pipeline.fit(X_train,y_train)
                        self.test_data_score = self.pipeline.score(X_test,y_test)
                        self.test_data_score_label.setText(str(self.test_data_score))
                    elif alg_type == "un_supervised":
                        self.pipeline.fit(X_train)
                        self.test_data_score = "unsupported for UnSupervised models"
                        self.test_data_score_label.setText(str(self.test_data_score))

                    self.predict_button.setEnabled(True)
                    self.predict_button.setCursor(Qt.PointingHandCursor)
                    self.predict_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    # ###
                    self.plot_button.setEnabled(True)
                    self.plot_button.setCursor(Qt.PointingHandCursor)
                    self.plot_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    # ###
                    self.save_button.setEnabled(True)
                    self.save_button.setCursor(Qt.PointingHandCursor)
                    self.save_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")

                    return self.test_data_score
                # train= QCustomWidgets.ClickableWidget(train_button_f)
                # train.data_ = "hi"
                train_layout = QVBoxLayout()
                # train.setLayout(train_layout)
                size_and_label_layout = QHBoxLayout();train_layout.addLayout(size_and_label_layout)
                if self.EN :
                    size_text = QLabel("Test data size (%):")
                else :
                    size_text = QLabel("حجم بيانات التجريب (%):")
                size_and_label_layout.addWidget(size_text)
                self.size_combo_box = QCustomWidgets.DarkComboBox();self.size_combo_box.addItems([str(i) for i in range(5,40,5)]);size_and_label_layout.addWidget(self.size_combo_box)
                self.size_combo_box.setCurrentText('30')
                if self.EN :
                    train_button = QPushButton("Train Model")
                else :
                    train_button = QPushButton("تدريب الخورزمية")
                if self.model_get_trained or not model_match:train_button.setEnabled(False)

                # train_button.__model_name__ = name
                
                if not self.model_get_trained and model_match:
                    train_button.setCursor(Qt.PointingHandCursor)
                    train_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    train_button.clicked.connect(train_button_f)
                else :
                    # train_button.setCursor(Qt.PointingHandCursor)
                    train_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                train_layout.addWidget(train_button)
                

                test_data_score_layout = QHBoxLayout()
                if self.EN :
                    test_data_score_text = QLabel("Test dataset score :");test_data_score_layout.addWidget(test_data_score_text)
                else :
                    test_data_score_text = QLabel("نتيجة بيانات التجريب :");test_data_score_layout.addWidget(test_data_score_text)
                self.test_data_score_label = QLabel(str(self.test_data_score));test_data_score_layout.addWidget(self.test_data_score_label)
                train_layout.addLayout(test_data_score_layout)
                self.R_box2_layout.addLayout(train_layout)
                def predict_button_f():
                    if self.model_get_trained :
                        self.predict_window = QWidget()
                        self.predict_window_layout = QVBoxLayout()
                        self.predict_window.setLayout(self.predict_window_layout)
                        # self.predict_window.setFixedHeight(500)
                        # self.predict_window.setFixedWidth(800)
                        self.predict_window.setParent(None)
                        self.predict_window.setWindowTitle(fr"DeData Sheets - Predict Window")
                        self.predict_window.show()
                        # self.predict_window.setWidgetResizable(True)
                        grid_layout = QGridLayout()
                        self.predict_window_layout.addLayout(grid_layout)
                        column_dic = {}
                        self.columns = []
                        self.max_columns_per_row = 6
                        pd_data = self.current_file.file_df                    
                        self.clean_data = clean_data(pd_data)

                        numeric_columns = []; nonnumeric_columns = []
                        for column in self.clean_data.columns:
                            if pd.api.types.is_numeric_dtype(self.current_file.file_df[column]):
                                numeric_columns.append(column)
                                if len(set(self.current_file.file_df[column])) <= 10:
                                    nonnumeric_columns.append(column)
                            else:nonnumeric_columns.append(column)

                        for i,column in enumerate(self.clean_data.columns):
                            if column != self.current_file.file_label and len(set(self.clean_data[column])) != self.clean_data.shape[0] :
                                column_widg = QWidget()
                                column_widg.setFixedHeight(70)
                                column_widg.setFixedWidth(100)
                                column_lay = QVBoxLayout();column_widg.setLayout(column_lay)
                                column_lay.addWidget(QLabel(column))
                                column_dic[column] = {}
                                if column in numeric_columns :
                                    column_dic[column]['obj'] = QLineEdit()
                                    column_dic[column]['type'] = 'QLine'
                                else :
                                    column_dic[column]['obj'] = QComboBox()
                                    column_dic[column]['type'] = 'QCombo'
                                    items = [str(i)  for i  in set(self.clean_data[column]) if str(i) != 'nan']
                                    column_dic[column]['obj'].addItems(items)
                                column_lay.addWidget(column_dic[column]['obj'])
                                self.columns.append(column_widg)
                                row, col = divmod(i, self.max_columns_per_row)
                                grid_layout.addWidget(column_widg, row, col)

                        predicted_label = QLabel()
                        predicted_label.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        predicted_proba_label = QLabel()
                        predicted_proba_label.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        def predict_f(x,proba=False):
                            
                            # data = [[int(x.text()) for x in column_dic.values()]]
                            data = []
                            one_missed = 0
                            for x in column_dic :
                                if column_dic[x]['type'] == 'QLine' :
                                    if not column_dic[x]['obj'].text() : one_missed = 1 
                                    else : data.append(int(column_dic[x]['obj'].text()))
                                else :
                                    if not column_dic[x]['obj'].currentText() : one_missed = 1 
                                    else : data.append(str(column_dic[x]['obj'].currentText()))
                            if one_missed :
                                msg_box = QMessageBox()
                                msg_box.setStyleSheet('background-color:#333; color:#fff;')
                                msg_box.setIcon(QMessageBox.Warning)
                                msg_box.setText("Missing Data!")
                                msg_box.setWindowTitle("Error")
                                msg_box.addButton("OK", QMessageBox.AcceptRole)
                                msg_box.exec_()
                            else :
                                cl = self.clean_data.columns.to_list()
                                cl.remove(self.current_file.file_label)
                                data = pd.DataFrame([data],columns=cl)
                                # data = self.pipeline.transform(data)
                                if not proba :
                                    pr = self.pipeline.predict(data)
                                    text = f"Predicted value {pr}" if self.current_file.reg else f"Predicted class {pr}"
                                    predicted_label.setText(text)
                                else :
                                    pr = self.pipeline.predict_proba(data)
                                    text = f"Classes predictions {pr}"
                                    predicted_proba_label.setText(text)
                        if self.EN :
                            inter_predict_button = QPushButton("Predict")
                        else :
                            inter_predict_button = QPushButton("توقع")
                        self.predict_window_layout.addWidget(inter_predict_button)
                        inter_predict_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        inter_predict_button.setCursor(Qt.PointingHandCursor)
                        inter_predict_button.clicked.connect(predict_f)
                        self.predict_window_layout.addWidget(predicted_label)

                        if alg_type == "supervised" :
                            if self.EN :
                                inter_predict_button = QPushButton("Predict Proba")
                            else :
                                inter_predict_button = QPushButton("توقع الاحتمالات")
                            self.predict_window_layout.addWidget(inter_predict_button)
                            inter_predict_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                            inter_predict_button.setCursor(Qt.PointingHandCursor)
                            inter_predict_button.clicked.connect(lambda x : predict_f(x,True))
                            self.predict_window_layout.addWidget(predicted_proba_label)


                        self.predict_window_layout.addStretch()
                if self.EN :
                    self.predict_button = QPushButton("Predict")
                else :
                    self.predict_button = QPushButton("توقع")
                if not self.model_get_trained:self.predict_button.setEnabled(False)
                if not model_match:self.predict_button.setEnabled(False)

                # self.circle_button = self.predict_button
                self.predict_button.__model_name__ = name
                self.predict_button.clicked.connect(predict_button_f)
                if self.model_get_trained and model_match:
                    self.predict_button.setCursor(Qt.PointingHandCursor)
                    self.predict_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                else :
                    # self.predict_button.setCursor(Qt.PointingHandCursor)
                    self.predict_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")



                self.R_box2_layout.addWidget(self.predict_button)
                self.R_box2_layout.addStretch()


                def plot_button_f():
                    if  self.model_get_trained:
                        self.plot_window = QWidget()
                        self.plot_window_layout = QGridLayout()
                        self.plot_window.setLayout(self.plot_window_layout)
                        # self.plot_window.setFixedHeight(500)
                        # self.plot_window.setFixedWidth(800)
                        self.plot_window.setParent(None)
                        self.plot_window.setWindowTitle(fr"DeData - Plot Window")
                        self.plot_window.show()


                        plot_texts = QFont("Arial", 13);plot_texts.setBold(1)
                        # Tree plot
                        # decision boundaries
                        # AUC 
                        # heat map (sensivity,sp..)
                        # clusters knives (silhouette diagram)
                        self.numeric_columns = []; self.nonnumeric_columns = []
                        for column in self.current_file.file_df.columns:
                            if pd.api.types.is_numeric_dtype(self.current_file.file_df[column]):
                                self.numeric_columns.append(column)
                            else:self.nonnumeric_columns.append(column)
                        if len(self.nonnumeric_columns) == 0 :
                            plot_area1 = QWidget();self.plot_window_layout.addWidget(plot_area1,0,0)
                            plot_area1.setFixedSize(250,310)
                            plot_area1_layout = QVBoxLayout();plot_area1.setLayout(plot_area1_layout)
                            plot_area1_img = QLabel();plot_area1_layout.addWidget(plot_area1_img)
                            plot_area1_img.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\de_bo.png"))
                            plot_area1_img.setAlignment(Qt.AlignCenter)
                            plot_area1_text = QLabel('Decision Boundaries');plot_area1_text.setFont(plot_texts)
                            plot_area1_text.setAlignment(Qt.AlignCenter)
                            plot_area1_layout.addWidget(plot_area1_text)
                            plot_area1_btn = QPushButton("Plot");plot_area1_layout.addWidget(plot_area1_btn)
                            plot_area1_btn.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                            plot_area1_btn.setCursor(Qt.PointingHandCursor)
                            plot_area1_btn.clicked.connect(lambda x : models_plot.Decision_Boundaries(name,clean_data(self.X),self.y,self.model))

                        plot_area2 = QWidget();self.plot_window_layout.addWidget(plot_area2,0,1)
                        plot_area2.setFixedSize(250,310)
                        plot_area2_layout = QVBoxLayout();plot_area2.setLayout(plot_area2_layout)
                        plot_area2_img = QLabel();plot_area2_layout.addWidget(plot_area2_img)
                        plot_area2_img.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\output.png"))
                        plot_area2_img.setAlignment(Qt.AlignCenter)
                        plot_area2_text = QLabel('Confusion Matrix');plot_area2_text.setFont(plot_texts)
                        plot_area2_text.setAlignment(Qt.AlignCenter)
                        plot_area2_layout.addWidget(plot_area2_text)
                        plot_area2_btn = QPushButton("Plot");plot_area2_layout.addWidget(plot_area2_btn)
                        plot_area2_btn.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        plot_area2_btn.setCursor(Qt.PointingHandCursor)
                        plot_area2_btn.clicked.connect(lambda x : models_plot.confusionMatrix(self.y,self.pipeline.predict(self.X)))

                        plot_area3 = QWidget();self.plot_window_layout.addWidget(plot_area3,0,2)
                        plot_area3.setFixedSize(250,310)
                        plot_area3_layout = QVBoxLayout();plot_area3.setLayout(plot_area3_layout)
                        plot_area3_img = QLabel();plot_area3_layout.addWidget(plot_area3_img)
                        plot_area3_img.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\auc.png"))
                        plot_area3_img.setAlignment(Qt.AlignCenter)
                        plot_area3_text = QLabel('AUC');plot_area3_text.setFont(plot_texts)
                        plot_area3_text.setAlignment(Qt.AlignCenter)
                        plot_area3_layout.addWidget(plot_area3_text)
                        plot_area3_btn = QPushButton("Plot");plot_area3_layout.addWidget(plot_area3_btn)
                        plot_area3_btn.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        plot_area3_btn.setCursor(Qt.PointingHandCursor)
                        plot_area3_btn.clicked.connect(lambda x : models_plot.AUC(self.y,self.pipeline.predict(self.X)))

                        if family in ['Trees'] :
                            plot_area4 = QWidget();self.plot_window_layout.addWidget(plot_area4,1,0)
                            plot_area4.setFixedSize(250,310)
                            plot_area4_layout = QVBoxLayout();plot_area4.setLayout(plot_area4_layout)
                            plot_area4_img = QLabel();plot_area4_layout.addWidget(plot_area4_img)
                            plot_area4_img.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\tree_plot.png"))
                            plot_area4_img.setAlignment(Qt.AlignCenter)
                            plot_area4_text = QLabel('Tree Plot');plot_area4_text.setFont(plot_texts)
                            plot_area4_text.setAlignment(Qt.AlignCenter)
                            plot_area4_layout.addWidget(plot_area4_text)
                            plot_area4_btn = QPushButton("Plot");plot_area4_layout.addWidget(plot_area4_btn)
                            plot_area4_btn.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                            plot_area4_btn.setCursor(Qt.PointingHandCursor)
                            plot_area4_btn.clicked.connect(lambda x : plot_tree(self.pipeline))
                            
                        if name == "K_Means" :
                            plot_area5 = QWidget();self.plot_window_layout.addWidget(plot_area5,1,1)
                            plot_area5.setFixedSize(250,310)
                            plot_area5_layout = QVBoxLayout();plot_area5.setLayout(plot_area5_layout)
                            plot_area5_img = QLabel();plot_area5_layout.addWidget(plot_area5_img)
                            plot_area5_img.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\silout.png"))
                            plot_area5_img.setAlignment(Qt.AlignCenter)
                            plot_area5_text = QLabel('Silhouette Diagram');plot_area5_text.setFont(plot_texts)
                            plot_area5_text.setAlignment(Qt.AlignCenter)
                            plot_area5_layout.addWidget(plot_area5_text)
                            plot_area5_btn = QPushButton("Plot");plot_area5_layout.addWidget(plot_area5_btn)
                            plot_area5_btn.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                            plot_area5_btn.setCursor(Qt.PointingHandCursor)
                            plot_area5_btn.clicked.connect(lambda x : models_plot.Silhouette_Diagram(self.X,int(n_clusters_comboBox.currentText())))
                                                            
                        # if ploting:
                        #     # make new model for pca 
                        #     # test_data_size = 0.01
                        #     # pd_data = self.current_file.file_df
                        #     # X_train, X_test, y_train, y_test, self.pipeline = clean_data(pd_data,self.current_file.file_label,test_data_size)
                            
                        #     test_data_size = float(self.size_combo_box.getOption()) / 100
                        #     pd_data = self.current_file.file_df
                        #     # self.X_train, X_test, self.y_train, y_test, self.pipeline = clean_data(pd_data,self.current_file.file_label,test_data_size)
                            
                            
                        #     X = pd_data.drop(columns=[self.current_file.file_label])
                        #     y = pd_data[self.current_file.file_label]

                        #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_data_size)
                        #     pca = PCA(n_components = 2)
                        #     X_train = pca.fit_transform(X_train)
                        #     X_train
                        #     pipeline = get_pipeline(X,self.model)
                        #     self.model.fit(X_train,y_train)

                        #     select_plot(name,X_train,y_train,self.model)
                    
                if self.EN :
                    self.plot_button = QPushButton("Plot Model")
                else :
                    self.plot_button = QPushButton("عرض بياني للخورزمية")
                if not self.model_get_trained:self.plot_button.setEnabled(False)
                if not model_match:self.plot_button.setEnabled(False)


                # self.circle_button = self.plot_button
                self.plot_button.__model_name__ = name
                self.plot_button.clicked.connect(plot_button_f)

                if  self.model_get_trained and model_match:
                    self.plot_button.setCursor(Qt.PointingHandCursor)
                    self.plot_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                else :
                    # self.plot_button.setCursor(Qt.PointingHandCursor)
                    self.plot_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                self.R_box2_layout.addWidget(self.plot_button)
                self.R_box2_layout.addStretch()

                def save_button_f():
                    if  self.model_get_trained:
                        added_model_dic['saved_file_path'] = 1
                        def generate_next_filename(base_filename, extension, folder_path):
                            if not os.path.exists(folder_path):
                                os.makedirs(folder_path)

                            existing_files = [f for f in os.listdir(folder_path) if f.startswith(base_filename) and f.endswith(extension)]
                            if existing_files:
                                latest_file = max(existing_files, key=lambda f: int(f[len(base_filename):-len(extension) - 1]))
                                last_number = int(latest_file[len(base_filename):-len(extension) - 1])
                                next_number = last_number + 1
                            else:
                                next_number = 1
                            next_filename = os.path.join(folder_path, f"{base_filename}{next_number}.{extension}")
                            return next_filename

                        base_name = name + str(added_model_dic['id']) + "_"
                        file_extension = "sav"
                        folder_name = "saved_models"

                        file = generate_next_filename(base_name, file_extension, folder_name)

                        to_pickle = [self.pipeline,self.test_data_score]
                        pickle.dump(to_pickle, open(file, 'wb'))
                        
                        cur = self.db.cursor()
                        cur.execute(f"UPDATE added_models set saved_file_path = 1 WHERE id = {added_model_dic['id']}")
                        for k in to_updata.keys() :
                            cur.execute(f"UPDATE added_models set {k} = '{to_updata[k]}' WHERE id = {added_model_dic['id']}")
                            added_model_dic[k] = to_updata[k]
                        self.db.commit()
                        cur.close()
                        # self.widget__.hide()

                if self.EN :
                    self.save_button = QPushButton("Save Model")
                else :
                    self.save_button = QPushButton("حفظ الخورزمية")
                if not self.model_get_trained:self.save_button.setEnabled(False)
                if not model_match:self.save_button.setEnabled(False)

                # self.circle_button = self.save_button
                self.save_button.__model_name__ = name
                self.save_button.clicked.connect(save_button_f)
                if  self.model_get_trained and model_match:
                    self.save_button.setCursor(Qt.PointingHandCursor)
                    self.save_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                else :
                    # self.save_button.setCursor(Qt.PointingHandCursor)
                    self.save_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")

                self.R_box2_layout.addWidget(self.save_button)
                self.R_box2_layout.addStretch()


                cur = self.db.cursor()
                cur.execute(f"SELECT saved_file_path FROM added_models WHERE id = '{added_model_dic['id']}'")
                saved_file_path = cur.fetchone()[0]
                cur.close()
                if saved_file_path :
                    def get_last_filename(base_filename, extension, folder_path):
                        existing_files = [f for f in os.listdir(folder_path) if f.startswith(base_filename) and f.endswith(extension)]
                        latest_file = max(existing_files, key=lambda f: int(f[len(base_filename):-len(extension) - 1]))
                        last_number = int(latest_file[len(base_filename):-len(extension) - 1])
                        next_filename = os.path.join(folder_path, f"{base_filename}{last_number}.{extension}")
                        return next_filename

                    base_name = name + str(added_model_dic['id']) + "_"
                    file_extension = "sav"
                    folder_name = "saved_models"
                    file = get_last_filename(base_name, file_extension, folder_name)
                    from_pickle = pickle.load(open(file, 'rb'))

                    self.test_data_score_label.setText(str(from_pickle[1]))

                    train_button.setEnabled(False)
                    train_button.setCursor(Qt.PointingHandCursor)
                    train_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    train_button.clicked.connect(train_button_f)

                    self.predict_button.setEnabled(True)
                    self.predict_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    self.predict_button.setCursor(Qt.PointingHandCursor)
                    self.plot_button.setEnabled(True)
                    self.plot_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    self.plot_button.setCursor(Qt.PointingHandCursor)
                    self.save_button.setEnabled(True)
                    self.save_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    self.save_button.setCursor(Qt.PointingHandCursor)

                ############
            ####### Parameters start

            # self.test_data_score_label.setText(str(self.test_data_score))

            one_at_least = 0
            if True: # adding Parameters
                para_font = QFont("Arial", 19);para_font.setBold(1)
                child_font = QFont("Arial", 15);child_font.setBold(1)
                if added_model_dic['criterion']:
                    if not one_at_least :
                        if self.EN :
                            Parameters_label = QLabel("Current Parameters :")
                        else :
                            Parameters_label = QLabel("المتغيرات الحالية :")
                        Parameters_label.setFont(para_font)
                        widget__L_layout.addWidget(Parameters_label)
                    one_at_least+=1
                    criterion_label = QLabel("criterion")
                    criterion_label.setFont(child_font)
                    widget__L_layout.addWidget(criterion_label)
                    criterion_comboBox = QComboBox()
                    criterion_comboBox.addItems(['gini', 'entropy'])
                    criterion_comboBox.setCurrentText(str(added_model_dic['criterion']))
                    parameters_adjust = 1
                    criterion_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('criterion',X) )
                    criterion_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                    criterion_layout = QHBoxLayout()
                    criterion_layout.addWidget(criterion_label)
                    criterion_layout.addWidget(criterion_comboBox)
                    widget__L_layout.addLayout(criterion_layout)
                if added_model_dic['alpha']:
                    if not one_at_least :
                        if self.EN :
                            Parameters_label = QLabel("Current Parameters :")
                        else :
                            Parameters_label = QLabel("المتغيرات الحالية :")
                        Parameters_label.setFont(para_font)
                        widget__L_layout.addWidget(Parameters_label)
                    one_at_least+=1
                    alpha_label = QLabel("alpha")
                    alpha_label.setFont(child_font)
                    widget__L_layout.addWidget(alpha_label)
                    alpha_comboBox = QComboBox()
                    alpha_comboBox.addItems([str(int(i/10)) if i in [0,10] else str(i/10) for i in range(11)])
                    alpha_comboBox.setCurrentText(str(added_model_dic['alpha']))
                    # alpha_comboBox.setCurrentIndex(4)
                    parameters_adjust = 1
                    alpha_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('alpha',X) )
                    alpha_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                    alpha_layout = QHBoxLayout()
                    alpha_layout.addWidget(alpha_label)
                    alpha_layout.addWidget(alpha_comboBox)
                    widget__L_layout.addLayout(alpha_layout)
                if added_model_dic['C']:
                    if not one_at_least :
                        if self.EN :
                            Parameters_label = QLabel("Current Parameters :")
                        else :
                            Parameters_label = QLabel("المتغيرات الحالية :")
                        Parameters_label.setFont(para_font)
                        widget__L_layout.addWidget(Parameters_label)
                    one_at_least+=1
                    C_label = QLabel("C")
                    C_label.setFont(child_font)
                    widget__L_layout.addWidget(C_label)
                    C_comboBox = QComboBox()
                    C_comboBox.addItems(['0.001', '0.01', '0.1', '1', '10', '100'])
                    C_comboBox.setCurrentText(str(added_model_dic['C']))
                    parameters_adjust = 1
                    C_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('C',X) )
                    C_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())

                    C_layout = QHBoxLayout()
                    C_layout.addWidget(C_label)
                    C_layout.addWidget(C_comboBox)
                    widget__L_layout.addLayout(C_layout)
                if added_model_dic['degree']:
                    if not one_at_least :
                        if self.EN :
                            Parameters_label = QLabel("Current Parameters :")
                        else :
                            Parameters_label = QLabel("المتغيرات الحالية :")
                        Parameters_label.setFont(para_font)
                        widget__L_layout.addWidget(Parameters_label)
                    one_at_least+=1
                    degree_label = QLabel("degree")
                    degree_label.setFont(child_font)
                    widget__L_layout.addWidget(degree_label)
                    degree_comboBox = QComboBox()
                    degree_comboBox.addItems(['1', '2', '3', '4', '5'])
                    degree_comboBox.setCurrentText(str(added_model_dic['degree']))
                    parameters_adjust = 1
                    degree_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('degree',X) )
                    degree_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())

                    degree_layout = QHBoxLayout()
                    degree_layout.addWidget(degree_label)
                    degree_layout.addWidget(degree_comboBox)
                    widget__L_layout.addLayout(degree_layout)
                if added_model_dic['n_estimators']:
                    if not one_at_least :
                        if self.EN :
                            Parameters_label = QLabel("Current Parameters :")
                        else :
                            Parameters_label = QLabel("المتغيرات الحالية :")
                        Parameters_label.setFont(para_font)
                        widget__L_layout.addWidget(Parameters_label)
                    one_at_least+=1
                    n_estimators_label = QLabel("n_estimators")
                    n_estimators_label.setFont(child_font)
                    widget__L_layout.addWidget(n_estimators_label)
                    n_estimators_comboBox = QComboBox()
                    n_estimators_comboBox.addItems(['1', '10', '30', '50',
                                        '70', '100', '120', '150', '200', '500'])
                    n_estimators_comboBox.setCurrentText(str(added_model_dic['n_estimators']))
                    parameters_adjust = 1
                    n_estimators_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('n_estimators',X) )
                    n_estimators_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())

                    n_estimators_layout = QHBoxLayout()
                    n_estimators_layout.addWidget(n_estimators_label)
                    n_estimators_layout.addWidget(n_estimators_comboBox)
                    widget__L_layout.addLayout(n_estimators_layout)
                if added_model_dic['learning_rate']:
                    if not one_at_least :
                        if self.EN :
                            Parameters_label = QLabel("Current Parameters :")
                        else :
                            Parameters_label = QLabel("المتغيرات الحالية :")
                        Parameters_label.setFont(para_font)
                        widget__L_layout.addWidget(Parameters_label)
                    one_at_least+=1
                    learning_rate_label = QLabel("learning_rate")
                    learning_rate_label.setFont(child_font)
                    widget__L_layout.addWidget(learning_rate_label)
                    learning_rate_comboBox = QComboBox()
                    learning_rate_comboBox.addItems([str(int(i/10)) if i in [0,10] else str(i/10) for i in range(11)])
                    learning_rate_comboBox.setCurrentText(str(added_model_dic['learning_rate']))
                    parameters_adjust = 1
                    learning_rate_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('learning_rate',X) )
                    learning_rate_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                    learning_rate_layout = QHBoxLayout()
                    learning_rate_layout.addWidget(learning_rate_label)
                    learning_rate_layout.addWidget(learning_rate_comboBox)
                    widget__L_layout.addLayout(learning_rate_layout)
                if added_model_dic['gamma']:
                    if not one_at_least :
                        if self.EN :
                            Parameters_label = QLabel("Current Parameters :")
                        else :
                            Parameters_label = QLabel("المتغيرات الحالية :")
                        Parameters_label.setFont(para_font)
                        widget__L_layout.addWidget(Parameters_label)
                    one_at_least+=1
                    gamma_label = QLabel("gamma")
                    gamma_label.setFont(child_font)
                    widget__L_layout.addWidget(gamma_label)
                    gamma_comboBox = QComboBox()
                    gamma_comboBox.addItems(['1', '0.1', '0.01', '0.001', '0.0001', 'auto'])
                    gamma_comboBox.setCurrentText(str(added_model_dic['gamma']))
                    parameters_adjust = 1
                    gamma_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('gamma',X) )
                    gamma_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                    gamma_layout = QHBoxLayout()
                    gamma_layout.addWidget(gamma_label)
                    gamma_layout.addWidget(gamma_comboBox)
                    widget__L_layout.addLayout(gamma_layout)
                if added_model_dic['n_clusters']:
                    if not one_at_least :
                        if self.EN :
                            Parameters_label = QLabel("Current Parameters :")
                        else :
                            Parameters_label = QLabel("المتغيرات الحالية :")
                        Parameters_label.setFont(para_font)
                        widget__L_layout.addWidget(Parameters_label)
                    one_at_least+=1
                    n_clusters_label = QLabel("n_clusters")
                    n_clusters_label.setFont(child_font)
                    widget__L_layout.addWidget(n_clusters_label)
                    n_clusters_comboBox = QComboBox()
                    n_clusters_comboBox.addItems([str(i) for i in range(1,11)])
                    n_clusters_comboBox.setCurrentText(str(added_model_dic['n_clusters']))
                    parameters_adjust = 1
                    n_clusters_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('n_clusters',X) )
                    n_clusters_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                    n_clusters_layout = QHBoxLayout()
                    n_clusters_layout.addWidget(n_clusters_label)
                    n_clusters_layout.addWidget(n_clusters_comboBox)
                    widget__L_layout.addLayout(n_clusters_layout)
                if added_model_dic['eps']:
                    if not one_at_least :
                        if self.EN :
                            Parameters_label = QLabel("Current Parameters :")
                        else :
                            Parameters_label = QLabel("المتغيرات الحالية :")
                        Parameters_label.setFont(para_font)
                        widget__L_layout.addWidget(Parameters_label)
                    one_at_least+=1
                    eps_label = QLabel("eps")
                    eps_label.setFont(child_font)
                    widget__L_layout.addWidget(eps_label)
                    eps_comboBox = QComboBox()
                    eps_comboBox.addItems([str(int(i/10)) if i in [0,10] else str(i/10) for i in range(11)])
                    eps_comboBox.setCurrentText(str(added_model_dic['eps']))
                    parameters_adjust = 1
                    eps_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('eps',X) )
                    eps_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                    eps_layout = QHBoxLayout()
                    eps_layout.addWidget(eps_label)
                    eps_layout.addWidget(eps_comboBox)
                    widget__L_layout.addLayout(eps_layout)
                if added_model_dic['min_samples']:
                    if not one_at_least :
                        if self.EN :
                            Parameters_label = QLabel("Current Parameters :")
                        else :
                            Parameters_label = QLabel("المتغيرات الحالية :")
                        Parameters_label.setFont(para_font)
                        widget__L_layout.addWidget(Parameters_label)
                    one_at_least+=1
                    min_samples_label = QLabel("min_samples")
                    min_samples_label.setFont(child_font)
                    widget__L_layout.addWidget(min_samples_label)
                    min_samples_comboBox = QComboBox()
                    min_samples_comboBox.addItems([str(i) for i in range(10)])
                    min_samples_comboBox.setCurrentText(str(added_model_dic['min_samples']))
                    parameters_adjust = 1
                    min_samples_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('min_samples',X) )
                    min_samples_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                    min_samples_layout = QHBoxLayout()
                    min_samples_layout.addWidget(min_samples_label)
                    min_samples_layout.addWidget(min_samples_comboBox)
                    widget__L_layout.addLayout(min_samples_layout)
            
            code_widget  = QWidget()
            # code_widget.setFixedHeight(100) # edit
            # code_widget.setFixedWidth(250)
            code_widget.setStyleSheet("background-color:#444; border-radius:7px")
            code_layout = QVBoxLayout()
            code_widget.setLayout(code_layout)
            import_code = QLabel(import_path);import_code.setFont(QFont("Arial", 10));code_layout.addWidget(import_code)
            self.code_label = QLabel(self.model_code);self.code_label.setFont(QFont("Arial", 10));code_layout.addWidget(self.code_label)
            widget__L_layout.addWidget(code_widget)
            # label_1:
            label_1 = QLabel(name.replace("_", " ")+":")
            f = QFont("Arial", 19);f.setBold(1)
            label_1.setFont(f)
            widget__L_layout.addWidget(label_1)
            # Bio
            Bio = QLabel()
            Bio.setWordWrap(1)
            Bio.setFont(QFont("Arial", 12))
            # widget__.setStyleSheet("background-color: #333;")
            Bio.setStyleSheet("background-color: #333; border-color:#333; border-width:2px; border-style:solid;")
            if self.EN :
                Bio.setText(bio)
            else :
                Bio.setText(bio_ar)
            widget__L_layout.addWidget(Bio)
            self.widget__.show()
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
            params.setFont(f)
            widget__L_layout.addWidget(params)
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
            
        self.all_models[id] = {}
        self.all_models[id]['data_set'] = new_model[-1]
        self.all_models[id]['model_container'] = QCustomWidgets.ClickableWidget(reveal_model)
        self.all_models[id]['model_container'].data_ = [model,new_model[0]] # ids
        self.all_models[id]['model_container'].setFixedWidth(260)
        model_container_layout = QVBoxLayout()
        self.all_models[id]['model_container'].setLayout(model_container_layout)
        self.all_models[id]['model_container'].setFixedHeight(260)
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
    
        self.choose_certian_models(0)

    def __init__(self, id_,file_combo):
        super().__init__()
        self.connect_database()
        self.widget__ = QMainWindow()
        self.un_s_models_layout = QVBoxLayout()

        # Supercised Models:
        self.un_s_models_sb = QScrollArea()
        self.un_s_models_sb_widget = QWidget()
        # self.un_s_models_sb_widget.setFixedWidth(810)
        self.un_s_models_sb_layout = QVBoxLayout()
        self.un_s_models_sb_widget.setLayout(self.un_s_models_sb_layout)
        self.un_s_models_sb.setWidget(self.un_s_models_sb_widget)
        self.un_s_models_sb.setWidgetResizable(True)
        self.un_s_models_layout.addWidget(self.un_s_models_sb)

        # DB stuff:
        cur = self.db.cursor()
        cur.execute(f"SELECT * FROM added_models WHERE project='{id_}'")
        self.models = cur.fetchall()
        cur.close()
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
                        msg_box = QMessageBox()
                        msg_box.setStyleSheet('background-color:#333; color:#fff;')
                        msg_box.setIcon(QMessageBox.Warning)
                        msg_box.setText("You fotgot to set the label to your file!")
                        msg_box.setWindowTitle("Error")
                        msg_box.addButton("OK", QMessageBox.AcceptRole)
                        msg_box.exec_()
                        self.un_labeled_file.emit()
        self.file_combo = file_combo
        self.file_combo.activated.connect(file_combo_f)
        self.un_s_models_sb_layout.addWidget(self.file_combo)
        ##
        cur = self.db.cursor()
        cur.execute(
            f"SELECT file_id, label, header FROM files WHERE  project_id = {id_}", )
        if cur.fetchone() :
            self.current_file = 1
            file_combo_f(0)
        else :
            self.current_file = 0

        self.EN = 1
        def change_lang(EN) :
            self.EN = EN
        self.change_lang = change_lang

        cur.close()
        self.model_container = QWidget()
        self.model_container_layout = QGridLayout()
        self.model_container.setLayout(self.model_container_layout)
        self.un_s_models_sb_layout.addWidget(self.model_container)
        for i,added_model in enumerate(self.models):
            organal_model_name = added_model[1]
            cur = self.db.cursor()
            cur.execute(f"SELECT * FROM models WHERE name= '{organal_model_name}'")
            model = cur.fetchall()[0]
            cur.close()
            # self.insert_model(model,added_model)

            id, family, alg_type, name, binary, reg, bio, bio_ar, related, parameters, parameters_ar, ploting, import_path, playground, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model

            def reveal_model(data):
                model = data[0]
                added_model_id = data[1]
                id, family, alg_type, name, binary, reg, bio, bio_ar, related, parameters, parameters_ar, ploting, import_path, playground, C, alpha, degree, criterion, n_estimators, learning_rate, gamma, n_clusters, eps, min_samples = model


                cur = self.db.cursor()
                cur.execute(f"SELECT * FROM added_models WHERE id='{added_model_id}'")
                added_model = cur.fetchone()
                cur.close()
                added_model_dic = {
                    "id":	added_model[0],
                    "model_FK":	added_model[1],
                    "project":	added_model[2],
                    "n_estimators":	added_model[3] if n_estimators else False,
                    "learning_rate":	added_model[4] if learning_rate else False,
                    "criterion":	added_model[5] if criterion else False,
                    "C":	added_model[6] if C else False,
                    "alpha":	added_model[7] if alpha else False,
                    "degree":added_model[8] if degree else False,
                    "gamma":	added_model[9] if gamma else False,
                    "n_clusters":	added_model[10] if n_clusters else False,
                    "eps":	added_model[11] if eps else False,
                    "min_samples":	added_model[12] if min_samples else False,
                    "saved_file_path":	added_model[13],
                    "Grid_Search":added_model[14],
                }

                reveal_model_layout = QVBoxLayout()
                reveal_model_widget = QWidget()
                # reveal_model_widget.setWidgetResizable(True)
                reveal_model_widget.setLayout(reveal_model_layout)
                reveal_model_widget.setWindowTitle(f'DeData Preview Model - {name.replace("_", " ")}')
                self.widget__.setWindowTitle(f'DeData Preview Model - {name.replace("_", " ")}')
                reveal_model_widget.setMinimumSize(880, 660)
                reveal_model_widget.setStyleSheet("background-color: #333;")
                self.widget__.setCentralWidget(reveal_model_widget)
                self.widget__.show()
                reveal_model_widget.show()


                self.model_get_trained = 0 if not added_model_dic['saved_file_path'] else 1
                self.test_data_score = 0
                parameters_adjust = 0

                last_parameters_adjustment = {
                    "n_estimators":	added_model[3] if n_estimators else False,
                    "learning_rate":	added_model[4] if learning_rate else False,
                    "criterion":	added_model[5] if criterion else False,
                    "C":	added_model[6] if C else False,
                    "alpha":	added_model[7] if alpha else False,
                    "degree":added_model[8] if degree else False,
                    "gamma":	added_model[9] if gamma else False,
                    "n_clusters":	added_model[10] if n_clusters else False,
                    "eps":	added_model[11] if eps else False,
                    "min_samples":	added_model[12] if min_samples else False,
                }
                to_updata = {}
                def parameters_adjust_fn(parameter,value):
                    last_parameters_adjustment[parameter] = value
                    added_model_dic[parameter] = value
                    to_updata[parameter] = value
                def get_model(parameters_adjust=False,pipeline=False):
                    if pipeline:
                        def get_last_filename(base_filename, extension, folder_path):
                            existing_files = [f for f in os.listdir(folder_path) if f.startswith(base_filename) and f.endswith(extension)]
                            latest_file = max(existing_files, key=lambda f: int(f[len(base_filename):-len(extension) - 1]))
                            last_number = int(latest_file[len(base_filename):-len(extension) - 1])
                            next_filename = os.path.join(folder_path, f"{base_filename}{last_number}.{extension}")
                            return next_filename

                        base_name = name + str(added_model_dic['id']) + "_"
                        file_extension = "sav"
                        folder_name = "saved_models"
                        file = get_last_filename(base_name, file_extension, folder_name)
                        from_pickle = pickle.load(open(file, 'rb'))

                        model = from_pickle[0]
                        self.test_data_score = from_pickle[1]
                        # self.test_data_score_label.setText(self.test_data_score)
                    else :

                        def get_model_(name, C=False, alpha=False, degree=False, criterion=False, n_estimators=False, learning_rate=False, gamma=False, n_clusters=False, eps=False, min_samples=False):
                            match name : 
                                    case "Decision_Tree":
                                        model = s_models.Trees().Decision_Tree(criterion=criterion) if criterion else s_models.Trees().Decision_Tree()
                                    case "Regressor_Tree":
                                        model = s_models.Trees().Regressor_Tree()
                                    case "Linear_Regression":
                                        model = s_models.Regression().Linear_Regression()
                                    case "Logistic_Regression":
                                        model = s_models.Regression().Logistic_Regression()
                                    case "Elastic_Net":
                                        model = s_models.Regression().Elastic_Net(alpha=alpha) if alpha else s_models.Regression().Elastic_Net()
                                    case "Polynomial_Regression":
                                        model = s_models.Regression().Polynomial_Regression(degree=degree) if degree else s_models.Regression().Polynomial_Regression()
                                    case "Random_Forest_Classifier":
                                        model = s_models.Ensemble_Learning().Random_Forest_Classifier(n_estimators=n_estimators) if n_estimators else s_models.Ensemble_Learning().Random_Forest_Classifier()
                                    case "Random_Forest_Regressor":
                                        model = s_models.Ensemble_Learning().Random_Forest_Regressor(n_estimators=n_estimators) if n_estimators else s_models.Ensemble_Learning().Random_Forest_Regressor()
                                    case "Extra_Trees_Classifier":
                                        model = s_models.Ensemble_Learning().Extra_Trees_Classifier(n_estimators=n_estimators) if n_estimators else s_models.Ensemble_Learning().Extra_Trees_Classifier()
                                    case "Extra_Trees_Regressor":
                                        model = s_models.Ensemble_Learning().Extra_Trees_Regressor(n_estimators=n_estimators) if n_estimators else s_models.Ensemble_Learning().Extra_Trees_Regressor()
                                    case "Ada_Boost_Classifier":
                                        if n_estimators and learning_rate :
                                            model = s_models.Ensemble_Learning().Ada_Boost_Classifier(n_estimators=n_estimators,learning_rate=learning_rate)
                                        elif n_estimators :
                                            model = s_models.Ensemble_Learning().Ada_Boost_Classifier(n_estimators=n_estimators)
                                        elif learning_rate :
                                            model = s_models.Ensemble_Learning().Ada_Boost_Classifier(learning_rate=learning_rate)
                                        else :
                                            model = s_models.Ensemble_Learning().Ada_Boost_Classifier(learning_rate=learning_rate)
                                    case "Ada_Boost_Regressor":
                                        if n_estimators and learning_rate :
                                            model = s_models.Ensemble_Learning().Ada_Boost_Regressor(n_estimators=n_estimators,learning_rate=learning_rate)
                                        elif n_estimators :
                                            model = s_models.Ensemble_Learning().Ada_Boost_Regressor(n_estimators=n_estimators)
                                        elif learning_rate :
                                            model = s_models.Ensemble_Learning().Ada_Boost_Regressor(learning_rate=learning_rate)
                                        else :
                                            model = s_models.Ensemble_Learning().Ada_Boost_Regressor(learning_rate=learning_rate)
                                    case "Gradient_Boosting_Classifier":
                                        if n_estimators and learning_rate :
                                            model = s_models.Ensemble_Learning().Gradient_Boosting_Classifier(n_estimators=n_estimators,learning_rate=learning_rate)
                                        elif n_estimators :
                                            model = s_models.Ensemble_Learning().Gradient_Boosting_Classifier(n_estimators=n_estimators)
                                        elif learning_rate :
                                            model = s_models.Ensemble_Learning().Gradient_Boosting_Classifier(learning_rate=learning_rate)
                                        else :
                                            model = s_models.Ensemble_Learning().Gradient_Boosting_Classifier(learning_rate=learning_rate)
                                    case "Gradient_Boosting_Regressor":
                                        if n_estimators and learning_rate :
                                            model = s_models.Ensemble_Learning().Gradient_Boosting_Regressor(n_estimators=n_estimators,learning_rate=learning_rate)
                                        elif n_estimators :
                                            model = s_models.Ensemble_Learning().Gradient_Boosting_Regressor(n_estimators=n_estimators)
                                        elif learning_rate :
                                            model = s_models.Ensemble_Learning().Gradient_Boosting_Regressor(learning_rate=learning_rate)
                                        else :
                                            model = s_models.Ensemble_Learning().Gradient_Boosting_Regressor(learning_rate=learning_rate)
                                    case "LinearSVM":
                                        model = s_models.SVM().LinearSVM()
                                    case "nonLinearSVM_ploy":
                                        if C and gamma :
                                            model = s_models.SVM().nonLinearSVM_ploy(C=C,gamma=gamma)
                                        elif C:
                                            model = s_models.SVM().nonLinearSVM_ploy(C=C,)
                                        elif gamma :
                                            model = s_models.SVM().nonLinearSVM_ploy(gamma=gamma)
                                        else  :
                                            model = s_models.SVM().nonLinearSVM_ploy()

                                    case "nonLinearSVM_rbf":
                                        if C and gamma :
                                            model = s_models.SVM().nonLinearSVM_rbf(C=C,gamma=gamma)
                                        elif C:
                                            model = s_models.SVM().nonLinearSVM_rbf(C=C,)
                                        elif gamma :
                                            model = s_models.SVM().nonLinearSVM_rbf(gamma=gamma)
                                        else  :
                                            model = s_models.SVM().nonLinearSVM_rbf()
                                    case "K_Means":
                                        model = un_s_models.Clusters().K_Means(n_clusters=n_clusters) if n_clusters else un_s_models.Clusters().K_Means()
                                    case "DBSCAN":
                                        model = un_s_models.Clusters().DB_SCAN(eps=eps,min_samples=min_samples)
                                        if eps and min_samples :
                                            model = un_s_models.Clusters().DB_SCAN(eps=eps,min_samples=min_samples)
                                        elif eps:
                                            model = un_s_models.Clusters().DB_SCAN(eps=eps,)
                                        elif min_samples :
                                            model = un_s_models.Clusters().DB_SCAN(min_samples=min_samples)
                                        else  :
                                            model = un_s_models.Clusters().DB_SCAN()
                            return model
                        if parameters_adjust :
                            model = get_model_(name,C=last_parameters_adjustment['C'], alpha=last_parameters_adjustment['alpha'], degree=last_parameters_adjustment['degree'],
                                criterion=last_parameters_adjustment['criterion'], n_estimators=last_parameters_adjustment['n_estimators'], learning_rate=last_parameters_adjustment['learning_rate'],
                                    gamma=last_parameters_adjustment['gamma'], n_clusters=last_parameters_adjustment['n_clusters'], eps=last_parameters_adjustment['eps'], min_samples=last_parameters_adjustment['min_samples'])
                            
                        else :
                            model = get_model_(name,C=added_model_dic['C'], alpha=added_model_dic['alpha'], degree=added_model_dic['degree'],
                                            criterion=added_model_dic['criterion'], n_estimators=added_model_dic['n_estimators'], learning_rate=added_model_dic['learning_rate'],
                                                gamma=added_model_dic['gamma'], n_clusters=added_model_dic['n_clusters'], eps=added_model_dic['eps'], min_samples=added_model_dic['min_samples'])

                    return model
                def get_code(parameters_adjust=False):
                    Grid_Search_code = ""
                    criterion_code=""
                    C_code = ""
                    alpha_code= ""
                    degree_code = ""
                    n_estimators_code = ""
                    learning_rate_code = ""
                    gamma_code = ""
                    n_clusters_code = ""
                    eps_code = ""
                    min_samples_code = ""

                    if parameters_adjust :
                        if  criterion :
                            criterion_code = f"criterion='{last_parameters_adjustment['criterion']}',"
                        if  C :
                            C_code = f"C={last_parameters_adjustment['C']},"
                        if  alpha :
                            alpha_code = f"alpha={last_parameters_adjustment['alpha']},"
                        if  degree :
                            degree_code = f"degree={last_parameters_adjustment['degree']},"
                        if  n_estimators :
                            n_estimators_code = f"n_estimators={last_parameters_adjustment['n_estimators']},"
                        if  learning_rate :
                            learning_rate_code = f"learning_rate={last_parameters_adjustment['learning_rate']},"
                        if  gamma :
                            gamma_code = f"gamma={last_parameters_adjustment['gamma']},"

                        if  n_clusters :
                            n_clusters_code = f"n_clusters={last_parameters_adjustment['n_clusters']},"
                        if  eps :
                            eps_code = f"eps={last_parameters_adjustment['eps']},"
                        if  min_samples :
                            min_samples_code = f"min_samples={last_parameters_adjustment['min_samples']},"
                    else :
                        if  criterion :
                            criterion_code = f"criterion='{added_model_dic['criterion']}',"
                        if  C :
                            C_code = f"C={added_model_dic['C']},"
                        if  alpha :
                            alpha_code = f"alpha={added_model_dic['alpha']},"
                        if  degree :
                            degree_code = f"degree={added_model_dic['degree']},"
                        if  n_estimators :
                            n_estimators_code = f"n_estimators={added_model_dic['n_estimators']},"
                        if  learning_rate :
                            learning_rate_code = f"learning_rate={added_model_dic['learning_rate']},"
                        if  gamma :
                            gamma_code = f"gamma={added_model_dic['gamma']},"

                        if  n_clusters :
                            n_clusters_code = f"n_clusters={added_model_dic['n_clusters']},"
                        if  eps :
                            eps_code = f"eps={added_model_dic['eps']},"
                        if  min_samples :
                            min_samples_code = f"min_samples={added_model_dic['min_samples']},"

                    model_name = import_path.split(" ")[3]
                    model_code = f"model = {model_name}({criterion_code}{C_code}{alpha_code}{degree_code}{n_estimators_code}{learning_rate_code}{gamma_code}{n_clusters_code}{eps_code}{min_samples_code})"
                    return model_code
                def new_model_andmodelCode():
                    self.model = get_model(parameters_adjust)
                    self.model_code = get_code(parameters_adjust)
                    self.code_label.setText(self.model_code)
                    self.model_get_trained = 0

                    self.test_data_score_label.setText(" ")

                    train_button.setEnabled(True)
                    train_button.setCursor(Qt.PointingHandCursor)
                    train_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    train_button.clicked.connect(train_button_f)

                    self.predict_button.setEnabled(False)
                    self.predict_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    self.plot_button.setEnabled(False)
                    self.plot_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    self.save_button.setEnabled(False)
                    self.save_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")

                

                btns_layout = QHBoxLayout();reveal_model_layout.addLayout(btns_layout)
                stacked_layout = QStackedLayout();reveal_model_layout.addLayout(stacked_layout)

                def tab_f(tab=None):
                    if not tab:
                        Tab = self.focusWidget()
                    else:
                        Tab = tab
                    for tab in [btn_1, btn_2]:
                        if tab == Tab:
                            tab.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        else:
                            tab.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
            
                if self.EN :
                    btn_1 = QPushButton("Your Data")
                else :
                    btn_1 = QPushButton("بياناتك")
                btns_layout.addWidget(btn_1)
                btn_1.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                btn_1.setCursor(Qt.PointingHandCursor)
                btn_1.clicked.connect(lambda: stacked_layout.setCurrentIndex(0))

                
                if playground :
                    btn_1.clicked.connect(lambda : tab_f(btn_1))
                    if self.EN :
                        btn_2 = QPushButton("Playground");btns_layout.addWidget(btn_2)
                    else :
                        btn_2 = QPushButton("ساحة اللعب");btns_layout.addWidget(btn_2)
                    btn_2.setStyleSheet("background-color: #555555; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    btn_2.setCursor(Qt.PointingHandCursor)
                    btn_2.clicked.connect(lambda: stacked_layout.setCurrentIndex(1))
                    btn_2.clicked.connect(lambda : tab_f(btn_2))
                # else :
                #     btn_2.setStyleSheet("background-color: #777777; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                #     btn_2.setEnabled(False)
                #     # btn_2.setCursor(Qt.PointingHandCursor)
                #     # btn_2.clicked.connect(lambda: stacked_layout.setCurrentIndex(1))
                #     # btn_2.clicked.connect(lambda : tab_f(btn_2))

                first = QWidget();stacked_layout.addWidget(first)
                first_layout = QHBoxLayout();first.setLayout(first_layout)

                if playground :
                    secand = QWebEngineView();stacked_layout.addWidget(secand)
                    secand.setUrl(QUrl("https://ml-playground.com"))
                # left

                left_sa = QScrollArea()
                widget__L = QWidget()
                left_sa.setWidget(widget__L)
                widget__L_layout = QVBoxLayout()
                widget__L.setLayout(widget__L_layout)
                first_layout.addWidget(left_sa)
                left_sa.setWidgetResizable(True)

                # right
                widget__R_picker = QWidget()
                widget__R_picker_layout = QVBoxLayout()
                widget__R_picker.setLayout(widget__R_picker_layout)
                first_layout.addWidget(widget__R_picker)

                

                model_match = 0

                if True: # R_box1 
                    self.R_box1 = QWidget()
                    self.R_box1.setFixedHeight(230) # edit
                    self.R_box1.setFixedWidth(200)
                    self.R_box1.setStyleSheet("background-color:#444; border-radius:10px")
                    self.R_box1_layout = QVBoxLayout()
                    self.R_box1.setLayout(self.R_box1_layout)
                    widget__R_picker_layout.addWidget(self.R_box1)
                    # Binary:
                    if self.EN :
                        label_bin = QLabel("Binary:")
                    else :
                        label_bin = QLabel("ثنائي الإخراج:")
                    f = QFont("Arial", 17);f.setBold(1)
                    label_bin.setFont(f); self.R_box1_layout.addWidget(label_bin)
                    if self.current_file.bin == binary: label_bin.setStyleSheet('color: #43e882;');model_match=1
                    else: label_bin.setStyleSheet('color: #ff5639;')
                    ##
                    label_bin = QLabel()
                    label_bin.setWordWrap(True)
                    f = QFont("Arial", 13);f.setBold(1)
                    label_bin.setFont(f); self.R_box1_layout.addWidget(label_bin)
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
                    # Classifier:
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
                    label_bin.setFont(f); self.R_box1_layout.addWidget(label_bin)
                    if self.current_file.reg == reg: label_bin.setStyleSheet('color: #43e882;');model_match=1 #green
                    else: label_bin.setStyleSheet('color: #ff5639;');model_match=0 # red
                    ##
                    label_bin = QLabel()
                    label_bin.setWordWrap(True)
                    f = QFont("Arial", 13);f.setBold(1)
                    label_bin.setFont(f); self.R_box1_layout.addWidget(label_bin)
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

                if model_match :
                    if added_model_dic['saved_file_path'] :
                        self.pipeline = get_model(parameters_adjust,True)
                        self.clean_data = clean_data(self.current_file.file_df )
                        self.X = self.clean_data.drop(columns=[self.current_file.file_label])
                        self.y = self.clean_data[self.current_file.file_label]
                    else :
                        self.model = get_model(parameters_adjust)
                self.model_code = get_code(parameters_adjust)
                if True: # R_box2
                    ############
                    self.R_box2 = QWidget()
                    self.R_box2.setFixedHeight(330) # edit
                    self.R_box2.setFixedWidth(200)
                    self.R_box2.setStyleSheet("background-color:#444; border-radius:10px")
                    self.R_box2_layout = QVBoxLayout()
                    self.R_box2.setLayout(self.R_box2_layout)
                    widget__R_picker_layout.addWidget(self.R_box2)
                    widget__R_picker_layout.addStretch()
                    def train_button_f():
                        # dubble
                        self.model_get_trained = 1               
                        test_data_size = float(self.size_combo_box.getOption()) / 100
                        pd_data = self.current_file.file_df
                        # self.X_train, X_test, self.y_train, y_test, self.pipeline = clean_data(pd_data,self.current_file.file_label,test_data_size)
                        
                        self.clean_data = clean_data(pd_data)
                        self.X = self.clean_data.drop(columns=[self.current_file.file_label])
                        self.y = self.clean_data[self.current_file.file_label]

                        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=test_data_size)
                        self.pipeline = get_pipeline(self.X,self.model)

                        if alg_type == "supervised" :
                            self.pipeline.fit(X_train,y_train)
                            self.test_data_score = self.pipeline.score(X_test,y_test)
                            self.test_data_score_label.setText(str(self.test_data_score))
                        elif alg_type == "un_supervised":
                            self.pipeline.fit(X_train)
                            self.test_data_score = "unsupported for UnSupervised models"
                            self.test_data_score_label.setText(str(self.test_data_score))

                        self.predict_button.setEnabled(True)
                        self.predict_button.setCursor(Qt.PointingHandCursor)
                        self.predict_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        # ###
                        self.plot_button.setEnabled(True)
                        self.plot_button.setCursor(Qt.PointingHandCursor)
                        self.plot_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        # ###
                        self.save_button.setEnabled(True)
                        self.save_button.setCursor(Qt.PointingHandCursor)
                        self.save_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")

                        return self.test_data_score
                    # train= QCustomWidgets.ClickableWidget(train_button_f)
                    # train.data_ = "hi"
                    train_layout = QVBoxLayout()
                    # train.setLayout(train_layout)
                    size_and_label_layout = QHBoxLayout();train_layout.addLayout(size_and_label_layout)
                    if self.EN :
                        size_text = QLabel("Test data size (%):")
                    else :
                        size_text = QLabel("حجم بيانات التجريب (%):")
                    size_and_label_layout.addWidget(size_text)
                    self.size_combo_box = QCustomWidgets.DarkComboBox();self.size_combo_box.addItems([str(i) for i in range(5,40,5)]);size_and_label_layout.addWidget(self.size_combo_box)
                    self.size_combo_box.setCurrentText('30')
                    if self.EN :
                        train_button = QPushButton("Train Model")
                    else :
                        train_button = QPushButton("تدريب الخورزمية")
                    if self.model_get_trained or not model_match:train_button.setEnabled(False)

                    # train_button.__model_name__ = name
                    
                    if not self.model_get_trained and model_match:
                        train_button.setCursor(Qt.PointingHandCursor)
                        train_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        train_button.clicked.connect(train_button_f)
                    else :
                        # train_button.setCursor(Qt.PointingHandCursor)
                        train_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    train_layout.addWidget(train_button)
                    

                    test_data_score_layout = QHBoxLayout()
                    if self.EN :
                        test_data_score_text = QLabel("Test dataset score :");test_data_score_layout.addWidget(test_data_score_text)
                    else :
                        test_data_score_text = QLabel("نتيجة بيانات التجريب :");test_data_score_layout.addWidget(test_data_score_text)
                    self.test_data_score_label = QLabel(str(self.test_data_score));test_data_score_layout.addWidget(self.test_data_score_label)
                    train_layout.addLayout(test_data_score_layout)
                    self.R_box2_layout.addLayout(train_layout)
                    def predict_button_f():
                        if self.model_get_trained :
                            self.predict_window = QWidget()
                            self.predict_window_layout = QVBoxLayout()
                            self.predict_window.setLayout(self.predict_window_layout)
                            # self.predict_window.setFixedHeight(500)
                            # self.predict_window.setFixedWidth(800)
                            self.predict_window.setParent(None)
                            self.predict_window.setWindowTitle(fr"DeData Sheets - Predict Window")
                            self.predict_window.show()
                            # self.predict_window.setWidgetResizable(True)
                            grid_layout = QGridLayout()
                            self.predict_window_layout.addLayout(grid_layout)
                            column_dic = {}
                            self.columns = []
                            self.max_columns_per_row = 6
                            pd_data = self.current_file.file_df                    
                            self.clean_data = clean_data(pd_data)

                            numeric_columns = []; nonnumeric_columns = []
                            for column in self.clean_data.columns:
                                if pd.api.types.is_numeric_dtype(self.current_file.file_df[column]):
                                    numeric_columns.append(column)
                                    if len(set(self.current_file.file_df[column])) <= 10:
                                        nonnumeric_columns.append(column)
                                else:nonnumeric_columns.append(column)

                            for i,column in enumerate(self.clean_data.columns):
                                if column != self.current_file.file_label and len(set(self.clean_data[column])) != self.clean_data.shape[0] :
                                    column_widg = QWidget()
                                    column_widg.setFixedHeight(70)
                                    column_widg.setFixedWidth(100)
                                    column_lay = QVBoxLayout();column_widg.setLayout(column_lay)
                                    column_lay.addWidget(QLabel(column))
                                    column_dic[column] = {}
                                    if column in numeric_columns :
                                        column_dic[column]['obj'] = QLineEdit()
                                        column_dic[column]['type'] = 'QLine'
                                    else :
                                        column_dic[column]['obj'] = QComboBox()
                                        column_dic[column]['type'] = 'QCombo'
                                        items = [str(i)  for i  in set(self.clean_data[column]) if str(i) != 'nan']
                                        column_dic[column]['obj'].addItems(items)
                                    column_lay.addWidget(column_dic[column]['obj'])
                                    self.columns.append(column_widg)
                                    row, col = divmod(i, self.max_columns_per_row)
                                    grid_layout.addWidget(column_widg, row, col)

                            predicted_label = QLabel()
                            predicted_label.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                            predicted_proba_label = QLabel()
                            predicted_proba_label.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                            def predict_f(x,proba=False):
                                
                                # data = [[int(x.text()) for x in column_dic.values()]]
                                data = []
                                one_missed = 0
                                for x in column_dic :
                                    if column_dic[x]['type'] == 'QLine' :
                                        if not column_dic[x]['obj'].text() : one_missed = 1 
                                        else : data.append(int(column_dic[x]['obj'].text()))
                                    else :
                                        if not column_dic[x]['obj'].currentText() : one_missed = 1 
                                        else : data.append(str(column_dic[x]['obj'].currentText()))
                                if one_missed :
                                    msg_box = QMessageBox()
                                    msg_box.setStyleSheet('background-color:#333; color:#fff;')
                                    msg_box.setIcon(QMessageBox.Warning)
                                    msg_box.setText("Missing Data!")
                                    msg_box.setWindowTitle("Error")
                                    msg_box.addButton("OK", QMessageBox.AcceptRole)
                                    msg_box.exec_()
                                else :
                                    cl = self.clean_data.columns.to_list()
                                    cl.remove(self.current_file.file_label)
                                    data = pd.DataFrame([data],columns=cl)
                                    # data = self.pipeline.transform(data)
                                    if not proba :
                                        pr = self.pipeline.predict(data)
                                        text = f"Predicted value {pr}" if self.current_file.reg else f"Predicted class {pr}"
                                        predicted_label.setText(text)
                                    else :
                                        pr = self.pipeline.predict_proba(data)
                                        text = f"Classes predictions {pr}"
                                        predicted_proba_label.setText(text)
                            if self.EN :
                                inter_predict_button = QPushButton("Predict")
                            else :
                                inter_predict_button = QPushButton("توقع")
                            self.predict_window_layout.addWidget(inter_predict_button)
                            inter_predict_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                            inter_predict_button.setCursor(Qt.PointingHandCursor)
                            inter_predict_button.clicked.connect(predict_f)
                            self.predict_window_layout.addWidget(predicted_label)

                            if alg_type == "supervised" :
                                if self.EN :
                                    inter_predict_button = QPushButton("Predict Proba")
                                else :
                                    inter_predict_button = QPushButton("توقع الاحتمالات")
                                self.predict_window_layout.addWidget(inter_predict_button)
                                inter_predict_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                                inter_predict_button.setCursor(Qt.PointingHandCursor)
                                inter_predict_button.clicked.connect(lambda x : predict_f(x,True))
                                self.predict_window_layout.addWidget(predicted_proba_label)


                            self.predict_window_layout.addStretch()
                    if self.EN :
                        self.predict_button = QPushButton("Predict")
                    else :
                        self.predict_button = QPushButton("توقع")
                    if not self.model_get_trained:self.predict_button.setEnabled(False)
                    if not model_match:self.predict_button.setEnabled(False)

                    # self.circle_button = self.predict_button
                    self.predict_button.__model_name__ = name
                    self.predict_button.clicked.connect(predict_button_f)
                    if self.model_get_trained and model_match:
                        self.predict_button.setCursor(Qt.PointingHandCursor)
                        self.predict_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    else :
                        # self.predict_button.setCursor(Qt.PointingHandCursor)
                        self.predict_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")



                    self.R_box2_layout.addWidget(self.predict_button)
                    self.R_box2_layout.addStretch()


                    def plot_button_f():
                        if  self.model_get_trained:
                            self.plot_window = QWidget()
                            self.plot_window_layout = QGridLayout()
                            self.plot_window.setLayout(self.plot_window_layout)
                            # self.plot_window.setFixedHeight(500)
                            # self.plot_window.setFixedWidth(800)
                            self.plot_window.setParent(None)
                            self.plot_window.setWindowTitle(fr"DeData - Plot Window")
                            self.plot_window.show()


                            plot_texts = QFont("Arial", 13);plot_texts.setBold(1)
                            # Tree plot
                            # decision boundaries
                            # AUC 
                            # heat map (sensivity,sp..)
                            # clusters knives (silhouette diagram)
                            self.numeric_columns = []; self.nonnumeric_columns = []
                            for column in self.current_file.file_df.columns:
                                if pd.api.types.is_numeric_dtype(self.current_file.file_df[column]):
                                    self.numeric_columns.append(column)
                                else:self.nonnumeric_columns.append(column)
                            if len(self.nonnumeric_columns) == 0 :
                                plot_area1 = QWidget();self.plot_window_layout.addWidget(plot_area1,0,0)
                                plot_area1.setFixedSize(250,310)
                                plot_area1_layout = QVBoxLayout();plot_area1.setLayout(plot_area1_layout)
                                plot_area1_img = QLabel();plot_area1_layout.addWidget(plot_area1_img)
                                plot_area1_img.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\de_bo.png"))
                                plot_area1_img.setAlignment(Qt.AlignCenter)
                                plot_area1_text = QLabel('Decision Boundaries');plot_area1_text.setFont(plot_texts)
                                plot_area1_text.setAlignment(Qt.AlignCenter)
                                plot_area1_layout.addWidget(plot_area1_text)
                                plot_area1_btn = QPushButton("Plot");plot_area1_layout.addWidget(plot_area1_btn)
                                plot_area1_btn.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                                plot_area1_btn.setCursor(Qt.PointingHandCursor)
                                plot_area1_btn.clicked.connect(lambda x : models_plot.Decision_Boundaries(name,clean_data(self.X),self.y,self.model))

                            plot_area2 = QWidget();self.plot_window_layout.addWidget(plot_area2,0,1)
                            plot_area2.setFixedSize(250,310)
                            plot_area2_layout = QVBoxLayout();plot_area2.setLayout(plot_area2_layout)
                            plot_area2_img = QLabel();plot_area2_layout.addWidget(plot_area2_img)
                            plot_area2_img.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\output.png"))
                            plot_area2_img.setAlignment(Qt.AlignCenter)
                            plot_area2_text = QLabel('Confusion Matrix');plot_area2_text.setFont(plot_texts)
                            plot_area2_text.setAlignment(Qt.AlignCenter)
                            plot_area2_layout.addWidget(plot_area2_text)
                            plot_area2_btn = QPushButton("Plot");plot_area2_layout.addWidget(plot_area2_btn)
                            plot_area2_btn.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                            plot_area2_btn.setCursor(Qt.PointingHandCursor)
                            plot_area2_btn.clicked.connect(lambda x : models_plot.confusionMatrix(self.y,self.pipeline.predict(self.X)))

                            plot_area3 = QWidget();self.plot_window_layout.addWidget(plot_area3,0,2)
                            plot_area3.setFixedSize(250,310)
                            plot_area3_layout = QVBoxLayout();plot_area3.setLayout(plot_area3_layout)
                            plot_area3_img = QLabel();plot_area3_layout.addWidget(plot_area3_img)
                            plot_area3_img.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\auc.png"))
                            plot_area3_img.setAlignment(Qt.AlignCenter)
                            plot_area3_text = QLabel('AUC');plot_area3_text.setFont(plot_texts)
                            plot_area3_text.setAlignment(Qt.AlignCenter)
                            plot_area3_layout.addWidget(plot_area3_text)
                            plot_area3_btn = QPushButton("Plot");plot_area3_layout.addWidget(plot_area3_btn)
                            plot_area3_btn.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                            plot_area3_btn.setCursor(Qt.PointingHandCursor)
                            plot_area3_btn.clicked.connect(lambda x : models_plot.AUC(self.y,self.pipeline.predict(self.X)))

                            if family in ['Trees'] :
                                plot_area4 = QWidget();self.plot_window_layout.addWidget(plot_area4,1,0)
                                plot_area4.setFixedSize(250,310)
                                plot_area4_layout = QVBoxLayout();plot_area4.setLayout(plot_area4_layout)
                                plot_area4_img = QLabel();plot_area4_layout.addWidget(plot_area4_img)
                                plot_area4_img.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\tree_plot.png"))
                                plot_area4_img.setAlignment(Qt.AlignCenter)
                                plot_area4_text = QLabel('Tree Plot');plot_area4_text.setFont(plot_texts)
                                plot_area4_text.setAlignment(Qt.AlignCenter)
                                plot_area4_layout.addWidget(plot_area4_text)
                                plot_area4_btn = QPushButton("Plot");plot_area4_layout.addWidget(plot_area4_btn)
                                plot_area4_btn.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                                plot_area4_btn.setCursor(Qt.PointingHandCursor)
                                plot_area4_btn.clicked.connect(lambda x : plot_tree(self.pipeline))
                                
                            if name == "K_Means" :
                                plot_area5 = QWidget();self.plot_window_layout.addWidget(plot_area5,1,1)
                                plot_area5.setFixedSize(250,310)
                                plot_area5_layout = QVBoxLayout();plot_area5.setLayout(plot_area5_layout)
                                plot_area5_img = QLabel();plot_area5_layout.addWidget(plot_area5_img)
                                plot_area5_img.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\silout.png"))
                                plot_area5_img.setAlignment(Qt.AlignCenter)
                                plot_area5_text = QLabel('Silhouette Diagram');plot_area5_text.setFont(plot_texts)
                                plot_area5_text.setAlignment(Qt.AlignCenter)
                                plot_area5_layout.addWidget(plot_area5_text)
                                plot_area5_btn = QPushButton("Plot");plot_area5_layout.addWidget(plot_area5_btn)
                                plot_area5_btn.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                                plot_area5_btn.setCursor(Qt.PointingHandCursor)
                                plot_area5_btn.clicked.connect(lambda x : models_plot.Silhouette_Diagram(self.X,int(n_clusters_comboBox.currentText())))
                                
                            # if ploting:
                            #     # make new model for pca 
                            #     # test_data_size = 0.01
                            #     # pd_data = self.current_file.file_df
                            #     # X_train, X_test, y_train, y_test, self.pipeline = clean_data(pd_data,self.current_file.file_label,test_data_size)
                                
                            #     test_data_size = float(self.size_combo_box.getOption()) / 100
                            #     pd_data = self.current_file.file_df
                            #     # self.X_train, X_test, self.y_train, y_test, self.pipeline = clean_data(pd_data,self.current_file.file_label,test_data_size)
                                
                                
                            #     X = pd_data.drop(columns=[self.current_file.file_label])
                            #     y = pd_data[self.current_file.file_label]

                            #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_data_size)
                            #     pca = PCA(n_components = 2)
                            #     X_train = pca.fit_transform(X_train)
                            #     X_train
                            #     pipeline = get_pipeline(X,self.model)
                            #     self.model.fit(X_train,y_train)

                            #     select_plot(name,X_train,y_train,self.model)
                        
                    if self.EN :
                        self.plot_button = QPushButton("Plot Model")
                    else :
                        self.plot_button = QPushButton("عرض بياني للخورزمية")
                    if not self.model_get_trained:self.plot_button.setEnabled(False)
                    if not model_match:self.plot_button.setEnabled(False)


                    # self.circle_button = self.plot_button
                    self.plot_button.__model_name__ = name
                    self.plot_button.clicked.connect(plot_button_f)

                    if  self.model_get_trained and model_match:
                        self.plot_button.setCursor(Qt.PointingHandCursor)
                        self.plot_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    else :
                        # self.plot_button.setCursor(Qt.PointingHandCursor)
                        self.plot_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    self.R_box2_layout.addWidget(self.plot_button)
                    self.R_box2_layout.addStretch()

                    def save_button_f():
                        if  self.model_get_trained:
                            added_model_dic['saved_file_path'] = 1
                            def generate_next_filename(base_filename, extension, folder_path):
                                if not os.path.exists(folder_path):
                                    os.makedirs(folder_path)

                                existing_files = [f for f in os.listdir(folder_path) if f.startswith(base_filename) and f.endswith(extension)]
                                if existing_files:
                                    latest_file = max(existing_files, key=lambda f: int(f[len(base_filename):-len(extension) - 1]))
                                    last_number = int(latest_file[len(base_filename):-len(extension) - 1])
                                    next_number = last_number + 1
                                else:
                                    next_number = 1
                                next_filename = os.path.join(folder_path, f"{base_filename}{next_number}.{extension}")
                                return next_filename

                            base_name = name + str(added_model_dic['id']) + "_"
                            file_extension = "sav"
                            folder_name = "saved_models"

                            file = generate_next_filename(base_name, file_extension, folder_name)

                            to_pickle = [self.pipeline,self.test_data_score]
                            pickle.dump(to_pickle, open(file, 'wb'))
                            
                            cur = self.db.cursor()
                            cur.execute(f"UPDATE added_models set saved_file_path = 1 WHERE id = {added_model_dic['id']}")
                            for k in to_updata.keys() :
                                cur.execute(f"UPDATE added_models set {k} = '{to_updata[k]}' WHERE id = {added_model_dic['id']}")
                                added_model_dic[k] = to_updata[k]
                            self.db.commit()
                            cur.close()
                            # self.widget__.hide()

                    if self.EN :
                        self.save_button = QPushButton("Save Model")
                    else :
                        self.save_button = QPushButton("حفظ الخورزمية")
                    if not self.model_get_trained:self.save_button.setEnabled(False)
                    if not model_match:self.save_button.setEnabled(False)

                    # self.circle_button = self.save_button
                    self.save_button.__model_name__ = name
                    self.save_button.clicked.connect(save_button_f)
                    if  self.model_get_trained and model_match:
                        self.save_button.setCursor(Qt.PointingHandCursor)
                        self.save_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                    else :
                        # self.save_button.setCursor(Qt.PointingHandCursor)
                        self.save_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")

                    self.R_box2_layout.addWidget(self.save_button)
                    self.R_box2_layout.addStretch()


                    cur = self.db.cursor()
                    cur.execute(f"SELECT saved_file_path FROM added_models WHERE id = '{added_model_dic['id']}'")
                    saved_file_path = cur.fetchone()[0]
                    cur.close()
                    if saved_file_path :
                        def get_last_filename(base_filename, extension, folder_path):
                            existing_files = [f for f in os.listdir(folder_path) if f.startswith(base_filename) and f.endswith(extension)]
                            latest_file = max(existing_files, key=lambda f: int(f[len(base_filename):-len(extension) - 1]))
                            last_number = int(latest_file[len(base_filename):-len(extension) - 1])
                            next_filename = os.path.join(folder_path, f"{base_filename}{last_number}.{extension}")
                            return next_filename

                        base_name = name + str(added_model_dic['id']) + "_"
                        file_extension = "sav"
                        folder_name = "saved_models"
                        file = get_last_filename(base_name, file_extension, folder_name)
                        from_pickle = pickle.load(open(file, 'rb'))

                        self.test_data_score_label.setText(str(from_pickle[1]))

                        train_button.setEnabled(False)
                        train_button.setCursor(Qt.PointingHandCursor)
                        train_button.setStyleSheet("background-color: #555555; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        train_button.clicked.connect(train_button_f)

                        self.predict_button.setEnabled(True)
                        self.predict_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        self.predict_button.setCursor(Qt.PointingHandCursor)
                        self.plot_button.setEnabled(True)
                        self.plot_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        self.plot_button.setCursor(Qt.PointingHandCursor)
                        self.save_button.setEnabled(True)
                        self.save_button.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                        self.save_button.setCursor(Qt.PointingHandCursor)

                    ############
                ####### Parameters start

                # self.test_data_score_label.setText(str(self.test_data_score))

                one_at_least = 0
                if True: # adding Parameters
                    para_font = QFont("Arial", 19);para_font.setBold(1)
                    child_font = QFont("Arial", 15);child_font.setBold(1)
                    if added_model_dic['criterion']:
                        if not one_at_least :
                            if self.EN :
                                Parameters_label = QLabel("Current Parameters :")
                            else :
                                Parameters_label = QLabel("المتغيرات الحالية :")
                            Parameters_label.setFont(para_font)
                            widget__L_layout.addWidget(Parameters_label)
                        one_at_least+=1
                        criterion_label = QLabel("criterion")
                        criterion_label.setFont(child_font)
                        widget__L_layout.addWidget(criterion_label)
                        criterion_comboBox = QComboBox()
                        criterion_comboBox.addItems(['gini', 'entropy'])
                        criterion_comboBox.setCurrentText(str(added_model_dic['criterion']))
                        parameters_adjust = 1
                        criterion_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('criterion',X) )
                        criterion_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                        criterion_layout = QHBoxLayout()
                        criterion_layout.addWidget(criterion_label)
                        criterion_layout.addWidget(criterion_comboBox)
                        widget__L_layout.addLayout(criterion_layout)
                    if added_model_dic['alpha']:
                        if not one_at_least :
                            if self.EN :
                                Parameters_label = QLabel("Current Parameters :")
                            else :
                                Parameters_label = QLabel("المتغيرات الحالية :")
                            Parameters_label.setFont(para_font)
                            widget__L_layout.addWidget(Parameters_label)
                        one_at_least+=1
                        alpha_label = QLabel("alpha")
                        alpha_label.setFont(child_font)
                        widget__L_layout.addWidget(alpha_label)
                        alpha_comboBox = QComboBox()
                        alpha_comboBox.addItems([str(int(i/10)) if i in [0,10] else str(i/10) for i in range(11)])
                        alpha_comboBox.setCurrentText(str(added_model_dic['alpha']))
                        # alpha_comboBox.setCurrentIndex(4)
                        parameters_adjust = 1
                        alpha_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('alpha',X) )
                        alpha_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                        alpha_layout = QHBoxLayout()
                        alpha_layout.addWidget(alpha_label)
                        alpha_layout.addWidget(alpha_comboBox)
                        widget__L_layout.addLayout(alpha_layout)
                    if added_model_dic['C']:
                        if not one_at_least :
                            if self.EN :
                                Parameters_label = QLabel("Current Parameters :")
                            else :
                                Parameters_label = QLabel("المتغيرات الحالية :")
                            Parameters_label.setFont(para_font)
                            widget__L_layout.addWidget(Parameters_label)
                        one_at_least+=1
                        C_label = QLabel("C")
                        C_label.setFont(child_font)
                        widget__L_layout.addWidget(C_label)
                        C_comboBox = QComboBox()
                        C_comboBox.addItems(['0.001', '0.01', '0.1', '1', '10', '100'])
                        C_comboBox.setCurrentText(str(added_model_dic['C']))
                        parameters_adjust = 1
                        C_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('C',X) )
                        C_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())

                        C_layout = QHBoxLayout()
                        C_layout.addWidget(C_label)
                        C_layout.addWidget(C_comboBox)
                        widget__L_layout.addLayout(C_layout)
                    if added_model_dic['degree']:
                        if not one_at_least :
                            if self.EN :
                                Parameters_label = QLabel("Current Parameters :")
                            else :
                                Parameters_label = QLabel("المتغيرات الحالية :")
                            Parameters_label.setFont(para_font)
                            widget__L_layout.addWidget(Parameters_label)
                        one_at_least+=1
                        degree_label = QLabel("degree")
                        degree_label.setFont(child_font)
                        widget__L_layout.addWidget(degree_label)
                        degree_comboBox = QComboBox()
                        degree_comboBox.addItems(['1', '2', '3', '4', '5'])
                        degree_comboBox.setCurrentText(str(added_model_dic['degree']))
                        parameters_adjust = 1
                        degree_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('degree',X) )
                        degree_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())

                        degree_layout = QHBoxLayout()
                        degree_layout.addWidget(degree_label)
                        degree_layout.addWidget(degree_comboBox)
                        widget__L_layout.addLayout(degree_layout)
                    if added_model_dic['n_estimators']:
                        if not one_at_least :
                            if self.EN :
                                Parameters_label = QLabel("Current Parameters :")
                            else :
                                Parameters_label = QLabel("المتغيرات الحالية :")
                            Parameters_label.setFont(para_font)
                            widget__L_layout.addWidget(Parameters_label)
                        one_at_least+=1
                        n_estimators_label = QLabel("n_estimators")
                        n_estimators_label.setFont(child_font)
                        widget__L_layout.addWidget(n_estimators_label)
                        n_estimators_comboBox = QComboBox()
                        n_estimators_comboBox.addItems(['1', '10', '30', '50',
                                            '70', '100', '120', '150', '200', '500'])
                        n_estimators_comboBox.setCurrentText(str(added_model_dic['n_estimators']))
                        parameters_adjust = 1
                        n_estimators_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('n_estimators',X) )
                        n_estimators_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())

                        n_estimators_layout = QHBoxLayout()
                        n_estimators_layout.addWidget(n_estimators_label)
                        n_estimators_layout.addWidget(n_estimators_comboBox)
                        widget__L_layout.addLayout(n_estimators_layout)
                    if added_model_dic['learning_rate']:
                        if not one_at_least :
                            if self.EN :
                                Parameters_label = QLabel("Current Parameters :")
                            else :
                                Parameters_label = QLabel("المتغيرات الحالية :")
                            Parameters_label.setFont(para_font)
                            widget__L_layout.addWidget(Parameters_label)
                        one_at_least+=1
                        learning_rate_label = QLabel("learning_rate")
                        learning_rate_label.setFont(child_font)
                        widget__L_layout.addWidget(learning_rate_label)
                        learning_rate_comboBox = QComboBox()
                        learning_rate_comboBox.addItems([str(int(i/10)) if i in [0,10] else str(i/10) for i in range(11)])
                        learning_rate_comboBox.setCurrentText(str(added_model_dic['learning_rate']))
                        parameters_adjust = 1
                        learning_rate_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('learning_rate',X) )
                        learning_rate_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                        learning_rate_layout = QHBoxLayout()
                        learning_rate_layout.addWidget(learning_rate_label)
                        learning_rate_layout.addWidget(learning_rate_comboBox)
                        widget__L_layout.addLayout(learning_rate_layout)
                    if added_model_dic['gamma']:
                        if not one_at_least :
                            if self.EN :
                                Parameters_label = QLabel("Current Parameters :")
                            else :
                                Parameters_label = QLabel("المتغيرات الحالية :")
                            Parameters_label.setFont(para_font)
                            widget__L_layout.addWidget(Parameters_label)
                        one_at_least+=1
                        gamma_label = QLabel("gamma")
                        gamma_label.setFont(child_font)
                        widget__L_layout.addWidget(gamma_label)
                        gamma_comboBox = QComboBox()
                        gamma_comboBox.addItems(['1', '0.1', '0.01', '0.001', '0.0001', 'auto'])
                        gamma_comboBox.setCurrentText(str(added_model_dic['gamma']))
                        parameters_adjust = 1
                        gamma_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('gamma',X) )
                        gamma_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                        gamma_layout = QHBoxLayout()
                        gamma_layout.addWidget(gamma_label)
                        gamma_layout.addWidget(gamma_comboBox)
                        widget__L_layout.addLayout(gamma_layout)
                    if added_model_dic['n_clusters']:
                        if not one_at_least :
                            if self.EN :
                                Parameters_label = QLabel("Current Parameters :")
                            else :
                                Parameters_label = QLabel("المتغيرات الحالية :")
                            Parameters_label.setFont(para_font)
                            widget__L_layout.addWidget(Parameters_label)
                        one_at_least+=1
                        n_clusters_label = QLabel("n_clusters")
                        n_clusters_label.setFont(child_font)
                        widget__L_layout.addWidget(n_clusters_label)
                        n_clusters_comboBox = QComboBox()
                        n_clusters_comboBox.addItems([str(i) for i in range(1,11)])
                        n_clusters_comboBox.setCurrentText(str(added_model_dic['n_clusters']))
                        parameters_adjust = 1
                        n_clusters_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('n_clusters',X) )
                        n_clusters_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                        n_clusters_layout = QHBoxLayout()
                        n_clusters_layout.addWidget(n_clusters_label)
                        n_clusters_layout.addWidget(n_clusters_comboBox)
                        widget__L_layout.addLayout(n_clusters_layout)
                    if added_model_dic['eps']:
                        if not one_at_least :
                            if self.EN :
                                Parameters_label = QLabel("Current Parameters :")
                            else :
                                Parameters_label = QLabel("المتغيرات الحالية :")
                            Parameters_label.setFont(para_font)
                            widget__L_layout.addWidget(Parameters_label)
                        one_at_least+=1
                        eps_label = QLabel("eps")
                        eps_label.setFont(child_font)
                        widget__L_layout.addWidget(eps_label)
                        eps_comboBox = QComboBox()
                        eps_comboBox.addItems([str(int(i/10)) if i in [0,10] else str(i/10) for i in range(11)])
                        eps_comboBox.setCurrentText(str(added_model_dic['eps']))
                        parameters_adjust = 1
                        eps_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('eps',X) )
                        eps_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                        eps_layout = QHBoxLayout()
                        eps_layout.addWidget(eps_label)
                        eps_layout.addWidget(eps_comboBox)
                        widget__L_layout.addLayout(eps_layout)
                    if added_model_dic['min_samples']:
                        if not one_at_least :
                            if self.EN :
                                Parameters_label = QLabel("Current Parameters :")
                            else :
                                Parameters_label = QLabel("المتغيرات الحالية :")
                            Parameters_label.setFont(para_font)
                            widget__L_layout.addWidget(Parameters_label)
                        one_at_least+=1
                        min_samples_label = QLabel("min_samples")
                        min_samples_label.setFont(child_font)
                        widget__L_layout.addWidget(min_samples_label)
                        min_samples_comboBox = QComboBox()
                        min_samples_comboBox.addItems([str(i) for i in range(10)])
                        min_samples_comboBox.setCurrentText(str(added_model_dic['min_samples']))
                        parameters_adjust = 1
                        min_samples_comboBox.currentTextChanged.connect( lambda X: parameters_adjust_fn('min_samples',X) )
                        min_samples_comboBox.currentTextChanged.connect( lambda : new_model_andmodelCode())
                        min_samples_layout = QHBoxLayout()
                        min_samples_layout.addWidget(min_samples_label)
                        min_samples_layout.addWidget(min_samples_comboBox)
                        widget__L_layout.addLayout(min_samples_layout)
                
                code_widget  = QWidget()
                # code_widget.setFixedHeight(100) # edit
                # code_widget.setFixedWidth(250)
                code_widget.setStyleSheet("background-color:#444; border-radius:7px")
                code_layout = QVBoxLayout()
                code_widget.setLayout(code_layout)
                import_code = QLabel(import_path);import_code.setFont(QFont("Arial", 10));code_layout.addWidget(import_code)
                self.code_label = QLabel(self.model_code);self.code_label.setFont(QFont("Arial", 10));code_layout.addWidget(self.code_label)
                widget__L_layout.addWidget(code_widget)
                # label_1:
                label_1 = QLabel(name.replace("_", " ")+":")
                f = QFont("Arial", 19);f.setBold(1)
                label_1.setFont(f)
                widget__L_layout.addWidget(label_1)
                # Bio
                Bio = QLabel()
                Bio.setWordWrap(1)
                Bio.setFont(QFont("Arial", 12))
                # widget__.setStyleSheet("background-color: #333;")
                Bio.setStyleSheet("background-color: #333; border-color:#333; border-width:2px; border-style:solid;")
                if self.EN :
                    Bio.setText(bio)
                else :
                    Bio.setText(bio_ar)
                widget__L_layout.addWidget(Bio)
                self.widget__.show()
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
                params.setFont(f)
                widget__L_layout.addWidget(params)
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
                
            self.all_models[id] = {}
            self.all_models[id]['data_set'] = added_model[-1]
            self.all_models[id]['model_container'] = QCustomWidgets.ClickableWidget(reveal_model)
            self.all_models[id]['model_container'].data_ = [model,added_model[0]] # ids
            self.all_models[id]['model_container'].setFixedWidth(260)
            model_container_layout = QVBoxLayout()
            self.all_models[id]['model_container'].setLayout(model_container_layout)
            self.all_models[id]['model_container'].setFixedHeight(260)
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


            # self.model_container_layout.addWidget(self.all_models[id]['model_container'],row,col)

        def choose_certian_models(e):
            # to_remove = []
            to_add = []
            for model_id in self.all_models.keys() : 
                if self.all_models[model_id]['data_set'] == self.file_combo.getOption() :
                    # self.model_container_layout.removeWidget(self.all_models[model_id]['model_container'])
                    # to_remove.append(self.all_models[model_id]['model_container'])
                    to_add.append(self.all_models[model_id]['model_container'])
            for model_id in self.all_models.keys() : 
                self.model_container_layout.removeWidget(self.all_models[model_id]['model_container'])
                self.all_models[model_id]['model_container'].hide()

            # del self.model_container_layout
            # del self.model_container
            # self.model_container = QWidget()
            # self.model_container_layout = QGridLayout()
            # self.model_container.setLayout(self.model_container_layout)
            # self.un_s_models_sb_layout.addWidget(self.model_container)
            for i,m in enumerate(to_add) :
                row, col = divmod(i, 4)
                self.model_container_layout.addWidget(m,row,col)
                m.show()
        choose_certian_models(0)
        self.choose_certian_models = choose_certian_models
        self.file_combo.activated.connect(choose_certian_models)
        if self.models :
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
                        self.un_labeled_file.emit()
        self.file_combo.activated.connect(check_fun)

        self.file_combo.fun1 = file_combo_f
        self.file_combo.fun2 = check_fun
        self.file_combo.fun3 = choose_certian_models

        layout = QVBoxLayout()  # Add a layout to center the button
        layout.addLayout(self.un_s_models_layout)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
