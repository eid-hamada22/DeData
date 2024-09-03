import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Enable dark mode for Matplotlib
plt.style.use('dark_background')

class MatplotlibWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.figure, (self.ax_pie, self.ax_hist, self.ax_scatter) = plt.subplots(1, 3, figsize=(15, 5))

        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot()

    def plot(self):
        # Sample data
        data = [
            ("Person 1", 18, "Engineer", "USA", 30000),
            ("Person 2", 19, "Teacher", "Canada", 31000),
            ("Person 3", 20, "Engineer", "Canada", 32000),
            ("Person 12", 29, "Teacher", "Canada", 41000),
            ("Person 15", 32, "Engineer", "USA", 44000),
            ("Person 21", 38, "Engineer", "Canada", 50000)
        ]

        # Extracting data for plotting
        ages = [entry[1] for entry in data]
        salaries = [entry[4] for entry in data]

        # Plotting a pie chart of occupations
        occupation_counts = {}
        for entry in data:
            occupation = entry[2]
            occupation_counts[occupation] = occupation_counts.get(occupation, 0) + 1

        occupation_labels = list(occupation_counts.keys())
        occupation_values = list(occupation_counts.values())

        self.ax_pie.pie(occupation_values, labels=occupation_labels, autopct='%1.1f%%', startangle=140)
        self.ax_pie.set_title("Occupation Distribution")

        # Plotting a histogram of ages
        self.ax_hist.hist(ages, bins=8, edgecolor='black')
        self.ax_hist.set_xlabel("Age")
        self.ax_hist.set_ylabel("Frequency")
        self.ax_hist.set_title("Age Distribution")

        # Plotting a scatter plot of age vs salary
        self.ax_scatter.scatter(ages, salaries, color='blue', alpha=0.7)
        self.ax_scatter.set_xlabel("Age")
        self.ax_scatter.set_ylabel("Salary")
        self.ax_scatter.set_title("Age vs Salary")

        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = MatplotlibWidget()
        self.setCentralWidget(central_widget)

def main():
    app = QApplication(sys.argv)

    # Enable dark mode for the application's UI
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

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
