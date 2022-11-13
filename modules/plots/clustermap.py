import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Clustermap():
    def __init__(self,df : pd.DataFrame,operation_type : str, deepness : list | None = None):
        self.df = df.copy()
        self.deepness = deepness
        self.row_colors = None
        self.operation_type = operation_type

    def deepness_checker(self):
        if self.deepness is None:
            return
        else:
            self.df['new_col'] = self.df[self.deepness].apply("/".join,axis = 1) if self.operation_type == "No operation" else self.df.index
            lut = dict(zip(self.df["new_col"].unique(), "bgrcmykw"))
            self.row_colors = self.df["new_col"].map(lut)
            self.df = self.df.drop(columns = [*self.deepness,'new_col']) if self.operation_type == "No operation" else self.df.drop(columns=['new_col'])
            self.df = self.df.astype(float)
            
    def show_cluster(self):
        sns.clustermap(data = self.df,
                row_cluster=False,
                row_colors=self.row_colors,
                dendrogram_ratio=(.1, .2),
                cbar_pos=(0, .2, .03, .4),
                    cmap = "RdYlGn")
        plt.show()