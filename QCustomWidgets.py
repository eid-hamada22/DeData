from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd, math, time
from matplotlib.backends.backend_qt5agg import (
        FigureCanvasQTAgg as FigureCanvas
    )
import QTools

class ClickableWidget(QWidget):
    def __init__(self, function_):
        super().__init__()
        self.setStyleSheet('background-color:#444; border-width:1.5px; border-color:#555; border-style:solid;')
        self.function = function_

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.function(self.data_)

class ClickableWidget_s(QWidget):
    def __init__(self, function_,model_):
        super().__init__()
        self.setStyleSheet('background-color:#444; border-width:1.5px; border-color:#555; border-style:solid;')
        self.function = function_
        self.model = model_
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.function(self.model)


class ClickableWidget_noData(QWidget):
    def __init__(self, function_):
        super().__init__()
        self.setStyleSheet('background-color:#444; border-width:1.5px; border-color:#555; border-style:solid;')
        self.function = function_

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.function()

class CustomContextMenuButton(QPushButton):
    def __init__(self, create_column_f,not_demo=True):
        super().__init__(None)
        self.create_column_f = create_column_f
        self.not_demo = not_demo
    def mousePressEvent(self, event):
        if event.button() == 1:  # Left mouse button
            self.showContextMenu(event.globalPos())
        else:
            super().mousePressEvent(event)
            
    def showContextMenu(self, pos):
        context_menu = QMenu(self)
        action1 = QAction("save changes", self)
        action3 = QAction("load previous page", self)
        action2 = QAction("load next page", self)
        action4 = QAction("create new column", self)
        action5 = QAction("view in separate window", self)
        if self.not_demo :
            context_menu.addAction(action1)
        context_menu.addAction(action3)
        context_menu.addAction(action2)
        if self.not_demo :
            context_menu.addAction(action4)
        context_menu.addAction(action5)
        
        selected_action = context_menu.exec_(pos)
        if selected_action == action1:
            df = self.mainclass.sheet.retrive_whole_dataframe()
            QTools.save_dataframe(df, self.mainclass.sheet.file_path)
        elif selected_action == action2:
            self.mainclass.sheet.display_next_page()
        elif selected_action == action3:
            self.mainclass.sheet.display_prev_page()
        elif selected_action == action4:
            self.create_column_f()
        elif selected_action == action5:
            self.mainclass.sheet_place_layout.addWidget(self.mainclass.retrive_sheet_button)
            self.sheet.setParent(None)
            self.sheet.setWindowTitle(fr"DeData Sheets - {self.mainclass.sheet.file_path}")
            self.sheet.show()

class CustomLineEdit(QLineEdit):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
    def mouseDoubleClickEvent(self, _):
        if self.text():
            self.mainclass.label = self.text()
            self.mainclass.set_headers_black()
            self.setStyleSheet("background-color: #007ACC; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")

class QSheet(QScrollArea):
    def retrive_whole_dataframe(self):
        data = self.retrive_dataframe()
        index = int(self.NUM_LABELS[0].text())-1
        x, y = self.df.iloc[index:index+100, :].shape
        rows_to_update = slice(index, index + 100)
        cols_to_update = slice(None)
        self.df.iloc[rows_to_update, cols_to_update] = data.iloc[0:x, 0:y]
        columns = []
        for HEAD in self.HEADERS:
            columns.append(HEAD.text())
        self.df.columns = columns
        cur = self.mainclass.db.cursor()
        reg = 0; bin = 0; len_ = len(set(self.df[self.label]))
        if len_ == 2: bin = 1
        if len_ >= 20 and pd.api.types.is_numeric_dtype(self.df[self.label]): reg = 1
        cur.execute("UPDATE files SET label = ?, reg = ?, binary = ? WHERE file_id=?", (self.label, reg, bin, self.file_id))
        self.mainclass.db.commit()
        cur.close()
        if self.file_id :
            self.mainclass.label_changed.emit(self.file_id,self.label)
        return self.df
    def display_prev_page(self):
        data = self.retrive_dataframe()
        index = int(self.NUM_LABELS[0].text())-1
        x, y = self.df.iloc[index:index+100, :].shape
        rows_to_update = slice(index, index + 100)
        cols_to_update = slice(None)
        self.df.iloc[rows_to_update, cols_to_update] = data.iloc[0:x, 0:y]
        if self.current_page - 1 != 0:
            self.current_page -= 1
            for row_index in range(len(self.SheetStructure)):
                self.NUM_LABELS[row_index].setText(((100*(self.current_page-1))+row_index+1).__str__())
                row = self.SheetStructure[row_index]
                for cell_input_index in range(len(row)):
                    try:
                        cell_input = row[cell_input_index]
                        cell_input.setText(self.df.iloc[(100*(self.current_page-1))+row_index, cell_input_index].__str__()) 
                    except:cell_input.setText('')
    def display_next_page(self):
        data = self.retrive_dataframe()
        index = int(self.NUM_LABELS[0].text())-1
        x, y = self.df.iloc[index:index+100, :].shape
        rows_to_update = slice(index, index + 100)
        cols_to_update = slice(None)
        self.df.iloc[rows_to_update, cols_to_update] = data.iloc[0:x, 0:y]
        if math.ceil(self.df.shape[0]/100) >= self.current_page + 1:
            self.current_page += 1
            for row_index in range(len(self.SheetStructure)):
                self.NUM_LABELS[row_index].setText(((100*(self.current_page-1))+row_index+1).__str__())
                row = self.SheetStructure[row_index]
                for cell_input_index in range(len(row)):
                    try:
                        cell_input = row[cell_input_index]
                        cell_input.setText(self.df.iloc[(100*(self.current_page-1))+row_index, cell_input_index].__str__())
                    except:cell_input.setText('')
    def __init__(self):
        super().__init__()
        self.equipped = False
        self.setStyleSheet('background-color: #222;')
        self.sheet_picker_widget = QWidget()
        self.setWidget(self.sheet_picker_widget)
        self.sheet_picker_layout = QVBoxLayout()
        self.sheet_picker_layout.setContentsMargins(0,0,0,0)
        self.sheet_picker_widget.setLayout(self.sheet_picker_layout)
        self.setWidgetResizable(True)
        self.sheet_picker_layout.addStretch()
    def cell_calc(self):
        cell = self.focusWidget()
        try: ans = eval(cell.text())
        except: ans = cell.text()
        cell.setText(ans.__str__())
    def set_headers_black(self):
        for HEAD in self.HEADERS:
            HEAD.setStyleSheet("background-color: #333; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
    def load_pandas_dataframe(self, df: pd.DataFrame, label, file_path, file_id,headers_ex=True): # added headers
        self.mainclass.sheet_place.setStyleSheet("border-radius:10px; background-color:#000;")
        
        self.file_id = file_id
        self.file_path = file_path
        self.NUM_LABELS = []
        self.current_page = 1
        self.df = df
        self.SheetStructure = []
        self.label = label; self.HEADERS = []
        self.columns_count = 0; self.rows_count = 0
        if 'sheet_widget' in dir(self): self.sheet_widget.setParent(None)
        self.rows = df.values
        if headers_ex :
            headers = df.columns.tolist()
        else :
            l = len(df.columns.tolist())
            headers = [f'col-{i}' for i in range(l)]

        self.numeric_columns = []; self.nonnumeric_columns = []
        for column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                self.numeric_columns.append(column)
                if len(set(df[column])) <= 10:
                    self.nonnumeric_columns.append(column)
            else:
                if len(set(df[column])) != df.shape[0]:
                    self.nonnumeric_columns.append(column)
        if len(headers) > len(set(headers)):
            msg_box = QMessageBox()
            msg_box.setStyleSheet('background-color:#333; color:#fff;')
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("The sheet is in an invalide format!")
            msg_box.setWindowTitle("Error rendering the sheet:")
            msg_box.addButton("OK", QMessageBox.AcceptRole)
            msg_box.exec_()
        else:
            self.sheet_widget = QWidget()
            self.sheet_layout = QGridLayout()
            self.sheet_widget.setLayout(self.sheet_layout)
            def create_column_f():
                header_input = CustomLineEdit('') if header else QLabel(header.__str__())
                self.HEADERS.append(header_input)
                header_input.mainclass = self
                header_input.setAlignment(Qt.AlignCenter)
                header_input.setStyleSheet("background-color: #333; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
                self.columns_count += 1
                self.sheet_layout.addWidget(header_input, 0, self.columns_count)
                for row in range(1, self.rows_count+1):
                    cell_input = QLineEdit()
                    self.SheetStructure[row-1].append(cell_input)
                    cell_input.returnPressed.connect(self.cell_calc)
                    cell_input.setStyleSheet("""
                    QLineEdit {
                        background-color: #444; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;
                    }
                    QLineEdit:focus {
                        background-color: #444; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px; border-width:1.5px; border-color:#00416D; border-style:solid;
                    }
                    """)
                    self.sheet_layout.addWidget(cell_input, row, self.columns_count)
                self.df[time.ctime()] = [''] * self.df.shape[0]
                header_input.setFocus()
            empty_label = CustomContextMenuButton(create_column_f,self.file_id)
            empty_label.sheet = self; empty_label.mainclass = self.mainclass
            empty_label.setCursor(Qt.PointingHandCursor)
            empty_label.setIcon(QIcon("Database\\archive\\static\\img\\settings_button.png"))
            empty_label.setIconSize(QSize(20, 20))
            empty_label.setMaximumWidth(65)
            empty_label.setStyleSheet("background-color: #333; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
            # if self.file_id :
            self.sheet_layout.addWidget(empty_label, 0, 0)
            if not label:
                tem_l = []
            for header_index in range(len(headers)):
                header = headers[header_index]
                header_input = CustomLineEdit(header.__str__()) if header else QLabel(header.__str__())
                self.HEADERS.append(header_input)
                header_input.mainclass = self
                header_input.setAlignment(Qt.AlignCenter)
                if header.__str__() == label: color_ = "007ACC"
                else: color_ = 333
                header_input.setStyleSheet(f"background-color: #{color_}; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
                self.sheet_layout.addWidget(header_input, 0, header_index+1)
                if not label:
                    tem_l.append(header_input)
            if not label :
                tem_l[-1].setStyleSheet(f"background-color: #007ACC; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
            for y in range(1, 101):
                number_input = QLabel(y.__str__())
                self.NUM_LABELS.append(number_input)
                number_input.setMaximumWidth(65)
                number_input.setAlignment(Qt.AlignCenter)
                number_input.setStyleSheet("background-color: #333; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;")
                self.sheet_layout.addWidget(number_input, y, 0)
                RawStructure = []
                for x in range(len(self.rows[0])):
                    try: cell = self.rows[y-1][x]
                    except: cell = ''
                    cell_input = QLineEdit(cell.__str__())
                    RawStructure.append(cell_input)
                    cell_input.returnPressed.connect(self.cell_calc)
                    cell_input.setStyleSheet("""
                    QLineEdit {
                        background-color: #444; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px;
                    }
                    QLineEdit:focus {
                        background-color: #444; color: #fff; font-size: 14px; border-radius: 5px; padding: 8px; border-width:1.5px; border-color:#00416D; border-style:solid;
                    }
                    """)
                    self.sheet_layout.addWidget(cell_input, y, x+1)
                    self.rows_count = y; self.columns_count = x+1
                self.SheetStructure.append(RawStructure)
            self.sheet_picker_layout.insertWidget(0, self.sheet_widget)
            self.equipped = True
            QTools.clear_layout(self.mainclass.plots_picker_layout)
            if not self.mainclass.plots_img.parent():
                self.mainclass.plots_picker_layout.addWidget(self.mainclass.plots_img)
    def retrive_dataframe(self):
        data = []
        if 'sheet_widget' in dir(self):
            for row_id in range(len(self.SheetStructure)):
                data_row = []
                row = self.SheetStructure[row_id]
                for cell in row:
                    data_row.append(cell.text())
                data.append(data_row)
            columns = []
            for HEAD in self.HEADERS:
                columns.append(HEAD.text())
            df = pd.DataFrame(data, columns=columns)
            return df
        else:
            print("there is no sheet widget load on the picker")
            return 0


class DarkComboBox(QComboBox):
    def wheelEvent(self, event):
        pass
    def getOption(self):
        return self.currentText()
    def setItems(self, items):
        self.clear()
        self.addItems(items)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QComboBox {
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
                background-color: #333333;
                color: #ffffff;
                font-size: 14px;
                selection-background-color: #444444;
                selection-color: #ffffff;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #555555;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
            QComboBox QAbstractItemView {
                border: 1px solid #555555;
                background-color: #333333;
                color: #ffffff;
                font-size: 14px;
                selection-background-color: #444444;
                selection-color: #ffffff;
            }
        """)

