import pandas as pd
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt


class AnalysisGraph():
    filename = "./analysis.csv"
    
    def __init__(self, name):
        self.name = name
        
        try:
            self.df = pd.read_csv(self.filename)
        except FileNotFoundError:
            self.df = pd.DataFrame({"name": [], "depth_len": [], "visited_len": []})

    def update_graph(self, depth_len, visited_len):
        self.df = self.df.append(
            {"name": self.name, "depth_len": depth_len, "visited_len": visited_len},
            ignore_index=True
        )
        self.df.to_csv(self.filename, index=False)
    
    def done(self):
        print("Plotting..")
        self.df[self.df["name"] == self.name]\
            .plot(kind='scatter', x='depth_len',y='visited_len',color='blue')
        plt.suptitle("Plot of the heuristic function "+self.name)
        plt.show()
