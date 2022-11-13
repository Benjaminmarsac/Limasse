import sys
from PyQt5.QtWidgets import (QApplication, QPushButton, QMainWindow)
from PyQt5.QtGui import QIcon
from modules.alignment_analysis import AlignmentAnalysis
from modules.ion_filter_tool import MassSpecterIonScreening
from modules.mass_specter_analysis import MassSpecterAnalysis
from modules.utils import placement


class GlycanToolLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        number_of_window = 3
        width, height = 290, (120*number_of_window+20)
        self.lateral_space = 20
        self.setFixedSize(width, height)
        self.analysis_button()
        self.setWindowTitle('Launcher')
        self.setWindowIcon(QIcon('modules/limasse_logo.png'))

    def analysis_button(self):
        button_width = 250
        button_height = 100
        specter_analysis_pushbutton = QPushButton("Glycan library", self)
        specter_analysis_pushbutton.setGeometry(self.lateral_space, placement(
            self.lateral_space, 1, button_height), button_width, button_height)
        specter_analysis_pushbutton.clicked.connect(self.glycan_filter)
        specter_data_analysis = QPushButton("Data analysis", self)
        specter_data_analysis.setGeometry(self.lateral_space, placement(
            self.lateral_space, 2, button_height), button_width, button_height)
        specter_data_analysis.clicked.connect(self.mass_analysis)
        alignment_analysis_pushbutton = QPushButton("Alignment analysis", self)
        alignment_analysis_pushbutton.setGeometry(self.lateral_space, placement(
            self.lateral_space, 3, button_height), button_width, button_height)
        alignment_analysis_pushbutton.clicked.connect(self.alignment_window)

    def glycan_filter(self):

        self.spectre_2 = MassSpecterIonScreening()
        self.spectre_2.show()

    def mass_analysis(self):
        self.mass_specter = MassSpecterAnalysis()
        self.mass_specter.show()

    def alignment_window(self):
        self.alignement_analysis = AlignmentAnalysis()
        self.alignement_analysis.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Breeze")
    spectre = GlycanToolLauncher()
    spectre.show()
    sys.exit(app.exec_())
