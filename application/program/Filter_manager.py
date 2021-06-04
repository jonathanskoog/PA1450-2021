from application.program import filter

class Filter_manager:
    def __init__(self):
        self.commands = {
            "period" : filter.filter_period,
            "series" : filter.filter_series,
            "compSeries": filter.filter_comp_series,
            "newSeries" : filter.filter_newSeries,
            "population": filter.filter_population,
            "perCapita" : filter.filter_casesPerSeries,
            "perRegion" : filter.filter_casesPerRegion
        }

    def command(self, cmd_str):
        if cmd_str not in self.commands:
            raise KeyError
        return self.commands[cmd_str]