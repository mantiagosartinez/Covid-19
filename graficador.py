# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 19:15:02 2020

@author: santi
"""

#Este codigo consta de armar una grafica de muertes y recuperados por país



import matplotlib
import numpy as np
import pandas as pd
from datetime import datetime

confirmed = "time_series_covid19_confirmed_global.csv"

deaths = "time_series_covid19_deaths_global.csv"

recovered = "time_series_covid19_recovered_global.csv"

cf = pd.read_csv(confirmed)


confirmed = cf.drop(columns = ["Province/State", "Lat", "Long"])
print(confirmed)
confirmed.T.rename(columns=confirmed["Country/Region"]).drop(index="Country/Region")
print(confirmed)
#plt.plot(confirmed.loc[6].index.values,confirmed.loc[6].values)

#print(dates,confirmed.iloc[6].values[1:])
#matplotlib.pyplot.plot_date(matplotlib.dates.date2num(confirmed.iloc[6].index.values[1:]), confirmed.loc[6].values)
#https://stackoverflow.com/questions/42372617/how-to-plot-csv-data-using-matplotlib-and-pandas-in-python
#cf['Country/Region'] = cf['Country/Region'].map(lambda x: datetime.strptime(str(x),
 # '%d/%m/%y.%f'))

"""
fig, ax = plt.subplots(figsize=(12, 12))

arg = confirmed.iloc[6]


ax.bar(confirmed.iloc[6].index.values,
       confirmed['DAILY_PRECIP'],
       color='purple')


ax.set(xlabel="Date",
       ylabel="Precipitation (inches)",
       title="Daily Total Precipitation\nJune - Aug 2005 for Boulder Creek")
#print(arg)

"""
"""
days = confirmed.columns

#confirmed.plot(x=days,y="Argentina")
arg.plot()
"""

#https://stackoverflow.com/questions/42372617/how-to-plot-csv-data-using-matplotlib-and-pandas-in-python