"""Module for serving an API."""

<<<<<<< HEAD
from flask import Flask, send_file, request
from application.program import input_handler as inp
from application.program import create_graph as cg
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plot
from flask import Response
=======
from io import BytesIO
import matplotlib.pyplot as plot
import numpy
from flask import Flask, send_file
>>>>>>> dba39019f641092c4ce7d7eba85278bea5b59fd6



def serve(options):
    """Serve an API."""

    # Create a Flask application
    app = Flask(__name__)

<<<<<<< HEAD
    @app.route("/", methods=['POST','GET'])
=======

    

    @app.route("/")
>>>>>>> dba39019f641092c4ce7d7eba85278bea5b59fd6
    def index():
        """Return the index page of the website."""
        return send_file("../www/index.html")

    # @app.route("/extract/<url>", methods=['POST'])
    # def extract(url):
    #     git_csv = inp.extract_csv(url)
    #     with open("..\\csv_cache\\cache1.csv","w") as cache_csv:
    #         writer = csv.writer(cache_csv)
    #         writer.writerows(git_csv)
        
    #     return send_file("../www/index.html")

<<<<<<< HEAD
        


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
        
    
=======

    @app.route("/add/<a>/<b>")
    def add(a, b):
        """Return a greeting for the user."""
        return str(int(a)+int(b))


    @app.route("/plot/<number_of_points>")
    def random_plot(number_of_points):
        """Return a greeting for the user."""
        values = numpy.random.rand(int(number_of_points))
        plot.plot(values)
        plot.ylabel("Values")
        plot.title("Random Values")
        image = BytesIO()
        plot.savefig(image)
        image.seek(0)
        plot.close('all')
        return send_file(image, mimetype='image/png')



>>>>>>> dba39019f641092c4ce7d7eba85278bea5b59fd6
    app.run(host=options.address, port=options.port, debug=True)

def create_parser(subparsers):
    """Create an argument parser for the "serve" command."""
    parser = subparsers.add_parser("serve")
    parser.set_defaults(command=serve)
    # Add optional parameters to control the server configuration
    parser.add_argument("-p", "--port", default=8080, type=int, help="The port to listen on")
    parser.add_argument("--address", default="0.0.0.0", help="The address to listen on")
