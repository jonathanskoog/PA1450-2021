from application.program import create_graph as cg

def run(options):
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    data = cg.read_giturl(url)
    cg.plot_graph(data)

def create_parser(subparsers):

    parser = subparsers.add_parser("run")
    parser.set_defaults(command=run)
    # Add a required parameter to specify the user to greet
    parser.add_argument("-r", "--run_app", required=False, help="Run the app")