"""Module for serving an API."""

from flask import Flask, send_file, request

from io import BytesIO
import matplotlib.pyplot as plot
from flask import Response
import csv
import pandas as pd
import os

from bs4 import BeautifulSoup as html_parser



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
            with open("application/csv_cache/cache1.csv", "w") as csv_file:
                csv_file.write(csv_data.to_string())
            return "success"
        except:
            return "error"





    @app.route("/drawTABLE", methods=["Post"])
    def drawTABLE():
        #csv_url = request.form["csv_file"]
     
        
        a = pd.read_csv("/home/pa1450/PA1450-2021/application/csv_cache/cache1.csv")
        a.to_html("output.html")





        # write html to file
        text_file = open("application/www/table.html", "w")

        text_file.write("\n<html>\n<head>\n")
        
        text_file.write("<link rel=\"stylesheet\" href=\"table.css\">\n")

        text_file.write("</head>\n<body>\n")

        text_file = open("application/www/table.html", "a")

        with open ("output.html", "r") as text:
            data = text.read()
            text_file.write(data)


        text_file.write("<button id=\"convert\">\n") 
        text_file.write("Convert to image\n")
        text_file.write("</button>\n") 


        text_file.write("<div id=\"result\"\n>") 
        text_file.write("</div>\n") 

        text_file.write("<script type=\"text/javascript\" src=\"https://github.com/niklasvh/html2canvas/releases/download/0.5.0-alpha1/html2canvas.js\"></script>\n")

        text_file.write("<script>\n"
         "function convertToImage() {"
            "var resultDiv = document.getElementById(\"result\");"
            "html2canvas(document.getElementByClass(\"dataframe\"), {"
                "onrendered: function(canvas) {"
                    "var img = canvas.toDataURL(\"image/png\");"
                    "result.innerHTML = '<a download=\"test.jpeg\" href=\"'+img+'\">test</a>';"
                    "}"
            "});"
         "}"     

         "var convertBtn = document.getElementById('convert');"
         "convertBtn.addEventListener('click', convertToImage);\n"
        "</script>\n")
       

        text_file.write("\n<form action=""/"" method=""post"" enctype=""multipart/form-data"">\n") 

        text_file.write("<button type='Index' id='button1' name='action' class='btn btn-primary btn-block bg-lg'>Return to index page!</button>\n")
        text_file.write("</form>\n") 

        text_file.write("\n</body>\n</html>\n")
        
        

        text_file.close()


        return send_file("../www/table.html")


    





    app.run(host=options.address, port=options.port, debug=True)

def create_parser(subparsers):
    """Create an argument parser for the "serve" command."""
    parser = subparsers.add_parser("serve")
    parser.set_defaults(command=serve)
    # Add optional parameters to control the server configuration
    parser.add_argument("-p", "--port", default=8080, type=int, help="The port to listen on")
    parser.add_argument("--address", default="0.0.0.0", help="The address to listen on")
