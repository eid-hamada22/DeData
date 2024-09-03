from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.QtCore as QtCore
import sqlite3 as sql
import requests
import os
import QCustomWidgets
import QTools
import pandas as pd


class Import_Data(QWidget):
    file_added = pyqtSignal()
    label_changed = pyqtSignal(str)
    def connect_database(self):
        self.db = sql.connect('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\database.sqlite3')
    label_combos = {}
    
    def label_updated(self,label_id,label_name):
        self.label_combos[str(label_id)].setCurrentText(label_name)
    def insert_dir_in_project_files(self, dir_,project_id, file_full_path=None):
        self.connect_database()
        if 'nothing_to_show_2' in dir(
            self): self.nothing_to_show_2.setParent(None)
        file_id = dir_[:dir_.find(".")]
        if not file_full_path:
            cur = self.db.cursor()
            cur.execute(
                "SELECT file_full_path FROM files WHERE file_id=?", (file_id,))
            file_full_path = cur.fetchall()[0][0]; cur.close()

        def start_file(e):
            os.startfile(
                f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\projects\\{project_id}\\{self.focusWidget().path_}")
        label_widget = QWidget()
        label_layout = QHBoxLayout()
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_widget.setLayout(label_layout)
        label = QPushButton(file_full_path)
        label_layout.addWidget(label)
        # label.setFixedWidth(600)
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
            if len_ >= 20 and pd.api.types.is_numeric_dtype(
                column_data): reg = 1
            cur.execute("UPDATE files SET label = ?, reg = ?, binary = ? WHERE file_id=?",
                        (label, reg, bin, combo.file_id))
            self.db.commit()
            cur.close()
            self.label_changed.emit(combo.file_full_path)
        
        self.label_combos[file_id] = QCustomWidgets.DarkComboBox()
        perc = int(label_widget.width() * 0.3)
        self.label_combos[file_id].setFixedWidth(perc)
        self.label_combos[file_id].label_combo_f = label_combo_f
        cur = self.db.cursor()
        cur.execute("SELECT label,header FROM files WHERE file_id = ?", (file_id,))
        label,header = cur.fetchone()
        cur.close()
        label_list = list(QTools.read_file(
            f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\projects\\{project_id}\\{dir_}").columns)
        if not label :
            List = ['None'] + label_list
        else :
            List =  label_list
        self.label_combos[file_id].setItems(List)
        self.label_combos[file_id].setCurrentIndex(List.index(label.__str__()))
        self.label_combos[file_id].path_ = f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\projects\\{project_id}\\{dir_}"
        self.label_combos[file_id].file_id = file_id
        self.label_combos[file_id].file_full_path = file_full_path
        self.label_combos[file_id].activated.connect(self.label_combos[file_id].label_combo_f)
        label_layout.addWidget(self.label_combos[file_id])
        self.project_files_layout.insertWidget(0, label_widget)
        for f_c in self.file_combos :
            f_c.addItem(file_full_path,0)
        self.file_added.emit()


    def insert_file_in_project(self, file_full_path, project_id, url=False, header=True):
        try:
            if not url:
                f = open(file_full_path, 'rb')
                data = f.read(); f.close()
            else:
                response = requests.get(file_full_path)
                data = response.content
                response.close()
            cur = self.db.cursor()
            if header:
                cur.execute("INSERT INTO files (file_full_path, project_id) VALUES(?, ?)", (file_full_path, project_id))
            else :
                cur.execute("INSERT INTO files (file_full_path, project_id, header) VALUES(?, ?, ?)", (file_full_path, project_id, 0))
            file_id = cur.lastrowid
            self.db.commit()
            cur.close()
            file = open(f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\projects\\{project_id}\\{file_id}.{file_full_path.split('.')[-1]}", 'wb')
            file.write(data)
            file.close()

            self.insert_dir_in_project_files(f"{file_id}.{file_full_path.split('.')[-1]}",project_id, file_full_path)
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
        self.connect_database()
        dirs = os.listdir(f"C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\projects\\{id_}")
        if dirs:
            cur = self.db.cursor()
            cur.execute(f"SELECT file_id,file_full_path FROM files WHERE project_id={self.project_id}")
            data = cur.fetchall()
            files_ids = [int(i[0]) for i in data]
            files_extensions = [i[1].split('.')[-1] for i in data]
            cur.close()
            for dir_ in dirs:
                file_id = dir_[:dir_.find(".")]
                if int(file_id) in files_ids :
                    index = files_ids.index(int(file_id))
                    if files_extensions[index] == dir_.split('.')[-1]:
                        self.insert_dir_in_project_files(dir_,id_)
                # TODO
                # else :
                #     os.remove()
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
    
    def __init__(self, id_,file_combos):
        super().__init__()
        # Import Data:
        self.id_layout = QVBoxLayout()
        self.project_id = id_
        self.file_combos = file_combos
        def import_1_f(e):
            file_path, _ = QFileDialog.getOpenFileName(
                None, "Open File", "", "All Files (*)")
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
        self.import_1_input.setPlaceholderText(
            r"C:\Directory\Datasets\file_data.csv")
        self.import_1_input.setStyleSheet(
            "background-color: #222; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")

        import_2 = QLabel("Import file from the cloud:")
        import_2.setStyleSheet("color: #fff; font-size: 16px;")

        self.import_2_input = QLineEdit()
        self.import_2_input.setPlaceholderText(
            r"https://www.example.com/file_data.csv")
        self.import_2_input.setStyleSheet(
            "background-color: #222; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")

        first_row_check = QWidget()
        first_row_check_layout = QHBoxLayout();first_row_check.setLayout(first_row_check_layout)
        check_box = QCheckBox();first_row_check_layout.addWidget(check_box)
        check_box.setChecked(True)
        # TODO check_box.setsize
        check_label = QLabel("The First Row Is the columns names.");first_row_check_layout.addWidget(check_label)
        check_label.setFont(QFont('arial', 12))
        first_row_check_layout.addStretch()
        # ############################
        def import_button_f():
            if self.import_1_input.text():
                self.insert_file_in_project(self.import_1_input.text(), id_,header=check_box.isChecked())
                self.import_1_input.setText('')
            if self.import_2_input.text():
                self.insert_file_in_project(
                    self.import_2_input.text(), id_, url=True,header=check_box.isChecked())
                self.import_2_input.setText('')
            check_box.setChecked(True)
        import_button = QPushButton("Import File")
        import_button.setStyleSheet(
            "background-color: #007ACC; color: #fff; font-size: 16px; border-radius: 5px; padding: 10px 16px;")
        import_button.setCursor(QtCore.Qt.PointingHandCursor)
        import_button.clicked.connect(import_button_f)
        # ############################



        file_and_combo = QWidget()
        file_and_combo_layout = QHBoxLayout()
        file_and_combo.setLayout(file_and_combo_layout)
        files_in_use_label = QLabel("Files in use:");file_and_combo_layout.addWidget(files_in_use_label)
        files_in_use_label.setStyleSheet("color: #fff; font-size: 24px;")
        files_in_use_label.setAlignment(Qt.AlignLeft )

        combo_label = QLabel("Data label:");file_and_combo_layout.addWidget(combo_label)
        combo_label.setStyleSheet("color: #fff; font-size: 24px;")
        combo_label.setAlignment(Qt.AlignRight )
        file_and_combo_layout.addSpacing(95)

        self.project_files_scrollarea = QScrollArea()
        self.project_files_scrollarea.setStyleSheet(
            "background-color: #222; color: #fff; font-size: 14px;border-radius: 8px;")
        self.project_files_widget = QWidget()
        self.project_files_layout = QVBoxLayout()
        self.project_files_layout.addStretch()
        self.project_files_scrollarea.setWidget(self.project_files_widget)
        self.project_files_widget.setLayout(self.project_files_layout)
        self.project_files_scrollarea.setWidgetResizable(True)
        self.seek_files_in_project(id_)

        demo_files_label = QLabel("Demo DataSets:")
        demo_files_label.setStyleSheet("color: #fff; font-size: 24px;")

        self.demo_files_scrollarea = QScrollArea()
        self.demo_files_scrollarea.setStyleSheet(
            "background-color: #222; color: #fff; font-size: 14px;border-radius: 8px;")
        self.demo_files_widget = QWidget()
        self.demo_files_layout = QVBoxLayout()
        self.demo_files_scrollarea.setWidget(self.demo_files_widget)
        self.demo_files_widget.setLayout(self.demo_files_layout)
        self.demo_files_scrollarea.setWidgetResizable(True)

        cur = self.db.cursor()
        cur.execute(f"SELECT * FROM demo_datasets")
        data = cur.fetchall()



        demo_datasets = [[i[1],i[2]] for i in data] # name,label
        for dataset in demo_datasets:
        # adding demo_datasets to comoboxs
            for c_b in self.file_combos :
                c_b.addItem(dataset[0],1)

            label_widget = QWidget()
            label_layout = QHBoxLayout()
            label_layout.setContentsMargins(0, 0, 0, 0)
            label_widget.setLayout(label_layout)
            label = QPushButton(dataset[0])
            label_layout.addWidget(label)
            # label.setFixedWidth(600)
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

            label.setFont(QFont('arial', 15))


            label_combo = QLabel(dataset[1])
            label_combo.setStyleSheet("""
                background-color:#333; color:#fff;
                text-align:left; border-radius:5px;
                padding:5px;
                border-width:1px;
                border-color: #555;
                border-style: solid;
            """)

            perc = int(label_widget.width() * 0.3)
            label_combo.setFixedWidth(perc)
            label_combo.setFixedHeight(30)
            label_layout.addWidget(label_combo)

            self.demo_files_layout.addWidget(label_widget)
        # self.seek_files_in_demo(id_)
        self.demo_files_layout.addStretch()


        def change_lang(EN):
            if EN :
                import_1.setText("Import file from your local machine:")
                # import_1.setAlignment(Qt.AlignLeft)
                import_2.setText("Import file from the cloud:")
                import_2.setAlignment(Qt.AlignLeft)
                check_label.setText("The First Row Is the columns names.")
                check_label.setAlignment(Qt.AlignLeft)
                import_button.setText("Import File")
                # import_button.setAlignment(Qt.AlignLeft)
                files_in_use_label.setText("Files in use:")
                files_in_use_label.setAlignment(Qt.AlignLeft)
                combo_label.setText("Data label:")
                # combo_label.setAlignment(Qt.AlignLeft)
                demo_files_label.setText("Demo DataSets:")
                demo_files_label.setAlignment(Qt.AlignLeft)
            else :
                import_1.setText("تحميل ملف من الجهاز:")
                # import_1.setAlignment(Qt.AlignRight)
                import_2.setText("تحميل ملف من الانترنت:")
                import_2.setAlignment(Qt.AlignRight)
                check_label.setText("الحقل الاول هو اسماء الاعمدة")
                check_label.setAlignment(Qt.AlignRight)
                import_button.setText("تحميل ملف")
                # import_button.setAlignment(Qt.AlignRight)
                files_in_use_label.setText("ملفات قيد الاستخدام:")
                files_in_use_label.setAlignment(Qt.AlignRight)
                combo_label.setText(" ")
                # combo_label.setAlignment(Qt.AlignRight)
                demo_files_label.setText("ملفات تجريبية:")
                demo_files_label.setAlignment(Qt.AlignRight)
        self.change_lang = change_lang
        for element in [import_1, self.import_1_input, import_2, self.import_2_input, first_row_check, import_button, file_and_combo, self.project_files_scrollarea, demo_files_label,self.demo_files_scrollarea]:
            if element == 0:
                self.id_layout.addStretch()
            else:
                # Add a layout to center the button
                self.id_layout.addWidget(element)        
                layout = QVBoxLayout()
        layout.addLayout(self.id_layout)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
