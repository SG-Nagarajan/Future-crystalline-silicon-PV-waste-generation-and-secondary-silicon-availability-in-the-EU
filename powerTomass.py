import streamlit as st
import pandas as pd
import plotly.express as px
import inputs as inp
from datetime import datetime
import numpy as np
import installations as inst
import marketShare as ms


# MW to Tonnes Conversion

import numpy as np
weight_cSi = np.zeros(len(inst.year_col))
cum_weight_cSi2050 = np.zeros(len(inst.year_col))
cum_weight_cSi_thisYear = np.zeros(len(inst.year_col))
cum_weight_cSi_thisYear1 = np.zeros(len(inst.year_col))
curve_PVICE = inp.df.iloc[:, 7].copy()  # PVICE curve data from the input file
curve_silicon = inp.df.iloc[:, 10]
curve_glass = inp.df.iloc[:, 9]
curve_aluminium = inp.df.iloc[:, 11]
curve_copper = inp.df.iloc[:, 12]
curve_silver = inp.df.iloc[:, 13]
wt_silicon=0
wt_glass=0
wt_aluminium=0
wt_copper=0
wt_silver=0
wt_remains=0
curve_remains = 100 - (
    inp.df.iloc[:, 9] +
    inp.df.iloc[:, 10] +
    inp.df.iloc[:, 11] +
    inp.df.iloc[:, 12] +
    inp.df.iloc[:, 13]
)
curve_remains[55:] = 0 #make zero after 2050

years = inst.year_col.iloc[:55] 
curve_massPerMW = np.zeros(len(years))

def calc_curve_massPerMW(variable):
    global curve_massPerMW
    curve_massPerMW = 1.11 * (10**20) * np.exp(-years / variable)  # Exponential decay curve with a variable decay rate

def calc_curve_massPerMW1(variable1, variable2, variable3):
    global curve_massPerMW1
    curve_massPerMW1 = variable1 * (10**variable3) * np.exp(-years / variable2)  # Exponential decay curve with a variable decay rate


def get_weight_cSi():
    global curve_massPerMW, weight_cSi, curve_PVICE
    weight_cSi = curve_massPerMW * ms.c_SiInstallations * 1000


def get_cum_weight_cSi_2050():
    global cum_weight_cSi2050
    cum_weight_cSi2050 = np.sum(weight_cSi[:56])  # Cumulative c-Si weight up to 2050    
    return cum_weight_cSi2050

def get_weight_cSi_PVICE():
    global curve_massPerMW, weight_cSi, curve_PVICE 
    weight_cSi = curve_PVICE * ms.c_SiInstallations * 1000
    

def get_cum_weight_cSi_thisYear():
    global cum_weight_cSi_thisYear
    cum_weight_cSi_thisYear = np.sum(weight_cSi[:inst.index2025])  # Cumulative c-Si weight for the current year    
    return cum_weight_cSi_thisYear
def get_weight_materials(): 
    global wt_silicon, wt_glass, wt_aluminium, wt_copper,wt_silver, weight_cSi, wt_remains
    wt_silicon=(curve_silicon*ms.c_SiInstallations*1000)

    

    wt_glass=(curve_glass/100)*weight_cSi
    wt_aluminium=(curve_aluminium/100)*weight_cSi
    wt_copper=(curve_copper/100)*weight_cSi
    wt_silver=(curve_silver/100)*weight_cSi
    wt_remains=(curve_remains/100)*weight_cSi
