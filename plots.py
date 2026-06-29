import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import inputs as inp
import installations as ins
import marketShare as ms
import powerTomass as pt
import lossScenarios as ls
import collection_eff as coleff





#________________________________________________________________________________
# Cumulative PV Installations in EU
def plot_cumulative_installations():
    import pandas as pd
    import plotly.express as px

    # Data
    year_col = ins.year_col.iloc[8:30]
    installation_col = ins.installation_cum.iloc[8:30]

    df_plot = pd.DataFrame({
        "Year": year_col,
        "Installation": installation_col
    })

    # Avoid clutter labels
    df_plot["label"] = df_plot["Installation"].apply(
        lambda v: f"{v:.1f}" if v > 1.5 else ""
    )

    # Plot
    figCum = px.bar(
        df_plot,
        x="Year",
        y="Installation",
        text="label",
        title="Cumulative PV Installations in EU",
        labels={
            "Year": "Year",
            "Installation": "Cumulative Installations (GW)"
        },
        color_discrete_sequence=["#A8E6CF"]  # ✅ same blue theme
    )

    # Labels & styling
    figCum.update_traces(
        textposition='outside',
        textfont=dict(size=13, color='black')
    )

    # Layout (match your other plots)
    figCum.update_layout(
        width=800,
        height=500,
        template="plotly_white",
        margin=dict(l=60, r=40, t=80, b=60),

        xaxis=dict(
            title="Year",
            title_font=dict(color="black", size=13),
            tickfont=dict(color="black", size=13)
        ),

        yaxis=dict(
            title="Cumulative Installations (GW)",
            title_font=dict(color="black", size=13),
            tickfont=dict(color="black", size=13),
            range=[0, max(df_plot["Installation"]) * 1.15]  # spacing
        )
    )

    return figCum



#_____________________annual plot___________________________________-

def plot_annual_installations():
    import pandas as pd
    import plotly.express as px

    # Data
    year_col = ins.year_col.iloc[8:30]
    installationAnnual_col = ins.installation_annual.iloc[8:30]

    df_plot = pd.DataFrame({
        "Year": year_col,
        "Installation": installationAnnual_col
    })

    # ✅ Cleaner labels (avoid clutter)
    df_plot["label"] = df_plot["Installation"].apply(
        lambda v: f"{v:.1f}" if v > 0.6 else ""
    )

    # Plot
    figAn = px.bar(
        df_plot,
        x="Year",
        y="Installation",
        text="label",
        title="Annual PV Installations in the EU",
        labels={
            "Year": "Year",
            "Installation": "Annual Installations (GW)"
        },
        color_discrete_sequence=["#A8E6CF"]  # ✅ same theme
    )

    # ✅ Label styling
    figAn.update_traces(
        textposition='outside',
        textfont=dict(size=13, color='black'),
        hovertemplate="Year: %{x}<br>Installation: %{y:.1f} GW"
    )
    figAn.update_traces(
        marker=dict(
            line=dict(
                color="#5FBF9F",  # dark blue border
                width=1.5
            )
            )
    )
    # ✅ Layout (match other plots)
    figAn.update_layout(
        width=800,
        height=500,
        template="plotly_white",
        margin=dict(l=60, r=40, t=80, b=60),

        xaxis=dict(
            title="Year",
            title_font=dict(color="black", size=13),
            tickfont=dict(color="black", size=13)
        ),

        yaxis=dict(
            title="Annual Installations (GW)",
            title_font=dict(color="black", size=13),
            tickfont=dict(color="black", size=13),
            range=[0, max(df_plot["Installation"]) * 1.15]
        )
    )

    return figAn

#_____________________annual plot__________________________________-


#_____________________market share plot___________________________________-

def plot_marketShare():
    year_col = ins.year_col.iloc[:ins.index2030+1]
    marketShare = ms.marketShare.iloc[:ins.index2030+1] * 100

    df_plot = pd.DataFrame({
        "Year": year_col,
        "Market Share": marketShare
    })

    # ✅ Labels every 5 points (clean + consistent unit)
    labels = [
        f"{v:.0f}" if (i % 1 == 0) else ""
        for i, v in enumerate(df_plot["Market Share"])
    ]

    figAn = px.bar(
        df_plot,
        x="Year",
        y="Market Share",
        title="Market Share of Crystalline Silicon PV Technologies",
        labels={
            "Year": "Year",
            "Market Share": "c-Si PV Market Share (%)"
        },
        color_discrete_sequence=["#B3D9F2"]  # ✅ same them
    )

    # ✅ Improved label styling ONLY
    figAn.update_traces(
        text=labels,
        textposition='outside',
        textfont=dict(size=14, color='black')   # ✅ reduced from 28 → cleaner
    )

    figAn.update_layout(
        width=600,
        height=450,
        margin=dict(l=40, r=40, t=80, b=40)
    )

    return figAn


#_____________________power to mass plot___________________________________-

def plot_powerToMass():
    
    year_col = ins.year_col.iloc[:ins.index2030]
    weight_cSi = pt.curve_massPerMW[:ins.index2030] 
    weight_cSi1 = pt.curve_massPerMW1[:ins.index2030]

    # ✅ Build DataFrame
    df_plot = pd.DataFrame({
        "Year": year_col,
        "cSi Scenario 1": weight_cSi,
        "cSi Scenario 2": weight_cSi1
    })

    # ✅ Labels every 5 points
    labels1 = [
        f"{v:,.0f}" if (i % 5 == 0) else ""
        for i, v in enumerate(df_plot["cSi Scenario 1"])
    ]

    labels2 = [
        f"{v:,.0f}" if (i % 5 == 0) else ""
        for i, v in enumerate(df_plot["cSi Scenario 2"])
    ]

    # ✅ Plot
    figAn = px.line(
        df_plot,
        x="Year",
        y=["cSi Scenario 1", "cSi Scenario 2"],
        markers=True,
        title="Power to Mass Conversion for Crystalline Silicon PV Technologies",
        labels={
            "value": "Weight (tonnes)",
            "variable": "Scenario"
        }
    )

    # ✅ Apply labels to each line
    figAn.data[0].update(
        text=labels1,
        textposition='top center',
        mode="lines+markers+text"
    )

    figAn.data[1].update(
        text=labels2,
        textposition='top center',
        mode="lines+markers+text"
    )

    # ✅ Reference annotation
    figAn.add_annotation(
        text='<a href="https://doi.org/10.1016/j.isci.2021.103488">Source: Ovaitt et al., iScience (2021)</a>',
        xref="paper", yref="paper",
        x=0, y=-0.2,
        showarrow=False,
        font=dict(size=12, color="gray")
    )

    # ✅ Layout
    figAn.update_layout(
        width=700,
        height=450,
        margin=dict(l=40, r=40, t=60, b=80),  # extra space for reference
        template="plotly_white"
    )

    return figAn


def plot_powerToMass_PVICE():
    year_col = ins.year_col.iloc[:ins.index2030]
    weight_cSi = pt.curve_PVICE[:ins.index2030]

    # ✅ Build DataFrame
    df_plot = pd.DataFrame({
        "Year": year_col,
        "cSi Scenario": weight_cSi
    })

    # ✅ Labels every 5 points
    labels = df_plot["cSi Scenario"].where(df_plot.index % 5 == 0).fillna("")

    # ✅ Plot
    figAn = px.line(
        df_plot,
        x="Year",
        y="cSi Scenario",
        markers=True,
        title="Power to Mass Conversion for Crystalline Silicon PV Technologies",
        labels={
            "cSi Scenario": "Weight (MW/tonnes)"
        }
    )

    # ✅ Apply labels
    figAn.update_traces(
        text=labels,
        texttemplate='%{text}',
        textposition='top center'
    )

    # ✅ Add reference (KEY PART ✅)
    figAn.add_annotation(
        text="Source: Ovaitt et al., iScience (2021)",
        xref="paper", yref="paper",
        x=0, y=-0.2,
        showarrow=False,
        font=dict(size=12, color="gray")
    )

    # ✅ Layout
    figAn.update_layout(
        height=500,
        margin=dict(l=40, r=40, t=60, b=80),  # 👈 extra bottom space for reference
        template="plotly_white"
    )

    return figAn

# ✅ Layout
    figAn.update_layout(
        height=500,
        margin=dict(l=40, r=40, t=60, b=40),
        template="plotly_white"
    )

    return figAn

   
    


#_____________________loss scenario plot___________________________________-

def plot_loss_scenarios():
 
    # ✅ Build DataFrame
    df_plot = pd.DataFrame({
        "PVage": ls.PVage[:51],
        "RegularLoss": ls.RegularLoss[:51]*100,
        "EUWEEE": ls.EUWEEE[:51]*100,
        "User-Defined": ls.User[:51]*100
    })

    # ✅ Plot
    fig = px.line(
        df_plot,
        x="PVage",
        y=["User-Defined", "RegularLoss", "EUWEEE"],
        title="Age of the PV Modules vs Failure Probability",
        labels={
            "PVage": "Age of the PV Modules (years)",
            "value": "Failure Probability (%)",
            "variable": "Scenario"
        }
    )

    # ✅ Add markers only to User-Defined
    for trace in fig.data:
        if trace.name == "User-Defined":
            trace.mode = "lines+markers"
            trace.marker = dict(size=6, symbol="circle")
        else:
            trace.mode = "lines"

    # ✅ Layout
    fig.update_layout(
        width=500,
        height=400,
        template="plotly_white"
    )

    return fig
#_____________________________plot waste_cumulative year wise 1997-2100




    #____________________________kt

    
def plot_eol_cumulative_mat_t(material_name, y_data):

    x_col = inp.df.iloc[1:, 0]
    x_col = np.append(x_col, 2101)

    # ✅ Full arrays
    years = x_col[:len(y_data)]
    values = np.array(y_data[:len(years)]) / 1   # ✅ convert to Mt

    # ✅ DataFrame
    df_plot = pd.DataFrame({
        "Year": years,
        f"Cumulative {material_name}": values
    })

    # ✅ Filter 2020–2040
    df_plot = df_plot[
        (df_plot["Year"] >= 2020) & (df_plot["Year"] <= 2040)
    ]

    # ✅ Labels (reduce clutter if needed → i % 3)
    labels = [
        f"{v:.2f}" if i % 1 == 0 else ""
        for i, v in enumerate(df_plot[f"Cumulative {material_name}"])
    ]

    # ✅ Plot
    figWaste = px.bar(
        df_plot,
        x="Year",
        y=f"Cumulative {material_name}",
        text=labels,
        title=f"Cumulative Generation of {material_name} in the EU (2020–2040)",
        labels={
            "Year": "Year",
            f"Cumulative {material_name}": f"Cumulative Generation of {material_name} (tonnes)"
        }
    )

    # ✅ Label styling
    figWaste.update_traces(
        textposition='outside',
        textfont=dict(size=12, color="black")
    )

    # ✅ Publication layout
    figWaste.update_layout(
        width=800,
        height=500,
        template="plotly_white",

        title=dict(
            font=dict(size=18),
            x=0.5,
            xanchor="center"
        ),

        xaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12),
            tickangle=-45
        ),

        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),

        margin=dict(l=60, r=40, t=80, b=60)
    )

    st.plotly_chart(figWaste)

#_________________________________annaul EOL

     # ======================================annaul EOL 


#================================================



#=============================================================


def plot_eol_cumulative_compare1():

    import numpy as np
    import pandas as pd
    import plotly.express as px
    import streamlit as st

    x_col = inp.df.iloc[1:, 0]
    x_col = np.append(x_col, 2101)

    years = x_col[:len(ls.yearlyEoL)]

    
    euweee_values = np.array(ls.EUWEEE_cum) / 1e6
    regular_loss  = np.array(ls.RegularLoss_cum) / 1e6


    df_plot = pd.DataFrame({
        "Year": years,
        "EU-WEEE": euweee_values,
        "Regular Loss": regular_loss
    })

    df_plot = df_plot[
        (df_plot["Year"] >= 2020) & (df_plot["Year"] <= 2040)
    ]

    # ✅ Label control (avoid clutter)
    df_long = df_plot.melt(
        id_vars="Year",
        value_vars=["EU-WEEE", "Regular Loss"],
        var_name="Category",
        value_name="Value"
    )

    df_long["label"] = df_long["Value"].apply(
        lambda v: f"{v:.2f}" if v > 0.34 else ""
    )

    # ✅ Plot
    figWaste2 = px.bar(
        df_long,
        x="Year",
        y="Value",
        color="Category",
        text="label",
        title="Cumulative EoL c-Si PV (2020–2040)",
        labels={"Value": "million tonnes", "Year": "Year"},
        color_discrete_map={
            "EU-WEEE": "#90CAF9",     # ✅ dark blue
            "Regular Loss": "#0B5394"    # ✅ light blue
        }
    )

    # ✅ Overlay mode (as you intended)
    figWaste2.update_layout(
    barmode="overlay",
    width=800,
    height=500,
    template="plotly_white",
    margin=dict(l=60, r=40, t=80, b=60),   # ✅ comma added
    

    legend=dict(
        x=0,              # move to left
        y=1,
        xanchor="left",
        yanchor="top",
        orientation="v"
    )
)


    # ✅ Vertical labels + styling
    figWaste2.update_traces(
        textposition='outside',
        textangle=90,                      # ✅ vertical labels
        textfont=dict(size=14, color="black")
    )

    figWaste2.update_layout(
    xaxis=dict(
        title="Year",
        title_font=dict(color="black", size=13),   # ✅ axis title color
        tickfont=dict(color="black", size=13)       # ✅ tick labels color
    ),
    yaxis=dict(
        title="million tonnes",
        title_font=dict(color="black", size=13),
        tickfont=dict(color="black", size=13)
    )
    )
    
    y_max = 11

    figWaste2.update_layout(
        yaxis=dict(
            title="million tonnes",
            range=[0, y_max * 1.15]   # ✅ increase space by 15%
        )
    )


    #figWaste2.update_xaxes(tickangle=-45)

    st.plotly_chart(figWaste2, key="compare_early_regular1")

def plot_eol_cumulative_compare1():

    import numpy as np
    import pandas as pd
    import plotly.express as px
    import streamlit as st

    x_col = inp.df.iloc[1:, 0]
    x_col = np.append(x_col, 2101)

    years = x_col[:len(ls.yearlyEoL)]

    
    euweee_values = np.array(ls.EUWEEE_cum) / 1e6
    regular_loss  = np.array(ls.RegularLoss_cum) / 1e6


    df_plot = pd.DataFrame({
        "Year": years,
        "EU-WEEE": euweee_values,
        "Regular Loss": regular_loss
    })

    df_plot = df_plot[
        (df_plot["Year"] >= 2020) & (df_plot["Year"] <= 2040)
    ]

    # ✅ Label control (avoid clutter)
    df_long = df_plot.melt(
        id_vars="Year",
        value_vars=["EU-WEEE", "Regular Loss"],
        var_name="Category",
        value_name="Value"
    )

    df_long["label"] = df_long["Value"].apply(
        lambda v: f"{v:.2f}" if v > 0.34 else ""
    )

    # ✅ Plot
    figWaste2 = px.bar(
        df_long,
        x="Year",
        y="Value",
        color="Category",
        text="label",
        title="Cumulative EoL c-Si PV (2020–2040)",
        labels={"Value": "million tonnes", "Year": "Year"},
        color_discrete_map={
            "EU-WEEE": "#90CAF9",     # ✅ dark blue
            "Regular Loss": "#0B5394"    # ✅ light blue
        }
    )

    # ✅ Overlay mode (as you intended)
    figWaste2.update_layout(
    barmode="overlay",
    width=800,
    height=500,
    template="plotly_white",
    margin=dict(l=60, r=40, t=80, b=60),   # ✅ comma added
    

    legend=dict(
        x=0,              # move to left
        y=1,
        xanchor="left",
        yanchor="top",
        orientation="v"
    )
)


    # ✅ Vertical labels + styling
    figWaste2.update_traces(
        textposition='outside',
        textangle=90,                      # ✅ vertical labels
        textfont=dict(size=14, color="black")
    )

    figWaste2.update_layout(
    xaxis=dict(
        title="Year",
        title_font=dict(color="black", size=13),   # ✅ axis title color
        tickfont=dict(color="black", size=13)       # ✅ tick labels color
    ),
    yaxis=dict(
        title="million tonnes",
        title_font=dict(color="black", size=13),
        tickfont=dict(color="black", size=13)
    )
    )
    
    y_max = 11

    figWaste2.update_layout(
        yaxis=dict(
            title="million tonnes",
            range=[0, y_max * 1.15]   # ✅ increase space by 15%
        )
    )


    #figWaste2.update_xaxes(tickangle=-45)

    st.plotly_chart(figWaste2, key="compare_early_regular1")


#===========================reuse compare
#===========================annaul compare

def plot_eol_annual_compare1():


    x_col = inp.df.iloc[1:, 0]
    x_col = np.append(x_col, 2101)

    years = x_col[:len(ls.yearlyEoL)]
    
    euweee_values = np.array(ls.EUWEEE_ann) / 1e3
    regular_loss  = np.array(ls.RegularLoss_ann) / 1e3

    df_plot = pd.DataFrame({
        "Year": years,
        "EU-WEEE": euweee_values,
        "Regular Loss": regular_loss
    })

    df_plot = df_plot[
        (df_plot["Year"] >= 2020) & (df_plot["Year"] <= 2040)
    ]

    # ✅ Label control (avoid clutter)
    df_long = df_plot.melt(
        id_vars="Year",
        value_vars=["EU-WEEE", "Regular Loss"],
        var_name="Category",
        value_name="Value"
    )

    df_long["label"] = df_long["Value"].apply(
        lambda v: f"{v:.0f}" if v > 45 else ""
    )

    # ✅ Plot
    figWaste2 = px.bar(
    df_long,
    x="Year",
    y="Value",
    color="Category",
    text="label",
    title="Annual EoL c-Si PV (2020–2040)",
    labels={"Value": "1000 tonnes", "Year": "Year"},
    color_discrete_map={
        "EU-WEEE": "#90CAF9",     # ✅ dark blue
        "Regular Loss": "#0B5394"
    }
)

    figWaste2.update_traces(
        marker=dict(
            line=dict(
                color="#2F4F6F",  # dark blue border
                width=1.5
            )
            )
)

    # ✅ Overlay mode (as you intended)
    figWaste2.update_layout(
    barmode="overlay",
    width=800,
    height=500,
    template="plotly_white",
    margin=dict(l=60, r=40, t=80, b=60),   # ✅ comma added
    

    legend=dict(
        x=0,              # move to left
        y=1,
        xanchor="left",
        yanchor="top",
        orientation="v"
    )
)


    # ✅ Vertical labels + styling
    figWaste2.update_traces(
        textposition='outside',
        textangle=90,                      # ✅ vertical labels
        textfont=dict(size=14, color="black")
    )

    figWaste2.update_layout(
    xaxis=dict(
        title="Year",
        title_font=dict(color="black", size=13),   # ✅ axis title color
        tickfont=dict(color="black", size=13)       # ✅ tick labels color
    ),
    yaxis=dict(
        title="1000 tonnes",
        title_font=dict(color="black", size=13),
        tickfont=dict(color="black", size=13)
    )
    )

    


    y_max = 1300


    figWaste2.update_layout(
        yaxis=dict(
            title="1000 tonnes",
            range=[0, y_max * 1.15]   # ✅ increase space by 15%
        )
    )


    #figWaste2.update_xaxes(tickangle=-45)

    st.plotly_chart(figWaste2, key="compare_early_regular11")



#===========================annaul compare

def plot_eol_annual_compare1_si():


    x_col = inp.df.iloc[1:, 0]
    x_col = np.append(x_col, 2101)

    years = x_col[:len(ls.yearlyEoL_si)]
    
    euweee_values = np.array(ls.EUWEEE_ann_si) / 1e3
    regular_loss  = np.array(ls.RegularLoss_ann_si) / 1e3

    df_plot = pd.DataFrame({
        "Year": years,
        "EU-WEEE": euweee_values,
        "Regular Loss": regular_loss
    })

    df_plot = df_plot[
        (df_plot["Year"] >= 2020) & (df_plot["Year"] <= 2040)
    ]

    # ✅ Label control (avoid clutter)
    df_long = df_plot.melt(
        id_vars="Year",
        value_vars=["EU-WEEE", "Regular Loss"],
        var_name="Category",
        value_name="Value"
    )

    df_long["label"] = df_long["Value"].apply(
        lambda v: f"{v:.1f}" if v > 2 else ""
    )

    # ✅ Plot
    figWaste2 = px.bar(
        df_long,
        x="Year",
        y="Value",
        color="Category",
        text="label",
        title="Annual Secondary Silicon from EoL c-Si PV (2020–2040)",
        labels={"Value": "1000 tonnes", "Year": "Year"},
        color_discrete_map={
            "EU-WEEE": "#00CFFF",
            "Regular Loss": "#006D77"
        }
    )

    figWaste2.update_traces(
        marker=dict(
            line=dict(
                color="#2F4F6F",  # dark blue border
                width=1.5
            )
            )
    )

    # ✅ Overlay mode (as you intended)
    figWaste2.update_layout(
    barmode="overlay",
    width=800,
    height=500,
    template="plotly_white",
    margin=dict(l=60, r=40, t=80, b=60),   # ✅ comma added
    

    legend=dict(
        x=0,              # move to left
        y=1,
        xanchor="left",
        yanchor="top",
        orientation="v"
    )
    )


    # ✅ Vertical labels + styling
    figWaste2.update_traces(
        textposition='outside',
        textangle=90,                      # ✅ vertical labels
        textfont=dict(size=14, color="black")
    )

    figWaste2.update_layout(
    xaxis=dict(
        title="Year",
        title_font=dict(color="black", size=13),   # ✅ axis title color
        tickfont=dict(color="black", size=13)       # ✅ tick labels color
    ),
    yaxis=dict(
        title="Value (1000 tonnes)",
        title_font=dict(color="black", size=13),
        tickfont=dict(color="black", size=13)
    )
    )

    


    y_max = 50


    figWaste2.update_layout(
        yaxis=dict(
            title="1000 tonnes",
            range=[0, y_max * 1.15]   # ✅ increase space by 15%
        )
    )


    #figWaste2.update_xaxes(tickangle=-45)

    st.plotly_chart(figWaste2, key="compare_early_regular11si")


#=============================================================


def plot_eol_cumulative_compare1_si():

    import numpy as np
    import pandas as pd
    import plotly.express as px
    import streamlit as st

    x_col = inp.df.iloc[1:, 0]
    x_col = np.append(x_col, 2101)

    years = x_col[:len(ls.yearlyEoL_si)]

    
    euweee_values = np.array(ls.EUWEEE_cum_si) / 1e3
    regular_loss  = np.array(ls.RegularLoss_cum_si) / 1e3


    df_plot = pd.DataFrame({
        "Year": years,
        "EU-WEEE": euweee_values,
        "Regular Loss": regular_loss
    })

    df_plot = df_plot[
        (df_plot["Year"] >= 2020) & (df_plot["Year"] <= 2040)
    ]

    # ✅ Label control (avoid clutter)
    df_long = df_plot.melt(
        id_vars="Year",
        value_vars=["EU-WEEE", "Regular Loss"],
        var_name="Category",
        value_name="Value"
    )

    df_long["label"] = df_long["Value"].apply(
        lambda v: f"{v:.1f}" if v > 10 else ""
    )

    # ✅ Plot
    figWaste2 = px.bar(
        df_long,
        x="Year",
        y="Value",
        color="Category",
        text="label",
        title="Cumulative Secondary Silicon from EoL c-Si PV (2020–2040)",
        labels={"Value": "1000 tonnes", "Year": "Year"},
        color_discrete_map={
            "EU-WEEE": "#00CFFF",
            "Regular Loss": "#006D77"
        }
    )

    # ✅ Overlay mode (as you intended)
    figWaste2.update_layout(
    barmode="overlay",
    width=800,
    height=500,
    template="plotly_white",
    margin=dict(l=60, r=40, t=80, b=60),   # ✅ comma added
    

    legend=dict(
        x=0,              # move to left
        y=1,
        xanchor="left",
        yanchor="top",
        orientation="v"
    )
)


    # ✅ Vertical labels + styling
    figWaste2.update_traces(
        textposition='outside',
        textangle=90,                      # ✅ vertical labels
        textfont=dict(size=14, color="black")
    )

    figWaste2.update_layout(
    xaxis=dict(
        title="Year",
        title_font=dict(color="black", size=13),   # ✅ axis title color
        tickfont=dict(color="black", size=13)       # ✅ tick labels color
    ),
    yaxis=dict(
        title="1000 tonnes",
        title_font=dict(color="black", size=13),
        tickfont=dict(color="black", size=13)
    )
    )
    
    y_max = 400
    

    figWaste2.update_layout(
        yaxis=dict(
            title="1000 tonnes",
            range=[0, y_max * 1.15]   # ✅ increase space by 15%
        )
    )


    #figWaste2.update_xaxes(tickangle=-45)

    st.plotly_chart(figWaste2, key="compare_early_regular1si")

def plot_eol_annual_compare1():


    x_col = inp.df.iloc[1:, 0]
    x_col = np.append(x_col, 2101)

    years = x_col[:len(ls.yearlyEoL)]
    
    euweee_values = np.array(ls.EUWEEE_ann) / 1e3
    regular_loss  = np.array(ls.RegularLoss_ann) / 1e3

    df_plot = pd.DataFrame({
        "Year": years,
        "EU-WEEE": euweee_values,
        "Regular Loss": regular_loss
    })

    df_plot = df_plot[
        (df_plot["Year"] >= 2020) & (df_plot["Year"] <= 2040)
    ]

    # ✅ Label control (avoid clutter)
    df_long = df_plot.melt(
        id_vars="Year",
        value_vars=["EU-WEEE", "Regular Loss"],
        var_name="Category",
        value_name="Value"
    )

    df_long["label"] = df_long["Value"].apply(
        lambda v: f"{v:.0f}" if v > 45 else ""
    )

    # ✅ Plot
    figWaste2 = px.bar(
    df_long,
    x="Year",
    y="Value",
    color="Category",
    text="label",
    title="Annual Secondary Silicon from EoL c-Si PV (2020–2040)",
    labels={"Value": "1000 tonnes", "Year": "Year"},
    color_discrete_map={
        "EU-WEEE": "#90CAF9",     # ✅ dark blue
        "Regular Loss": "#0B5394"
    }
)

    figWaste2.update_traces(
        marker=dict(
            line=dict(
                color="#2F4F6F",  # dark blue border
                width=1.5
            )
            )
)

    # ✅ Overlay mode (as you intended)
    figWaste2.update_layout(
    barmode="overlay",
    width=800,
    height=500,
    template="plotly_white",
    margin=dict(l=60, r=40, t=80, b=60),   # ✅ comma added
    

    legend=dict(
        x=0,              # move to left
        y=1,
        xanchor="left",
        yanchor="top",
        orientation="v"
    )
)


    # ✅ Vertical labels + styling
    figWaste2.update_traces(
        textposition='outside',
        textangle=90,                      # ✅ vertical labels
        textfont=dict(size=14, color="black")
    )

    figWaste2.update_layout(
    xaxis=dict(
        title="Year",
        title_font=dict(color="black", size=13),   # ✅ axis title color
        tickfont=dict(color="black", size=13)       # ✅ tick labels color
    ),
    yaxis=dict(
        title="1000 tonnes",
        title_font=dict(color="black", size=13),
        tickfont=dict(color="black", size=13)
    )
    )

    


    y_max = 1300


    figWaste2.update_layout(
        yaxis=dict(
            title="1000 tonnes",
            range=[0, y_max * 1.15]   # ✅ increase space by 15%
        )
    )


    #figWaste2.update_xaxes(tickangle=-45)

    st.plotly_chart(figWaste2, key="compare_early_regular11")



#===========================annaul compare

def plot_eol_annual_compare1_gw(reg, eu):


    x_col = inp.df.iloc[1:, 0]
    x_col = np.append(x_col, 2101)

    years = x_col[:len(ls.yearlyEoL_si)]
    
    euweee_values = np.array(eu) / 1e3
    regular_loss  = np.array(reg) / 1e3
    

    df_plot = pd.DataFrame({
        "Year": years,
        "EU-WEEE": euweee_values,
        "Regular Loss": regular_loss
    })

    df_plot = df_plot[
        (df_plot["Year"] >= 2020) & (df_plot["Year"] <= 2040)
    ]

    # ✅ Label control (avoid clutter)
    df_long = df_plot.melt(
        id_vars="Year",
        value_vars=["EU-WEEE", "Regular Loss"],
        var_name="Category",
        value_name="Value"
    )

    df_long["label"] = df_long["Value"].apply(
        lambda v: f"{v:.1f}" if v > 0.6 else ""
    )

    # ✅ Plot
    figWaste2 = px.bar(
        df_long,
        x="Year",
        y="Value",
        color="Category",
        text="label",
        title="Potential of Secondary Silicon from EoL c-Si PV",
        labels={"Value": "1000 tonnes", "Year": "Year"},
        color_discrete_map={
            "EU-WEEE": "#FFD6A5",
            "Regular Loss": "#0B3C5D"
        }
    )

    figWaste2.update_traces(
        marker=dict(
            line=dict(
                color="#2F4F6F",  # dark blue border
                width=1.5
            )
            )
    )

    # ✅ Overlay mode (as you intended)
    figWaste2.update_layout(
    barmode="overlay",
    width=800,
    height=500,
    template="plotly_white",
    margin=dict(l=60, r=40, t=80, b=60),   # ✅ comma added
    

    legend=dict(
        x=0,              # move to left
        y=1,
        xanchor="left",
        yanchor="top",
        orientation="v"
    )
    )


    # ✅ Vertical labels + styling
    figWaste2.update_traces(
        textposition='outside',
        textangle=90,                      # ✅ vertical labels
        textfont=dict(size=14, color="black")
    )

    figWaste2.update_layout(
    xaxis=dict(
        title="Year",
        title_font=dict(color="black", size=13),   # ✅ axis title color
        tickfont=dict(color="black", size=13)       # ✅ tick labels color
    ),
    yaxis=dict(
        title="GW",
        title_font=dict(color="black", size=13),
        tickfont=dict(color="black", size=13)
    )
    )

    


    y_max = 22


    figWaste2.update_layout(
        yaxis=dict(
            title="GW",
            range=[0, y_max * 1.15]   # ✅ increase space by 15%
        )
    )


    #figWaste2.update_xaxes(tickangle=-45)

    st.plotly_chart(figWaste2, key="compare_early_regular11gw")

