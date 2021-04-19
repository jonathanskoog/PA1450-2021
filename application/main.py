"""Main module of the application"""

from argparse import ArgumentParser

from application.commands import serve, greet

import pandas as pd
import plotly.express as px




def main():
    """Main method of the application."""
    # Create an argument parser for parsing CLI arguments
    parser = ArgumentParser(description="An example application")
    # Create collection of subparsers, one for each command such as "download"
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    # Add the parser for each specific command
    serve.create_parser(subparsers)
    greet.create_parser(subparsers)
    run.create_parser(subparsers)

    # Parse the arguments and execute the chosen command
    options = parser.parse_args()
    options.command(options)
    
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv')

    fig = px.line(df, x = 'AAPL_x', y = 'AAPL_y', title='Apple Share Prices over time (2014)')
    fig.show()

if __name__ == "__main__":
    main()
