import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="PV Waste Dashboard", layout="wide")

import inputs as inp
import installations as inst
import marketShare as ms
import plots as pl
import powerTomass as ptm
import lossScenarios as ls
import collection_eff as coleff
import recycling as recycle
loss=np.zeros(len(inst.year_col))





def check_login():
    password = st.text_input("Enter password", type="password")
    if password == "EoLPV":
        return True
    return False

if not check_login():
    st.stop()


st.markdown("""
<style>

/* ✅ Banner container */
.marquee-container {
    width: 100%;
    overflow: hidden;
    background: #0e1a2b;
    color: white;
    padding: 10px 0;
    position: relative;
    background: #003399;
    color: #ffcc00;
}

/* ✅ Moving text */
.marquee-text {
    display: inline-block;
    white-space: nowrap;
    padding-left: 100%;
    animation: scroll-right 18s linear infinite;
    font-size: 16px;
}

/* ✅ Animation */
@keyframes scroll-right {
    0%   { transform: translateX(0%); }
    100% { transform: translateX(-100%); }
}

</style>

<div class="marquee-container">
    <div class="marquee-text">
        This is intended for reviewers' view
    </div>
</div>
""", unsafe_allow_html=True)

#========================about quasar"

st.markdown("""
<div style="
    height:5px;
    background: linear-gradient(90deg,#4facfe,#00f2fe);
    border-radius:8px;
    margin:20px 0;">
</div>
""", unsafe_allow_html=True)
st.markdown(
    """
    <div class="header-container">
        <div class="overlay"></div>
        <div class="text">
        <h1 style="white-space: nowrap;">
            End-of-Life PV Waste in the EU
        </h1
        <h1>Forecast Analysis</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ================= SIDEBAR (ALL CONTROLS HERE) =================
st.sidebar.header("⚙️ Controls Panel")

# ---- Deployment target ----

st.sidebar.subheader("📈PV Deployment Forecast")
target_option = st.sidebar.radio(
    "Target PV Deployment in the EU by 2030",
    ["Default (750 GW)", "User-Defined Target"]
)

if target_option == "Default (750 GW)":
    by2050 = 750

else:
    by2050 = st.sidebar.number_input(
        "Target (GW)",
        min_value=406,
        max_value=1500,
        value=750,
        step=10,
        help="Select a value between 406 and 1500 GW"
    )

    

inst.forecast_installations(by2050)
ms.get_column_index(4)
ms.calc_cSi_installations()


# ---- Loss scenario ----
st.sidebar.subheader("📉 Loss Scenario")
loss_option = st.sidebar.radio(
    "Select Weibull Curve",
    [ "EU-WEEE Scenario", "Regular Loss Scenario", "User-Defined Loss Scenario"]
)

if loss_option == "Regular Loss Scenario":
    ls.calc_loss_scenarios()
    loss = ls.RegularLoss
    st.sidebar.markdown(
        f'<span title="α = 5.3759, β = 30" >ℹ️ α = 5.3759, β = 30</span>',
        unsafe_allow_html=True
)
elif loss_option == "EU-WEEE Scenario":
    ls.calc_loss_scenarios()
    loss = ls.EUWEEE
    st.sidebar.markdown(
        '<span title="alpha=3.5, beta=25">ℹ️ α = 3.5, β = 25',
        unsafe_allow_html=True
)
else:
    ls.calc_loss_scenarios()

    # ✅ Initialize session state
    if "alpha" not in st.session_state:
        st.session_state.alpha = 3.5
    if "beta" not in st.session_state:
        st.session_state.beta = 25

    param_choice = st.sidebar.radio(
        "Select parameter to tune",
        ["Alpha (α)", "Beta (β)"]
    )

    if param_choice == "Alpha (α)":
        st.session_state.alpha = st.sidebar.number_input(
            "α",
            min_value=0.5000,
            max_value=10.0000,
            value=st.session_state.alpha,
            step=0.1000
        )

        st.sidebar.write(f"Current β value: **{st.session_state.beta}**")
        st.sidebar.info("Next: Enter the Beta (β) value")

    else:
        st.session_state.beta = st.sidebar.number_input(
            "β",
            min_value=15,
            max_value=50,
            value=st.session_state.beta,
            step=1
        )

        st.sidebar.write(f"Current α value: **{st.session_state.alpha}**")
        st.sidebar.info("Click 'Apply' to update the model")

    # ✅ Apply button
    if st.sidebar.button("Apply"):
        ls.alpha = st.session_state.alpha
        ls.beta = st.session_state.beta
        st.rerun()
    loss = ls.User
st.sidebar.markdown("[📈Plot : Failure Probability Curves](#plot_loss_scenarios)")

# ---- Reuse ----
st.sidebar.subheader("🔁 Reuse")
ls.reuseAge = 0
reuse_option = st.sidebar.radio(
    "Reuse Practice in the EoL Estimation",
    ["Not Included", "Reuse (<12 yrs)", "User-Defined Reuse Age"]
)
if reuse_option == "Not Included":
    ls.reuseAge = 0
elif reuse_option == "Reuse (<12 yrs)":
    ls.reuseAge = 12
elif reuse_option == "User-Defined Reuse Age":
    ls.reuseAge = st.sidebar.number_input(
        "Age",
        min_value=0,
        max_value=25,
        value=12,
        step=1,
        help="Select a value between 1 and 25"
        )
if ls.reuseAge>0:
    ls.reusepercent=st.sidebar.number_input(
        "% of modules reach EoL from the reuse stream",
        min_value=0,
        max_value=100,
        value=100,
        step=5,
        help="Select a value between 1 and 100"
        )
    
    
   # st.sidebar.number_input("Age", value=12)


# ---- Collection ----
st.sidebar.subheader("📦 EoL PV Collection Efficiency")
col_option = st.sidebar.radio(
    "Select EoL PV Collection Efficiency",
    ["Default (100%)", "85%", "User-Defined Efficiency"]
)

if col_option == "Default (100%)":
    col_eff = 100
elif col_option == "85%":
    col_eff = 85
elif col_option == "User-Defined Efficiency":
    col_eff = st.sidebar.number_input(
        "Collection Efficienct %",
        min_value=0,
        max_value=100,
        value=90,
        step=1,
        help="Select a value between 1 and 100"
        )
    
    



# ---- Recycling silicon----
st.sidebar.subheader("♻️Silicon Recycling Efficiency")
rec_option = st.sidebar.radio(
    "Select Silicon Recycling Efficiency",
    ["Default (100%)", "Custom"]
)

if rec_option == "Custom":
    re_eff_si = st.sidebar.number_input(
        "Silicon Recycling Efficiency %",
        min_value=0,
        max_value=100,
        value=90,
        step=1,
        help="Select a value between 1 and 100"
        )
else:
    re_eff_si = 100

#_____________Refining
st.sidebar.subheader("♻️Silicon Refining Efficiency")
rec_option = st.sidebar.radio(
    "Select Silicon Refining Efficiency",
    ["Default (100%)", "Custom"]
)

if rec_option == "Custom":
    ref_eff_si = st.sidebar.number_input(
        "Silicon Refining Efficiency %",
        min_value=1,
        max_value=100,
        value=85,
        step=1,
        help="Select a value between 1 and 100"
        )
else:
    ref_eff_si = 100

# ================= CALCULATIONS =================
# installation and market share
cum_total = inst.get_cum_installations_2050()
cum_total_this_year = inst.get_cum_installations_thisYear()
cum_2050 = ms.get_cum_cSi_2050()
cum_this_year = ms.get_cum_cSi_thisYear()

# ---- Power to mass ----

ptm.get_weight_cSi_PVICE()
col1, col2, col3, col4 = st.columns(4, gap="large")
cum_cSi_weight_2050 = ptm.get_cum_weight_cSi_2050()
cum_cSi_weight_thisYear = ptm.get_cum_weight_cSi_thisYear()
# ---- Loss & EOL ----

# ---- Reuse models ----

ls.calc_eol_reuse(loss)
ls.calc_annual_eol_reuse()




# ---- Collection ----
coleff.implement_collection(col_eff)

# ---- Waste summary ----
index50 = inst.year_col[inst.year_col == 2040].index[0]
index40 = inst.year_col[inst.year_col == 2035].index[0]
index30 = inst.year_col[inst.year_col == 2030].index[0]
EoL50=ls.yearlyEoL[index50-1]/1000000
EoL40=ls.yearlyEoL[index40-1]/1000000
EoL30=ls.yearlyEoL[index30-1]/1000000
sen_cum=EoL50


st.markdown("""
<div style="
    height:5px;
    background: linear-gradient(90deg,#4facfe,#00f2fe);
    border-radius:8px;
    margin:20px 0;">
</div>
""", unsafe_allow_html=True)
# ================= CALCULATIONS =================


# ✅ Global CSS for KPI cards (add once at top of app)
st.markdown("""
<style>

.kpi-card {
    height: 140px;  /* ✅ fixed height ensures equal size */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    color: white;
    box-shadow: 2px 4px 12px rgba(0,0,0,0.2);
}

.kpi-title {
    font-size: 16px;
    margin-bottom: 6px;
    opacity: 0.9;
}

.kpi-value {
    font-size: 28px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown("### PV Deployment in the EU")

# ------------------------------
# ✅ FIRST ROW
# ------------------------------
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown(f"""
    <div style="
        background-color:#f4f4f4;
        border:1px solid #d9d9d9;
        border-radius:6px;
        padding:14px;
        text-align:center;
        height:140px;
    ">
        <div style="font-size:14px; color:#555;">PV Deployment</div>
        <div style="font-size:13px; color:#777;">2025</div>
        <div style="font-size:20px; font-weight:600; margin:6px 0;">
            {cum_total_this_year:.0f}
        </div>
        <div style="font-size:12px; color:#666;">GW</div>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown(f"""
    <div style="
        background-color:#f4f4f4;
        border:1px solid #d9d9d9;
        border-radius:6px;
        padding:14px;
        text-align:center;
        height:140px;
    ">
        <div style="font-size:14px; color:#555;">c-Si Deployment</div>
        <div style="font-size:13px; color:#777;">2025</div>
        <div style="font-size:20px; font-weight:600; margin:6px 0;">
            {cum_this_year:.0f}
        </div>
        <div style="font-size:12px; color:#666;">GW</div>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown(f"""
    <div style="
        background-color:#f7f7f7;
        border:1px solid #d9d9d9;
        border-radius:6px;
        padding:14px;
        text-align:center;
        height:140px;
    ">
        <div style="font-size:14px; color:#555;">PV Deployment</div>
        <div style="font-size:13px; color:#777;">2030</div>
        <div style="font-size:20px; font-weight:600; margin:6px 0;">
            {cum_total:.0f}
        </div>
        <div style="font-size:12px; color:#666;">GW</div>
        <div style="margin-top:4px; font-size:11px; color:#888;">
            Avg. annual installations (2026–2030): {inst.AvgAnInsFrcst:.1f} GW
        </div>
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown(f"""
    <div style="
        background-color:#f7f7f7;
        border:1px solid #d9d9d9;
        border-radius:6px;
        padding:14px;
        text-align:center;
        height:140px;
    ">
        <div style="font-size:14px; color:#555;">c-Si Deployment</div>
        <div style="font-size:13px; color:#777;">2030</div>
        <div style="font-size:20px; font-weight:600; margin:6px 0;">
            {cum_2050:.0f}
        </div>
        <div style="font-size:12px; color:#666;">GW</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<hr style="margin-top:30px; margin-bottom:30px;">
""", unsafe_allow_html=True)
# ------------------------------
# ✅ SECOND ROW
# ------------------------------
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col2:
    st.markdown(f"""
    <div style="
        background-color:#fafafa;
        border:1px solid #e0e0e0;
        border-radius:6px;
        padding:16px;
        text-align:center;
        height:150px;
    ">
        <div style="font-size:14px; color:#555;">
            c-Si Deployment in tonnes ({cum_this_year:.0f} GW)
        </div>
        <div style="font-size:13px; color:#777;">2025</div>
        <div style="font-size:20px; font-weight:600; margin:6px 0;">
            {cum_cSi_weight_thisYear/1e6:.2f}
        </div>
        <div style="font-size:12px; color:#666;">million tonnes (Mt)</div>
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown(f"""
    <div style="
        background-color:#fafafa;
        border:1px solid #e0e0e0;
        border-radius:6px;
        padding:16px;
        text-align:center;
        height:150px;
    ">
        <div style="font-size:14px; color:#555;">
            c-Si Deployment in tonnes ({cum_2050:.0f} GW)
        </div>
        <div style="font-size:13px; color:#777;">2030</div>
        <div style="font-size:20px; font-weight:600; margin:6px 0;">
            {cum_cSi_weight_2050/1e6:.2f}
        </div>
        <div style="font-size:12px; color:#666;">million tonnes (Mt)</div>
    </div>
    """, unsafe_allow_html=True)

#============================PV weight=============================
st.markdown("""
<hr style="margin-top:30px; margin-bottom:30px;">
""", unsafe_allow_html=True)
#============================EoLWasteProjections===================

#=================KPIVisualization================
st.markdown("### EoL PV Estimation")
col1, col2, col3 = st.columns(3, gap="large")

# 🟢 2030 (muted green)
with col1:
    st.markdown(f"""
    <div style="
        background-color:#f4f8f4;
        border:1px solid #d6e5d6;
        border-radius:8px;
        padding:16px;
        text-align:center;
    ">
        <div style="font-size:14px; color:#555;">Cumulative EoL c‑Si PV</div>
        <div style="font-size:13px; color:#777;">by 2030</div>
        <div style="font-size:22px; font-weight:600; margin:8px 0;">
            {EoL30:,.2f}
        </div>
        <div style="font-size:12px; color:#666;">million tonnes (Mt)</div>
    </div>
    """, unsafe_allow_html=True)


# 🟡 2035 (neutral tone instead of bright yellow)
with col2:
    st.markdown(f"""
    <div style="
        background-color:#faf7f2;
        border:1px solid #e8d8c2;
        border-radius:8px;
        padding:16px;
        text-align:center;
    ">
        <div style="font-size:14px; color:#555;">Cumulative EoL c‑Si PV</div>
        <div style="font-size:13px; color:#777;">by 2035</div>
        <div style="font-size:22px; font-weight:600; margin:8px 0;">
            {EoL40:,.2f}
        </div>
        <div style="font-size:12px; color:#666;">million tonnes (Mt)</div>
    </div>
    """, unsafe_allow_html=True)


# 🔴 2040 (muted red)
with col3:
    st.markdown(f"""
    <div style="
        background-color:#f8f4f4;
        border:1px solid #e5cfcf;
        border-radius:8px;
        padding:16px;
        text-align:center;
    ">
        <div style="font-size:14px; color:#555;">Cumulative EoL c‑Si PV</div>
        <div style="font-size:13px; color:#777;">by 2040</div>
        <div style="font-size:22px; font-weight:600; margin:8px 0;">
            {EoL50:,.2f}
        </div>
        <div style="font-size:12px; color:#666;">million tonnes (Mt)</div>
    </div>
    """, unsafe_allow_html=True)



#==============================================================
st.markdown("""
<hr style="margin-top:30px; margin-bottom:30px;">
""", unsafe_allow_html=True)
# ---- outputs ----


ptm.get_weight_materials()

ls.calc_eol_si(ptm.wt_silicon, loss)
ls.calc_annual_eol_si()
ls.yearlyEoL_si = ls.yearlyEoL_si * (col_eff/100) * (re_eff_si/100) * (ref_eff_si/100)
EoL50si=ls.yearlyEoL_si[index50-1]/1000
EoL40si=ls.yearlyEoL_si[index40-1]/1000
EoL30si=ls.yearlyEoL_si[index30-1]/1000



################################################################################



ls.calc_eol_reuse(ls.RegularLoss)
ls.RegularLoss_cum=ls.yearlyEoL
ls.RegularLoss_cum = np.array(ls.RegularLoss_cum)
ls.RegularLoss_cum=ls.RegularLoss_cum*(col_eff/100)
ls.RegularLoss_ann[1:] = ls.RegularLoss_cum[1:] - ls.RegularLoss_cum[:-1]


ls.calc_eol_reuse(ls.EarlyLoss)
ls.EarlyLoss_cum=ls.yearlyEoL
ls.EarlyLoss_cum = np.array(ls.EarlyLoss_cum)
ls.EarlyLoss_cum=ls.EarlyLoss_cum*(col_eff/100)
ls.EarlyLoss_ann[1:] = ls.EarlyLoss_cum[1:] - ls.EarlyLoss_cum[:-1]

sen_base=0
ls.calc_eol_reuse(ls.EUWEEE)
ls.EUWEEE_cum=ls.yearlyEoL
ls.EUWEEE_cum = np.array(ls.EUWEEE_cum)
sen_col_100=(ls.EUWEEE_cum[index50-1]/1000000)
sen_col_75=(ls.EUWEEE_cum[index50-1]/1000000)*(0.70)
ls.EUWEEE_cum=ls.EUWEEE_cum*(col_eff/100)
sen_base=ls.EUWEEE_cum[index50-1]/1000000




ls.EUWEEE_ann[1:] = ls.EUWEEE_cum[1:] - ls.EUWEEE_cum[:-1]


ls.calc_eol_si(ptm.wt_silicon, ls.RegularLoss)
ls.RegularLoss_cum_si=ls.yearlyEoL_si
ls.RegularLoss_cum_si = np.array(ls.RegularLoss_cum_si)
ls.RegularLoss_cum_si = ls.RegularLoss_cum_si * (col_eff/100) * (re_eff_si/100) * (ref_eff_si/100)
ls.RegularLoss_ann_si[1:] = ls.RegularLoss_cum_si[1:] - ls.RegularLoss_cum_si[:-1]



ls.calc_eol_si(ptm.wt_silicon, ls.EUWEEE)
ls.EUWEEE_cum_si=ls.yearlyEoL_si
ls.EUWEEE_cum_si = np.array(ls.EUWEEE_cum_si)
sen_base_si=ls.EUWEEE_cum_si[index50-1]*0.85*0.75*0.75
ls.EUWEEE_cum_si = ls.EUWEEE_cum_si * (col_eff/100) * (re_eff_si/100) * (ref_eff_si/100)
ls.EUWEEE_ann_si[1:] = ls.EUWEEE_cum_si[1:] - ls.EUWEEE_cum_si[:-1]


#=================KPIVisualization================
col1, col2, col3 = st.columns(3, gap="large")

# 🟢 2030
with col1:
    st.markdown(f"""
    <div style="
        background-color:#f4f8f4;
        border:1px solid #d6e5d6;
        border-radius:8px;
        padding:16px;
        text-align:center;
    ">
        <div style="font-size:14px; color:#555;">Cumulative Silicon in EoL PV</div>
        <div style="font-size:13px; color:#777;">by 2030</div>
        <div style="font-size:22px; font-weight:600; margin:8px 0;">
            {EoL30si:,.1f}
        </div>
        <div style="font-size:12px; color:#666;">thousand tonnes (kt)</div>
    </div>
    """, unsafe_allow_html=True)


# 🟡 2035
with col2:
    st.markdown(f"""
    <div style="
        background-color:#faf7f2;
        border:1px solid #e8d8c2;
        border-radius:8px;
        padding:16px;
        text-align:center;
    ">
        <div style="font-size:14px; color:#555;">Cumulative Silicon in EoL PV</div>
        <div style="font-size:13px; color:#777;">by 2035</div>
        <div style="font-size:22px; font-weight:600; margin:8px 0;">
            {EoL40si:,.1f}
        </div>
        <div style="font-size:12px; color:#666;">thousand tonnes (kt)</div>
    </div>
    """, unsafe_allow_html=True)


# 🔴 2040
with col3:
    st.markdown(f"""
    <div style="
        background-color:#f8f4f4;
        border:1px solid #e5cfcf;
        border-radius:8px;
        padding:16px;
        text-align:center;
    ">
        <div style="font-size:14px; color:#555;">Cumulative Silicon in EoL PV</div>
        <div style="font-size:13px; color:#777;">by 2040</div>
        <div style="font-size:22px; font-weight:600; margin:8px 0;">
            {EoL50si:,.1f}
        </div>
        <div style="font-size:12px; color:#666;">thousand tonnes (kt)</div>
    </div>
    """, unsafe_allow_html=True)
#============================EoLWasteProjections===================
#==============================================================
st.markdown("""
<hr style="margin-top:30px; margin-bottom:30px;">
""", unsafe_allow_html=True)
st.markdown("### Cumulative and Annual EoL c-Si PV")

col1, col2 = st.columns(2)

with col1:
    pl.plot_eol_cumulative_compare1()
with col2:
    pl.plot_eol_annual_compare1()
col1, col2 = st.columns(2)

with col1:
    pl.plot_eol_cumulative_compare1_si()
with col2:
    pl.plot_eol_annual_compare1_si()

gw_regular=np.zeros(len(inst.year_col))
gw_euweee=np.zeros(len(inst.year_col))
gw_regular=ls.RegularLoss_ann_si/2
gw_euweee=ls.EUWEEE_ann_si/2

col1, col2 = st.columns(2)
with col1:
    st.write(pl.plot_eol_annual_compare1_gw(gw_regular, gw_euweee))

st.markdown("""
<hr style="margin-top:30px; margin-bottom:30px;">
""", unsafe_allow_html=True)
st.markdown("#### Background data")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(pl.plot_cumulative_installations(), use_container_width=True)

with col2:
    st.plotly_chart(pl.plot_annual_installations(), use_container_width=True)


col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(pl.plot_marketShare(), use_container_width=True)

with col4:
    st.plotly_chart(pl.plot_powerToMass_PVICE(), use_container_width=True)


st.markdown("<div id='plot_loss_scenarios'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.write(pl.plot_loss_scenarios())
st.markdown("""
<hr style="margin-top:30px; margin-bottom:30px;">
""", unsafe_allow_html=True)




#pl.plot_eol_cumulative_reuse()
#pl.plot_annual_eol_reuse()
#st.metric("📦 Collected Waste", f"{sum(coleff.annual_coll)/1e6:.2f} Mt")



#===========================================
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def plot_tornado_two_sided():

    # ✅ Example baseline output (replace with your model)
    baseline = sen_base  # e.g., total EoL in Mt
    st.write(sen_base)

    # ✅ Replace these with your actual model results
    data = pd.DataFrame({
        "Variable": [
            "Weibull curve",
            "Collection Efficiency",
            "Reuse Efficiency",
        ],

        # ✅ Model output when variable at LOW bound
        "Low": [
            5.63,
            5.70,
            5.86
           
        ],

        # ✅ Model output when variable at HIGH bound
        "High": [
            8.27,
            8.14,
            7.98,
            
        ]
    })

    # ✅ Calculate deviations from baseline
    data["Low_dev"] = data["Low"] - baseline
    data["High_dev"] = data["High"] - baseline

    # ✅ Calculate impact magnitude for sorting
    data["Impact"] = (data["High"] - data["Low"]).abs()

    # ✅ Sort for tornado shape
    data = data.sort_values("Impact", ascending=True)

    # ✅ Plot
    fig = go.Figure()

    # 🔴 LEFT SIDE (Low case)
    fig.add_trace(go.Bar(
        y=data["Variable"],
        x=data["Low_dev"],
        orientation='h',
        name="Low",
        marker_color="indianred",
        text=[f"{v:.1f}" for v in data["Low"]],
        textposition='outside'
    ))

    # 🔵 RIGHT SIDE (High case)
    fig.add_trace(go.Bar(
        y=data["Variable"],
        x=data["High_dev"],
        orientation='h',
        name="High",
        marker_color="steelblue",
        text=[f"{v:.1f}" for v in data["High"]],
        textposition='outside'
    ))

    # ✅ Vertical baseline line
    fig.add_vline(x=0, line_color="black", line_width=1)

    # ✅ Layout (publication quality)
    fig.update_layout(
        title="Sensitivity Analysis (Tornado Diagram)",
        xaxis_title="Change from Baseline (Mt)",
        yaxis_title="Input Parameters",
        template="plotly_white",
        width=800,
        height=500,

      

        xaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12),
            zeroline=True
        ),

        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),

        legend=dict(
            font=dict(size=12)
        ),

        margin=dict(l=80, r=40, t=80, b=60)
    )

    st.plotly_chart(fig)

#plot_tornado_two_sided()


def plot_tornado_two_sided_si():

    # ✅ Example baseline output (replace with your model)
    baseline = sen_base_si/1000  # e.g., total EoL in Mt
    st.write(sen_base_si/1000)

    # ✅ Replace these with your actual model results
    data = pd.DataFrame({
        "Variable": [
            "Recovering Efficiency",
            "Refining Efficiency",
        ],

        # ✅ Model output when variable at LOW bound
        "Low": [
            109.0,
            83.87,
           
        ],

        # ✅ Model output when variable at HIGH bound
        "High": [
            142.6,
            167.74,
            
        ]
    })

    # ✅ Calculate deviations from baseline
    data["Low_dev"] = data["Low"] - baseline
    data["High_dev"] = data["High"] - baseline

    # ✅ Calculate impact magnitude for sorting
    data["Impact"] = (data["High"] - data["Low"]).abs()

    # ✅ Sort for tornado shape
    data = data.sort_values("Impact", ascending=True)

    # ✅ Plot
    fig = go.Figure()

    # 🔴 LEFT SIDE (Low case)
    fig.add_trace(go.Bar(
        y=data["Variable"],
        x=data["Low_dev"],
        orientation='h',
        name="Low",
        marker_color="indianred",
        text=[f"{v:.1f}" for v in data["Low"]],
        textposition='outside'
    ))

    # 🔵 RIGHT SIDE (High case)
    fig.add_trace(go.Bar(
        y=data["Variable"],
        x=data["High_dev"],
        orientation='h',
        name="High",
        marker_color="steelblue",
        text=[f"{v:.1f}" for v in data["High"]],
        textposition='outside'
    ))

    # ✅ Vertical baseline line
    fig.add_vline(x=0, line_color="black", line_width=1)

    # ✅ Layout (publication quality)
    fig.update_layout(
        title="Sensitivity Analysis (Tornado Diagram)",
        xaxis_title="Change from Baseline (1000 tonnes)",
        yaxis_title="Input Parameters",
        template="plotly_white",
        width=800,
        height=500,

      

        xaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12),
            zeroline=True
        ),

        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),

        legend=dict(
            font=dict(size=12)
        ),

        margin=dict(l=80, r=40, t=80, b=60)
    )

    st.plotly_chart(fig)

#plot_tornado_two_sided_si()


    # ✅ Vertical baseline line

#=======================chart
import streamlit as st
from graphviz import Digraph
from graphviz import Digraph
import streamlit as st

def show_advanced_flowchart():
    dot = Digraph()

    # ===== Compact Vertical Layout =====
    dot.attr(rankdir='TB',
             splines='line',
             nodesep='0.5',
             ranksep='0.35',   # ↓↓↓ shorter arrows
             margin='0.02')

    # ===== Node Style =====
    dot.attr('node',
             shape='rect',
             style='filled,rounded',
             fontname='Helvetica',
             fontsize='10',
             margin='0.08,0.05')   # slightly tighter boxes

    # =========================
    # NODES
    # =========================

    dot.node('PV', 'Annual PV Deployment (GW)',
             fillcolor='#BBDEFB', color='#1E88E5')

    dot.node('cSi', 'Annual c-Si PV Deployment (GW)',
             fillcolor='#E3F2FD', color='#1E88E5')

    dot.node('MassToPower', 'GW to Tonnes',
             fillcolor='#FFE0B2', color='#F57C00')

    dot.node('Regular', 'Regular Loss Scenario',
             fillcolor='#C8E6C9', color='#2E7D32')

    dot.node('EUWEEE', 'EU-WEEE Scenario',
             fillcolor='#A5D6A7', color='#2E7D32')

    dot.node('EoL', 'EoL PV Generation',
             fillcolor='#66BB6A', color='#1B5E20',
             fontcolor='white')

    dot.node('Collection', 'Collection & Sorting',
             fillcolor='#FFF9C4', color='#F9A825')

    dot.node('Reuse', 'Reuse / Second-life',
             fillcolor='#B2DFDB', color='#00796B')

    dot.node('Recycling', 'Recycling Process',
             fillcolor='#CE93D8', color='#6A1B9A')

    dot.node('SiRecovery', 'Si Recovery & Refining',
             fillcolor='#E1BEE7', color='#6A1B9A')

    dot.node('exp', 'Exported',
             fillcolor='gray', color='#6A1B9A')

    # =========================
    # ALIGNMENT
    # =========================

    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('Regular')
        s.node('EUWEEE')

    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('Reuse')
        s.node('Recycling')

    # =========================
    # EDGES
    # =========================

    dot.edge('PV', 'cSi', label='annual PV x c-Si market share')
    dot.edge('cSi', 'MassToPower')

    dot.edge('MassToPower', 'Regular')
    dot.edge('MassToPower', 'EUWEEE')

    dot.edge('Regular', 'EoL')
    dot.edge('EUWEEE', 'EoL')

    dot.edge('EoL', 'Collection')

    dot.edge('Collection', 'Reuse')
    dot.edge('Collection', 'Recycling')

    dot.edge('Recycling', 'SiRecovery')
    dot.edge('Reuse', 'exp',
             style='dashed', label='Refurbished', color='#00796B')

    # ===== Render =====
    
    col1, col2, col3 = st.columns([1, 2, 1])  # middle column wider

    with col2:
        st.graphviz_chart(dot)


# Run it
show_advanced_flowchart()




#========================ACKNOWLEDGEMENT=====================================
st.markdown("""
<style>

/* ✅ Banner container */
.marquee-container {
    width: 100%;
    overflow: hidden;
    background: #0e1a2b;
    color: white;
    padding: 10px 0;
    position: relative;
    background: #003399;
    color: #ffcc00;
}

/* ✅ Moving text */
.marquee-text {
    display: inline-block;
    white-space: nowrap;
    padding-left: 100%;
    animation: scroll-right 18s linear infinite;
    font-size: 16px;
}

/* ✅ Animation */
@keyframes scroll-right {
    0%   { transform: translateX(0%); }
    100% { transform: translateX(-100%); }
}

</style>

<div class="marquee-container">
    <div class="marquee-text">
        This work has received funding from the European Union's Horizon Europe Research and Innovation Programme under Grant Agreement No 101122298 "QUASAR"
    </div>
</div>
""", unsafe_allow_html=True)

#========================about quasar"

st.markdown("""
<div style="
    height:5px;
    background: linear-gradient(90deg,#4facfe,#00f2fe);
    border-radius:8px;
    margin:20px 0;">
</div>
""", unsafe_allow_html=True)
