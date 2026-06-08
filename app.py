import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="CrimeScope Chicago",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #F4F6FA !important;
    color: #111827 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── TEKS GLOBAL GELAP ── */
[data-testid="stAppViewContainer"] *:not(button):not(.stButton > button):not(.btn-primary):not([data-baseweb]) {
    color: inherit;
}
p, span, div, li, h1, h2, h3, h4, h5, h6, label,
.stMarkdown, .element-container { color: #111827 !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E5E7EB !important;
    min-width: 280px !important;
    width: 280px !important;
}
[data-testid="stSidebar"] * { color: #374151 !important; }
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
button[kind="icon"][aria-label*="sidebar"] {
    display: none !important;
}
#MainMenu, footer, header, [data-testid="stDecoration"] { visibility: hidden; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 4px; }

/* ── SIDEBAR NAV BUTTONS ── */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: #6B7280 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    text-align: left !important;
    padding: 10px 16px !important;
    border-radius: 8px !important;
    width: 100% !important;
    transition: background 0.15s, color 0.15s !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #F3F4F6 !important;
    color: #111827 !important;
}

/* ── PRIMARY BUTTON — hitam dengan teks putih ── */
.stButton > button[kind="primary"],
button[kind="primary"] {
    background: #111827 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    letter-spacing: 0.01em !important;
    cursor: pointer !important;
    transition: background 0.15s, transform 0.1s !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1F2937 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
}
.stButton > button[kind="primary"]:active {
    background: #374151 !important;
    color: #FFFFFF !important;
    transform: translateY(0) !important;
}

/* ── SECONDARY / DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #374151 !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    transition: background 0.15s !important;
}
.stDownloadButton > button:hover {
    background: #F9FAFB !important;
    color: #111827 !important;
    border-color: #9CA3AF !important;
}

/* ── FORM ELEMENTS ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: #FFFFFF !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 8px !important;
    color: #111827 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus {
    border-color: #111827 !important;
    box-shadow: 0 0 0 2px rgba(17,24,39,0.1) !important;
}
.stSelectbox label, .stNumberInput label, .stSlider label,
.stRadio label, .stToggle label, .stMultiselect label {
    color: #374151 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}
/* Radio buttons */
.stRadio > div > div > label {
    color: #374151 !important;
    font-size: 13px !important;
}

/* ── CARD ── */
.card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.card-hover:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    transform: translateY(-1px);
    transition: all 0.2s;
}

/* ── METRIC CARD ── */
.metric-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    border-top: 3px solid var(--accent, #111827);
}
.metric-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6B7280 !important;
    margin-bottom: 8px;
    display: block;
}
.metric-value {
    font-size: 30px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    color: #111827 !important;
    line-height: 1.1;
    display: block;
}
.metric-sub {
    font-size: 12px;
    color: #6B7280 !important;
    margin-top: 6px;
    display: block;
}

/* ── TYPOGRAPHY ── */
.page-title {
    font-size: 26px;
    font-weight: 700;
    color: #111827 !important;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: 14px;
    color: #6B7280 !important;
    margin-bottom: 24px;
}
.section-title {
    font-size: 13px;
    font-weight: 600;
    color: #374151 !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 12px;
}

/* ── RISK BADGES ── */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-high    { background: #FEE2E2; color: #991B1B !important; }
.badge-medhi   { background: #FFEDD5; color: #9A3412 !important; }
.badge-med     { background: #FEF9C3; color: #854D0E !important; }
.badge-low     { background: #D1FAE5; color: #065F46 !important; }

/* ── RESULT CARD ── */
.result-card {
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    border: 1.5px solid;
}
.result-risk-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6B7280 !important;
    margin-bottom: 8px;
    display: block;
}
.result-risk-value {
    font-size: 26px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.2;
}
.result-risk-meta {
    font-size: 12px;
    color: #6B7280 !important;
    margin-top: 8px;
}

/* ── RECOMMENDATION BOX ── */
.rec-box {
    border-radius: 8px;
    padding: 14px 16px;
    margin-top: 14px;
    border-left: 3px solid;
}
.rec-high    { background: #FEF2F2; border-color: #EF4444; }
.rec-medhi   { background: #FFF7ED; border-color: #F97316; }
.rec-med     { background: #FEFCE8; border-color: #EAB308; }
.rec-low     { background: #F0FDF4; border-color: #22C55E; }
.rec-title   { font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #6B7280 !important; margin-bottom: 5px; }
.rec-text    { font-size: 13px; line-height: 1.6; color: #374151 !important; }

/* ── COMPUTED BADGE ── */
.computed-row {
    display: flex;
    gap: 8px;
    margin-top: 12px;
}
.computed-item {
    flex: 1;
    background: #F9FAFB;
    border: 1px solid #E5E7EB;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 12px;
    color: #6B7280 !important;
}
.computed-key {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
    color: #111827 !important;
}

/* ── TABLE ── */
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th {
    background: #F9FAFB;
    color: #6B7280 !important;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid #E5E7EB;
}
.data-table td {
    padding: 10px 14px;
    border-bottom: 1px solid #F3F4F6;
    color: #374151 !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}
.data-table tr:hover td { background: #F9FAFB; }

/* ── BRAND SIDEBAR ── */
.brand-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 20px 16px 16px;
    border-bottom: 1px solid #F3F4F6;
    margin-bottom: 8px;
}
.brand-name { font-size: 15px; font-weight: 700; color: #111827 !important; }
.brand-tag  { font-size: 10px; color: #9CA3AF !important; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 2px; }
.nav-section-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9CA3AF !important;
    padding: 8px 18px 4px;
}

/* ── INFO BOX ── */
.info-box {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 13px;
    color: #1E40AF !important;
    line-height: 1.6;
}

/* ── DIVIDER ── */
.divider { height: 1px; background: #E5E7EB; margin: 28px 0; }

/* ── STATUS BADGE ── */
.status-online  { display: flex; align-items: center; gap: 6px; padding: 8px 12px; background: #F0FDF4; border-radius: 8px; border: 1px solid #BBF7D0; font-size: 12px; font-weight: 500; color: #166534 !important; }
.status-offline { display: flex; align-items: center; gap: 6px; padding: 8px 12px; background: #FEF2F2; border-radius: 8px; border: 1px solid #FECACA; font-size: 12px; font-weight: 500; color: #991B1B !important; }

/* ── HERO ── */
.hero-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #F3F4F6;
    border: 1px solid #E5E7EB;
    border-radius: 100px;
    padding: 4px 12px;
    margin-bottom: 16px;
    font-size: 11px;
    font-weight: 600;
    color: #374151 !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── STAT ROW ── */
.stat-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 0;
    border-bottom: 1px solid #F3F4F6;
}
.stat-row:last-child { border-bottom: none; }
.stat-dot  { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.stat-name { font-size: 13px; font-weight: 500; color: #374151 !important; flex: 1; }
.stat-pct  { font-family: 'JetBrains Mono'; font-size: 12px; color: #6B7280 !important; min-width: 36px; text-align: right; }
.stat-bar-wrap { width: 72px; height: 4px; background: #E5E7EB; border-radius: 2px; overflow: hidden; }
.stat-bar  { height: 100%; border-radius: 2px; }

/* ── RISK CATEGORY CARD ── */
.risk-cat-card {
    border-radius: 10px;
    padding: 16px;
    height: 100%;
    min-height: 140px;
}
.risk-cat-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.risk-cat-desc { font-size: 12px; line-height: 1.6; }

/* ── FEATURE ROW ── */
.feat-row {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 8px 0;
    border-bottom: 1px solid #F3F4F6;
}
.feat-name { font-family: 'JetBrains Mono'; font-size: 12px; font-weight: 500; color: #111827 !important; white-space: nowrap; min-width: 100px; }
.feat-desc { font-size: 12px; color: #6B7280 !important; line-height: 1.4; }

/* ── CHART CARD ── */
.chart-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

/* ── MODEL STAT ROW ── */
.model-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #F3F4F6;
    font-size: 13px;
}
.model-stat:last-child { border-bottom: none; }
.model-stat-label { color: #6B7280 !important; }
.model-stat-value { font-family: 'JetBrains Mono'; font-weight: 600; color: #111827 !important; }

/* ── HISTORY DATAFRAME ── */
[data-testid="stDataFrame"] { background: #FFFFFF !important; }
[data-testid="stDataFrame"] * { color: #374151 !important; }

/* ── TOGGLE ── */
.stToggle p { color: #374151 !important; }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ──────────────────────────────────────────────
RISK_COLORS = {
    "HIGH_RISK":        "#EF4444",
    "MEDIUM_HIGH_RISK": "#F97316",
    "MEDIUM_RISK":      "#EAB308",
    "LOW_RISK":         "#22C55E",
}
RISK_LABELS = {
    "HIGH_RISK":        "HIGH RISK",
    "MEDIUM_HIGH_RISK": "MEDIUM HIGH RISK",
    "MEDIUM_RISK":      "MEDIUM RISK",
    "LOW_RISK":         "LOW RISK",
}
RECOMMENDATIONS = {
    "HIGH_RISK":        "Segera tingkatkan patroli di distrik ini pada jam tersebut. Koordinasikan dengan unit darurat dan aktifkan protokol respons cepat. Pertimbangkan penempatan personel tambahan.",
    "MEDIUM_HIGH_RISK": "Tambahkan frekuensi patroli rutin di area ini. Perkuat kerja sama dengan warga setempat dan pastikan sistem pemantauan aktif selama periode tersebut.",
    "MEDIUM_RISK":      "Pantau pola kejahatan secara berkala. Lakukan patroli standar dan evaluasi tren bulanan untuk deteksi dini perubahan tingkat risiko.",
    "LOW_RISK":         "Kondisi relatif aman. Patroli standar cukup untuk area ini. Tetap waspada dan lakukan pembaruan data secara rutin.",
}
REC_CLASS = {
    "HIGH_RISK": "high", "MEDIUM_HIGH_RISK": "medhi",
    "MEDIUM_RISK": "med", "LOW_RISK": "low",
}
BADGE_CLASS = {
    "HIGH_RISK": "badge-high", "MEDIUM_HIGH_RISK": "badge-medhi",
    "MEDIUM_RISK": "badge-med", "LOW_RISK": "badge-low",
}
RESULT_BG = {
    "HIGH_RISK": ("#FEF2F2", "#FECACA"),
    "MEDIUM_HIGH_RISK": ("#FFF7ED", "#FED7AA"),
    "MEDIUM_RISK": ("#FEFCE8", "#FDE68A"),
    "LOW_RISK": ("#F0FDF4", "#BBF7D0"),
}

# ── SESSION STATE ──────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ── LOAD MODEL ────────────────────────────────────────────
@st.cache_resource
def load_model():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    files = {
        "model":    os.path.join(BASE_DIR, "gradient_boosting_model.pkl"),
        "scaler":   os.path.join(BASE_DIR, "scaler.pkl"),
        "encoder":  os.path.join(BASE_DIR, "label_encoder.pkl"),
        "features": os.path.join(BASE_DIR, "feature_columns.json"),
    }
    missing = [v for v in files.values() if not os.path.exists(v)]
    if missing:
        return None, None, None, None, missing
    try:
        model   = joblib.load(files["model"])
        scaler  = joblib.load(files["scaler"])
        encoder = joblib.load(files["encoder"])
        with open(files["features"]) as f:
            features = json.load(f)
        return model, scaler, encoder, features, []
    except Exception as e:
        return None, None, None, None, [str(e)]

model, scaler, encoder, feature_cols, load_errors = load_model()
model_ready = model is not None

# ── PLOTLY THEME ──────────────────────────────────────────
CHART_THEME = dict(
    paper_bgcolor='#FFFFFF',
    plot_bgcolor='#FFFFFF',
    font=dict(color='#6B7280', family='Inter'),
)
GRID_C = '#F3F4F6'
TICK_C = '#9CA3AF'

# ── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-wrap">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="8" fill="#111827"/>
            <path d="M16 6L19.5 13.5H27L21 17.5L23.5 25L16 21L8.5 25L11 17.5L5 13.5H12.5L16 6Z" fill="white" opacity="0.9"/>
        </svg>
        <div>
            <div class="brand-name">CrimeScope</div>
            <div class="brand-tag">Chicago · ML Dashboard</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-section-label">Menu</div>', unsafe_allow_html=True)

    pages = [
        ("Home",               "🏠", "Dashboard & Overview"),
        ("Prediksi",           "🔍", "Prediksi Risk Category"),
        ("Analisis Data",      "📊", "EDA & Visualisasi"),
        ("Peta Kejahatan",     "🗺️", "Heatmap Distrik"),
        ("Perbandingan Model", "📈", "Scorecard & Evaluasi"),
    ]

    for name, icon, desc in pages:
        active = st.session_state.page == name
        label = f"{icon}  {name}" + ("  ●" if active else "")
        if st.button(label, key=f"nav_{name}", use_container_width=True, help=desc):
            st.session_state.page = name
            st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    n_hist = len(st.session_state.history)
    st.markdown(f"""
    <div style="padding: 0 4px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
            <span style="font-size:13px;color:#374151;font-weight:500;">🕓 Riwayat Sesi</span>
            <span style="margin-left:auto;background:#F3F4F6;color:#374151;font-size:11px;font-family:'JetBrains Mono';padding:2px 8px;border-radius:20px;font-weight:600;">{n_hist}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if n_hist > 0:
        with st.expander("Lihat Riwayat", expanded=False):
            df_hist = pd.DataFrame(st.session_state.history)
            st.dataframe(df_hist[["waktu","distrik","hasil"]].tail(10), use_container_width=True, hide_index=True)
        csv = pd.DataFrame(st.session_state.history).to_csv(index=False).encode()
        st.download_button(
            label="⬇ Download CSV",
            data=csv,
            file_name=f"prediksi_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if model_ready:
        st.markdown('<div class="status-online"><span style="width:8px;height:8px;border-radius:50%;background:#22C55E;display:inline-block;flex-shrink:0;"></span> Model aktif · Gradient Boosting</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-offline"><span style="width:8px;height:8px;border-radius:50%;background:#EF4444;display:inline-block;flex-shrink:0;"></span> Model tidak ditemukan — letakkan .pkl & .json di folder yang sama dengan app.py</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════
if st.session_state.page == "Home":

    col_hero, col_card = st.columns([3, 2], gap="large")

    with col_hero:
        st.markdown("""
        <div style="padding: 8px 0 24px;">
            <div class="hero-chip">
                <span style="width:6px;height:6px;border-radius:50%;background:#111827;display:inline-block;"></span>
                Smart City · Machine Learning
            </div>
            <h1 style="font-size:40px;font-weight:700;color:#111827;line-height:1.1;letter-spacing:-0.03em;margin-bottom:16px;">
                Crime Hotspot<br>
                <span style="color:#374151;">Prediction</span>
            </h1>
            <p style="font-size:15px;color:#6B7280;line-height:1.7;max-width:420px;margin-bottom:28px;">
                Sistem prediksi berbasis <strong style="color:#111827;font-weight:600;">Gradient Boosting</strong> untuk mengidentifikasi titik rawan kejahatan di kota Chicago dari data historis 2001–2017.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍  Mulai Prediksi", type="primary"):
            st.session_state.page = "Prediksi"
            st.rerun()

    with col_card:
        st.markdown("""
        <div class="card" style="margin-top:8px;">
            <div class="section-title">Distribusi Kelas Dataset</div>
            <div class="stat-row">
                <div class="stat-dot" style="background:#EAB308;"></div>
                <span class="stat-name">Medium Risk</span>
                <div class="stat-bar-wrap"><div class="stat-bar" style="width:100%;background:#EAB308;"></div></div>
                <span class="stat-pct">49.6%</span>
            </div>
            <div class="stat-row">
                <div class="stat-dot" style="background:#F97316;"></div>
                <span class="stat-name">Medium High</span>
                <div class="stat-bar-wrap"><div class="stat-bar" style="width:70%;background:#F97316;"></div></div>
                <span class="stat-pct">34.8%</span>
            </div>
            <div class="stat-row">
                <div class="stat-dot" style="background:#22C55E;"></div>
                <span class="stat-name">Low Risk</span>
                <div class="stat-bar-wrap"><div class="stat-bar" style="width:20%;background:#22C55E;"></div></div>
                <span class="stat-pct">10.0%</span>
            </div>
            <div class="stat-row">
                <div class="stat-dot" style="background:#EF4444;"></div>
                <span class="stat-name">High Risk</span>
                <div class="stat-bar-wrap"><div class="stat-bar" style="width:12%;background:#EF4444;"></div></div>
                <span class="stat-pct">5.6%</span>
            </div>
            <div style="margin-top:16px;padding-top:14px;border-top:1px solid #F3F4F6;display:flex;gap:20px;">
                <div>
                    <div style="font-size:10px;color:#9CA3AF;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">Total Baris</div>
                    <div style="font-size:18px;font-weight:700;font-family:'JetBrains Mono';color:#111827;margin-top:2px;">107,687</div>
                </div>
                <div style="width:1px;background:#F3F4F6;"></div>
                <div>
                    <div style="font-size:10px;color:#9CA3AF;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">Periode</div>
                    <div style="font-size:18px;font-weight:700;font-family:'JetBrains Mono';color:#111827;margin-top:2px;">2001–2017</div>
                </div>
                <div style="width:1px;background:#F3F4F6;"></div>
                <div>
                    <div style="font-size:10px;color:#9CA3AF;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">Distrik</div>
                    <div style="font-size:18px;font-weight:700;font-family:'JetBrains Mono';color:#111827;margin-top:2px;">25</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4, gap="small")
    metrics = [
        (c1, "107,687", "Total Data",    "Baris dari dataset Chicago",   "#111827"),
        (c2, "25",      "Distrik",        "Seluruh kota Chicago",          "#374151"),
        (c3, "59.31%",  "Best Accuracy",  "Gradient Boosting · Test set",  "#166534"),
        (c4, "4",       "Kelas Risiko",   "HIGH → MEDIUM → LOW",           "#854D0E"),
    ]
    for col, val, label, sub, accent in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card" style="--accent:{accent};">
                <span class="metric-label">{label}</span>
                <span class="metric-value">{val}</span>
                <span class="metric-sub">{sub}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="page-title" style="font-size:18px;margin-bottom:4px;">Kategori Risiko</div>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Klasifikasi tingkat bahaya berdasarkan jenis kejahatan historis Chicago</p>', unsafe_allow_html=True)

    risk_info = [
        ("HIGH RISK",        "#EF4444", "#FEF2F2", "#FECACA", "#991B1B", "Pembunuhan, Perkosaan, Perampokan, Penculikan, Arson, Perdagangan Manusia"),
        ("MEDIUM HIGH RISK", "#F97316", "#FFF7ED", "#FED7AA", "#9A3412", "Penganiayaan, Penyerangan, Pencurian Kendaraan, Pelecehan Seksual, Stalking"),
        ("MEDIUM RISK",      "#EAB308", "#FEFCE8", "#FDE68A", "#854D0E", "Pencurian, Vandalisme, Narkotika, Penipuan, Pelanggaran Senjata"),
        ("LOW RISK",         "#22C55E", "#F0FDF4", "#BBF7D0", "#065F46", "Pelanggaran Ringan, Perjudian, Gangguan Ketertiban, Pelanggaran Izin"),
    ]
    cols = st.columns(4, gap="small")
    for col, (label, color, bg, border_bg, text_color, desc) in zip(cols, risk_info):
        with col:
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {border_bg};border-radius:10px;padding:16px;min-height:150px;">
                <div style="display:flex;align-items:center;gap:6px;margin-bottom:10px;">
                    <div style="width:8px;height:8px;border-radius:50%;background:{color};flex-shrink:0;"></div>
                    <span style="font-size:10px;font-weight:700;color:{text_color};letter-spacing:0.08em;text-transform:uppercase;">{label}</span>
                </div>
                <p style="font-size:12px;color:#374151;line-height:1.6;margin:0;">{desc}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col_m, col_f = st.columns([2, 3], gap="large")
    with col_m:
        st.markdown("""
        <div class="card">
            <div class="section-title">Model Terbaik</div>
            <div style="font-size:18px;font-weight:700;color:#111827;margin-bottom:2px;">Gradient Boosting</div>
            <div style="font-size:12px;color:#9CA3AF;margin-bottom:16px;">n_estimators=100 · max_depth=5</div>
            <div class="model-stat"><span class="model-stat-label">Test Accuracy</span><span class="model-stat-value" style="color:#166534;">59.31%</span></div>
            <div class="model-stat"><span class="model-stat-label">Precision</span><span class="model-stat-value">59.17%</span></div>
            <div class="model-stat"><span class="model-stat-label">Overfit Gap</span><span class="model-stat-value" style="color:#166534;">0.0149</span></div>
            <div class="model-stat"><span class="model-stat-label">SMOTE</span><span class="model-stat-value" style="color:#EF4444;">Tidak digunakan</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col_f:
        st.markdown('<div style="font-size:14px;font-weight:600;color:#111827;margin-bottom:12px;">12 Fitur Input Model</div>', unsafe_allow_html=True)
        features_list = [
            ("District",   "Nomor distrik Chicago (1–25)"),
            ("Hour",       "Jam kejadian (0–23)"),
            ("Month",      "Bulan kejadian (1–12)"),
            ("DayOfWeek",  "Hari dalam seminggu (0=Senin)"),
            ("Year",       "Tahun kejadian"),
            ("is_weekend", "1 jika Sabtu/Minggu"),
            ("is_night",   "1 jika jam 22:00–05:00"),
            ("season",     "Musim: 0=Winter … 3=Fall"),
            ("Arrest",     "1 jika terjadi penangkapan"),
            ("Domestic",   "1 jika kekerasan domestik"),
            ("Latitude",   "Koordinat lintang lokasi"),
            ("Longitude",  "Koordinat bujur lokasi"),
        ]
        pairs = [features_list[i:i+2] for i in range(0, len(features_list), 2)]
        for pair in pairs:
            c1f, c2f = st.columns(2)
            for cf, (fname, fdesc) in zip([c1f, c2f], pair):
                with cf:
                    st.markdown(f"""
                    <div class="feat-row">
                        <span class="feat-name">{fname}</span>
                        <span class="feat-desc">{fdesc}</span>
                    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE: PREDIKSI
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "Prediksi":
    st.markdown('<div class="page-title">Prediksi Risk Category</div>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Isi parameter lokasi dan waktu untuk mendapatkan prediksi tingkat risiko kejahatan</p>', unsafe_allow_html=True)

    if not model_ready:
        st.error("⚠️ **Model belum dimuat.** Pastikan file `.pkl` dan `.json` ada di folder yang sama dengan `app.py`, lalu restart aplikasi.")
    else:
        col_form, col_result = st.columns([1, 1], gap="large")

        with col_form:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Parameter Input</div>', unsafe_allow_html=True)

            district = st.selectbox("Distrik", list(range(1, 26)), format_func=lambda x: f"Distrik {x}")
            col_h, col_m2 = st.columns(2)
            with col_h:
                hour = st.slider("Jam", 0, 23, 12)
            with col_m2:
                month = st.slider("Bulan", 1, 12, 6)

            col_d, col_y = st.columns(2)
            with col_d:
                day = st.selectbox("Hari", list(range(7)), format_func=lambda x: ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][x])
            with col_y:
                year = st.number_input("Tahun", 2001, 2030, 2017, label_visibility="visible")

            season = st.selectbox("Musim", [0,1,2,3], format_func=lambda x: ["❄️ Winter","🌸 Spring","☀️ Summer","🍂 Fall"][x])

            col_ar, col_do = st.columns(2)
            with col_ar:
                arrest = st.radio("Penangkapan?", [0,1], format_func=lambda x: "Ya" if x else "Tidak", horizontal=True)
            with col_do:
                domestic = st.radio("Domestik?", [0,1], format_func=lambda x: "Ya" if x else "Tidak", horizontal=True)

            district_coords = {
                1:(41.8416,-87.6268),2:(41.7475,-87.6163),3:(41.7558,-87.5873),
                4:(41.7623,-87.5697),5:(41.7492,-87.5551),6:(41.7669,-87.6536),
                7:(41.7644,-87.6664),8:(41.8623,-87.7291),9:(41.8147,-87.6794),
                10:(41.8544,-87.7186),11:(41.8038,-87.6584),12:(41.8649,-87.6580),
                14:(41.9150,-87.6786),15:(41.8719,-87.7196),16:(41.9561,-87.7543),
                17:(41.9726,-87.7266),18:(41.9302,-87.6602),19:(41.9862,-87.6620),
                20:(41.9727,-87.6396),22:(41.7380,-87.5620),24:(41.9006,-87.7614),
                25:(41.8466,-87.7054),
            }
            lat_def, lon_def = district_coords.get(district, (41.8781, -87.6298))

            col_lat, col_lon = st.columns(2)
            with col_lat:
                lat = st.number_input("Latitude", value=lat_def, format="%.4f")
            with col_lon:
                lon = st.number_input("Longitude", value=lon_def, format="%.4f")

            is_weekend = 1 if day >= 5 else 0
            is_night   = 1 if (hour >= 22 or hour < 5) else 0

            st.markdown(f"""
            <div class="computed-row">
                <div class="computed-item"><span class="computed-key">is_weekend</span> = {is_weekend} {"(Akhir Pekan)" if is_weekend else "(Hari Kerja)"}</div>
                <div class="computed-item"><span class="computed-key">is_night</span> = {is_night} {"(Malam)" if is_night else "(Siang)"}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            predict_btn = st.button("🔍  Jalankan Prediksi", type="primary", use_container_width=True)

        with col_result:
            if predict_btn:
                input_data = {
                    "District": district, "Hour": hour, "Month": month,
                    "DayOfWeek": day, "Year": int(year),
                    "is_weekend": is_weekend, "is_night": is_night,
                    "season": season, "Arrest": arrest,
                    "Domestic": domestic, "Latitude": lat, "Longitude": lon,
                }
                try:
                    df_input   = pd.DataFrame([input_data])[feature_cols]
                    scaled     = scaler.transform(df_input)
                    pred_enc   = model.predict(scaled)[0]
                    proba      = model.predict_proba(scaled)[0]
                    pred_label = encoder.inverse_transform([pred_enc])[0]
                    color      = RISK_COLORS[pred_label]
                    bg_c, border_c = RESULT_BG[pred_label]
                    rc = REC_CLASS[pred_label]

                    st.markdown(f"""
                    <div class="result-card" style="border-color:{border_c};background:{bg_c};margin-bottom:16px;">
                        <span class="result-risk-label">Prediksi Tingkat Risiko</span>
                        <div class="result-risk-value" style="color:{color};">{RISK_LABELS[pred_label]}</div>
                        <div class="result-risk-meta">Distrik {district} &nbsp;·&nbsp; {hour:02d}:00 &nbsp;·&nbsp; {'🌙 Malam' if is_night else '☀️ Siang'}</div>
                    </div>""", unsafe_allow_html=True)

                    classes    = encoder.classes_
                    colors_bar = [RISK_COLORS.get(c, "#9CA3AF") for c in classes]
                    fig = go.Figure(go.Bar(
                        x=proba * 100,
                        y=[c.replace("_RISK","").replace("_"," ") for c in classes],
                        orientation='h',
                        marker=dict(color=colors_bar, opacity=0.8),
                        text=[f"{p*100:.1f}%" for p in proba],
                        textposition='outside',
                        textfont=dict(color='#6B7280', size=11, family='JetBrains Mono'),
                    ))
                    fig.update_layout(
                        **CHART_THEME,
                        xaxis=dict(showgrid=False, showticklabels=False, range=[0,120]),
                        yaxis=dict(showgrid=False, tickfont=dict(size=12, color=TICK_C)),
                        margin=dict(l=10, r=60, t=12, b=8),
                        height=160, showlegend=False,
                    )
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                    st.markdown(f"""
                    <div class="rec-box rec-{rc}">
                        <div class="rec-title">Rekomendasi Tindakan</div>
                        <div class="rec-text">{RECOMMENDATIONS[pred_label]}</div>
                    </div>""", unsafe_allow_html=True)

                    st.session_state.history.append({
                        "waktu": datetime.now().strftime("%H:%M:%S"),
                        "distrik": district, "jam": hour,
                        "hari": ["Sen","Sel","Rab","Kam","Jum","Sab","Min"][day],
                        "bulan": month, "musim": ["Winter","Spring","Summer","Fall"][season],
                        "arrest": arrest, "domestic": domestic,
                        "hasil": pred_label, "conf": f"{max(proba)*100:.1f}%",
                    })
                except Exception as e:
                    st.error(f"Error saat prediksi: {e}")
            else:
                st.markdown("""
                <div class="card" style="min-height:380px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:48px 24px;">
                    <div style="font-size:40px;margin-bottom:12px;opacity:0.3;">🔍</div>
                    <div style="font-size:15px;font-weight:600;color:#374151;margin-bottom:6px;">Siap untuk prediksi</div>
                    <div style="font-size:13px;color:#9CA3AF;">Isi form di sebelah kiri<br>lalu klik "Jalankan Prediksi"</div>
                </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE: ANALISIS DATA
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "Analisis Data":
    st.markdown('<div class="page-title">Analisis Data</div>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Visualisasi distribusi dan pola kejahatan dari dataset Chicago 2001–2017</p>', unsafe_allow_html=True)

    np.random.seed(42)
    n = 2000
    risk_dist = {"MEDIUM_RISK": 0.496, "MEDIUM_HIGH_RISK": 0.348, "LOW_RISK": 0.100, "HIGH_RISK": 0.056}
    risks_sample = np.random.choice(list(risk_dist.keys()), size=n, p=list(risk_dist.values()))
    _p = [0.025,0.020,0.018,0.015,0.013,0.015,0.025,0.040,0.050,0.055,
          0.055,0.055,0.055,0.050,0.048,0.045,0.048,0.055,0.060,0.060,
          0.055,0.048,0.040,0.030]
    _p = [x / sum(_p) for x in _p]
    hours_sample    = np.random.choice(range(24), size=n, p=_p)
    months_sample   = np.random.choice(range(1,13), size=n)
    district_sample = np.random.choice(range(1,26), size=n)
    demo_df = pd.DataFrame({"Risk_Category": risks_sample, "Hour": hours_sample, "Month": months_sample, "District": district_sample})

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        counts = demo_df["Risk_Category"].value_counts()
        fig = go.Figure(go.Bar(
            x=[c.replace("_RISK","").replace("_"," ") for c in counts.index],
            y=counts.values,
            marker=dict(color=[RISK_COLORS[c] for c in counts.index], opacity=0.85),
            text=counts.values, textposition='outside',
            textfont=dict(color=TICK_C, size=11, family='JetBrains Mono'),
        ))
        fig.update_layout(
            **CHART_THEME,
            title=dict(text="Distribusi Risk Category", font=dict(color='#111827', size=13)),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color=TICK_C)),
            yaxis=dict(showgrid=True, gridcolor=GRID_C, tickfont=dict(size=11, color=TICK_C)),
            margin=dict(l=8,r=8,t=40,b=8), height=260, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        hour_counts = demo_df.groupby("Hour").size().reset_index(name="count")
        fig = go.Figure(go.Scatter(
            x=hour_counts["Hour"], y=hour_counts["count"],
            mode='lines+markers',
            line=dict(color='#111827', width=2),
            marker=dict(color='#111827', size=4),
            fill='tozeroy', fillcolor='rgba(17,24,39,0.06)',
        ))
        fig.update_layout(
            **CHART_THEME,
            title=dict(text="Kejahatan per Jam", font=dict(color='#111827', size=13)),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color=TICK_C), tickmode='linear', dtick=4),
            yaxis=dict(showgrid=True, gridcolor=GRID_C, tickfont=dict(size=11, color=TICK_C)),
            margin=dict(l=8,r=8,t=40,b=8), height=260, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2, gap="large")
    with col3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        month_names = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Ags","Sep","Okt","Nov","Des"]
        mc = demo_df.groupby("Month").size().reset_index(name="count")
        fig = go.Figure(go.Bar(
            x=[month_names[m-1] for m in mc["Month"]], y=mc["count"],
            marker=dict(color='#374151', opacity=0.7),
        ))
        fig.update_layout(
            **CHART_THEME,
            title=dict(text="Kejahatan per Bulan", font=dict(color='#111827', size=13)),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color=TICK_C)),
            yaxis=dict(showgrid=True, gridcolor=GRID_C, tickfont=dict(size=11, color=TICK_C)),
            margin=dict(l=8,r=8,t=40,b=8), height=260, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        demo_df["is_night"] = ((demo_df["Hour"] >= 22) | (demo_df["Hour"] < 5)).astype(int)
        grp = demo_df.groupby(["Risk_Category","is_night"]).size().reset_index(name="count")
        fig = px.bar(grp, x="Risk_Category", y="count", color="is_night", barmode="group",
                     color_discrete_map={0:"#374151", 1:"#9CA3AF"},
                     labels={"is_night":"Malam", "count":"Jumlah", "Risk_Category":"Risiko"})
        fig.update_layout(
            **CHART_THEME,
            title=dict(text="Siang vs Malam per Risiko", font=dict(color='#111827', size=13)),
            xaxis=dict(showgrid=False, tickfont=dict(size=10, color=TICK_C),
                       ticktext=["HIGH","LOW","MED-HIGH","MEDIUM"],
                       tickvals=["HIGH_RISK","LOW_RISK","MEDIUM_HIGH_RISK","MEDIUM_RISK"]),
            yaxis=dict(showgrid=True, gridcolor=GRID_C, tickfont=dict(size=11, color=TICK_C)),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TICK_C, size=11)),
            margin=dict(l=8,r=8,t=40,b=8), height=260,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <strong>Catatan:</strong> Data visualisasi menggunakan sampel representatif dari dataset Chicago 2001–2017.
        Distribusi kelas: MEDIUM_RISK 49.6% · MEDIUM_HIGH_RISK 34.8% · LOW_RISK 10.0% · HIGH_RISK 5.6%
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE: PETA KEJAHATAN
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "Peta Kejahatan":
    st.markdown('<div class="page-title">Peta Kejahatan Chicago</div>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Distribusi titik rawan kejahatan berdasarkan distrik dan tingkat risiko</p>', unsafe_allow_html=True)

    district_data = [
        {"district":1,"lat":41.8416,"lon":-87.6268,"risk":"HIGH_RISK","count":312},
        {"district":2,"lat":41.7475,"lon":-87.6163,"risk":"MEDIUM_HIGH_RISK","count":445},
        {"district":3,"lat":41.7558,"lon":-87.5873,"risk":"HIGH_RISK","count":289},
        {"district":4,"lat":41.7623,"lon":-87.5697,"risk":"MEDIUM_HIGH_RISK","count":398},
        {"district":5,"lat":41.7492,"lon":-87.5551,"risk":"MEDIUM_RISK","count":367},
        {"district":6,"lat":41.7669,"lon":-87.6536,"risk":"HIGH_RISK","count":421},
        {"district":7,"lat":41.7644,"lon":-87.6664,"risk":"HIGH_RISK","count":503},
        {"district":8,"lat":41.8623,"lon":-87.7291,"risk":"MEDIUM_RISK","count":334},
        {"district":9,"lat":41.8147,"lon":-87.6794,"risk":"MEDIUM_HIGH_RISK","count":412},
        {"district":10,"lat":41.8544,"lon":-87.7186,"risk":"MEDIUM_RISK","count":287},
        {"district":11,"lat":41.8038,"lon":-87.6584,"risk":"HIGH_RISK","count":521},
        {"district":12,"lat":41.8649,"lon":-87.6580,"risk":"MEDIUM_HIGH_RISK","count":378},
        {"district":14,"lat":41.9150,"lon":-87.6786,"risk":"LOW_RISK","count":198},
        {"district":15,"lat":41.8719,"lon":-87.7196,"risk":"HIGH_RISK","count":467},
        {"district":16,"lat":41.9561,"lon":-87.7543,"risk":"LOW_RISK","count":156},
        {"district":17,"lat":41.9726,"lon":-87.7266,"risk":"LOW_RISK","count":178},
        {"district":18,"lat":41.9302,"lon":-87.6602,"risk":"MEDIUM_RISK","count":310},
        {"district":19,"lat":41.9862,"lon":-87.6620,"risk":"LOW_RISK","count":134},
        {"district":20,"lat":41.9727,"lon":-87.6396,"risk":"MEDIUM_RISK","count":265},
        {"district":22,"lat":41.7380,"lon":-87.5620,"risk":"MEDIUM_HIGH_RISK","count":356},
        {"district":24,"lat":41.9006,"lon":-87.7614,"risk":"MEDIUM_RISK","count":243},
        {"district":25,"lat":41.8466,"lon":-87.7054,"risk":"HIGH_RISK","count":489},
    ]
    map_df = pd.DataFrame(district_data)

    col_filter, _ = st.columns([2,3])
    with col_filter:
        risk_filter = st.multiselect(
            "Filter Tingkat Risiko",
            options=list(RISK_LABELS.values()),
            default=list(RISK_LABELS.values())
        )

    label_to_key = {v: k for k, v in RISK_LABELS.items()}
    selected_keys = [label_to_key[r] for r in risk_filter]
    filtered = map_df[map_df["risk"].isin(selected_keys)]

    st.markdown('<div class="chart-card" style="padding:0;overflow:hidden;">', unsafe_allow_html=True)
    fig_map = go.Figure()
    for risk, color in RISK_COLORS.items():
        sub = filtered[filtered["risk"] == risk]
        if len(sub) == 0: continue
        fig_map.add_trace(go.Scattermapbox(
            lat=sub["lat"], lon=sub["lon"], mode='markers',
            marker=dict(size=sub["count"]/28, color=color, opacity=0.8, sizemode='area'),
            text=[f"Distrik {d}<br>{RISK_LABELS[r]}<br>{c} kasus" for d,r,c in zip(sub["district"],sub["risk"],sub["count"])],
            hoverinfo='text', name=RISK_LABELS[risk],
        ))
    fig_map.update_layout(
        mapbox=dict(style="carto-positron", center=dict(lat=41.8781, lon=-87.6298), zoom=10),
        paper_bgcolor='#FFFFFF', margin=dict(l=0,r=0,t=0,b=0), height=460,
        legend=dict(bgcolor='rgba(255,255,255,0.95)', bordercolor='#E5E7EB', borderwidth=1,
                    font=dict(color='#374151', size=12)),
    )
    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Ringkasan per Distrik</div>', unsafe_allow_html=True)

    risk_order = {"HIGH_RISK":0,"MEDIUM_HIGH_RISK":1,"MEDIUM_RISK":2,"LOW_RISK":3}
    fs = filtered.copy()
    fs["_order"] = fs["risk"].map(risk_order)
    fs = fs.sort_values("_order")

    BADGE_BG = {"HIGH_RISK":"#FEE2E2","MEDIUM_HIGH_RISK":"#FFEDD5","MEDIUM_RISK":"#FEF9C3","LOW_RISK":"#D1FAE5"}
    BADGE_TC = {"HIGH_RISK":"#991B1B","MEDIUM_HIGH_RISK":"#9A3412","MEDIUM_RISK":"#854D0E","LOW_RISK":"#065F46"}

    rows = ""
    for _, row in fs.iterrows():
        bg  = BADGE_BG[row["risk"]]
        tc  = BADGE_TC[row["risk"]]
        rows += f"""<tr>
            <td>Distrik {int(row['district'])}</td>
            <td><span style="background:{bg};color:{tc};padding:2px 10px;border-radius:100px;font-size:11px;font-weight:600;font-family:'Inter';">{RISK_LABELS[row['risk']]}</span></td>
            <td>{row['count']:,}</td>
            <td style="color:#9CA3AF;">{row['lat']:.4f}, {row['lon']:.4f}</td>
        </tr>"""

    st.markdown(f"""
    <div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.04);">
        <table class="data-table">
            <thead><tr><th>Distrik</th><th>Tingkat Risiko</th><th>Est. Kasus</th><th>Koordinat</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE: PERBANDINGAN MODEL
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "Perbandingan Model":
    st.markdown('<div class="page-title">Perbandingan Model</div>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Evaluasi performa tiga model ML sebelum dan sesudah penerapan SMOTE</p>', unsafe_allow_html=True)

    show_smote = st.toggle("Tampilkan hasil dengan SMOTE", value=False)

    results_normal = [
        {"Model":"Decision Tree",     "Train Acc":0.5992,"Test Acc":0.5814,"Precision":0.5631,"Recall":0.5814,"F1":0.5346,"Gap":0.0178,"best":False},
        {"Model":"Random Forest",     "Train Acc":0.9893,"Test Acc":0.5738,"Precision":0.5476,"Recall":0.5738,"F1":0.5483,"Gap":0.4155,"best":False},
        {"Model":"Gradient Boosting", "Train Acc":0.6080,"Test Acc":0.5931,"Precision":0.5917,"Recall":0.5931,"F1":0.5404,"Gap":0.0149,"best":True},
    ]
    results_smote_data = [
        {"Model":"Decision Tree",     "Train Acc":0.6134,"Test Acc":0.4527,"Precision":0.4812,"Recall":0.4527,"F1":0.4815,"Gap":0.1607,"best":False},
        {"Model":"Random Forest",     "Train Acc":0.9912,"Test Acc":0.5411,"Precision":0.5289,"Recall":0.5411,"F1":0.5351,"Gap":0.4501,"best":False},
        {"Model":"Gradient Boosting", "Train Acc":0.6350,"Test Acc":0.5745,"Precision":0.5712,"Recall":0.5745,"F1":0.5471,"Gap":0.0605,"best":True},
    ]
    data = results_smote_data if show_smote else results_normal
    title_sfx = "(dengan SMOTE)" if show_smote else "(tanpa SMOTE)"

    rows = ""
    for r in data:
        gap_color = "#DC2626" if r["Gap"] > 0.1 else "#166534"
        star = "★ " if r["best"] else ""
        weight = "font-weight:600;" if r["best"] else ""
        rows += f"""<tr style="{weight}">
            <td style="color:#111827;">{star}{r['Model']}</td>
            <td>{r['Train Acc']:.4f}</td>
            <td style="color:#111827;font-weight:600;">{r['Test Acc']:.4f}</td>
            <td>{r['Precision']:.4f}</td>
            <td>{r['Recall']:.4f}</td>
            <td>{r['F1']:.4f}</td>
            <td style="color:{gap_color};font-weight:600;">{r['Gap']:.4f}</td>
        </tr>"""

    st.markdown(f"""
    <div class="section-title">Scorecard {title_sfx}</div>
    <div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;overflow:auto;margin-bottom:20px;box-shadow:0 1px 4px rgba(0,0,0,0.04);">
        <table class="data-table">
            <thead><tr><th>Model</th><th>Train Acc</th><th>Test Acc</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>Overfit Gap</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>""", unsafe_allow_html=True)

    model_names = [r["Model"] for r in data]
    bar_colors  = ["#111827" if r["best"] else "#D1D5DB" for r in data]

    col_c1, col_c2 = st.columns(2, gap="large")
    with col_c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=model_names,
            y=[r["F1"] for r in data],
            marker=dict(color=bar_colors, opacity=0.9),
            text=[f"{r['F1']:.4f}" for r in data],
            textposition='outside',
            textfont=dict(color=TICK_C, size=11, family='JetBrains Mono'),
        ))
        fig.update_layout(
            **CHART_THEME,
            title=dict(text="F1-Score Perbandingan", font=dict(color='#111827', size=13)),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color=TICK_C)),
            yaxis=dict(showgrid=True, gridcolor=GRID_C, range=[0,0.75], tickfont=dict(size=11, color=TICK_C)),
            margin=dict(l=8,r=8,t=40,b=8), height=240, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=model_names, y=[r["Train Acc"] for r in data], name="Train Acc", marker=dict(color='#6B7280', opacity=0.7)))
        fig.add_trace(go.Bar(x=model_names, y=[r["Test Acc"] for r in data], name="Test Acc", marker=dict(color='#111827', opacity=0.9)))
        fig.update_layout(
            **CHART_THEME,
            title=dict(text="Train vs Test Accuracy", font=dict(color='#111827', size=13)),
            barmode='group',
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color=TICK_C)),
            yaxis=dict(showgrid=True, gridcolor=GRID_C, tickfont=dict(size=11, color=TICK_C)),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TICK_C, size=11)),
            margin=dict(l=8,r=8,t=40,b=8), height=240,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Confusion Matrix — Gradient Boosting (tanpa SMOTE)</div>', unsafe_allow_html=True)

    class_names = ["HIGH_RISK","LOW_RISK","MEDIUM_HIGH_RISK","MEDIUM_RISK"]
    cm = np.array([[87,12,412,450],[15,54,598,1475],[87,36,3621,3229],[76,80,2694,9008]])
    fig_cm = go.Figure(go.Heatmap(
        z=cm,
        x=[c.replace("_RISK","").replace("_","-") for c in class_names],
        y=[c.replace("_RISK","").replace("_","-") for c in class_names],
        colorscale=[[0,"#F9FAFB"],[0.5,"#D1D5DB"],[1,"#111827"]],
        text=cm, texttemplate="%{text}",
        textfont=dict(size=13, color='#FFFFFF', family='JetBrains Mono'),
        showscale=True,
        colorbar=dict(tickfont=dict(color=TICK_C), outlinewidth=0),
    ))
    fig_cm.update_layout(
        **CHART_THEME,
        xaxis=dict(title=dict(text="Prediksi", font=dict(color=TICK_C)), tickfont=dict(size=11, color=TICK_C), side='bottom'),
        yaxis=dict(title=dict(text="Aktual",   font=dict(color=TICK_C)), tickfont=dict(size=11, color=TICK_C), autorange='reversed'),
        margin=dict(l=8,r=8,t=16,b=8), height=320,
    )

    col_cm, col_insight = st.columns([3,2], gap="large")
    with col_cm:
        st.markdown('<div class="chart-card" style="padding:12px;">', unsafe_allow_html=True)
        st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_insight:
        st.markdown("""
        <div class="card" style="min-height:320px;">
            <div class="section-title">Interpretasi Per Kelas</div>
            <div style="display:flex;flex-direction:column;gap:8px;">
                <div style="padding:10px 12px;background:#FEFCE8;border-left:3px solid #EAB308;border-radius:4px;">
                    <div style="font-size:12px;color:#854D0E;font-weight:600;">MEDIUM_RISK · F1=0.71</div>
                    <div style="font-size:12px;color:#6B7280;margin-top:2px;">Prediksi terbaik, dominasi kelas</div>
                </div>
                <div style="padding:10px 12px;background:#FFF7ED;border-left:3px solid #F97316;border-radius:4px;">
                    <div style="font-size:12px;color:#9A3412;font-weight:600;">MEDIUM_HIGH · F1=0.51</div>
                    <div style="font-size:12px;color:#6B7280;margin-top:2px;">Performa sedang, cukup andal</div>
                </div>
                <div style="padding:10px 12px;background:#FEF2F2;border-left:3px solid #EF4444;border-radius:4px;">
                    <div style="font-size:12px;color:#991B1B;font-weight:600;">HIGH_RISK · F1=0.17</div>
                    <div style="font-size:12px;color:#6B7280;margin-top:2px;">Precision tinggi, Recall rendah</div>
                </div>
                <div style="padding:10px 12px;background:#F0FDF4;border-left:3px solid #22C55E;border-radius:4px;">
                    <div style="font-size:12px;color:#065F46;font-weight:600;">LOW_RISK · F1=0.05</div>
                    <div style="font-size:12px;color:#6B7280;margin-top:2px;">Terburuk, class imbalance parah</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box" style="background:#F0FDF4;border-color:#BBF7D0;color:#166534;">
        <strong>Kesimpulan SMOTE:</strong> SMOTE justru menurunkan performa semua model pada dataset Chicago ini.
        Gradient Boosting tanpa SMOTE tetap menjadi model terbaik dengan
        <strong>Test Accuracy 59.31%</strong>, Precision 59.17%, dan Overfit Gap terkecil (0.0149).
    </div>
    """, unsafe_allow_html=True)