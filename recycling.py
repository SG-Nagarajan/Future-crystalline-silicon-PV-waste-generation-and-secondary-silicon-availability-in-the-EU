import streamlit as st
import pandas as pd
import plotly.express as px
import inputs as inp
from datetime import datetime
import numpy as np
import installations as inst
import marketShare as ms
import powerTomass as ptm
import lossScenarios as ls
import plots as pl


def glass_recycling(col_eff):
    efficiency=col_eff/100
    ls.annualEoL_gl = ls.annualEoL_gl.astype(float) * efficiency
    ls.yearlyEoL_gl = np.cumsum(ls.annualEoL_gl)

    
def silicon_recycling(col_eff):
    efficiency=col_eff/100
    ls.annualEoL_si = ls.annualEoL_si.astype(float) * efficiency
    ls.yearlyEoL_si = np.cumsum(ls.annualEoL_si)

    
def aluminium_recycling(col_eff):
    efficiency=col_eff/100
    ls.annualEoL_al = ls.annualEoL_al.astype(float) * efficiency
    ls.yearlyEoL_al = np.cumsum(ls.annualEoL_al)


    
def copper_recycling(col_eff):
    efficiency=col_eff/100
    ls.annualEoL_cu = ls.annualEoL_cu.astype(float) * efficiency
    ls.yearlyEoL_cu = np.cumsum(ls.annualEoL_cu)


    
def silver_recycling(col_eff):
    efficiency=col_eff/100
    ls.annualEoL_ag = ls.annualEoL_ag.astype(float) * efficiency
    ls.yearlyEoL_ag = np.cumsum(ls.annualEoL_ag)


    
def remaining_recycling(col_eff):
    efficiency=col_eff/100
    ls.annualEoL_rem = ls.annualEoL_rem.astype(float) * efficiency
    ls.yearlyEoL_rem = np.cumsum(ls.annualEoL_rem)
