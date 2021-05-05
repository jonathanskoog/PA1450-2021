"""Module for serving an API."""

from flask import Flask, send_file, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plot
from flask import Response
import csv
import pandas as pd
import os
import io


def serve(options):
    """Serve an API."""

    # Create a Flask application
    app = Flask(__name__)

    @app.route("/", methods=['POST','GET'])
    def index():
        """Return the index page of the website."""
        return send_file("../www/index.html")
    
    @app.route("/saveCSV", methods=["Post"])
    def saveCSV():
        csv_url = request.form["csv_file"]
        try:
            csv_data = pd.read_csv(csv_url)
            # with open("application/csv_cache/cache1.csv", "w", newline="") as csv_file:
            #     csv_file.write(csv_data.to_string())
            csv_data.to_csv("application/csv_cache/cache1.csv", index = False, header=True)
            return "success"
        except:
            return "error"
    
    @app.route("/plotGraph", methods=['POST'])
    def plotGraph():
        country = request.form["country"]
        # Get countries data

        x_axis = request.form["x_axis"]
        y_axis = request.form["y_axis"]
        data = pd.read_csv("application/csv_cache/cache1.csv",delimiter=',', header=0, encoding='ascii')
        plt = data.plot(x="Country/Region", y=y_axis)
        image = io.BytesIO()
        FigureCanvas(plt.get_figure()).print_png(image)
        return Response(image.getvalue(), mimetype='image/png')


    # @app.route("/generate/plot", methods=['POST','GET'])
    # def generate_plot():



    # @app.route("/extract/<url>", methods=['POST'])
    # def extract(url):
    #     git_csv = inp.extract_csv(url)
    #     with open("..\\csv_cache\\cache1.csv","w") as cache_csv:
    #         writer = csv.writer(cache_csv)
    #         writer.writerows(git_csv)
        
    #     return send_file("../www/index.html")

        


    # @app.route("/plot/<yAxis>/<xAxis>/data", methods=['POST'])
    # def plot(y,x,data):
    #     plot.plot()
    #     image = io.BytesIO()
    #     plot.savefig(image)
    #     image.seek(0)
    #     return send_file(image, mimetype='image/png')


    # @app.route("/show_graph", methods=['POST'])
    # def show_graph():
    #     git_url = request.form['furl']
    #     if request.form['action'] == 'Display Graph':
    #         data = cg.read_giturl(git_url)
    #         plt = cg.plot_graph(data)
    #         output = io.BytesIO()
    #         FigureCanvas(plt.get_figure()).print_png(output)
    #         return Response(output.getvalue(), mimetype='image/png')

    #     elif request.form['action']== 'Display Table':
    #         return "Table"

    #     return request.form['action']
        
    

    # @app.route("/add/<a>/<b>")
    # def add(a, b):
    #     """Return a greeting for the user."""
    #     return str(int(a)+int(b))


    # @app.route("/plot/<number_of_points>")
    # def random_plot(number_of_points):
    #     """Return a greeting for the user."""
    #     values = numpy.random.rand(int(number_of_points))
    #     plot.plot(values)
    #     plot.ylabel("Values")
    #     plot.title("Random Values")
    #     image = BytesIO()
    #     plot.savefig(image)
    #     image.seek(0)
    #     plot.close('all')
    #     return send_file(image, mimetype='image/png')


    app.run(host=options.address, port=options.port, debug=True)

def create_parser(subparsers):
    """Create an argument parser for the "serve" command."""
    parser = subparsers.add_parser("serve")
    parser.set_defaults(command=serve)
    # Add optional parameters to control the server configuration
    parser.add_argument("-p", "--port", default=8080, type=int, help="The port to listen on")
    parser.add_argument("--address", default="0.0.0.0", help="The address to listen on")
