import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import json
import abc
import io
from filter import filter

class CSV_Graph:
    def __init__(self, csv_file):
        self.data = __readcsv__(csv_file).json() 
        self.country_filter = ""
        self.filter_x = ""
        self.filter_y = ""
        self.graph_type = ""

    def __readcsv__(self, csv_file):
        return pd.read_csv(csv_file)
        
    def set_type(self, graph_type):
        self.graph_type = graph_type
    
    def set_filters(self, x, y, country="Country/Region"):
        country_filter = country
        filter_x.set_filter(x)
        filter_y.set_filter(y)
    
    def plot_image(self):
        plt = data.plot(x=filter_x,y=filter_y,kind=graph_type)
        image = io.BytesIO()
        FigureCanvas(plt.get_figure()).print_png(image)
        return image



class CSV_List:
    def __init__(self, csv_file):
        self.data = __readcsv__(csv_file)
        self.filter_by = ""
        self.order_by = ""
    
    def __readcsv__(self, csv_file):
        return pd.read_csv(csv_file)
    
    def set_filters(self, filter_by, order_by):
        self.filter_by = filter_by
        self.order_by = order_by
    
    def plot_table(self):
        
        return 








