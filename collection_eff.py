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



def implement_collection(col_eff):
    global yearly_coll, annual_coll
    efficiency=col_eff/100
    ls.annualEoL = ls.annualEoL.astype(float) * efficiency
    ls.yearlyEoL = np.cumsum(ls.annualEoL)

def implement_collection_glass(col_eff):
    global yearly_coll, annual_coll
    efficiency=col_eff/100
    ls.annualEoL_gl = ls.annualEoL_gl.astype(float) * efficiency
    ls.yearlyEoL_gl = np.cumsum(ls.annualEoL_gl)

def implement_collection_al(col_eff):
    global yearly_coll, annual_coll
    efficiency=col_eff/100
    ls.annualEoL_al = ls.annualEoL_al.astype(float) * efficiency
    ls.yearlyEoL_al = np.cumsum(ls.annualEoL_al)

def implement_collection_si(col_eff):
    global yearly_coll, annual_coll
    efficiency=col_eff/100
    ls.annualEoL_si = ls.annualEoL_si.astype(float) * efficiency
    ls.yearlyEoL_si = np.cumsum(ls.annualEoL_si)

def implement_collection_cu(col_eff):
    global yearly_coll, annual_coll
    efficiency=col_eff/100
    ls.annualEoL_cu = ls.annualEoL_cu.astype(float) * efficiency
    ls.yearlyEoL_cu = np.cumsum(ls.annualEoL_cu)

def implement_collection_ag(col_eff):
    global yearly_coll, annual_coll
    efficiency=col_eff/100
    ls.annualEoL_ag = ls.annualEoL_ag.astype(float) * efficiency
    ls.yearlyEoL_ag = np.cumsum(ls.annualEoL_ag)
    
def implement_collection_rem(col_eff):
    global yearly_coll, annual_coll
    efficiency=col_eff/100
    ls.annualEoL_rem = ls.annualEoL_rem.astype(float) * efficiency
    ls.yearlyEoL_rem = np.cumsum(ls.annualEoL_rem)


