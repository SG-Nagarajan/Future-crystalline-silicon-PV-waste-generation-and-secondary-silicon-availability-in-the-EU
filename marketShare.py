import streamlit as st
import pandas as pd
import plotly.express as px
import inputs as inp
from datetime import datetime
import numpy as np
import installations as inst



marketShare = np.zeros(len(inst.year_col))  
c_SiInstallations = np.zeros(len(inst.year_col))  

def get_column_index(number):
    global marketShare
    marketShare = inp.df.iloc[:, number]  # Convert percentage to decimal
   


#_________________________________________________________________________plots

# c-Si PV Installations
def calc_cSi_installations():
    global c_SiInstallations, marketShare
    c_SiInstallations = inst.installation_annual * marketShare


def get_cum_cSi_2050 ():
    cum_cSi = np.sum(c_SiInstallations[:56])  # Cumulative c-Si installations up to 2050    
    return cum_cSi

def get_cum_cSi_thisYear ():
    thisYear = datetime.now().year
    index = inst.year_col[inst.year_col == thisYear].index[0]
    cum_cSi = np.sum(c_SiInstallations[:index])  # Cumulative c-Si installations up to 2050    
    return cum_cSi