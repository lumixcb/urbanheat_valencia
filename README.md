# 🌡️ UrbanHeat Valencia – Geospatial-Climate Dashboard & Heat-Island Prediction

UrbanHeat Valencia is an interactive web application that identifies urban heat-island hotspots in Valencia by combining historical climate records, high-resolution vegetation maps, and machine-learning models. Built with Streamlit, Folium, PyDeck and scikit-learn, UrbanHeat supports urban planners, researchers and citizens in understanding spatial thermal risks and planning mitigation strategies.

---

## 📁 Project Structure

- **app/** – Streamlit application  
  - `main.py` — entry point & UI logic  
  - `utils.py` — data-loading & helper functions
- **data/**  
  - **raw/** — original CSV & GeoJSON datasets  
  - **processed/** — cleaned data & model inputs
- **models/** — trained pipelines & pickled models  
- **notebooks/** — EDA & modeling Jupyter notebooks  
- **media/** — static assets (maps, screenshots)  
- `requirements.txt` — Python dependencies  
- `README.md` — this guide

---

## 📊 Datasets

1. **Temperatura València (2018–2022)**  
   Daily mean/max/min temperature, precipitation, wind speed & gusts  
   Source: Valencia OpenData  
2. **Cartografía Base Vegetación**  
   GeoJSON polygons of urban greenery (parks, gardens, agricultural limits)  
   Source: Valencia OpenData  
3. **[Optional] Socioeconomic & Urban Factors**  
   (Future integration: building density, land use, demographics)

---

## 🎯 Features & Workflow

- **Data Exploration**  
  - Filter by date range & temperature thresholds  
  - Interactive tables & summary statistics  
  - Time-series chart of daily mean temperature
- **Spatial Visualization**  
  - Folium map of vegetation cover with light/dark basemaps  
  - Tooltips showing type & creation date of each polygon
- **Predictive Modeling**  
  - **Linear Regression** for interpretability (inspect coefficients)  
  - **Random Forest** for non-linear accuracy (view feature importances)  
  - Instant Tmax forecasts from user inputs
- **User Journey**  
  1. **Data** – explore, filter & download subsets  
  2. **Map** – assess green infrastructure distribution  
  3. **Prediction** – enter today’s metrics & choose model for forecast

---

## ⚙️ Installation & Run

1. **Clone the repo**

git clone https://github.com/lumixcb/urbanheat_valencia.git
cd urbanheat_valencia

3. **Create & activate venv**

python -m venv venv

Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

4. **Install dependencies**

pip install -r requirements.txt
Launch the app
streamlit run app/main.py

## 🔍 Methodology & Pipeline

- Cleaning: parse semicolon-delimited CSV, replace decimal commas, coerce dates

- Features: six climate predictors, drop missing, 80/20 train/test split

- Models:

     - Linear Regression baseline (R² ~1.00)
     - Random Forest (100 trees, R² ~0.996), 5-fold CV & feature importances
     - Deployment: pipelines serialized with joblib, integrated into Streamlit

## 🤝 Collaboration

GitHub: https://github.com/lumixcb/urbanheat_valencia

Team: Luminita Ciobanu Borinschi, Javier Elena Navarro & Pau Amores Giner

Contributions and issues welcome via GitHub!
