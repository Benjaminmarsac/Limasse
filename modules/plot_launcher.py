from PyQt5.QtWidgets import (QPushButton,QMainWindow,QErrorMessage,QMessageBox)
import pandas as pd
from modules.utils import get_save_file, placement,prepare_df_to_plot,floatisation
from PyQt5.QtGui import QIcon
from modules.plots.scatterplot import ScatterPlot
from modules.plots.boxplot import BoxPlot
from modules.plots.histogram import HistPlot
from modules.plots.clustermap import Clustermap
from modules.plots.barplot import Barplot

class PlotLauncher(QMainWindow):
    def __init__(self,df : pd.DataFrame,information : pd.DataFrame | None,deepness : str,operation_type : str, all_data : bool):
        super().__init__()
        self.df = df.copy()
        self.all_data = all_data
        self.information = information.index.to_list() if information is not None else None
        self.deepness = deepness.split("/") if (len(deepness) > 0 and all_data == False) else None
        self.operation_type = operation_type if all_data == False else None
        number_of_window_height = 3
        number_of_window_width = 3
        self.button_width = 150
        self.button_height = 40
        self.lateral_space = 20
        width, height = (self.button_width*number_of_window_width +
                         self.lateral_space*(number_of_window_width+1)), ((self.button_height+20)*number_of_window_height+20)
        self.plot_buttons()
        self.setFixedSize(width, height)
        self.setWindowTitle('plot_launcher')
        self.setWindowIcon(QIcon('modules/limasse_logo.png'))

    def plot_buttons(self):

        scatter_plot_button = QPushButton("Scatter plot", self)
        scatter_plot_button.setGeometry(placement(self.lateral_space, 1, self.button_width), placement(
            self.lateral_space, 1, self.button_height), self.button_width, self.button_height)
        scatter_plot_button.clicked.connect(self.scatter)
        heat_map_button = QPushButton("Heat Map", self)
        heat_map_button.setGeometry(placement(self.lateral_space, 2, self.button_width), placement(
            self.lateral_space, 1, self.button_height), self.button_width, self.button_height)
        heat_map_button.clicked.connect(self.cluster_map)
        barplot_button = QPushButton("Bar plot", self)
        barplot_button.setGeometry(placement(self.lateral_space, 3, self.button_width), placement(
            self.lateral_space, 1, self.button_height), self.button_width, self.button_height)
        barplot_button.clicked.connect(self.bar_plot)
        histogram_button = QPushButton("Histogram", self)
        histogram_button.setGeometry(placement(self.lateral_space, 1, self.button_width), placement(
            self.lateral_space, 2, self.button_height), self.button_width, self.button_height)
        histogram_button.clicked.connect(self.histo)
        boxplot_button = QPushButton("Boxplot", self)
        boxplot_button.setGeometry(placement(self.lateral_space, 2, self.button_width), placement(
            self.lateral_space, 2, self.button_height), self.button_width, self.button_height)
        boxplot_button.clicked.connect(self.box_plot)
        pairplot_button = QPushButton("Pairplot", self)
        pairplot_button.setGeometry(placement(self.lateral_space, 3, self.button_width), placement(
            self.lateral_space, 2, self.button_height), self.button_width, self.button_height)
        pca = QPushButton("Principal componant\n analysis", self)
        pca.setGeometry(placement(self.lateral_space, 1, self.button_width), placement(
            self.lateral_space, 3, self.button_height), self.button_width, self.button_height)
        pca.clicked.connect(self.pca_plot)
        save_df = QPushButton("Save current\n DataFrame", self)
        save_df.setGeometry(placement(self.lateral_space, 3, self.button_width), placement(
            self.lateral_space, 3, self.button_height), self.button_width, self.button_height)
        save_df.clicked.connect(self.save_file)

    def no_information(self):
        err = QErrorMessage(self)
        err.showMessage("Information are needed for this kind of plot.")

    def scatter(self):
        if self.information is None:
            self.no_information()
        else:
            df = floatisation(prepare_df_to_plot(self.df,self.operation_type,self.deepness)) if self.all_data == False else self.df
            self.scat = ScatterPlot(df,self.information)
            self.scat.show()

    def histo(self):
        if self.information is None:
            self.no_information()
        else:
            df = floatisation(prepare_df_to_plot(self.df,self.operation_type,self.deepness)) if self.all_data == False else self.df
            self.hist = HistPlot(df,self.information)
            self.hist.show()

    def box_plot(self):
        if self.information is None:
            self.no_information()
        else:
            df = floatisation(prepare_df_to_plot(self.df,self.operation_type,self.deepness)) if self.all_data == False else self.df
            self.box_p = BoxPlot(df,self.information)
            self.box_p.show()

    def cluster_map(self):
        df = self.df.drop(index = self.information) if self.information else self.df
        df = floatisation(prepare_df_to_plot(df,self.operation_type,self.deepness,mode = "cluster")).T if self.all_data == False else df.astype(float)

        self.cluster = Clustermap(df,self.operation_type,self.deepness)
        self.cluster.deepness_checker()
        self.cluster.show_cluster()

    def pair_plot(self):
        pass

    def bar_plot(self):
        if self.information is None:
            self.no_information()
        else:
            df = floatisation(prepare_df_to_plot(self.df,self.operation_type,self.deepness)) if self.all_data == False else self.df
            self.box_p = Barplot(df,self.information)
            self.box_p.show()
    
    def pca_plot(self):
        QMessageBox.about(self,"Coming soon","The PCA analysis is coming soon")
#### ajouter un barplot?

    def save_file(self):
        response = get_save_file(self)
        self.df.to_excel(response,sheet_name="Analyse")

