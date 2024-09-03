from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import QCustomWidgets
import QTools, QPloting
import sqlite3 as sql
from demo_fils import get_df
class Data_Visualization(QWidget):
    def connect_database(self):
        self.db = sql.connect('C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\database.sqlite3')
    label_changed = pyqtSignal(int,str)
    
    def label_updated(self,full_path):
        # file_full_path = self.file_combo.getOption()
        extension = full_path.split('.')[-1]
        cur = self.db.cursor()
        cur.execute(
            "SELECT file_id, label, header FROM files WHERE file_full_path = ? AND project_id = ?", (full_path, self.project_id))

        file_id, label, header = cur.fetchone()
        cur.close()
        path = fr"Database\archive\projects\{self.project_id}\{file_id}.{extension}"
        if header or not header:
            df = QTools.read_file(path)
        # else:
        #     df = QTools.read_file(path)
        #     import pandas as pd
        #     pd.read_csv('',header=)
        self.sheet.load_pandas_dataframe(
    df, label, file_path=path, file_id=file_id,headers_ex=header)

    def __init__(self, id_,file_combo):
        super().__init__()
        self.project_id = id_
        self.connect_database()
        self.file_combo = file_combo
        self.dv_layout = QVBoxLayout()
        self.dv_scrollarea = QScrollArea()
        self.dv_sa_widget = QWidget()
        self.dv_sa_layout = QVBoxLayout()
        self.dv_scrollarea.setWidget(self.dv_sa_widget)
        self.dv_sa_widget.setLayout(self.dv_sa_layout)
        self.dv_scrollarea.setWidgetResizable(True)
        self.dv_layout.addWidget(self.dv_scrollarea)
        self.dv_scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        # ####
        
        self.dv_sa_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        set_file_label = QLabel("Load a file to the workbench:")
        set_file_label.setStyleSheet("color: #fff; font-size: 16px;")
        self.dv_sa_layout.addWidget(set_file_label)
        self.dv_sa_layout.addWidget(self.file_combo)

        def file_combo_f(e):
            file_full_path = self.file_combo.getOption()
            cur = self.db.cursor()
            cur.execute(f"SELECT name FROM demo_datasets")
            data = cur.fetchall()
            data = [i[0]  for i in data]
            if file_full_path in data :
                df,label = get_df(file_full_path)
                path = None
                file_id = None
                header = 1
                self.sheet.load_pandas_dataframe(
                    df, label, file_path=path, file_id=file_id,headers_ex=header)
            else :
                extension = file_full_path.split('.')[-1]
                cur = self.db.cursor()
                cur.execute(
                    "SELECT file_id, label, header FROM files WHERE file_full_path = ? AND project_id = ?", (file_full_path, id_))

                file_id, label, header = cur.fetchone()
                cur.close()
                path = fr"Database\archive\projects\{id_}\{file_id}.{extension}"
                if header or not header:
                    df = QTools.read_file(path)
                # else:
                #     df = QTools.read_file(path)
                #     import pandas as pd
                #     pd.read_csv('',header=)

                self.sheet.load_pandas_dataframe(
                    df, label, file_path=path, file_id=file_id,headers_ex=header)
        self.file_combo.activated.connect(file_combo_f)
        self.file_combo.setSizePolicy(self.dv_sa_widget.sizePolicy())
        # Sheet:
        self.sheet_place = QWidget()
        self.sheet_place.setMaximumHeight(300)
        self.sheet_place.setStyleSheet(
            "border-radius:10px; background-color:#000; background-image:url(C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\archive\\static\\img\\sheet.png); background-repeat:no-repeat; background-position: center;")
        self.sheet_place_layout = QVBoxLayout()
        self.sheet_place_layout.setContentsMargins(1, 1, 1, 1)
        self.sheet_place.setLayout(self.sheet_place_layout)
        self.sheet = QCustomWidgets.QSheet()
        self.sheet.mainclass = self
        self.sheet.setMinimumHeight(300)
        self.sheet_place_layout.addWidget(self.sheet)
        self.dv_sa_layout.addWidget(self.sheet_place)

        def retrive_sheet_button_f(e):
            self.retrive_sheet_button.setParent(None)
            self.sheet.show()
            self.sheet_place_layout.addWidget(self.sheet)
        self.retrive_sheet_button = QPushButton("Retrive Sheet")
        self.retrive_sheet_button.clicked.connect(retrive_sheet_button_f)
        self.retrive_sheet_button.setStyleSheet(
            "background-color: #007ACC; color: #fff; font-size: 14px; border-radius: 5px; padding: 10px 15px;")
        


        self.dv_sa_layout.addSpacing(20)
        plot_titel = QLabel("Plot your Dataset :")
        plot_titel.setFont(QFont('arial', 20))
        plot_titel.setAlignment(Qt.AlignCenter)
        self.dv_sa_layout.addWidget(plot_titel)
        self.dv_sa_layout.addSpacing(20)

        plot_widget = QWidget()
        plot_items_sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        plot_widget.setSizePolicy(plot_items_sizePolicy)

        plot_layout = QGridLayout()
        plot_widget.setLayout(plot_layout)
        chart_types = ['Pie Chart', 'Scatter Chart', 'Line Chart', 'Histogram']

        if True : # charts
            f = QFont("Arial", 13);f.setBold(1)

            pie_layout = QVBoxLayout();plot_layout.addLayout(pie_layout,0,0)
            pie_img_label = QLabel();pie_layout.addWidget(pie_img_label)
            pie_img_label.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\pie_chart_preview.png"))
            pie_label = QLabel("Pie Chart");pie_label.setFont(f)
            pie_layout.addWidget(pie_label)
            pie_img_label.setAlignment(Qt.AlignCenter);pie_img_label.setCursor(Qt.PointingHandCursor)
            pie_label.setAlignment(Qt.AlignCenter);pie_label.setCursor(Qt.PointingHandCursor)

            scatter_layout = QVBoxLayout();plot_layout.addLayout(scatter_layout,0,1)
            scatter_img_label = QLabel();scatter_layout.addWidget(scatter_img_label)
            scatter_img_label.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\scatter_plot.png"))
            scatter_label = QLabel("Scatter Chart");scatter_label.setFont(f)
            scatter_layout.addWidget(scatter_label)
            scatter_img_label.setAlignment(Qt.AlignCenter);scatter_img_label.setCursor(Qt.PointingHandCursor)
            scatter_label.setAlignment(Qt.AlignCenter);scatter_label.setCursor(Qt.PointingHandCursor)

            line_layout = QVBoxLayout();plot_layout.addLayout(line_layout,0,2)
            line_img_label = QLabel();line_layout.addWidget(line_img_label)
            line_img_label.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\line_plot.png"))
            line_label = QLabel("Line Chart");line_label.setFont(f)
            line_layout.addWidget(line_label)
            line_img_label.setAlignment(Qt.AlignCenter);line_img_label.setCursor(Qt.PointingHandCursor)
            line_label.setAlignment(Qt.AlignCenter);line_label.setCursor(Qt.PointingHandCursor)

            histogram_layout = QVBoxLayout();plot_layout.addLayout(histogram_layout,0,3)
            histogram_img_label = QLabel();histogram_layout.addWidget(histogram_img_label)
            histogram_img_label.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\histogram_graph.png"))
            histogram_label = QLabel("Histogram Chart");histogram_label.setFont(f)
            histogram_layout.addWidget(histogram_label)
            histogram_img_label.setAlignment(Qt.AlignCenter);histogram_img_label.setCursor(Qt.PointingHandCursor)
            histogram_label.setAlignment(Qt.AlignCenter);histogram_label.setCursor(Qt.PointingHandCursor)

            # bubble_layout = QVBoxLayout();plot_layout.addLayout(bubble_layout,1,0)
            # bubble_img_label = QLabel();bubble_layout.addWidget(bubble_img_label)
            # bubble_img_label.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\scatter_plot.png"))
            # bubble_label = QLabel("Bubble Chart");bubble_label.setFont(f)
            # bubble_layout.addWidget(bubble_label)
            # bubble_img_label.setAlignment(Qt.AlignCenter);bubble_img_label.setCursor(Qt.PointingHandCursor)
            # bubble_label.setAlignment(Qt.AlignCenter);bubble_label.setCursor(Qt.PointingHandCursor)


        self.pie_window = QPloting.PieChartGeneratorWindow()
        self.pie_window.mainclass = self
        self.scatter_window = QPloting.ScatterPlotGeneratorWindow()
        self.scatter_window.mainclass = self
        self.histogram_window = QPloting.HistogramGeneratorWindow()
        self.histogram_window.mainclass = self
        self.line_window = QPloting.LinePlotGeneratorWindow()
        self.line_window.mainclass = self
        self.bubble_window = QPloting.BubblePlotGeneratorWindow()
        self.bubble_window.mainclass = self
        # self.ploting_combo.setFixedWidth(780)

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
        # self.ploting_combo.activated.connect(ploting_combo_f)
        # self.dv_sa_layout.addWidget(self.ploting_combo)


        pie_img_label.mousePressEvent = lambda X : self.pie_window.initui()
        scatter_img_label.mousePressEvent = lambda X : self.scatter_window.initui()
        line_img_label.mousePressEvent = lambda X : self.line_window.initui()
        histogram_img_label.mousePressEvent = lambda X : self.histogram_window.initui()
        # bubble_img_label.mousePressEvent = lambda X : self.bubble_window.initui()

        pie_label.mousePressEvent = lambda X : self.pie_window.initui()
        scatter_label.mousePressEvent = lambda X : self.scatter_window.initui()
        line_label.mousePressEvent = lambda X : self.line_window.initui()
        histogram_label.mousePressEvent = lambda X : self.histogram_window.initui()
        # bubble_label.mousePressEvent = lambda X : self.bubble_window.initui()

        
        self.dv_sa_layout.addWidget(plot_widget)
        self.dv_sa_layout.addSpacing(20)

        self.plots_picker = QWidget()
        self.plots_picker_layout = QVBoxLayout()
        self.plots_picker.setLayout(self.plots_picker_layout)
        self.plots_picker.setStyleSheet(
            "border-radius:10px; background-color:#000;")
        self.plots_img = QLabel()
        self.plots_img.setAlignment(Qt.AlignCenter)
        self.plots_img.setPixmap(
            QPixmap("Database\\Archive\\static\\img\\ploting.png"))
        self.plots_picker_layout.addWidget(self.plots_img)
        self.dv_sa_layout.addWidget(self.plots_picker)
        self.dv_sa_layout.addStretch()


        cur = self.db.cursor()
        cur.execute(
            f"SELECT file_id, label, header FROM files WHERE  project_id = {id_}", )
        if cur.fetchone() :
            file_combo_f(0)
        cur.close()

        def check_fun(e):
            file_full_path = self.file_combo.getOption()
            extension = file_full_path.split('.')[-1]
            cur = self.db.cursor()
            cur.execute(
                "SELECT file_id, label FROM files WHERE file_full_path = ? AND project_id = ?", (file_full_path, id_))
            f = cur.fetchone()
            if f :
                file_combo_f(0)
        self.file_combo.activated.connect(check_fun)

        def change_lang(EN):
            if EN :
                set_file_label.setText("Load a file to the workbench:")
                self.retrive_sheet_button.setText("Retrive Sheet")
                plot_titel.setText("Plot your Dataset :")
                pie_label.setText("Pie Chart")
                scatter_label.setText("Scatter Chart")
                line_label.setText("Line Chart")
                histogram_label.setText("Histogram Chart")
            
            else :
                set_file_label.setText("تحميل ملف الى ساحة العمل:")
                self.retrive_sheet_button.setText("استعادة الجدول")
                plot_titel.setText("اعرض بياناتك :")
                pie_label.setText("رسمة الكعك")
                scatter_label.setText("رسمة المبعثر")
                line_label.setText("رسمة الخط")
                histogram_label.setText("رسمة هوستغرام")
            
        self.change_lang = change_lang
        self.file_combo.fun1 = file_combo_f
        self.file_combo.fun2 = check_fun
        layout = QVBoxLayout()  # Add a layout to center the button
        layout.addLayout(self.dv_layout)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
