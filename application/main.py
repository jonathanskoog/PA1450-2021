"""Main module of the application"""

# from argparse import ArgumentParser

<<<<<<< HEAD
from application.commands import serve, greet, run
=======
# from application.commands import serve, greet

# import pandas as pd
# import matplotlib.pyplot as plt
# import plotly.express as px


>>>>>>> dba39019f641092c4ce7d7eba85278bea5b59fd6

from application.program import create_graph

def main():
    """Main method of the application."""
    # Create an argument parser for parsing CLI arguments
<<<<<<< HEAD
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
=======
    # parser = ArgumentParser(description="An example application")
    # # Create collection of subparsers, one for each command such as "download"
    # subparsers = parser.add_subparsers(dest="command")
    # subparsers.required = True

    # # Add the parser for each specific command
    # serve.create_parser(subparsers)
    # greet.create_parser(subparsers)

    # # Parse the arguments and execute the chosen command
    # options = parser.parse_args()
    # options.command(options)
    


    # plt.style.use("bmh")
    # # df = pd.read_csv('prices.csv')
    # df = pd.read_csv('covid_stats.csv')

    
    # x = df['Province_State']
    # y = df['Deaths']


    # plt.xlabel('Province_State', fontsize=18)
    # plt.ylabel('Deaths', fontsize=16)
    # plt.scatter(x, y)
    # plt.plot(x, y)

    # plt.savefig('foo.png', bbox_inches='tight')

    # plt.show()
    







    # fig = px.line(df, x = 'AAPL_x', y = 'AAPL_y', title='Apple Share Prices over time (2014)')
    # fig.show()
>>>>>>> dba39019f641092c4ce7d7eba85278bea5b59fd6

if __name__ == "__main__":
    main()
