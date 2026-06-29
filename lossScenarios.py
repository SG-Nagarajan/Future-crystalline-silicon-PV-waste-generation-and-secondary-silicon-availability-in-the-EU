import streamlit as st
import pandas as pd
import plotly.express as px
import inputs as inp
from datetime import datetime
import numpy as np
import installations as inst
import marketShare as ms
import powerTomass as ptm






PVage = np.arange(1, len(inst.year_col) + 1)   # ✅ NumPy array
EarlyLoss = np.zeros(len(inst.year_col))
RegularLoss = np.zeros(len(inst.year_col))
EUWEEE = np.zeros(len(inst.year_col))
User=np.zeros(len(inst.year_col))
yealryEoL = np.zeros(len(inst.year_col))
annualEoL = np.zeros(len(inst.year_col))
reuse_cum = np.zeros(len(inst.year_col))
reuse_ann = np.zeros(len(inst.year_col))
reuse_cum_si = np.zeros(len(inst.year_col))
reuse_ann_si = np.zeros(len(inst.year_col))

yealryEoL_si = np.zeros(len(inst.year_col))
annualEoL_si = np.zeros(len(inst.year_col))


EarlyLoss_cum = np.zeros(len(inst.year_col))
EarlyLoss_ann = np.zeros(len(inst.year_col))
RegularLoss_cum = np.zeros(len(inst.year_col))
RegularLoss_ann = np.zeros(len(inst.year_col))
EUWEEE_cum = np.zeros(len(inst.year_col))
EUWEEE_ann = np.zeros(len(inst.year_col))

EarlyLoss_cum_si = np.zeros(len(inst.year_col))
EarlyLoss_ann_si = np.zeros(len(inst.year_col))
RegularLoss_cum_si = np.zeros(len(inst.year_col))
RegularLoss_ann_si = np.zeros(len(inst.year_col))
EUWEEE_cum_si = np.zeros(len(inst.year_col))
EUWEEE_ann_si = np.zeros(len(inst.year_col))


yealryEoL_reuse = np.zeros(len(inst.year_col))
annualEoL_reuse = np.zeros(len(inst.year_col))
reuseAge=0
reusepercent=100
alpha=2.4928
beta=30
five=0
fifteen=0
twentyFive=0



def calc_loss_scenarios():
    global PVage, EarlyLoss, RegularLoss, EUWEEE, User, alpha, beta
    # Weibull
    EarlyLoss = 1 - np.exp(-((PVage / 30) ** 2.4928))
    # Weibull
    RegularLoss = 1 - np.exp(-((PVage / 30) ** 5.3759))
    # Weibull
    EUWEEE = 1 - np.exp(-((PVage / 25) ** 3.5))
    # User
    User = 1 - np.exp(-((PVage / beta) ** alpha))

# CALCULATE LOSSES_____________________________________________________________________________
def calc_eol(loss):
    global yearlyEoL
    ten=loss[10]
    twenty=loss[20]
    thirty=loss[30]
    n = len(inst.year_col)

    # ✅ Compute once (no repetition ✅)
    waste = np.outer(ptm.weight_cSi, loss)

    cumWaste = np.zeros((n, n))

    for start_j in range(n - 1, -1, -1):
        i = 0
        j = start_j

        while j >= 0 and i < n:
            cumWaste[i, j] += ptm.weight_cSi[i] * loss[j]
            i += 1
            j -= 1

    # _________________________________________________________________________yeALY WASTE

    n = cumWaste.shape[0]

    diag_sums = []

    for start_j in range(n - 1, -1, -1):
        i = 0
        j = start_j
        s = 0

        while j >= 0 and i < n:
            s += cumWaste[i, j]
            i += 1
            j -= 1

        diag_sums.append(s)

    yearlyEoL = diag_sums[::-1]

    diag_sums = np.array(diag_sums)
 

    # ______________________________________________________________________________
    
def calc_annual_eol():
    global yearlyEoL, annualEoL, reuse_cum
    yearlyEoL = np.array(yearlyEoL)
    annualEoL = yearlyEoL[1:] - yearlyEoL[:-1]


def calc_eol_reuse(loss):
    global yearlyEoL, ten, twenty, thirty
    loss_sub = np.zeros(len(inst.year_col))
    n = len(inst.year_col)
    # ✅ Compute once (no repetition ✅)
    
    if reuseAge > 0:
        loss_sub=loss.copy()
        loss_sub[:reuseAge]= loss_sub[:reuseAge]*(reusepercent/100)
    else: 
        loss_sub=loss.copy()
    waste = np.outer(ptm.weight_cSi, loss_sub)
    
    cumWaste = np.zeros((n, n))
    cumWaste_noReuse = np.zeros((n, n))
    cumWaste_reuse_matrix = np.zeros((n, n))
    reuse = np.zeros((n, n))
    reuse_12 = np.zeros((n, n))
    for start_j in range(n - 1, -1, -1):
        i = 0
        j = start_j
        while j >= 0 and i < n:
            cumWaste[i, j] += (ptm.weight_cSi[i] * loss_sub[j])
            i += 1
            j -= 1
    for start_j in range(n - 1, -1, -1):
        i = 0
        j = start_j
        while j >= 0 and i < n:
            cumWaste_noReuse[i, j] += (ptm.weight_cSi[i] * loss[j])
            i += 1
            j -= 1
    # _________________________________________________________________________yeALY WASTE
    
    
    col_12_noReuse = cumWaste_noReuse[:, (reuseAge-1)]
    col_12 = cumWaste[:, (reuseAge-1)]
    
    for i in range(n):
        for j in range(n):
            if cumWaste[i, j] != 0:
                if j < reuseAge:
                    reuse[i, j] = cumWaste[i, j]
                else:
                    reuse[i, j] = cumWaste[i, j] - (col_12_noReuse[i] - col_12[i])


    n = cumWaste.shape[0]
    cumWaste_reuse_matrix = cumWaste_noReuse - reuse
    diag_sums = []
    diag_sums_reuse = []
    
    for start_j in range(n - 1, -1, -1):
        i = 0
        j = start_j
        s = 0
        p = 0

        while j >= 0 and i < n:
            s += reuse[i, j]
            p += cumWaste_reuse_matrix[i, j]
            i += 1
            j -= 1

        diag_sums.append(s)
        diag_sums_reuse.append(s)
    yearlyEoL = diag_sums[::-1]
    reuse_cum = diag_sums_reuse[::-1]
    diag_sums = np.array(diag_sums)


    # ______________________________________________________________________________
    
def calc_annual_eol_reuse():
    global yearlyEoL, annualEoL, reuse_ann, reuse_cum
    yearlyEoL = np.array(yearlyEoL)
    annualEoL[1:] = yearlyEoL[1:] - yearlyEoL[:-1]
    reuse_ann[1:] = reuse_cum[1:] - reuse_cum[:-1]



#============================Materials==================================================


#============================silicon==================================================

def calc_eol_si(wt_si, loss):
    global yearlyEoL_si, reuse_cum_si, reuse_ann_si
    loss_sub = np.zeros(len(inst.year_col))
    n = len(inst.year_col)
    # ✅ Compute once (no repetition ✅)
    
    if reuseAge > 0:
        loss_sub=loss.copy()
        loss_sub[:reuseAge]= loss_sub[:reuseAge]*(reusepercent/100)
    else: 
        loss_sub=loss.copy()
    waste = np.outer(wt_si, loss_sub)
    
    
    cumWaste = np.zeros((n, n))
    cumWaste_noReuse = np.zeros((n, n))
    cumWaste_reuse_matrix = np.zeros((n, n))
    reuse = np.zeros((n, n))
    reuse_12 = np.zeros((n, n))
    for start_j in range(n - 1, -1, -1):
        i = 0
        j = start_j
        while j >= 0 and i < n:
            cumWaste[i, j] += (wt_si[i] * loss_sub[j])
            i += 1
            j -= 1
    for start_j in range(n - 1, -1, -1):
        i = 0
        j = start_j
        while j >= 0 and i < n:
            cumWaste_noReuse[i, j] += (wt_si[i] * loss[j])
            i += 1
            j -= 1
    # _________________________________________________________________________yeALY WASTE    
    col_12_noReuse = cumWaste_noReuse[:, (reuseAge-1)]
    col_12 = cumWaste[:, (reuseAge-1)]
    
    for i in range(n):
        for j in range(n):
            if cumWaste[i, j] != 0:
                if j < reuseAge:
                    reuse[i, j] = cumWaste[i, j]
                else:
                    reuse[i, j] = cumWaste[i, j] - (col_12_noReuse[i] - col_12[i])


    n = cumWaste.shape[0]
    cumWaste_reuse_matrix = cumWaste_noReuse - reuse
    diag_sums = []
    diag_sums_reuse = []
    
    for start_j in range(n - 1, -1, -1):
        i = 0
        j = start_j
        s = 0
        p = 0

        while j >= 0 and i < n:
            s += reuse[i, j]
            p += cumWaste_reuse_matrix[i, j]
            i += 1
            j -= 1

        diag_sums.append(s)
        diag_sums_reuse.append(s)
    
    yearlyEoL_si = diag_sums[::-1]
    reuse_cum_si = diag_sums_reuse[::-1]
    diag_sums = np.array(diag_sums)


    # ______________________________________________________________________________
    
def calc_annual_eol_si():
    global yearlyEoL_si, annualEoL_si, reuse_ann_si, reuse_cum_si
    yearlyEoL_si = np.array(yearlyEoL_si)
    annualEoL_si[1:] = yearlyEoL_si[1:] - yearlyEoL_si[:-1]
 