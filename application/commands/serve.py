"""Module for serving an API."""

from flask import Flask, send_file, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plot
from flask import Response



def serve(options):
    """Serve an API."""

    # Create a Flask application
    app = Flask(__name__)

    @app.route("/", methods=['POST','GET'])
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
