import streamlit as st
import pandas as pd
import plotly.express as px
import inputs as inp
from datetime import datetime
import numpy as np


year_col = inp.df.iloc[:, 0]  #1996 to 2050
installation_annual = inp.df.iloc[:, 1].copy()/1000 # reading and converting from MW to GW
AvgAnInsFrcst = 0
thisYear = datetime.now().year
installation_cum = installation_annual.copy()
installation_cum.iloc[0] = installation_annual.iloc[0]  # Start with the first year's installation
index2040 = year_col[year_col == 2040].index[0]
index2030 = year_col[year_col == 2030].index[0]
index2025 = year_col[year_col == 2025].index[0]
st.write(index2030)
for i in range(1, index2040): 
    installation_cum.iloc[i] = installation_cum.iloc[i-1] + installation_annual.iloc[i]


def forecast_installations(by2050):
    global installation_annual, installation_cum, AvgAnInsFrcst, thisYear
    thisYear = datetime.now().year
    index = year_col[year_col == thisYear].index[0]
    index1 = year_col[year_col == 2031].index[0]
    CumInstThisYear=np.sum(installation_annual.iloc[0:index])
    noOfYears= 2030 - (thisYear - 1)
    AvgAnInsFrcst = (by2050 - CumInstThisYear) / noOfYears
    installation_annual.iloc[30:index1] = AvgAnInsFrcst
    installation_cum = installation_annual.copy()
    installation_cum.iloc[0] = installation_annual.iloc[0]  # Start with the first year's installation
    for i in range(1, index1): #2025 to 2050
        installation_cum.iloc[i] = installation_cum.iloc[i-1] + installation_annual.iloc[i]
    
def show_forecast(AvgAnInsFrcst, thisYear):
    st.write(f"Projected average annual PV installations from {thisYear} to 2040: {AvgAnInsFrcst:.2f} GW")
    
def get_cum_installations_thisYear():
    thisYear = datetime.now().year
    index = year_col[year_col == thisYear].index[0]
    cum_installations_this_year = installation_cum.iloc[index-1]  # Cumulative installations up to this year
    return cum_installations_this_year

def get_cum_installations_2050():
    global index2030
    cum_installations_2050 = installation_cum.iloc[index2030]  # Cumulative installations in 2050
    return cum_installations_2050



  
