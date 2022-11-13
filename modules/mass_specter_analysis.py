import sys,os
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLineEdit, QProgressBar
import pandas as pd
from modules.utils import (alignment_matrix, check_save, placement, get_directory,
                   get_file_to_analysis, presentation_settlement, ion_alignment, unitary_statistics,header_normalizer)
from PyQt5.QtGui import QIcon

class MassSpecterAnalysis(QMainWindow):
    def __init__(self):
        super().__init__()
        number_of_window_height = 4
        number_of_window_width = 2
        self.button_width = 150
        self.button_height = 40
        width, height = (self.button_width*number_of_window_width +
                         60), ((self.button_height+20)*number_of_window_height+20)
        self.lateral_space = 20
        self.setFixedSize(width, height)
        self.set_file()
        self.set_output()
        self.set_file_for_save()
        self.run()
        self.progress()
        self.setWindowTitle('Mass specter analysis')
        self.setWindowIcon(QIcon('modules/limasse_logo.png'))
        
    def set_file(self):
        input_file = QPushButton("Select file for analyse", self)
        input_file.setGeometry(placement(self.lateral_space, 1, self.button_width), placement(
            self.lateral_space, 1, self.button_height), self.button_width, self.button_height)
        input_file.clicked.connect(self.input_action)
        self.input_file_lineedit = QLineEdit(self)
        self.input_file_lineedit.setGeometry(placement(self.lateral_space, 2, self.button_width), placement(
            self.lateral_space, 1, self.button_height), self.button_width, self.button_height)
        self.input_file_lineedit.setReadOnly(True)

    def set_output(self):
        output_folder = QPushButton("Select output folder", self)
        output_folder.setGeometry(placement(self.lateral_space, 1, self.button_width), placement(
            self.lateral_space, 2, self.button_height), self.button_width, self.button_height)
        output_folder.clicked.connect(self.directory)
        self.output_folder_lineedit = QLineEdit(self)
        self.output_folder_lineedit.setGeometry(placement(self.lateral_space, 2, self.button_width), placement(
            self.lateral_space, 2, self.button_height), self.button_width, self.button_height)
        self.output_folder_lineedit.setReadOnly(True)

    def set_file_for_save(self):
        self.file_name_lineedit = QLineEdit(self)
        self.file_name_lineedit.setText("Set your file name")
        self.file_name_lineedit.setGeometry(placement(self.lateral_space, 1, self.button_width), placement(
            self.lateral_space, 3, self.button_height), self.button_width, self.button_height)

    def run(self):
        run_pushbutton = QPushButton("Mass analysis", self)
        run_pushbutton.setGeometry(placement(self.lateral_space, 2, self.button_width), placement(
            self.lateral_space, 3, self.button_height), self.button_width, self.button_height)
        run_pushbutton.clicked.connect(self.analyzer)

    def progress(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(placement(self.lateral_space, 1, self.button_width), placement(
            self.lateral_space, 4, self.button_height), (self.button_width*2+self.lateral_space), self.button_height)

    def directory(self):
        dir = get_directory(self)
        os.chdir(dir)
        self.output_folder_lineedit.setText(dir)

    def input_action(self):
        response = get_file_to_analysis(self)
        self.input = f'{response[0]}'
        self.input_file_lineedit.setText(response[0].split("/")[-1])

    def analyzer(self):
        data = pd.ExcelFile(self.input)
        key = pd.read_excel(data, sheet_name=0, index_col=0)
        sheets = data.sheet_names
        alignment = alignment_matrix(key)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        check_save(
            f"{self.file_name_lineedit.text()}_unitary.xlsx", key, "key")
        check_save(
            f"{self.file_name_lineedit.text()}_presentation.xlsx", key, "key")
        for sheet in range(1, len(sheets)):
            sheet_percent = (int(((sheet+1)/len(sheets))*100)-10)
            df = header_normalizer(pd.read_excel(data, sheets[sheet], index_col=0))
            analyse = unitary_statistics(df)
            presentation = analyse.copy()
            presentation = presentation_settlement(presentation)
            check_save(f"{self.file_name_lineedit.text()}_unitary.xlsx",analyse, sheets[sheet], sheet)
            check_save(f"{self.file_name_lineedit.text()}_presentation.xlsx",presentation, sheets[sheet], sheet)
            if analyse.shape[0] > 0:
                alignment[sheets[sheet]] = ion_alignment(analyse, alignment)
            self.progress_bar.setValue(sheet_percent)
        alignment = alignment.loc[(alignment.loc[:, ~alignment.columns.isin(["code", "mass", "nomenclature"])] != 0).any(axis=1)]
        alignment.to_excel(f"{self.file_name_lineedit.text()}_alignment.xlsx", sheet_name="alignment")
        check_save(f"{self.file_name_lineedit.text()}_alignment.xlsx", alignment, "alignment")
        self.progress_bar.setValue(100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    spectre = MassSpecterAnalysis()
    spectre.show()
    sys.exit(app.exec_())
