import sys
from PyQt5.QtWidgets import (QApplication, QPushButton,QMainWindow, QComboBox, QLineEdit, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt
import pandas as pd
import numpy as np
from modules.utils import placement, save_data, get_save_file, get_file_to_analysis, get_folder, open_filter, header_normalizer, check_save
from PyQt5.QtGui import QIcon

class MassSpecterIonScreening(QMainWindow):
    def __init__(self):
        super().__init__()
        number_of_window_height = 3
        number_of_window_width = 2
        self.button_width = 150
        self.button_height = 40
        width, height = (self.button_width*number_of_window_width +
                         60), ((self.button_height+20)*number_of_window_height+20)
        self.lateral_space = 20
        self.setFixedSize(width, height)
        self.analysis_button()
        self.progress()
        self.setWindowTitle('Launcher')
        self.setWindowIcon(QIcon('modules/limasse_logo.png'))

    def analysis_button(self):
        input_file = QPushButton("Select file for analyse", self)
        input_file.setGeometry(placement(self.lateral_space, 1, self.button_width), placement(
            self.lateral_space, 1, self.button_height), self.button_width, self.button_height)
        input_file.clicked.connect(self.ion_filter)
        self.files_names, files_visu = get_folder("ion library")
        self.input_file_lineedit = QLineEdit(self)
        self.input_file_lineedit.setReadOnly(True)
        self.input_file_lineedit.setGeometry(placement(self.lateral_space, 2, self.button_width), placement(
            self.lateral_space, 1, self.button_height), self.button_width, self.button_height)
        self.ion_filter_combobox = QComboBox(self)
        self.ion_filter_combobox.setEditable(True)
        self.ion_filter_combobox.addItems(files_visu)
        self.ion_filter_edit = self.ion_filter_combobox.lineEdit()
        self.ion_filter_edit.setAlignment(Qt.AlignCenter)
        self.ion_filter_edit.setReadOnly(True)
        self.generate_ion_library_pushbutton = QPushButton(
            "Generate library", self)
        self.generate_ion_library_pushbutton.setGeometry(placement(self.lateral_space, 2, self.button_width),
                                                         placement(self.lateral_space, 2, self.button_height), self.button_width, self.button_height)
        self.generate_ion_library_pushbutton.clicked.connect(
            self.ion_library)
        self.ion_filter_combobox.setGeometry(self.lateral_space, placement(
            self.lateral_space, 2, self.button_height), self.button_width, self.button_height)
        alignment_analysis_pushbutton = QPushButton("Run ion analysis", self)
        alignment_analysis_pushbutton.setGeometry(self.lateral_space, placement(
            self.lateral_space, 3, self.button_height), self.button_width, self.button_height)
        alignment_analysis_pushbutton.clicked.connect(
            self.alignment_analysis_action)

    def progress(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(placement(self.lateral_space, 2, self.button_width), placement(
            self.lateral_space, 3, self.button_height), self.button_width, self.button_height)

    def ion_filter(self):
        response = get_file_to_analysis(self)
        self.alignement = f'{response[0]}'
        self.input_file_lineedit.setText(response[0].split("/")[-1])

    def alignment_analysis_action(self):
        data_base = header_normalizer(open_filter(
            self.ion_filter_combobox.currentText(), self.files_names, "ion library"))
        first_page = data_base.copy()
        molecule = data_base.columns.to_list()
        molecule.remove('mass')
        save_file = get_save_file(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        xlsx = pd.ExcelFile(self.alignement)
        sheets = xlsx.sheet_names
        header = molecule.copy()
        header.extend(["mass", "intensity", "acceptation"])
        save_data(save_file, first_page, "filter",
                  header=first_page.columns.to_list(), mode="w")
        missing = []
        no_mz = []
        for sheet in range(len(sheets)):
            sheet_percent = int(((sheet+1)/len(sheets))*100)
            df = header_normalizer(pd.read_excel(xlsx, sheets[sheet]))
            filtered_df = np.zeros(len(header))
            if "m/z" in df.columns:
                counter = 0
                for mass in df["m/z"]:
                    for scan in data_base.loc[:, "mass"]:
                        if mass <= scan * 1.0005 and mass >= scan * 0.9995:
                            counter += 1
                            ion = data_base.loc[(
                                data_base.loc[:, "mass"] == scan), molecule]
                            intensity = df.loc[df["m/z"] == mass]
                            intensity = float(intensity["intens."])
                            filtre_ligne = np.hstack(
                                (ion.values[0], mass, intensity, 1))
                            filtered_df = np.vstack(
                                (filtered_df, filtre_ligne))
                if counter > 0:
                    filtered_df = pd.DataFrame(filtered_df)
                    save_data(save_file, filtered_df,
                              sheets[sheet], header=header, mode="a")
                else:
                    missing.append(sheets[sheet])
            else:
                no_mz.append(sheets[sheet])
            self.progress_bar.setValue(sheet_percent)
        missing = f"Empty sheet(s) : {' / '.join(missing)}" if len(
            missing) != 0 else "No empty sheet return."
        no_mz = f"sheets without mz: {' / '.join(no_mz)}" if len(
            no_mz) != 0 else "No empty sheet return."
        QMessageBox.about(self, "Run over", f"Run done\n{missing}\n{no_mz}")

    def ion_library(self):
        save_file = get_save_file(self)
        count = 0
        for i in self.files_names:
            to_merge = pd.read_csv(f"/ion library/{i}", sep=",")
            check_save(save_file, to_merge, i.split('.')[0], count)
            count += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    spectre = MassSpecterIonScreening()
    spectre.show()
    sys.exit(app.exec_())
