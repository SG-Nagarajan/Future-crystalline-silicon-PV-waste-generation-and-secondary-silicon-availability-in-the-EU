
    col1 = inp.df.iloc[:, 10]
    col2 = inp.df.iloc[:, 11]

    df_plot = pd.DataFrame({
        "Year": col1,
        "Weight": col2
    }).dropna()

    df_plot["Year"] = df_plot["Year"].astype(int)
    df_plot = df_plot.sort_values("Year")

    fig = px.violin(
        df_plot,
        x="Year",
        y="Weight",
        box=True,
        points=False
    )

    fig.update_layout(
        template="plotly_white",
        width=800,
        height=400
    )

st.plotly_chart(fig)


import plotly.express as px
import plotly.graph_objects as go

def plot_violin_with_overlay():

    # ✅ OLD DATA → many values per year
    col1 = inp.df.iloc[:, 10]
    col2 = inp.df.iloc[:, 11]

    df_plot = pd.DataFrame({
        "Year": col1,
        "Weight": col2
    }).dropna()

    df_plot["Year"] = df_plot["Year"].astype(int)
    df_plot = df_plot.sort_values("Year")

    # ✅ NEW DATA → single value per year
    year_new = new_df["Year"]        # 2006–2024
    weight_new = new_df["Weight"]   # one value per year

    # ✅ Create violin plot
    fig = px.violin(
        df_plot,
        x="Year",
        y="Weight",
        box=True,
        points=False
    )

    # ✅ ADD LINE OVERLAY (your new data)
    fig.add_trace(
        go.Scatter(
            x=year_new,
            y=weight_new,
            mode="lines+markers",   # ✅ line + dots
            name="New Dataset",
            line=dict(color="red", width=3),
            marker=dict(size=6)
        )
    )

    # ✅ Layout
    fig.update_layout(
        template="plotly_white",
        width=800,
        height=450,
        title="Weight Distribution + Trend Overlay"
    )
       