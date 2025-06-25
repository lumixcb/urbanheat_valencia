import os

import streamlit as st
import pandas as pd
import geopandas as gpd
import joblib
import folium
from streamlit_folium import st_folium
import plotly.express as px

# ─── 1 ─ Page config & custom CSS ────────────────────────────────────────────
st.set_page_config(
    page_title="UrbanHeat Valencia",
    layout="wide",
)

st.markdown(
    """
    <style>
      body {background-color: #e8f5e9;}
      .stApp, .css-18e3th9 {background-color: #e8f5e9;}
      h1, h2, h3, h4, h5, p, li {
        color: #1b5e20 !important;
        font-family: 'Arial', sans-serif;
      }
      .css-10trblm {
        color: #1b5e20 !important;
        font-weight: bold !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── 2 ─ Sidebar navigation ──────────────────────────────────────────────────
page = st.sidebar.radio("", ("Home", "Data", "Map", "Prediction"))

# ─── 3 ─ Cached loaders ──────────────────────────────────────────────────────
@st.cache_data
def load_temperature():
    path = os.path.join("data", "raw", "temperatura_valencia.csv")
    df = pd.read_csv(path, sep=";")
    for col in ["tmed", "tmax", "tmin", "prec", "velmedia", "racha"]:
        df[col] = df[col].str.replace(",", ".").astype(float)
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce", infer_datetime_format=True)
    return df

@st.cache_data
def load_vegetation():
    path = os.path.join("data", "raw", "vegetacion_valencia.geojson")
    return gpd.read_file(path)

# ─── 4 ─ Home ─────────────────────────────────────────────────────────────────
if page == "Home":
    st.title("UrbanHeat Valencia")
    st.markdown(
        """
        **UrbanHeat Valencia** is a geospatial–climate dashboard that:

        1. **Detects** urban heat-island hotspots.  
        2. **Visualizes** historical temperature & vegetation data.  
        3. **Predicts** daily maximum temperature from climate inputs.  
        4. **Offers** interactive maps, charts & model interpretability.

        **Use the menu to navigate:**

        - **Data:** Browse and summarize climate & vegetation tables.  
        - **Map:** Explore the city’s green infrastructure and its role in urban cooling.  
        - **Prediction:** Input today’s metrics and choose Linear vs Random Forest for instant Tmax forecasts.
        """
    )
    st.markdown(
        "_Built by Luminita Ciobanu Borinschi, Javier Elena Navarro & Pau Amores Giner, integrating Valencia Open Data._"
    )

# ─── 5 ─ Data ─────────────────────────────────────────────────────────────────
elif page == "Data":
    st.title("Data")
    st.markdown(
        """
        **Browse the datasets below.**  
        - **Climate time series:** Daily mean, max, min, precipitation, wind speed & gusts (2018–2022).  
        - **Vegetation cover:** Polygonal boundaries of urban parks, gardens & agricultural limits.
        """
    )

    df = load_temperature()

    # — 5.1 — Date range filter
    fecha_min = df["fecha"].min().date()
    fecha_max = df["fecha"].max().date()
    start, end = st.slider(
        "Select date range:",
        min_value=fecha_min,
        max_value=fecha_max,
        value=(fecha_min, fecha_max),
        format="YYYY-MM-DD"
    )
    st.caption("Choose the period you want to explore.")
    mask = (df["fecha"].dt.date >= start) & (df["fecha"].dt.date <= end)
    df_filt = df.loc[mask]

    # — 5.2 — Min/Max temp filters
    col1, col2 = st.columns(2)
    with col1:
        tmin_val = st.slider(
            "Min Temp ≥",
            float(df_filt["tmin"].min()), float(df_filt["tmin"].max()),
            float(df_filt["tmin"].min())
        )
        st.caption("Filter out days colder than this value.")
    with col2:
        tmax_val = st.slider(
            "Max Temp ≤",
            float(df_filt["tmax"].min()), float(df_filt["tmax"].max()),
            float(df_filt["tmax"].max())
        )
        st.caption("Filter out days hotter than this value.")
    df_filt = df_filt[(df_filt["tmin"] >= tmin_val) & (df_filt["tmax"] <= tmax_val)]

    # — 5.3 — Climate snapshot (dataframe)
    st.subheader("Climate Data Snapshot")
    st.dataframe(df_filt.head(10), use_container_width=True)
    st.markdown("_Above are the first 10 records of the filtered climate dataset._")

    # — 5.4 — Summary statistics
    st.subheader("Summary Statistics")
    st.dataframe(df_filt.describe().round(2), use_container_width=True)
    st.markdown("_Basic metrics (count, mean, std, min/max) for the selected subset._")

    # — 5.5 — Time-series plot
    st.subheader("Daily Mean Temperature Over Time")
    fig_ts = px.line(
        df_filt, x="fecha", y="tmed",
        labels={"fecha": "Date", "tmed": "Mean Temp (°C)"}
    )
    fig_ts.update_traces(connectgaps=False)
    st.plotly_chart(fig_ts, use_container_width=True)
    st.markdown("_Seasonal cycles and interannual variations in mean daily temperature._")

    # — 5.6 — Download button
    csv = df_filt.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data as CSV",
        data=csv,
        file_name="temperatura_valencia_filtered.csv",
        mime="text/csv"
    )

# ─── 6 ─ Map ──────────────────────────────────────────────────────────────────
elif page == "Map":
    st.title("Map")
    st.markdown(
        """
        **Interactive Vegetation Map**  
        Explore how Valencia’s green infrastructure — parks, gardens, tree-lined streets — is distributed across the city.  
        Urban greenery plays a key role in moderating local temperatures and mitigating heat-island effects.
        """
    )

    veg = load_vegetation()
    veg["fechacreac"] = veg["fechacreac"].astype(str)

    m = folium.Map(location=[39.4699, -0.3763], zoom_start=12)
    folium.TileLayer("cartodbpositron", name="Light").add_to(m)
    folium.TileLayer("cartodbdark_matter", name="Dark").add_to(m)

    folium.GeoJson(
        veg[["elemento", "fechacreac", "geometry"]].to_json(),
        name="Vegetation",
        tooltip=folium.GeoJsonTooltip(
            fields=["elemento", "fechacreac"],
            aliases=["Type", "Created on"],
            localize=True
        ),
        style_function=lambda f: {"color": "#2ECC71", "weight": 1, "fillOpacity": 0.5}
    ).add_to(m)

    folium.LayerControl().add_to(m)
    st_folium(m, width=900, height=600)
    st.markdown(
        "_Understanding the spatial distribution of vegetation helps explain model predictions: areas with denser greenery tend to exhibit lower maximum temperatures._"
    )

# ─── 7 ─ Prediction ───────────────────────────────────────────────────────────
elif page == "Prediction":
    st.title("Prediction")
    st.markdown(
        """
        In this section you can forecast Valencia’s daily maximum temperature using two machine-learning models:

        - **Linear Regression:** A straightforward statistical model where each climate feature contributes linearly to the predicted Tmax.  
        - **Random Forest:** An ensemble of decision trees that captures complex, non-linear interactions between variables, often improving accuracy at the cost of interpretability.

        **How it works:**  
        1. We trained both models on five years of historical data (2018–2022), preprocessing and splitting into training/testing sets.  
        2. The Linear Regression provides coefficient values you can inspect in the code to understand each feature’s direct impact.  
        3. The Random Forest outputs feature importances so you can see which variables drive the temperature forecast most strongly.  

        Simply enter today’s weather observations below, choose your preferred model, and click **Compute Tmax** to obtain an instant estimate.
        """
    )

    tmed     = st.number_input("Mean Temp (°C)",     0.0, 50.0, 25.0, step=0.1)
    tmin     = st.number_input("Min Temp (°C)",     -5.0, 50.0, 18.0, step=0.1)
    prec     = st.number_input("Precipitation (mm)",  0.0,200.0, 0.0, step=0.1)
    velmedia = st.number_input("Wind Speed (km/h)",   0.0,20.0, 1.5, step=0.1)
    racha    = st.number_input("Wind Gust (km/h)",    0.0,50.0, 4.0, step=0.1)
    direc    = st.number_input("Wind Direction (°)",  0.0,360.0,180.0, step=1.0)

    model_choice = st.radio("Model", ["Linear Regression", "Random Forest"])
    model_file   = "pipeline_tmax_lr.pkl" if model_choice=="Linear Regression" else "pipeline_tmax_rf.pkl"
    pipeline     = joblib.load(os.path.join("models", model_file))

    if st.button("Compute Tmax"):
        X_new = pd.DataFrame([{
            "tmed":tmed, "tmin":tmin, "prec":prec,
            "velmedia":velmedia, "racha":racha, "dir":direc
        }])
        pred = pipeline.predict(X_new)[0]
        st.success(f"Estimated Tmax: **{pred:.1f} °C**")

        if model_choice == "Random Forest":
            rf_model = pipeline.named_steps["model"]
            fi = pd.Series(
                rf_model.feature_importances_,
                index=["tmed","tmin","prec","velmedia","racha","dir"]
            ).sort_values()
            fig_fi = px.bar(
                fi, x=fi.values, y=fi.index, orientation="h",
                labels={"x":"Importance","index":"Feature"},
                title="Random Forest Feature Importances"
            )
            st.plotly_chart(fig_fi, use_container_width=True)
            st.markdown("_Which inputs most influence the RF prediction._")
        else:
            st.markdown("_Inspect the LR coefficients in code for direct feature effects._")

# ─── How to run ───────────────────────────────────────────────────────────────
# cd "C:\Users\lumin\Desktop\2 Cuatri\Evaluación, Despliegue y Monitorización de Modelos\urbanheat_valencia"
# C:/Users/lumin/AppData/Local/Programs/Python/Python310/python.exe -m streamlit run app/main.py