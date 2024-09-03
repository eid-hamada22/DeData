from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
        FigureCanvasQTAgg as FigureCanvas
    )
import seaborn as sns

def save_dataframe(df, file_path):
    extension = file_path.split('.')[-1]
    if extension in ['csv','data']:
        df.to_csv(file_path, index=False)
    elif extension == 'xlsx':
        df.to_excel(file_path, index=False)
    elif extension == 'json':
        df.to_json(file_path, orient='records', lines=True)
    else:
        raise ValueError("Unsupported file format. Supported formats are CSV, Excel, and JSON.")

def read_file(file_path):
    file_extension = file_path.split('.')[-1].lower()
    extension_to_function = {
        'csv': pd.read_csv,
        'xlsx': pd.read_excel,
        'json': pd.read_json,
        'data': pd.read_csv,
    }
    if file_extension in extension_to_function:
        reading_function = extension_to_function[file_extension]
        try:
            return reading_function(file_path, on_bad_lines="skip", keep_default_na=False)
        except Exception as e:
            print("error", e)
            msg_box = QMessageBox()
            msg_box.setStyleSheet('background-color:#333; color:#fff;')
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Unable to access the file choosed!")
            msg_box.setWindowTitle("Error")
            msg_box.addButton("OK", QMessageBox.AcceptRole)
            msg_box.exec_()
    else:
        msg_box = QMessageBox()
        msg_box.setStyleSheet('background-color:#333; color:#fff;')
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(f"The ectension of the file you loaded is not supported: {file_extension}")
        msg_box.setWindowTitle("Error")
        msg_box.addButton("OK", QMessageBox.AcceptRole)
        msg_box.exec_()


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
        else:
            clear_layout(item.layout())

def create_pie_chart(categories, layout):
    figure, ax = plt.subplots(figsize=(6, 6))
    picker = QWidget()
    picker.setFixedHeight(400)
    picker_layout = QVBoxLayout()
    picker.setLayout(picker_layout)
    
    canvas = FigureCanvas(figure)
    picker_layout.addWidget(canvas)
    
    layout.insertWidget(0, picker)
    
    category_counts = {}
    for category in categories:
        category_counts[category] = category_counts.get(category, 0) + 1
    labels = list(category_counts.keys())
    values = list(category_counts.values())
    
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Categorical Data Distribution')
    canvas.draw()
    
def create_histogram_chart(list_of_numbers, bins, layout):
    figure, ax = plt.subplots(figsize=(6, 6))
    picker = QWidget()
    picker.setFixedHeight(400)
    picker_layout = QVBoxLayout()
    picker.setLayout(picker_layout)
    
    canvas = FigureCanvas(figure)
    picker_layout.addWidget(canvas)
    
    layout.insertWidget(0, picker)
    
    ax.hist(list_of_numbers, bins=bins, color="#007ACC")
    ax.set_title('Categorical Data Distribution')
    canvas.draw()

def create_scatter_plot(X, Y, X_ : str, Y_ : str, layout):
    figure, ax = plt.subplots(figsize=(6, 6))
    picker = QWidget()
    picker.setFixedHeight(400)
    picker_layout = QVBoxLayout()
    picker.setLayout(picker_layout)
    
    canvas = FigureCanvas(figure)
    picker_layout.addWidget(canvas)
    
    layout.insertWidget(0, picker)
    ax.scatter(X, Y, color='#007ACC', alpha=0.7)
    ax.set_xlabel(X_)
    ax.set_ylabel(Y_)
    ax.set_title(f"{X_} vs {Y_}")
    canvas.draw()

def create_line_plot(X, Y, X_, Y_, layout):
    figure, ax = plt.subplots(figsize=(6, 6))
    picker = QWidget()
    picker.setFixedHeight(400)
    picker_layout = QVBoxLayout()
    picker.setLayout(picker_layout)
    
    canvas = FigureCanvas(figure)
    picker_layout.addWidget(canvas)
    
    layout.insertWidget(0, picker)
    
    ax.plot(X, Y, marker='o', linestyle='-', color='#007ACC')
    ax.set_xlabel(X_)
    ax.set_ylabel(Y_)
    ax.set_title(f"{X_} vs {Y_}")
    canvas.draw()

def create_bubble_plot(X, Y, Z, X_, Y_, Z_, layout):
    figure, ax = plt.subplots(figsize=(6, 6))
    picker = QWidget()
    picker.setFixedHeight(400)
    picker_layout = QVBoxLayout()
    picker.setLayout(picker_layout)
    
    canvas = FigureCanvas(figure)
    picker_layout.addWidget(canvas)
    
    layout.insertWidget(0, picker)
    
    ax.scatter(X, Y, Z, color='#007ACC', alpha=0.7)
    ax.set_xlabel(X_)
    ax.set_ylabel(Y_)
    ax.set_title(f"{X_} vs {Y_} vs {Z_}")
    canvas.draw()
