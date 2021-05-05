"""Module for serving an API."""

from io import BytesIO
import matplotlib.pyplot as plot
import numpy
from flask import Flask, send_file



def serve(options):
    """Serve an API."""

    # Create a Flask application
    app = Flask(__name__)


    

    @app.route("/")
    def index():
        """Return the index page of the website."""
        return send_file("../www/index.html")

    @app.route("/greeting/<name>")
    def greeting(name):
        """Return a greeting for the user."""
        return "Hello, {}!".format(name)


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



    app.run(host=options.address, port=options.port, debug=True)

def create_parser(subparsers):
    """Create an argument parser for the "serve" command."""
    parser = subparsers.add_parser("serve")
    parser.set_defaults(command=serve)
    # Add optional parameters to control the server configuration
    parser.add_argument("-p", "--port", default=8080, type=int, help="The port to listen on")
    parser.add_argument("--address", default="0.0.0.0", help="The address to listen on")
