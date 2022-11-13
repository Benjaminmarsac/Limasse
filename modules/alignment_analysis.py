import sys
from PyQt5.QtWidgets import (QApplication, QPushButton, QMainWindow, QComboBox,
                             QLineEdit, QCheckBox, QTextBrowser, QMessageBox, QErrorMessage, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from modules.data_previsualisation import DataPrevisualisation
from modules.plot_launcher import PlotLauncher
import pandas as pd
import numpy as np
from itertools import combinations
from modules.utils import get_folder, get_file_to_analysis, open_filter, ion_from_class_filter, unitary_ion_filter, class_operation, header_normalizer


class AlignmentAnalysis(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ion_key_names, self.ion_key_view = get_folder("ion classes")
        self.alignment = None
        self.information = None
        self.information_df = None
        self.all_ion = list()
        self.memory = list()
        self.output = np.array([])
        self.setFixedSize(570, 400)
        self.setWindowTitle("Alignment analysis")
        self.setWindowIcon(QIcon('modules/limasse_logo.png'))
        self.input_buttons()
        self.file_checker()
        self.clear_button()
        self.ion_class()
        self.class_library()
        self.analysis_deepness()
        self.operation_type()
        self.data_previsualisation()
        self.launcher()

    def input_buttons(self):
        alignment_file_pushbutton = QPushButton(
            'Choose an alignment file', self)
        alignment_file_pushbutton.setGeometry(30, 10, 200, 30)
        alignment_file_pushbutton.clicked.connect(self.get_path_alignment)
        information_file_pushbutton = QPushButton(
            'Choose an information file', self)
        information_file_pushbutton.setGeometry(30, 50, 200, 30)
        information_file_pushbutton.clicked.connect(self.get_path_information)

    def file_checker(self):
        self.alignment_file_lineedit = QLineEdit(self)
        self.alignment_file_lineedit.setReadOnly(True)
        self.alignment_file_lineedit.setText("-- No alignment file --")
        self.alignment_file_lineedit.setGeometry(250, 10, 200, 30)
        self.information_file_lineedit = QLineEdit(self)
        self.information_file_lineedit.setReadOnly(True)
        self.information_file_lineedit.setText("-- No information file--")
        self.information_file_lineedit.setGeometry(250, 50, 200, 30)

    def clear_button(self):
        clear = QPushButton("Clear\nfiles", self)
        clear.setGeometry(470, 10, 70, 70)
        clear.clicked.connect(self.action_clear_path)

    def ion_class(self):
        self.keys_menu_combobox = QComboBox(self)
        self.keys_menu_combobox.setEditable(True)
        self.keys_menu_combobox.addItems(
            ["No class filter", *self.ion_key_view])
        keys_menu_lineedit = self.keys_menu_combobox.lineEdit()
        keys_menu_lineedit.setAlignment(Qt.AlignCenter)
        keys_menu_lineedit.setReadOnly(True)
        self.keys_menu_combobox.setGeometry(20, 100, 265, 30)
        self.all_data_box = QCheckBox("All data", self)
        self.all_data_box.setGeometry(20, 140, 80, 30)
        self.primary_class_menu_combobox = QComboBox(self)
        self.primary_class_menu_combobox.setGeometry(105, 140, 180, 30)
        self.primary_class_menu_combobox.addItem("Select a class")
        self.keys_menu_combobox.currentTextChanged.connect(self.get_ion_class)
        self.primary_class_menu_combobox.currentIndexChanged.connect(
            self.add_class_to_browser)

    def class_library(self):
        precise_ion_label = QLabel("Precise an ion", self)
        precise_ion_label.setGeometry(20, 180, 95, 30)
        self.precise_ion_lineedit = QLineEdit(self)
        self.precise_ion_lineedit.setGeometry(125, 180, 160, 30)
        add_button = QPushButton("Add", self)
        add_button.setGeometry(20, 220, 80, 30)
        add_button.clicked.connect(self.add_unitary_ion)
        backspace = QPushButton("Backspace", self)
        backspace.setGeometry(113, 220, 80, 30)
        backspace.clicked.connect(self.delete_last_input)
        clear_whole_button = QPushButton("Reset", self)
        clear_whole_button.setGeometry(205, 220, 80, 30)
        clear_whole_button.clicked.connect(self.clear_class_browser)
        self.ion_class_textbrowser = QTextBrowser(self)
        self.ion_class_textbrowser.setGeometry(20, 260, 265, 100)

    def analysis_deepness(self):
        deepness_label = QLabel("Select the deepness of the analysis", self)
        deepness_label.setGeometry(310, 100, 240, 30)
        self.deepness_combobox = QComboBox(self)
        self.deepness_combobox.setGeometry(310, 140, 240, 30)
        self.deepness_combobox.addItem(None)
        self.primary_class_menu_combobox.currentIndexChanged.connect(
            self.get_ion_class_deepness)

    def operation_type(self):
        type_of_operation_label = QLabel("Select a type of operation", self)
        type_of_operation_label.setGeometry(340, 180, 240, 30)
        self.type_of_operation_combobox = QComboBox(self)
        self.type_of_operation_combobox.setGeometry(310, 220, 240, 30)
        self.deepness_combobox.currentIndexChanged.connect(
            self.class_inclusion)

    def data_previsualisation(self):
        data_previsualisation_pushbutton = QPushButton(
            "Data previsualisation", self)
        data_previsualisation_pushbutton.setGeometry(310, 260, 240, 30)
        data_previsualisation_pushbutton.clicked.connect(
            self.prepare_information)
        data_previsualisation_pushbutton.clicked.connect(self.prepare_df)
        data_previsualisation_pushbutton.clicked.connect(
            self.action_previsualisation)

    def launcher(self):
        launch_analysis = QPushButton("Launch analysis !", self)
        launch_analysis.setGeometry(310, 300, 240, 60)
        launch_analysis.clicked.connect(self.prepare_information)
        launch_analysis.clicked.connect(self.prepare_df)
        launch_analysis.clicked.connect(self.action_launcher)

    def get_path_alignment(self):
        response = get_file_to_analysis(self)
        self.alignment = f'{response[0]}'
        self.alignment_file_lineedit.setText(response[0].split("/")[-1])

    def get_path_information(self):
        response = get_file_to_analysis(self)
        self.information = f'{response[0]}'
        self.information_file_lineedit.setText(response[0].split("/")[-1])

    def action_clear_path(self):
        self.information = None
        self.information_file_lineedit.setText("-- No information file--")
        self.alignment = None
        self.alignment_file_lineedit.setText("-- No alignment file --")
        self.output = np.array([])

    def get_ion_class(self):
        if self.keys_menu_combobox.currentText() != "No class filter":
            df = open_filter(self.keys_menu_combobox.currentText(),
                             self.ion_key_names, "ion classes")
            self.primary_class_menu_combobox.clear()
            self.primary_class_menu_combobox.addItem('None')
            self.primary_class_menu_combobox.addItems(
                [*df.iloc[:, 0].unique()])
        else:
            self.primary_class_menu_combobox.clear()
            self.primary_class_menu_combobox.addItem("Select a class")

    def add_class_to_browser(self):

        if self.primary_class_menu_combobox.currentText() != "No class filter" and self.primary_class_menu_combobox.currentText() != 'None' \
                and self.primary_class_menu_combobox.currentText() not in self.all_ion and len(self.primary_class_menu_combobox.currentText().strip()) > 0 \
                and self.primary_class_menu_combobox.currentText() != "Select a class":
            self.memory.append(self.primary_class_menu_combobox.currentText())
            self.all_ion.append(self.primary_class_menu_combobox.currentText())
            self.ion_class_textbrowser.setText("/".join(self.all_ion))
        elif self.primary_class_menu_combobox.currentText() == 'Select a class':
            self.all_ion = [i for i in self.all_ion if i not in self.memory]
            self.ion_class_textbrowser.setText("/".join(self.all_ion))
            self.memory = list()

    def add_unitary_ion(self):
        if self.precise_ion_lineedit.text() not in self.all_ion:
            self.all_ion.append(self.precise_ion_lineedit.text())
            self.ion_class_textbrowser.setText("/".join(self.all_ion))
        else:
            QMessageBox.about(self, "information",
                              "This mass is already in the list")

    def delete_last_input(self):
        if len(self.all_ion) > 0:
            self.all_ion = self.all_ion[:-1]
            self.ion_class_textbrowser.setText("/".join(self.all_ion))

    def clear_class_browser(self):
        self.all_ion.clear()
        self.ion_class_textbrowser.setText("")

    def get_ion_class_deepness(self):
        if self.keys_menu_combobox.currentText() != "No class filter":
            df = open_filter(self.keys_menu_combobox.currentText(),
                             self.ion_key_names, "ion classes")
            deepness = ["/".join(df.columns.to_list()[:i])
                        for i, j in enumerate(df.columns.to_list()) if i > 0]
            self.deepness_combobox.clear()
            self.deepness_combobox.addItems(deepness)
        else:
            self.deepness_combobox.clear()
            self.deepness_combobox.addItem("Select a deepness")

    def class_inclusion(self):
        self.type_of_operation_combobox.clear()
        if self.deepness_combobox.currentText() != "None":
            res = list()
            res_2 = list()
            divider = self.deepness_combobox.currentText().split("/")
            for i in range(1, len(divider)+1):
                res = res + divider if i == 1 else res + \
                    list(combinations(divider, i))
            for j in res:
                res_2 = res_2 + \
                    [f'sum of {j}'] if type(
                        j) is str else res_2 + [f'sum of {" ⊂ ".join(j[::-1])}']
            self.type_of_operation_combobox.addItem("No operation")
            self.type_of_operation_combobox.addItems(res_2)

    def prepare_df(self):
        try:
            buffer = pd.ExcelFile(self.alignment)
            if "alignment" not in buffer.sheet_names:
                err = QErrorMessage(self)
                err.showMessage(f"You didn't load an alignment Dataframe")
                return
            else:
                self.output = header_normalizer(
                    pd.read_excel(buffer, sheet_name=0, index_col=0))
                if self.all_data_box.isChecked() == True:
                    self.output.drop(columns=["mass", "code"], inplace=True)
                    self.output.set_index("nomenclature", inplace=True)
                else:
                    df_unitary = unitary_ion_filter(
                        self.output, self.all_ion, self.memory)
                    df_ion_from_class = ion_from_class_filter(self.output, open_filter(self.keys_menu_combobox.currentText(
                    ), self.ion_key_names, "ion classes"), self.all_ion, self.deepness_combobox.currentText())
                    df_ion_from_class = class_operation(
                        df_ion_from_class, self.type_of_operation_combobox.currentText(), self.deepness_combobox.currentText())
                    self.output = pd.concat(
                        [df_unitary, df_ion_from_class], join="outer", axis=0)
                if self.information_df is not None:
                    drop = []
                    for i in self.information_df.columns:
                        if i not in self.output.columns.to_list():
                            drop.append(i)
                    self.information_df.drop(columns=drop, inplace=True)
                if self.information_df is not None and self.information_df.shape[1] > 0:
                    self.output = pd.concat(
                        [self.output, self.information_df], join="outer", axis=0)
        except ValueError:
            err = QErrorMessage(self)
            err.showMessage(f"There is no Dataframe")

    def prepare_information(self):
        if self.information is None or self.information == "" or len(self.information) == 0:
            self.information_df = None
            return
        else:
            self.information_df = header_normalizer(
                pd.read_excel(self.information, index_col=0, sheet_name=0))
            return

    def action_previsualisation(self):
        if self.output.size > 0:
            self.previsu = DataPrevisualisation(self.output)
            self.previsu.show()

    def action_launcher(self):
        if self.output.size > 0:
            self.plot_launcher = PlotLauncher(self.output, self.information_df, self.deepness_combobox.currentText(
            ), self.type_of_operation_combobox.currentText(), self.all_data_box.isChecked())
            self.plot_launcher.show()


def main():
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    alignment_analyser = AlignmentAnalysis()
    alignment_analyser.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
