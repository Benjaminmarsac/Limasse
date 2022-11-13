from PyQt5.QtWidgets import (
    QPushButton, QMainWindow, QComboBox, QLineEdit, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pandas as pd
from modules.utils import placement
import matplotlib.pyplot as plt
import seaborn as sns


class Barplot(QMainWindow):
    def __init__(self, df: pd.DataFrame, information: list):
        super().__init__()
        self.df = df.copy()
        self.information = information
        number_of_window_height = 4.3
        number_of_window_width = 2
        self.button_width = 150
        self.button_height = 40
        width, height = (self.button_width*number_of_window_width +
                         60), int(((self.button_height+20)*number_of_window_height+20))
        self.lateral_space = 20
        self.setFixedSize(width, height)
        self.plot_parameters()
        self.setWindowTitle("Barplot")

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
        type_label = QLabel(self)
        type_label.setText("Palette")
        type_label.setFont(writting)
        type_label.setGeometry(240, 78, 100, 25)
        x_label_label = QLabel(self)
        x_label_label.setText("x label")
        x_label_label.setFont(writting)
        x_label_label.setGeometry(30, 150, 100, 25)
        y_label_label = QLabel(self)
        y_label_label.setText("y label")
        y_label_label.setFont(writting)
        y_label_label.setGeometry(155, 150, 100, 25)
        title_label = QLabel(self)
        title_label.setText("Title")
        title_label.setFont(writting)
        title_label.setGeometry(287, 150, 100, 25)
        self.x_parameter = QComboBox(self)
        self.x_parameter.setEditable(True)
        self.x_parameter.addItems(self.information)
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
        self.type_parameter = QComboBox(self)
        self.type_parameter.setEditable(True)
        self.type_parameter.addItems(
            ["None", "ocean", "binary", "gray", "winter", "spring", "autumn", "summer"])
        self.style_parameter_edit = self.type_parameter.lineEdit()
        self.style_parameter_edit.setAlignment(Qt.AlignCenter)
        self.style_parameter_edit.setReadOnly(True)
        self.type_parameter.setGeometry(placement(self.lateral_space, 2, self.button_width), placement(
            self.lateral_space, 2.4, self.button_height), self.button_width, self.button_height)
        self.x_label = QLineEdit(self)
        self.x_label.setGeometry(5, 175, 100, 30)
        self.y_label = QLineEdit(self)
        self.y_label.setGeometry(130, 175, 100, 30)
        self.plot_title = QLineEdit(self)
        self.plot_title.setGeometry(255, 175, 100, 30)
        plot_pushbutton = QPushButton("Plot!", self)
        plot_pushbutton.setGeometry(placement(self.lateral_space, 1.5, self.button_width), placement(
            self.lateral_space, 4.4, self.button_height), self.button_width, self.button_height)
        plot_pushbutton.clicked.connect(self.plot_button)

    def plot_button(self):
        color_parameter = self.color_parameter.currentText(
        ) if self.color_parameter.currentText() != "Empty" else None
        xlab = self.x_label.text() if len(
            self.x_label.text()) != 0 else self.x_parameter.currentText()
        ylab = self.y_label.text() if len(
            self.y_label.text()) != 0 else self.y_parameter.currentText()
        plot_title = self.plot_title.text() if len(
            self.plot_title.text()) != 0 else None
        fig, ax = plt.subplots(figsize=(6.5, 6.5))
        palette_parameter = self.type_parameter.currentText(
        ) if self.type_parameter.currentText() != "None" else None
        sns.despine(fig, left=True, bottom=True)
        fig = sns.barplot(
            data=self.df,
            x=self.x_parameter.currentText(),
            y=self.df.iloc[:, self.y_parameter.currentIndex()],
            hue=color_parameter,
            palette=palette_parameter
        )
        ax.set(xlabel=xlab, ylabel=ylab, title=plot_title)
        plt.show()
