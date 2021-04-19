def run(options):
    """Run"""
    print("Run!")

def create_parser(subparsers):
    parser = subparsers.add_parser("run")
    parser.set_defaults(command=run)
    # Add a required parameter to specify the user to greet
    parser.add_argument("-r", "--python_file", required=False, help="The command to run")