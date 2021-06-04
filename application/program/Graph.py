import pandas as pd
import matplotlib.pyplot as plot
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import io

class Graph:
    def __init__(self, data_frame, size):
        self.df = data_frame
        self.x_axis = ""
        self.y_axis = ""
        self.kind = ""
        self.x_label = ""
        self.y_label = ""
        self.size = size
    
    def set_axis(self, x_axis, y_axis):
        self.x_axis = x_axis
        self.y_axis = y_axis
    
    def set_kind(self, kind):
        self.kind = kind
    
    def set_labels(self, x_label, y_label):
        self.x_label = x_label
        self.y_label = y_label

    def get_plot(self):
        if (self.kind):
            return self.df.plot(x=self.x_axis, y=self.y_axis, kind=self.kind, figsize=self.size)
        return self.df.plot(x=self.x_axis, y=self.y_axis, figsize=self.size)

    def get_image(self):
        plt = self.get_plot()
        img = imagify(plt)
        return img
    
    def get_X(self):
        return self.x_axis
    
    def get_Y(self):
        return self.y_axis
    
    def get_frame(self):
        return self.df


def imagify(pd_plot):
    fig = pd_plot.get_figure()
    image = io.BytesIO()
    FigureCanvas(pd_plot.get_figure()).print_png(image)
    return image


def plotify(graph_lst):
    fig = plot.figure()
    for grph in graph_lst:
        df = grph.get_frame()
        plot.plot(df[grph.get_X()], df[grph.get_Y()])
    return 

