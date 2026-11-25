import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

# Page Configuration
st.set_page_config(
    page_title="AQI Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Complete Dark Glassmorphism CSS (Fixes all light-mode text & widget contrast)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Main App, Top Header & Sidebar Dark Background */
    .stApp {
        background-color: #0B0F19;
        color: #F1F5F9;
    }
    header[data-testid="stHeader"] {
        background-color: #0B0F19 !important;
        color: #F1F5F9 !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1F2937;
    }

    /* Force All Headings, Paragraphs, and Widget Labels to Light Text */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    [data-testid="stWidgetLabel"] p {
        color: #F1F5F9 !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #94A3B8 !important;
    }

    /* Main Area Preset & Action Buttons */
    .main .stButton > button {
        background-color: rgba(30, 41, 59, 0.75) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .main .stButton > button:hover {
        background-color: rgba(56, 189, 248, 0.18) !important;
        border-color: #38BDF8 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2) !important;
    }

    /* Sidebar Navigation Bar Buttons (Inactive) */
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background-color: rgba(30, 41, 59, 0.5) !important;
        color: #CBD5E1 !important;
        border: 1px solid rgba(148, 163, 184, 0.15) !important;
        border-left: 4px solid transparent !important;
        border-radius: 10px !important;
        padding: 0.65rem 1rem !important;
        text-align: left !important;
        justify-content: flex-start !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.22s ease !important;
    }

    /* Sidebar Navigation Bar Buttons (Hover Effect) */
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        background-color: rgba(56, 189, 248, 0.15) !important;
        color: #FFFFFF !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
        border-left: 4px solid #38BDF8 !important;
        transform: translateX(6px);
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.2) !important;
    }

    /* Sidebar Navigation Bar Buttons (Active Page) */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, rgba(56, 189, 248, 0.28) 0%, rgba(30, 41, 59, 0.9) 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(56, 189, 248, 0.55) !important;
        border-left: 4px solid #38BDF8 !important;
        border-radius: 10px !important;
        padding: 0.65rem 1rem !important;
        text-align: left !important;
        justify-content: flex-start !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        box-shadow: 0 4px 16px rgba(56, 189, 248, 0.22) !important;
    }

    /* Minimal Top Header */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 16px;
        margin-bottom: 20px;
        border-bottom: 1px solid #1F2937;
    }
    .top-title {
        font-size: 1.85rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0;
    }
    .top-sub {
        font-size: 0.92rem;
        color: #94A3B8;
        margin: 4px 0 0 0;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 14px;
    }
    .aqi-hero-box {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 18px;
        padding: 24px 20px;
        text-align: center;
        margin-bottom: 16px;
    }
    .aqi-big-num {
        font-size: 4.1rem;
        font-weight: 700;
        line-height: 1;
        margin: 8px 0;
    }
    .aqi-badge {
        display: inline-block;
        padding: 5px 16px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.92rem;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        color: #FFFFFF;
    }

    /* 2x2 Action Grid */
    .action-tile {
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 12px;
        padding: 14px 12px;
        text-align: left;
        margin-bottom: 10px;
    }
    .action-label {
        font-size: 0.72rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        font-weight: 600;
    }
    .action-val {
        font-size: 0.98rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 4px;
        white-space: nowrap;
    }

    /* CPCB Styled Row */
    .cpcb-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 14px;
        border-radius: 10px;
        background: rgba(30, 41, 59, 0.55);
        margin-bottom: 8px;
        border-left: 5px solid #38BDF8;
    }
</style>
""", unsafe_allow_html=True)

# Load Model & Dataset
FEATURES = ['PM2.5', 'PM10', 'NO2', 'NH3', 'CO', 'SO2', 'O3']

@st.cache_resource
def load_model():
    return joblib.load("models/aqi_model.pkl")

@st.cache_data
def load_city_data():
    if os.path.exists("city_day.csv"):
        df = pd.read_csv("city_day.csv")
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df.dropna(subset=['AQI'])
    return None

model = load_model()
city_df = load_city_data()

# CPCB Helper
def get_aqi_details(aqi):
    if aqi <= 50:
        return ("Good", "#22C55E", "Minimal impact. Air is clean and fresh.",
                "Safe", "Keep Open", "Not Needed", "Optional")
    elif aqi <= 100:
        return ("Satisfactory", "#84CC16", "Minor breathing discomfort possible for sensitive people.",
                "Safe", "Keep Open", "Not Needed", "Optional")
    elif aqi <= 200:
        return ("Moderate", "#F59E0B", "Discomfort possible for people with asthma, lung, or heart disease.",
                "Light Only", "Limit", "Optional", "Recommended")
    elif aqi <= 300:
        return ("Poor", "#F97316", "Breathing discomfort on prolonged exposure. Reduce outdoor time.",
                "Avoid", "Close", "Wear Mask", "Turn On")
    elif aqi <= 400:
        return ("Very Poor", "#EF4444", "Respiratory illness risk on prolonged exposure. Stay indoors.",
                "Stay Indoors", "Keep Closed", "N95 Mask", "High Mode")
    else:
        return ("Severe", "#B91C1C", "Health emergency! Affects healthy people and seriously impacts those with conditions.",
                "No Outdoor", "Seal Tight", "N95 Mandatory", "Max Mode")

# Session State for Navigation & Presets
if "page" not in st.session_state:
    st.session_state.page = "Live Predictor"

defaults = {"pm25": 65.0, "pm10": 115.0, "no2": 32.0, "nh3": 20.0, "co": 1.1, "so2": 14.0, "o3": 38.0}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def set_preset(pm25, pm10, no2, nh3, co, so2, o3):
    st.session_state.pm25 = pm25
    st.session_state.pm10 = pm10
    st.session_state.no2 = no2
    st.session_state.nh3 = nh3
    st.session_state.co = co
    st.session_state.so2 = so2
    st.session_state.o3 = o3

# Sidebar Navigation (Bar Buttons with Hover Effects)
with st.sidebar:
    st.markdown("""
    <div style="padding: 4px 0 6px 0;">
        <div style="font-size: 1.25rem; font-weight: 700; color: #F8FAFC;">⚡ AQI Command Center</div>
        <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 2px;">Hyperlocal Air Pollution Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    nav_items = [
        ("Live Predictor", "🎛️  Live Predictor"),
        ("Indian City Explorer", "🏙️  Indian City Explorer"),
        ("Batch CSV Analysis", "📂  Batch CSV Analysis"),
        ("Model & CPCB Scale", "📊  Model & CPCB Scale"),
    ]

    for page_key, label in nav_items:
        btn_type = "primary" if st.session_state.page == page_key else "secondary"
        if st.button(label, key=f"nav_{page_key}", use_container_width=True, type=btn_type):
            st.session_state.page = page_key
            st.rerun()

    st.divider()
    st.markdown("""
    <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.8;">
        <b style="color:#E2E8F0;">Model:</b> Random Forest Regressor<br>
        <b style="color:#E2E8F0;">Standard:</b> Indian CPCB AQI<br>
        <b style="color:#E2E8F0;">Data:</b> India City Day (2015–2020)
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.page

# ==========================================
# PAGE 1: LIVE PREDICTOR
# ==========================================
if page == "Live Predictor":
    st.markdown("""
    <div class="top-header">
        <div>
            <div class="top-title">Live AQI Telemetry & Prediction</div>
            <div class="top-sub">Adjust atmospheric pollutant levels or load a preset scenario below.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Horizontal Quick Preset Bar
    p1, p2, p3, p4 = st.columns(4)
    p1.button("🌿 Clean Morning", use_container_width=True, on_click=set_preset, args=(18.0, 35.0, 12.0, 8.0, 0.4, 6.0, 25.0))
    p2.button("🏙️ Moderate City", use_container_width=True, on_click=set_preset, args=(75.0, 140.0, 40.0, 22.0, 1.3, 18.0, 45.0))
    p3.button("🏭 Industrial Haze", use_container_width=True, on_click=set_preset, args=(160.0, 260.0, 68.0, 38.0, 2.4, 35.0, 55.0))
    p4.button("🌫️ Severe Winter Smog", use_container_width=True, on_click=set_preset, args=(280.0, 420.0, 95.0, 55.0, 3.8, 42.0, 75.0))

    st.write("")
    col_inputs, col_result, col_radar = st.columns([1.0, 1.05, 1.15], gap="large")

    with col_inputs:
        st.markdown("#### Sensor Controls")
        pm25 = st.slider("PM2.5 (µg/m³)", 0.0, 500.0, key="pm25", step=1.0)
        pm10 = st.slider("PM10 (µg/m³)", 0.0, 600.0, key="pm10", step=1.0)
        no2  = st.slider("NO₂ (µg/m³)", 0.0, 200.0, key="no2", step=1.0)
        nh3  = st.slider("NH₃ (µg/m³)", 0.0, 150.0, key="nh3", step=1.0)
        co   = st.slider("CO (mg/m³)", 0.0, 10.0, key="co", step=0.1)
        so2  = st.slider("SO₂ (µg/m³)", 0.0, 150.0, key="so2", step=1.0)
        o3   = st.slider("O₃ (µg/m³)", 0.0, 200.0, key="o3", step=1.0)

    # Prediction
    input_df = pd.DataFrame([[pm25, pm10, no2, nh3, co, so2, o3]], columns=FEATURES)
    predicted_aqi = max(0.0, round(float(model.predict(input_df)[0]), 1))
    category, color, advisory, outdoor, windows, mask, purifier = get_aqi_details(predicted_aqi)

    ratios = {
        "PM2.5": pm25 / 60, "PM10": pm10 / 100, "NO₂": no2 / 80,
        "NH₃": nh3 / 400, "CO": co / 2.0, "SO₂": so2 / 80, "O₃": o3 / 100
    }
    dominant = max(ratios, key=ratios.get)

    with col_result:
        st.markdown(f"""
        <div class="aqi-hero-box" style="border: 1px solid {color}; box-shadow: 0 0 28px {color}33;">
            <div style="font-size: 0.8rem; color: #94A3B8; letter-spacing: 1px; text-transform: uppercase;">Predicted AQI</div>
            <div class="aqi-big-num" style="color: {color};">{predicted_aqi}</div>
            <div class="aqi-badge" style="background-color: {color};">{category}</div>
            <div style="margin-top: 14px; font-size: 0.88rem; color: #CBD5E1;">{advisory}</div>
        </div>
        """, unsafe_allow_html=True)

        # 2x2 Action Grid
        g1, g2 = st.columns(2)
        with g1:
            st.markdown(f'<div class="action-tile"><div class="action-label">Outdoor Activity</div><div class="action-val">{outdoor}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="action-tile"><div class="action-label">Mask Advice</div><div class="action-val">{mask}</div></div>', unsafe_allow_html=True)
        with g2:
            st.markdown(f'<div class="action-tile"><div class="action-label">Ventilation</div><div class="action-val">{windows}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="action-tile"><div class="action-label">Air Purifier</div><div class="action-val">{purifier}</div></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="glass-card" style="padding: 12px 16px; border-left: 4px solid {color};">
            <span style="color:#94A3B8; font-size:0.85rem;">Dominant Pollutant:</span>
            <strong style="color:#F8FAFC; font-size:1rem; margin-left:6px;">{dominant}</strong>
        </div>
        """, unsafe_allow_html=True)

    with col_radar:
        st.markdown("#### Pollutant Footprint (Normalized %)")
        radar_vals = [
            min(pm25 / 60 * 100, 300),
            min(pm10 / 100 * 100, 300),
            min(no2 / 80 * 100, 300),
            min(nh3 / 400 * 100, 300),
            min(co / 2.0 * 100, 300),
            min(so2 / 80 * 100, 300),
            min(o3 / 100 * 100, 300),
        ]
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=radar_vals + [radar_vals[0]],
            theta=FEATURES + [FEATURES[0]],
            fill='toself',
            fillcolor=f"{color}44",
            line=dict(color=color, width=2.5)
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="rgba(15, 23, 42, 0.6)",
                radialaxis=dict(visible=True, range=[0, 300], gridcolor="#334155", tickfont=dict(color="#94A3B8")),
                angularaxis=dict(gridcolor="#334155", tickfont=dict(color="#E2E8F0", size=12))
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=410,
            margin=dict(l=55, r=55, t=30, b=30),
            showlegend=False
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# ==========================================
# PAGE 2: INDIAN CITY EXPLORER
# ==========================================
elif page == "Indian City Explorer":
    st.markdown("""
    <div class="top-header">
        <div>
            <div class="top-title">Indian City Air Quality Explorer</div>
            <div class="top-sub">Historical daily AQI trends from 2015 to 2020 across major Indian cities.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if city_df is None:
        st.warning("`city_day.csv` not found in the project folder.")
    else:
        cities = sorted(city_df['City'].unique())
        default_idx = cities.index("Delhi") if "Delhi" in cities else 0
        selected_city = st.selectbox("Select City", cities, index=default_idx)

        cdf = city_df[city_df['City'] == selected_city].sort_values("Date")

        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(f'<div class="glass-card"><div class="action-label">Average AQI</div><div class="action-val" style="font-size:1.7rem; color:#38BDF8;">{cdf["AQI"].mean():.1f}</div></div>', unsafe_allow_html=True)
        k2.markdown(f'<div class="glass-card"><div class="action-label">Peak AQI</div><div class="action-val" style="font-size:1.7rem; color:#EF4444;">{cdf["AQI"].max():.0f}</div></div>', unsafe_allow_html=True)
        k3.markdown(f'<div class="glass-card"><div class="action-label">Lowest AQI</div><div class="action-val" style="font-size:1.7rem; color:#22C55E;">{cdf["AQI"].min():.0f}</div></div>', unsafe_allow_html=True)
        k4.markdown(f'<div class="glass-card"><div class="action-label">Days Logged</div><div class="action-val" style="font-size:1.7rem;">{len(cdf):,}</div></div>', unsafe_allow_html=True)

        fig_line = px.area(
            cdf, x="Date", y="AQI",
            title=f"{selected_city} — Daily AQI Timeline",
            color_discrete_sequence=["#38BDF8"],
            template="plotly_dark"
        )
        fig_line.add_hline(y=200, line_dash="dot", line_color="#F97316", annotation_text="Poor (200)")
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            height=400
        )
        st.plotly_chart(fig_line, use_container_width=True)

# ==========================================
# PAGE 3: BATCH CSV ANALYSIS
# ==========================================
elif page == "Batch CSV Analysis":
    st.markdown("""
    <div class="top-header">
        <div>
            <div class="top-title">Batch CSV AQI Prediction</div>
            <div class="top-sub">Upload a CSV file with sensor readings to predict AQI for multiple records at once.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info(f"Required columns: `{', '.join(FEATURES)}`")
    uploaded_file = st.file_uploader("Upload Sensor CSV", type=["csv"])

    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
        missing_cols = [c for c in FEATURES if c not in batch_df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {missing_cols}")
        else:
            clean_batch = batch_df[FEATURES].fillna(batch_df[FEATURES].median())
            preds = np.maximum(0, np.round(model.predict(clean_batch), 1))
            batch_df["Predicted_AQI"] = preds
            batch_df["AQI_Category"] = [get_aqi_details(v)[0] for v in preds]

            st.success(f"Generated predictions for {len(batch_df)} rows.")
            st.dataframe(batch_df.head(25), use_container_width=True)

            csv_out = batch_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Predictions CSV",
                data=csv_out,
                file_name="aqi_predictions.csv",
                mime="text/csv",
                type="primary"
            )

# ==========================================
# PAGE 4: MODEL & CPCB SCALE
# ==========================================
elif page == "Model & CPCB Scale":
    st.markdown("""
    <div class="top-header">
        <div>
            <div class="top-title">Model Insights & CPCB Reference</div>
            <div class="top-sub">Feature importance from the Random Forest model and Indian CPCB AQI thresholds.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_left, c_right = st.columns([1.1, 1.0], gap="large")

    with c_left:
        st.markdown("#### Feature Importance (%)")
        if hasattr(model, "feature_importances_"):
            imp_df = pd.DataFrame({
                "Pollutant": FEATURES,
                "Importance (%)": np.round(model.feature_importances_ * 100, 2)
            }).sort_values("Importance (%)", ascending=True)
            fig_imp = px.bar(
                imp_df, x="Importance (%)", y="Pollutant", orientation="h",
                color="Importance (%)", color_continuous_scale="Ice",
                text_auto=True, template="plotly_dark"
            )
            fig_imp.update_layout(
                showlegend=False,
                height=380,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15, 23, 42, 0.5)"
            )
            st.plotly_chart(fig_imp, use_container_width=True)

    with c_right:
        st.markdown("#### Indian CPCB AQI Categories")
        cpcb_items = [
            ("0 – 50", "Good", "#22C55E", "Minimal impact"),
            ("51 – 100", "Satisfactory", "#84CC16", "Minor discomfort to sensitive people"),
            ("101 – 200", "Moderate", "#F59E0B", "Discomfort to people with lung/heart disease"),
            ("201 – 300", "Poor", "#F97316", "Discomfort on prolonged exposure"),
            ("301 – 400", "Very Poor", "#EF4444", "Respiratory illness on prolonged exposure"),
            ("401 – 500+", "Severe", "#B91C1C", "Serious impact even on healthy people"),
        ]
        for rng, cat, clr, desc in cpcb_items:
            st.markdown(f"""
            <div class="cpcb-row" style="border-left-color: {clr};">
                <div>
                    <strong style="color:{clr};">{cat}</strong>
                    <div style="font-size:0.82rem; color:#94A3B8;">{desc}</div>
                </div>
                <div style="font-weight:700; color:#E2E8F0; font-size:0.9rem;">{rng}</div>
            </div>
            """, unsafe_allow_html=True)

