from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
import pandas as pd


class DataPrevisualisation(QWidget):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df
        self.window_width, self.window_heigth = 700, 500
        layout = QVBoxLayout(self)
        self.setLayout = layout
        self.resize(self.window_width, self.window_heigth)
        self.table = QTableWidget(self)
        layout.addWidget(self.table)
        self.display_table(df)

    def display_table(self, df):
        df.reset_index(inplace=True)
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)
        for row in df.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.3f}'.format(value)
                table_item = QTableWidgetItem(str(value))
                self.table.setItem(row[0], col_index, table_item)
