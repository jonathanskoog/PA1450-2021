import pandas as pd
def test(options):
    """Greet a user."""
    print()

def create_parser(subparsers):
    """Create an argument parser for the "greet" command."""
    parser = subparsers.add_parser("test")
    parser.set_defaults(command=test)
    # Add a required parameter to specify the user to greet
    parser.add_argument("-t", "--test", required=False, help="")