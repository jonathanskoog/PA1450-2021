from abc import ABC
from datetime import date
from datetime import timedelta
import pandas as pd
import calendar
import requests
import json

class filter(ABC):
    def exe(self):
        pass

class filter_period(filter):
    def __init__(self, country, filt_data, days=0, months=0):
        self.url_start = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
        self.country = country
        self.data = filt_data
        self.delta_days = days
        self.delta_mnths = months
        self.data_dict = {}
    
    def get_dates(self):
        today = date.today()
        start_recorded = date(2020, 1, 22)
        end_date = today - timedelta(days=1)
        start_date = self.remove_months(end_date, self.delta_mnths)
        start_date -= timedelta(days=self.delta_days)
        if (start_recorded > start_date):
            start_date = start_recorded
        return start_date, end_date

    def exe(self):
        if not self.data_dict:
            start_date, end_date = self.get_dates()
            url_lst = self.get_urls(start_date, end_date)
            data_dic = self.get_filtered_dataFrames(url_lst)
            self.data_dict = data_dic
        return self.data_dict


    def get_filtered_dataFrames(self, url_lst):
        data_dic = {"Date" : [], self.data : []}
        for i,url in enumerate(url_lst):
            file_date = url[112:122]
            df = pd.read_csv(url)
            row = df.loc[df["Country_Region"]==self.country, self.data]
            data_dic["Date"].append(file_date)
            data_dic[self.data].append(sum(row.tolist()))
        return data_dic
        

    def get_urls(self, start_date, end_date):
        url_lst = []
        period = end_date - start_date
        for i in range(0, period.days+1):
            temp_date = start_date + timedelta(days=i)
            temp_url = self.url_start + temp_date.strftime("%m-%d-%Y") + ".csv"
            url_lst.append(temp_url)
        return url_lst
    
    def remove_months(self, sourcedate, months):
        month = sourcedate.month - 1 - months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return date(year,month,day)


class filter_series(filter):
    def __init__(self, stat_type, series, country, population, days, months):
        self.country = country
        self.stat_type = stat_type
        self.population = population
        self.delta_days = days
        self.delta_mnths = months
        self.series = series
        self.url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_' + self.series + '_global.csv'
        self.data_dict = {}
    
    def exe(self):
        if(not self.data_dict):
            start_date, end_date = self.get_dates()
            data_dic = self.get_cases_by_date(start_date, end_date)
            self.data_dict = data_dic
        return self.data_dict

    def get_dates(self):
        today = date.today()
        start_recorded = date(2020, 1, 22)
        end_date = today - timedelta(days=1)
        start_date = self.remove_months(end_date, self.delta_mnths)
        start_date -= timedelta(days=self.delta_days+1)
        if (start_recorded > start_date):
            start_date = start_recorded
        return start_date, end_date
    
    def remove_months(self, sourcedate, months):
        month = sourcedate.month - 1 - months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return date(year,month,day)
    
    def get_cases_by_date(self, start_date, end_date):
        data_dict = {"Date":[], self.series:[]}
        period = end_date - start_date
        temp_frame = pd.read_csv(self.url)
        date_frame = temp_frame.loc[temp_frame["Country/Region"]==self.country]
        pre_date_data = 0
        for i in range(period.days + 1):
            temp_date = start_date + timedelta(days=i)
            str_date = str(temp_date.month) + "/" + str(temp_date.day) + "/" + str(temp_date.year)[2:]
            if self.stat_type != "Overall" and i != 0:
                data_dict["Date"].append(str_date)
                data_dict[self.series].append(date_frame.iloc[0][str_date]/self.population-pre_date_data)
            elif self.stat_type == "Overall":
                data_dict["Date"].append(str_date)
                data_dict[self.series].append(date_frame.iloc[0][str_date]/self.population)
            pre_date_data += (date_frame.iloc[0][str_date]/self.population) - pre_date_data
        return data_dict

    
class filter_comp_series(filter):
    def __init__(self, series1, series2, country, days, months):
        self.country = country
        self.series = (series1, series2)
        self.delta_days = days
        self.delta_mnths = months
        self.seriesUrls = [
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_' + series1 + '_global.csv',
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_' + series2 + '_global.csv'
        ]
        self.data_dict = {}
    
    def exe(self):
        if not self.data_dict:
            start_date, end_date = self.get_dates()
            data_dict = self.get_cases_by_date(start_date, end_date)
            self.data_dict = data_dict
        return self.data_dict
    
    def get_dates(self):
        today = date.today()
        start_recorded = date(2020, 1, 22)
        end_date = today - timedelta(days=1)
        start_date = self.remove_months(end_date, self.delta_mnths)
        start_date -= timedelta(days=self.delta_days)
        if (start_recorded > start_date):
            start_date = start_recorded
        return start_date, end_date
    
    def remove_months(self, sourcedate, months):
        month = sourcedate.month - 1 - months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return date(year,month,day)
    
    def get_cases_by_date(self, start_date, end_date):
        data_dict = {"Date":[], self.series[0]:[], self.series[1]:[]}
        period = end_date - start_date
        for j, url in enumerate(self.seriesUrls):
            temp_frame = pd.read_csv(url)
            date_frame = temp_frame.loc[temp_frame["Country/Region"]==self.country]
            for i in range(period.days + 1):
                temp_date = start_date + timedelta(days=i)
                date_str = str(temp_date.month) + "/" + str(temp_date.day) + "/" + str(temp_date.year)[2:]
                if j == 0:
                    data_dict["Date"].append(date_str)
                data_dict[self.series[j]].append(date_frame.iloc[0][date_str])
        return data_dict
                

class filter_newSeries(filter):
    def __init__(self, series, country, days, months):
        self.country = country
        self.delta_days = days
        self.delta_mnths = months
        self.series = series
        self.url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_' + self.series + '_global.csv'
        self.data_dict = {}
    
    def exe(self):
        if(not self.data_dict):
            start_date, end_date = self.get_dates()
            data_dic = self.get_cases_by_date(start_date, end_date)
            self.data_dict = data_dic
        return self.data_dict
        

    def get_dates(self):
        today = date.today()
        start_recorded = date(2020, 1, 22)
        end_date = today - timedelta(days=1)
        start_date = self.remove_months(end_date, self.delta_mnths)
        start_date -= timedelta(days=self.delta_days)
        if (start_recorded > start_date):
            start_date = start_recorded
        return start_date, end_date
    
    def remove_months(self, sourcedate, months):
        month = sourcedate.month - 1 - months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return date(year,month,day)
    
    def get_cases_by_date(self, start_date, end_date):
        data_dict = {"Date":[], self.series:[]}
        period = end_date - start_date
        temp_frame = pd.read_csv(self.url)
        date_frame = temp_frame.loc[temp_frame["Country/Region"]==self.country]
        for i in range(period.days + 1):
            temp_date = start_date + timedelta(days=i)
            total_date = temp_date -timedelta(days=1)
            date_str = str(temp_date.month) + "/" + str(temp_date.day) + "/" + str(temp_date.year)[2:]
            pre_date_str = str(total_date.month) + "/" + str(total_date.day) + "/" + str(total_date.year)[2:]
            data_dict["Date"].append(date_str)
            if not data_dict[self.series]:
                data_dict[self.series].append(date_frame.iloc[0][date_str] - date_frame.iloc[0][pre_date_str])
            else:
                data = date_frame.iloc[0][date_str] - date_frame.iloc[0][pre_date_str]
                data_dict[self.series].append(data) # - data_dict[self.series][i-1]
        return data_dict


class filter_population(filter):
    def __init__(self, country):
        self.country = country
        self.api_url = 'https://restcountries.eu/rest/v2/name/{}?fullText=true'.format(country)

    def exe(self):
        response = requests.get(self.api_url)
        return response.json()[0]["population"]


class filter_casesPerSeries(filter):
    def __init__(self, stat_type, population,series, country, days, months):
        self.stat_type = stat_type
        self.population = population
        self.country = country
        self.delta_days = days
        self.delta_mnths = months
        self.series = series
        self.url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_' + self.series + '_global.csv'
        self.data_dict = {}
    
    def exe(self):
        if(not self.data_dict):
            start_date, end_date = self.get_dates()
            data_dic = self.get_cases_by_date(start_date, end_date)
            self.data_dict = data_dic
        return self.data_dict
        

    def get_dates(self):
        today = date.today()
        start_recorded = date(2020, 1, 22)
        end_date = today - timedelta(days=1)
        start_date = self.remove_months(end_date, self.delta_mnths)
        start_date -= timedelta(days=self.delta_days)
        if (start_recorded > start_date):
            start_date = start_recorded
        return start_date, end_date
    
    def remove_months(self, sourcedate, months):
        month = sourcedate.month - 1 - months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return date(year,month,day)
    
    def get_cases_by_date(self, start_date, end_date):
        data_dict = {"Date":[], self.series:[]}
        period = end_date - start_date
        temp_frame = pd.read_csv(self.url)
        date_frame = temp_frame.loc[temp_frame["Country/Region"]==self.country]
        for i in range(period.days + 1):
            temp_date = start_date + timedelta(days=i)
            total_date = temp_date -timedelta(days=1)
            date_str = str(temp_date.month) + "/" + str(temp_date.day) + "/" + str(temp_date.year)[2:]
            pre_date_str = str(total_date.month) + "/" + str(total_date.day) + "/" + str(total_date.year)[2:]
            data_dict["Date"].append(date_str)
            if self.stat_type == "Overall":
                data_dict[self.series].append(date_frame.iloc[0][date_str])
            elif not data_dict[self.series]:
                data_dict[self.series].append((date_frame.iloc[0][date_str] - date_frame.iloc[0][pre_date_str])/self.population)
            else:
                data = (date_frame.iloc[0][date_str] - date_frame.iloc[0][pre_date_str])/self.population
                data_dict[self.series].append(data) # - data_dict[self.series][i-1]
        return data_dict
    
class filter_casesPerRegion(filter):
    def __init__(self, stat_type, filt_data, population, country, region, days):
        self.stat_type = stat_type
        self.population = population
        self.filt_data = filt_data
        self.country = country
        self.region = region
        self.delta_days = days
        self.start_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
        self.data_dict = {}

    def exe(self):
        if not self.data_dict:
            start_date, end_date = self.get_days()
            data_dict = self.get_cases_by_date(start_date, end_date)
            self.data_dict = data_dict
        return self.data_dict

    def get_days(self):
        today = date.today()
        end_date = today - timedelta(days=1)
        start_date = end_date - timedelta(days=self.delta_days)
        if self.stat_type != "Overall":
            start_date = end_date - timedelta(days=self.delta_days+1)
        return start_date, end_date

    def get_cases_by_date(self, start_date, end_date):
        data_dict = {"Date":[], self.region:[]}
        period = end_date - start_date
        pre_date_data = 0
        for i in range(period.days + 1):
            # Creating correct date and creating correct url
            current_date = start_date + timedelta(days=i)
            str_date = current_date.strftime("%m-%d-%Y")
            url = self.start_url + str_date + '.csv'
            
            # Overall dataframe
            df = pd.read_csv(url)

            # Dataframe for the choosen country
            country_rows = df.loc[(df["Country_Region"]==self.country) & (df['Province_State']==self.region), self.filt_data]
            if self.stat_type != "Overall" and i != 0:
                data_dict["Date"].append(str_date)
                data_dict[self.region].append(country_rows.tolist()[0]/self.population-pre_date_data)
            elif self.stat_type == "Overall":
                data_dict["Date"].append(str_date)
                data_dict[self.region].append(country_rows.tolist()[0]/self.population)
            pre_date_data += (country_rows.tolist()[0]/self.population) - pre_date_data
        return data_dict

                    
# class filter_top(filter):
#     def __init__(self, perCapita, stat_type, series, amount):
#         self.url = ""
#         self.amount = amount
#         self.stat_type = stat_type
#         self.perCapita = perCapita
#         self.data_dict = {}
#         self.population = population
    
#     def exe(self):
#         if not self.data_dict:
#             end_date = date.today() - timedelta(days=1)

    
#     def get_data(self, end_date):
#         data_dict = {"Country":[], self.series:[]}
#         latest_date = end_date - timedelta(days=1)
#         pre_date_str = str(latest_date.month) + "/" + str(latest_date.day) + "/" + str(temp_date.year)[2:]
#         date_str = str(end_date.month) + "/" + str(end_date.day) + "/" + str(end_date.year)[2:]







            
