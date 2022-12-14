from PyQt5.QtWidgets import (
    QPushButton, QMainWindow, QComboBox, QLineEdit, QErrorMessage, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pandas as pd
from modules.utils import placement
import matplotlib.pyplot as plt
import seaborn as sns


class ScatterPlot(QMainWindow):
    def __init__(self, df: pd.DataFrame, information: list):
        super().__init__()
        self.df = df
        self.information = information
        number_of_window_height = 5
        number_of_window_width = 2
        self.button_width = 150
        self.button_height = 40
        width, height = (self.button_width*number_of_window_width +
                         60), ((self.button_height+20)*number_of_window_height+20)
        self.lateral_space = 20
        self.setFixedSize(width, height)
        self.plot_parameters()
        self.setWindowTitle("Scatter plot")

    def plot_parameters(self):
        writting = QFont("Arial", 13)
        x_label = QLabel(self)
        x_label.setText("x axis")
        x_label.setFont(writting)
        x_label.setGeometry(70, 5, 100, 25)
        y_label = QLabel(self)
        y_label.setText("y axis")
        y_label.setFont(writting)
        y_label.setGeometry(240, 5, 100, 25)
        color_label = QLabel(self)
        color_label.setText("Color")
        color_label.setFont(writting)
        color_label.setGeometry(70, 78, 100, 25)
        style_label = QLabel(self)
        style_label.setText("Style")
        style_label.setFont(writting)
        style_label.setGeometry(240, 78, 100, 25)
        x_min_label = QLabel(self)
        x_min_label.setText("x min")
        x_min_label.setFont(writting)
        x_min_label.setGeometry(29, 150, 100, 25)
        x_max_label = QLabel(self)
        x_max_label.setText("x max")
        x_max_label.setFont(writting)
        x_max_label.setGeometry(111, 150, 100, 25)
        y_min_label = QLabel(self)
        y_min_label.setText("y min")
        y_min_label.setFont(writting)
        y_min_label.setGeometry(194, 150, 100, 25)
        y_max_label = QLabel(self)
        y_max_label.setText("y max")
        y_max_label.setFont(writting)
        y_max_label.setGeometry(281, 150, 100, 25)
        x_label_label = QLabel(self)
        x_label_label.setText("x label")
        x_label_label.setFont(writting)
        x_label_label.setGeometry(30, 210, 100, 25)
        y_label_label = QLabel(self)
        y_label_label.setText("y label")
        y_label_label.setFont(writting)
        y_label_label.setGeometry(155, 210, 100, 25)
        title_label = QLabel(self)
        title_label.setText("Title")
        title_label.setFont(writting)
        title_label.setGeometry(287, 210, 100, 25)
        self.x_parameter = QComboBox(self)
        self.x_parameter.setEditable(True)
        self.x_parameter.addItems([f'{i}' for i in self.df.columns.to_list()])
        self.x_parameter_edit = self.x_parameter.lineEdit()
        self.x_parameter_edit.setAlignment(Qt.AlignCenter)
        self.x_parameter_edit.setReadOnly(True)
        self.x_parameter.setGeometry(placement(self.lateral_space, 1, self.button_width), placement(
            self.lateral_space, 1.2, self.button_height), self.button_width, self.button_height)
        self.y_parameter = QComboBox(self)
        self.y_parameter.setEditable(True)
        self.y_parameter.addItems([f'{i}' for i in self.df.columns.to_list()])
        self.y_parameter_edit = self.y_parameter.lineEdit()
        self.y_parameter_edit.setAlignment(Qt.AlignCenter)
        self.y_parameter_edit.setReadOnly(True)
        self.y_parameter.setGeometry(placement(self.lateral_space, 2, self.button_width), int(placement(
            self.lateral_space, 1.2, self.button_height)), self.button_width, self.button_height)
        self.color_parameter = QComboBox(self)
        self.color_parameter.setEditable(True)
        self.color_parameter.addItem("Empty")
        self.color_parameter.addItems(self.information)
        self.color_parameter_edit = self.color_parameter.lineEdit()
        self.color_parameter_edit.setAlignment(Qt.AlignCenter)
        self.color_parameter_edit.setReadOnly(True)
        self.color_parameter.setGeometry(placement(self.lateral_space, 1, self.button_width), int(placement(
            self.lateral_space, 2.4, self.button_height)), self.button_width, self.button_height)
        self.style_parameter = QComboBox(self)
        self.style_parameter.setEditable(True)
        self.style_parameter.addItem("Empty")
        self.style_parameter.addItems(self.information)
        self.style_parameter_edit = self.style_parameter.lineEdit()
        self.style_parameter_edit.setAlignment(Qt.AlignCenter)
        self.style_parameter_edit.setReadOnly(True)
        self.style_parameter.setGeometry(placement(self.lateral_space, 2, self.button_width), placement(
            self.lateral_space, 2.4, self.button_height), self.button_width, self.button_height)
        self.x_min_parameter = QLineEdit(self)
        self.x_min_parameter.setGeometry(25, 175, 50, 30)
        self.x_max_parameter = QLineEdit(self)
        self.x_max_parameter.setGeometry(110, 175, 50, 30)
        self.y_min_parameter = QLineEdit(self)
        self.y_min_parameter.setGeometry(195, 175, 50, 30)
        self.y_max_parameter = QLineEdit(self)
        self.y_max_parameter.setGeometry(280, 175, 50, 30)
        self.x_label = QLineEdit(self)
        self.x_label.setGeometry(5, 235, 100, 30)
        self.y_label = QLineEdit(self)
        self.y_label.setGeometry(130, 235, 100, 30)
        self.plot_title = QLineEdit(self)
        self.plot_title.setGeometry(255, 235, 100, 30)
        plot_pushbutton = QPushButton("Plot!", self)
        plot_pushbutton.setGeometry(placement(self.lateral_space, 1.5, self.button_width), placement(
            self.lateral_space, 5.3, self.button_height), self.button_width, self.button_height)
        plot_pushbutton.clicked.connect(self.plot_button)

    def plot_button(self):
        color_parameter = self.color_parameter.currentText(
        ) if self.color_parameter.currentText() != "Empty" else None
        style_parameter = self.style_parameter.currentText(
        ) if self.style_parameter.currentText() != "Empty" else None
        x_min = int(self.x_min_parameter.text()) if (
            (len(self.x_min_parameter.text())) != 0) else None
        x_max = int(self.x_max_parameter.text()) if (
            (len(self.x_max_parameter.text())) != 0) else None
        y_min = int(self.y_min_parameter.text()) if (
            (len(self.y_min_parameter.text())) != 0) else None
        y_max = int(self.y_max_parameter.text()) if (
            (len(self.y_max_parameter.text())) != 0) else None
        xlab = self.x_label.text() if len(
            self.x_label.text()) != 0 else self.x_parameter.currentText()
        ylab = self.y_label.text() if len(
            self.y_label.text()) != 0 else self.y_parameter.currentText()
        plot_title = self.plot_title.text() if len(
            self.plot_title.text()) != 0 else None
        fig, ax = plt.subplots(figsize=(6.5, 6.5))
        sns.despine(fig, left=True, bottom=True)
        sns.scatterplot(x=self.df.iloc[:, self.x_parameter.currentIndex()],
                        y=self.df.iloc[:, self.y_parameter.currentIndex()],
                        linewidth=0,
                        data=self.df,
                        ax=ax,
                        hue=color_parameter,
                        style=style_parameter)
        ax.set(
            xlim=[x_min, x_max], ylim=[y_min, y_max], xlabel=xlab, ylabel=ylab, title=plot_title)
        plt.show()
