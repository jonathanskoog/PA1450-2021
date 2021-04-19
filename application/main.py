"""Main module of the application"""

from argparse import ArgumentParser

from application.commands import serve, greet

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

    # Parse the arguments and execute the chosen command
    options = parser.parse_args()
    options.command(options)
    print("hej")
    print("bjbhjbhj")

if __name__ == "__main__":
    main()
