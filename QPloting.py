from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
import QTools, QCustomWidgets
import numpy as np
plt.style.use('dark_background')

class LinePlotGeneratorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color: #222;')
        self.layout_ = QHBoxLayout()
        self.setLayout(self.layout_)
        self.initui_()
    def initui_(self):
        self.setWindowTitle("DeData - Line Plot")
        ## img
        pie_img_label = QLabel()
        pie_img_label.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\line_plot.png"))
        pie_img_label.setAlignment(Qt.AlignCenter)
        self.layout_.addWidget(pie_img_label)
        ## elements widget
        self.elements_widget = QWidget()
        self.elements_widget_layout = QVBoxLayout()
        self.elements_widget.setLayout(self.elements_widget_layout)
        self.layout_.addWidget(self.elements_widget)
        # combo box
        label = QLabel('Enter X axis:')
        label.setStyleSheet("color:#fff; background-color: #222; font-size:16px")
        self.elements_widget_layout.addWidget(label)
        
        self.X_combo = QCustomWidgets.DarkComboBox()
        self.X_combo.setFixedWidth(200)
        self.elements_widget_layout.addWidget(self.X_combo)
        
        label = QLabel('Enter Y axis:')
        label.setStyleSheet("color:#fff; background-color: #222; font-size:16px")
        self.elements_widget_layout.addWidget(label)
        
        self.Y_combo = QCustomWidgets.DarkComboBox()
        self.Y_combo.setFixedWidth(200)
        self.elements_widget_layout.addWidget(self.Y_combo)
        
        self.elements_widget_layout.addStretch()
        # button
        def plot_button_f(e):
            self.mainclass.plots_img.setParent(None)
            X = self.mainclass.sheet.df[self.X_combo.getOption()]
            Y = self.mainclass.sheet.df[self.Y_combo.getOption()]
            QTools.create_line_plot(X, Y, self.X_combo.getOption(), self.Y_combo.getOption(), self.mainclass.plots_picker_layout)
            self.hide()
        self.plot_button = QPushButton("Plot")
        self.plot_button.setFixedWidth(200)
        self.plot_button.clicked.connect(plot_button_f)
        self.plot_button.setCursor(Qt.PointingHandCursor)
        self.plot_button.setStyleSheet("""
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 5px;
            background-color: #007ACC;
            color: #ffffff;
            font-size: 14px;
            selection-background-color: #444444;
            selection-color: #ffffff;""")
        self.elements_widget_layout.addWidget(self.plot_button)
    def initui(self):
        if self.mainclass.sheet.equipped:
            self.X_combo.setItems(self.mainclass.sheet.numeric_columns)
            self.Y_combo.setItems(self.mainclass.sheet.numeric_columns)
            self.show()
            self.setFixedSize(self.size())

class ScatterPlotGeneratorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color: #222;')
        self.layout_ = QHBoxLayout()
        self.setLayout(self.layout_)
        self.initui_()
    def initui_(self):
        self.setWindowTitle("DeData - Scatter Plot")
        ## img
        pie_img_label = QLabel()
        pie_img_label.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\scatter_plot.png"))
        pie_img_label.setAlignment(Qt.AlignCenter)
        self.layout_.addWidget(pie_img_label)
        ## elements widget
        self.elements_widget = QWidget()
        self.elements_widget_layout = QVBoxLayout()
        self.elements_widget.setLayout(self.elements_widget_layout)
        self.layout_.addWidget(self.elements_widget)
        # combo box
        label = QLabel('Enter X axis:')
        label.setStyleSheet("color:#fff; background-color: #222; font-size:16px")
        self.elements_widget_layout.addWidget(label)
        
        self.X_combo = QCustomWidgets.DarkComboBox()
        self.X_combo.setFixedWidth(200)
        self.elements_widget_layout.addWidget(self.X_combo)
        
        label = QLabel('Enter Y axis:')
        label.setStyleSheet("color:#fff; background-color: #222; font-size:16px")
        self.elements_widget_layout.addWidget(label)

        self.Y_combo = QCustomWidgets.DarkComboBox()
        self.Y_combo.setFixedWidth(200)
        self.elements_widget_layout.addWidget(self.Y_combo)
        
        # label = QLabel('Colors (optional):')
        # label.setStyleSheet("color:#fff; background-color: #222; font-size:16px")
        # self.elements_widget_layout.addWidget(label)

        # self.colors_combo = QCustomWidgets.DarkComboBox()
        # self.colors_combo.setFixedWidth(200)
        # self.elements_widget_layout.addWidget(self.colors_combo)
        # self.colors_combo.addItem('None')

        self.elements_widget_layout.addStretch()
        # button
        def plot_button_f(e):
            self.mainclass.plots_img.setParent(None)
            X = self.mainclass.sheet.df[self.X_combo.getOption()]
            Y = self.mainclass.sheet.df[self.Y_combo.getOption()]
            QTools.create_scatter_plot(X, Y, self.X_combo.getOption(), self.Y_combo.getOption(), self.mainclass.plots_picker_layout)
            self.hide()
        self.plot_button = QPushButton("Plot")
        self.plot_button.setFixedWidth(200)
        self.plot_button.setCursor(Qt.PointingHandCursor)
        self.plot_button.clicked.connect(plot_button_f)
        self.plot_button.setStyleSheet("""
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 5px;
            background-color: #007ACC;
            color: #ffffff;
            font-size: 14px;
            selection-background-color: #444444;
            selection-color: #ffffff;""")
        self.elements_widget_layout.addWidget(self.plot_button)
    def initui(self):
        if self.mainclass.sheet.equipped:
            self.X_combo.setItems(self.mainclass.sheet.numeric_columns)
            self.Y_combo.setItems(self.mainclass.sheet.numeric_columns)
            # self.colors_combo.addItems(self.mainclass.sheet.nonnumeric_columns)
            self.show()
            self.setFixedSize(self.size())

class HistogramGeneratorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color: #222;')
        self.layout_ = QHBoxLayout()
        self.setLayout(self.layout_)
        self.initui_()
    def initui_(self):
        ## img
        self.setWindowTitle("DeData - Histogram")
        pie_img_label = QLabel()
        pie_img_label.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\histogram_graph.png"))
        pie_img_label.setAlignment(Qt.AlignCenter)
        self.layout_.addWidget(pie_img_label)
        ## elements widget
        self.elements_widget = QWidget()
        self.elements_widget_layout = QVBoxLayout()
        self.elements_widget.setLayout(self.elements_widget_layout)
        self.layout_.addWidget(self.elements_widget)
        # combo box
        self.numeric_headers_combo = QCustomWidgets.DarkComboBox()
        self.numeric_headers_combo.setFixedWidth(200)
        self.elements_widget_layout.addWidget(self.numeric_headers_combo)
        # bins:
        self.bins_cell = QLineEdit()
        self.bins_cell.setStyleSheet("""
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 5px;
            background-color: #444;
            color: #ffffff;
            font-size: 14px;
            selection-background-color: #444444;
            selection-color: #ffffff;""")
        self.bins_cell.setPlaceholderText("Number of bins")
        self.bins_cell.setFixedWidth(200)
        self.elements_widget_layout.addWidget(self.bins_cell)
        self.elements_widget_layout.addStretch()
        # text:
        label = QLabel('• This figure works only with numeric data!')
        label.setStyleSheet("color:yellow; background-color: #222; font-size:9px")
        # button
        def plot_button_f(e):
            if self.bins_cell.text().isdigit():
                self.mainclass.plots_img.setParent(None)
                QTools.create_histogram_chart(self.mainclass.sheet.df[self.numeric_headers_combo.getOption()], int(self.bins_cell.text()), self.mainclass.plots_picker_layout)
                self.bins_cell.setText('')
                self.hide()
            else:
                msg_box = QMessageBox()
                msg_box.setStyleSheet('background-color:#333; color:#fff;')
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText("The bins parameter should be an intger!")
                msg_box.setWindowTitle("Ploting Error:")
                msg_box.addButton("OK", QMessageBox.AcceptRole)
                msg_box.exec_()
        self.plot_button = QPushButton("Plot")
        self.plot_button.setFixedWidth(200)
        self.plot_button.setCursor(Qt.PointingHandCursor)
        self.plot_button.clicked.connect(plot_button_f)
        self.plot_button.setStyleSheet("""
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 5px;
            background-color: #007ACC;
            color: #ffffff;
            font-size: 14px;
            selection-background-color: #444444;
            selection-color: #ffffff;""")
        self.elements_widget_layout.addWidget(label)
        self.elements_widget_layout.addWidget(self.plot_button)
    def initui(self):
        if self.mainclass.sheet.equipped:
            self.numeric_headers_combo.setItems(self.mainclass.sheet.numeric_columns)
            self.show()
            self.setFixedSize(self.size())

class PieChartGeneratorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color: #222;')
        self.layout_ = QHBoxLayout()
        self.setLayout(self.layout_)
        self.initui_()
    def initui_(self):
        ## img
        self.setWindowTitle("DeData - Pie Chart")
        pie_img_label = QLabel()
        pie_img_label.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\pie_chart_preview.png"))
        pie_img_label.setAlignment(Qt.AlignCenter)
        self.layout_.addWidget(pie_img_label)
        ## elements widget
        self.elements_widget = QWidget()
        self.elements_widget_layout = QVBoxLayout()
        self.elements_widget.setLayout(self.elements_widget_layout)
        self.layout_.addWidget(self.elements_widget)
        # combo box
        self.nonnumeric_headers_combo = QCustomWidgets.DarkComboBox()
        self.nonnumeric_headers_combo.setFixedWidth(200)
        self.elements_widget_layout.addWidget(self.nonnumeric_headers_combo)
        self.elements_widget_layout.addStretch()
        # text:
        label = QLabel('• This figure works only with non-numeric data!')
        label.setStyleSheet("color:yellow; background-color: #222; font-size:9px")
        # button
        def plot_button_f(e):
            self.mainclass.plots_img.setParent(None)
            QTools.create_pie_chart(self.mainclass.sheet.df[self.nonnumeric_headers_combo.getOption()], self.mainclass.plots_picker_layout)
            self.hide()
        self.plot_button = QPushButton("Plot")
        self.plot_button.setFixedWidth(200)
        self.plot_button.setCursor(Qt.PointingHandCursor)
        self.plot_button.clicked.connect(plot_button_f)
        self.plot_button.setStyleSheet("""
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 5px;
            background-color: #007ACC;
            color: #ffffff;
            font-size: 14px;
            selection-background-color: #444444;
            selection-color: #ffffff;""")
        self.elements_widget_layout.addWidget(label)
        self.elements_widget_layout.addWidget(self.plot_button)
    def initui(self):
        if self.mainclass.sheet.equipped:
            self.nonnumeric_headers_combo.setItems(self.mainclass.sheet.nonnumeric_columns)
            self.show()
            self.setFixedSize(self.size())


class BubblePlotGeneratorWindow(QWidget): 
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color: #222;')
        self.layout_ = QHBoxLayout()
        self.setLayout(self.layout_)
        self.initui_()
    def initui_(self):
        self.setWindowTitle("DeData - Bubble Plot")
        ## img
        pie_img_label = QLabel()
        pie_img_label.setPixmap(QPixmap("C:\\Users\\ss\\Desktop\\GUI-AI-Django\\AIProject\\Database\\Archive\\static\\img\\scatter_plot.png"))
        pie_img_label.setAlignment(Qt.AlignCenter)
        self.layout_.addWidget(pie_img_label)
        ## elements widget
        self.elements_widget = QWidget()
        self.elements_widget_layout = QVBoxLayout()
        self.elements_widget.setLayout(self.elements_widget_layout)
        self.layout_.addWidget(self.elements_widget)
        # combo box
        label = QLabel('Enter X axis:')
        label.setStyleSheet("color:#fff; background-color: #222; font-size:16px")
        self.elements_widget_layout.addWidget(label)
        
        self.X_combo = QCustomWidgets.DarkComboBox()
        self.X_combo.setFixedWidth(200)
        self.elements_widget_layout.addWidget(self.X_combo)
        
        label = QLabel('Enter Y axis:')
        label.setStyleSheet("color:#fff; background-color: #222; font-size:16px")
        self.elements_widget_layout.addWidget(label)
        
        self.Y_combo = QCustomWidgets.DarkComboBox()
        self.Y_combo.setFixedWidth(200)
        self.elements_widget_layout.addWidget(self.Y_combo)
        
        label = QLabel('Enter Z axis (bubbles sizes):')
        label.setStyleSheet("color:#fff; background-color: #222; font-size:16px")
        self.elements_widget_layout.addWidget(label)
        
        self.Z_combo = QCustomWidgets.DarkComboBox()
        self.Z_combo.setFixedWidth(200)
        self.elements_widget_layout.addWidget(self.Z_combo)

        self.elements_widget_layout.addStretch()
        # button
        def plot_button_f(e):
            self.mainclass.plots_img.setParent(None)
            X = self.mainclass.sheet.df[self.X_combo.getOption()]
            Y = self.mainclass.sheet.df[self.Y_combo.getOption()]
            Z = self.mainclass.sheet.df[self.Z_combo.getOption()]
            
            Z = Z / Z.max() 
            Z = Z.astype(np.float)
            QTools.create_bubble_plot(X, Y, Z, self.X_combo.getOption(), self.Y_combo.getOption(), self.Z_combo.getOption(), self.mainclass.plots_picker_layout)
            self.hide()
        self.plot_button = QPushButton("Plot")
        self.plot_button.setFixedWidth(200)
        self.plot_button.setCursor(Qt.PointingHandCursor)
        self.plot_button.clicked.connect(plot_button_f)
        self.plot_button.setStyleSheet("""
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 5px;
            background-color: #007ACC;
            color: #ffffff;
            font-size: 14px;
            selection-background-color: #444444;
            selection-color: #ffffff;""")
        self.elements_widget_layout.addWidget(self.plot_button)
    def initui(self):
        if self.mainclass.sheet.equipped:
            self.X_combo.setItems(self.mainclass.sheet.numeric_columns)
            self.Y_combo.setItems(self.mainclass.sheet.numeric_columns)
            self.Z_combo.setItems(self.mainclass.sheet.numeric_columns)
            self.show()
            self.setFixedSize(self.size())
