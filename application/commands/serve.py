"""Module for serving an API."""

from flask import Flask, send_file, request

from io import BytesIO
import matplotlib.pyplot as plot
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Response
from matplotlib.figure import Figure
import csv
import pandas as pd
import os
import io
from shutil import copyfile
from application.program import Filter_manager as filt_mangr
from application.program import Graph

from bs4 import BeautifulSoup as html_parser


manager = filt_mangr.Filter_manager()

def serve(options):
    """Serve an API."""

    # Create a Flask application
    app = Flask(__name__)

    @app.route("/", methods=['POST','GET'])
    def index():
        """Return the index page of the website."""
        return send_file("../www/test.html")
    
    @app.route("/test_scripts.js", methods=['GET'])
    def get_script():
        return send_file("../www/test_scripts.js")

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
    
    @app.route("/createGraphPeriod/<country>/<filt_data>/<days>/<months>", methods=["POST","GET"])
    def createGraphPeriod(country, filt_data, days, months):
        filtr = manager.command("period")(country, filt_data, int(days), int(months))
        data_dict = filtr.exe()
        df = pd.DataFrame(data=data_dict)
        grph = Graph.Graph(df, (14,6))
        grph.set_axis("Date", filt_data)
        img = grph.get_image()
        return Response(img.getvalue(), mimetype='image/png')

        # plt = df.plot(x="Date", y=filt_data, figsize=(14,6))
        # fig = plt.get_figure()
        # image = io.BytesIO()
        # FigureCanvas(plt.get_figure()).print_png(image)
        # return Response(image.getvalue(), mimetype='image/png')

    @app.route("/createGraphSeries/<stat_type>/<perCapita>/<series>/<country>/<days>/<months>", methods=["GET"])
    def createGraphSeries(stat_type, perCapita, series, country, days, months):
        population = 1
        if perCapita == "Capita":
            pop_filtr = manager.command("population")(country)
            population = pop_filtr.exe()
        filtr = manager.command("series")(stat_type, series, country, population,int(days), int(months))
        data_dict = filtr.exe()
        df = pd.DataFrame(data=data_dict)
        grph = Graph.Graph(df, (14,6))
        grph.set_axis("Date", series)
        img = grph.get_image()
        return Response(img.getvalue(), mimetype='image/png')
    
    @app.route("/compareGraphSeries/<series1>/<series2>/<country>/<days>/<months>", methods=["GET"])
    def compareGraphSeries(series1, series2, country, days, months):
        filtr = manager.command("compSeries")(series1, series2, country, int(days), int(months))
        data_dict = filtr.exe()
        grph_dict1 = {"Date": data_dict["Date"], series1 : data_dict[series1]}
        grph_dict2 = {"Date": data_dict["Date"], series2 : data_dict[series2]}
        df1 = pd.DataFrame(data=grph_dict1)
        df2 = pd.DataFrame(data=grph_dict2)
        fig = plot.figure()
        ax = df1.plot(x="Date", y=series1, figsize=(14,6))
        ax2 = df2.plot(x="Date", y=series2, figsize=(14,6), ax=ax)
        img = Graph.imagify(ax2)
        return Response(img.getvalue(), mimetype='image/png')

    @app.route("/newCasesSeries/<series>/<country>/<days>/<months>", methods=['GET'])
    def newCasesSeries(series, country, days, months):
        filtr = manager.command("newSeries")(series, country, int(days), int(months))
        data_dict = filtr.exe()
        grph_frame = pd.DataFrame(data=data_dict)
        grph = Graph.Graph(grph_frame, (14,6))
        grph.set_axis("Date", series)
        grph.set_kind("bar")
        img = grph.get_image()
        return Response(img.getvalue(), mimetype="image/png")
    
    @app.route("/seriesPerCapita/<stat_type>/<series>/<country>/<days>/<months>", methods=['GET'])
    def newSeriesPerCapita(stat_type, series, country, days, months):
        pop_filtr = manager.command("population")(country)
        population = pop_filtr.exe()
        perCap_filtr = manager.command("perCapita")(stat_type, population, series, country, int(days), int(months))
        data_dict = perCap_filtr.exe()
        grph_frame = pd.DataFrame(data=data_dict)
        grph = Graph.Graph(grph_frame, (14,6))
        grph.set_axis("Date", series)
        img = grph.get_image()
        return Response(img.getvalue(), mimetype="image/png")
    
    @app.route("/casesPerRegion/<stat_type>/<perCapita>/<series>/<country>/<region>/<days>", methods=['GET'])
    def casesPerRegion(stat_type, perCapita, series, country, region, days):
        series = series.capitalize()
        population = 1
        if perCapita == "Capita":
            pop_filtr = manager.command("population")(country)
            population = pop_filtr.exe()
        reg_filtr = manager.command("perRegion")(stat_type, series, population, country, region, int(days))
        data_dict = reg_filtr.exe()
        grph_frame = pd.DataFrame(data=data_dict)
        grph = Graph.Graph(grph_frame, (14,6))
        grph.set_axis("Date", region)
        grph.set_labels("Date", series)
        grph.set_kind("bar")
        img = grph.get_image()
        return Response(img.getvalue(), mimetype="image/png")

    @app.route("/placeHolderGraph", methods=['GET'])
    def placeHolderGraph():
        fig = plot.figure()
        canvas = FigureCanvas(fig)
        return Response(canvas, mimetype="image/png")

    @app.route("/plotGraph", methods=['POST'])
    def plotGraph():
        country = request.form["country"]
        if (not country):
            country = "Country/Region"
        # Get countries data
        x_axis = country
        y_axis = request.form["y_axis"]

        data = pd.read_csv("application/csv_cache/cache1.csv",delimiter=',', header=0, encoding='ascii')
        if (country != "Country/Region"):
            print(data.loc[data["Country/Region"]==country])
            data = data.loc[data["Country/Region"]==country]
            x_axis = "Province/State"

        plt = data.plot(x=x_axis, y=y_axis, kind="bar")
        fig = plt.get_figure()
        fig.savefig("application/csv_cache/graphPNG.png")
        image = io.BytesIO()
        FigureCanvas(plt.get_figure()).print_png(image)
        return Response(image.getvalue(), mimetype='image/png')
    
    @app.route("/displayGraph", methods=['GET'])
    def displayGraph():
        return send_file("../csv_cache/graphPNG.png", mimetype="image/gif")

    @app.route("/saveGraph", methods=['POST'])
    def saveGraph():
        copyfile("application/csv_cache/graphPNG.png", "/home/pa1450/Downloads/download.png")
        return "success"

    # @app.route("/drawTableSeries/",methods=['GET'])

    @app.route("/drawTABLE", methods=["GET"])
    def drawTABLE():
        #csv_url = request.form["csv_file"]
        # https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/05-19-2021.csv
        a = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/05-19-2021.csv")
        html_table = a.to_html()

        # write html to file
        # text_file = open("application/www/table.html", "w")

        # text_file.write("\n<html>\n<head>\n")
        
        # text_file.write("<link rel=\"stylesheet\" href=\"table.css\">\n")

        # text_file.write("</head>\n<body>\n")

        # text_file = open("application/www/table.html", "a")

        # with open ("output.html", "r") as text:
        #     data = text.read()
        #     text_file.write(data)


        # text_file.write("<button id=\"convert\">\n") 
        # text_file.write("Convert to image\n")
        # text_file.write("</button>\n") 


        # text_file.write("<div id=\"result\"\n>") 
        # text_file.write("</div>\n") 

        # text_file.write("<script type=\"text/javascript\" src=\"https://github.com/niklasvh/html2canvas/releases/download/0.5.0-alpha1/html2canvas.js\"></script>\n")

        # text_file.write("<script>\n"
        #  "function convertToImage() {"
        #     "var resultDiv = document.getElementById(\"result\");"
        #     "html2canvas(document.getElementByClass(\"dataframe\"), {"
        #         "onrendered: function(canvas) {"
        #             "var img = canvas.toDataURL(\"image/png\");"
        #             "result.innerHTML = '<a download=\"test.jpeg\" href=\"'+img+'\">test</a>';"
        #             "}"
        #     "});"
        #  "}"     

        #  "var convertBtn = document.getElementById('convert');"
        #  "convertBtn.addEventListener('click', convertToImage);\n"
        # "</script>\n")
       

        # text_file.write("\n<form action=""/"" method=""post"" enctype=""multipart/form-data"">\n") 

        # text_file.write("<button type='Index' id='button1' name='action' class='btn btn-primary btn-block bg-lg'>Return to index page!</button>\n")
        # text_file.write("</form>\n") 

        # text_file.write("\n</body>\n</html>\n")
        
        

        # text_file.close()


        return Response(html_table, mimetype="html")


    


    @app.route("/getPictures/<img>" , methods=["GET"])
    def getPictures(img):
        file_name = "../Pictures/" + img
        return send_file(file_name, mimetype="image/png")





    app.run(host=options.address, port=options.port, debug=True)

def create_parser(subparsers):
    """Create an argument parser for the "serve" command."""
    parser = subparsers.add_parser("serve")
    parser.set_defaults(command=serve)
    # Add optional parameters to control the server configuration
    parser.add_argument("-p", "--port", default=8080, type=int, help="The port to listen on")
    parser.add_argument("--address", default="0.0.0.0", help="The address to listen on")
