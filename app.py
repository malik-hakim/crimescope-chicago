import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib
import json
import os
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CrimeScope Chicago",
    page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSI+PHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiHJ4D0iOCIgZmlsbD0iIzFBM0E2QyIvPjxwYXRoIGQ9Ik0xNiA2TDE5IDEzSDI2TDIwIDE3TDIyIDI0TDE2IDIwTDEwIDI0TDEyIDE3TDYgMTNIMTNMMTYgNloiIGZpbGw9IiNGRkZGRkYiLz48L3N2Zz4=",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS — Clean Elegant Light Theme (FIXED SIDEBAR)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #F7F8FA !important;
    color: #1A1F2E !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* FIX 1: Pastikan SEMUA teks default berwarna gelap */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] div,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] h5,
[data-testid="stAppViewContainer"] h6,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] .stMarkdown {
    color: #1A1F2E !important;
}

/* Override untuk teks sekunder / label */
[data-testid="stAppViewContainer"] .st-emotion-cache-1q7q0r2 p,
[data-testid="stAppViewContainer"] .st-emotion-cache-1l03zft p {
    color: #3D4863 !important;
}

/* Streamlit native widgets */
.stSelectbox label, .stNumberInput label, .stSlider label,
.stRadio label, .stMultiselect label, .stToggle label,
.stDownloadButton label, .stButton label {
    color: #3D4863 !important;
}

/* ═══════════════════════════════════════════════════════════
   FIX 2: SIDEBAR — Pastikan SELALU terlihat & toggle berfungsi
   ═══════════════════════════════════════════════════════════ */

/* Sidebar container - selalu visible */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E8EBF0 !important;
    box-shadow: 2px 0 12px rgba(0,0,0,0.04) !important;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    width: 300px !important;
    min-width: 300px !important;
    max-width: 300px !important;
    z-index: 999 !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

/* Teks di dalam sidebar tetap gelap */
[data-testid="stSidebar"] * {
    color: #1A1F2E !important;
}

/* Sidebar nav buttons override */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: #6B7A99 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    text-align: left !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    transition: all 0.18s ease !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #F0F4FF !important;
    color: #1A3A6C !important;
}
[data-testid="stSidebar"] .stButton > button:focus {
    box-shadow: none !important;
    outline: none !important;
}

/* ═══════════════════════════════════════════════════════════
   FIX 3: SIDEBAR TOGGLE BUTTON — Selalu terlihat saat ditutup
   ═══════════════════════════════════════════════════════════ */

/* Tombol toggle di kiri atas saat sidebar ditutup */
button[kind="header"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebar"] + div button,
header button[data-testid="baseButton-headerNoPadding"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: fixed !important;
    top: 12px !important;
    left: 12px !important;
    z-index: 1001 !important;
    background: #1A3A6C !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    min-height: 40px !important;
    padding: 8px !important;
    box-shadow: 0 2px 8px rgba(26,58,108,0.3) !important;
    transition: all 0.2s ease !important;
    align-items: center !important;
    justify-content: center !important;
}

button[kind="header"]:hover,
[data-testid="stSidebarCollapsedControl"]:hover,
header button[data-testid="baseButton-headerNoPadding"]:hover {
    background: #16325C !important;
    transform: scale(1.05) !important;
    box-shadow: 0 4px 12px rgba(26,58,108,0.4) !important;
}

/* Icon di dalam toggle button harus putih */
button[kind="header"] svg,
[data-testid="stSidebarCollapsedControl"] svg,
header button[data-testid="baseButton-headerNoPadding"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    width: 20px !important;
    height: 20px !important;
}

/* Header bar - pastikan tidak menutupi toggle */
[data-testid="stHeader"] {
    background: transparent !important;
    z-index: 998 !important;
}

/* ═══════════════════════════════════════════════════════════
   END SIDEBAR FIX
   ═══════════════════════════════════════════════════════════ */

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #F7F8FA; }
::-webkit-scrollbar-thumb { background: #D1D8E0; border-radius: 10px; }

/* Primary button */
.stButton > button[kind="primary"] {
    background: #1A3A6C !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 28px !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 8px rgba(26,58,108,0.25) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #16325C !important;
    box-shadow: 0 4px 16px rgba(26,58,108,0.35) !important;
    transform: translateY(-1px) !important;
}

/* Streamlit form elements */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stSlider { font-family: 'DM Sans', sans-serif !important; }

/* Main content container dengan max-width */
.main-content-wrap {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 24px;
}

/* Metric card */
.metric-card {
    background: #FFFFFF;
    border: 1px solid #E8EBF0;
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s, transform 0.2s;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.metric-card:hover {
    box-shadow: 0 6px 24px rgba(0,0,0,0.08);
    transform: translateY(-2px);
}
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, #1A3A6C);
    border-radius: 0 0 16px 16px;
}
.metric-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8895B3;
    margin-bottom: 10px;
}
.metric-value {
    font-size: 34px;
    font-weight: 700;
    font-family: 'DM Mono', monospace;
    color: #1A1F2E;
    line-height: 1;
}
.metric-sub {
    font-size: 12px;
    color: #6B7A99;
    margin-top: 8px;
    font-weight: 400;
}

/* Section headers */
.section-header {
    font-size: 24px;
    font-weight: 700;
    color: #1A1F2E;
    margin: 0 0 4px;
    letter-spacing: -0.02em;
}
.section-sub {
    font-size: 14px;
    color: #6B7A99;
    margin: 0 0 28px;
    font-weight: 400;
}

/* Divider */
.divider { height: 1px; background: #E8EBF0; margin: 32px 0; }

/* Brand header sidebar */
.brand-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 24px 20px 18px;
    border-bottom: 1px solid #F0F2F7;
    margin-bottom: 12px;
}
.brand-name { font-size: 16px; font-weight: 700; color: #1A1F2E; line-height: 1; }
.brand-tag { font-size: 10px; color: #6B7A99; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 3px; }

/* Nav section label */
.nav-section {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #A8B3CC;
    padding: 8px 18px 4px;
}

/* Result box */
.result-box {
    border-radius: 18px;
    padding: 28px 32px;
    text-align: center;
    border: 1.5px solid;
    background: #FFFFFF;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}
.result-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #6B7A99;
    margin-bottom: 10px;
}
.result-title {
    font-size: 30px;
    font-weight: 700;
    font-family: 'DM Mono', monospace;
    line-height: 1.15;
    letter-spacing: -0.01em;
}

/* Recommendation box */
.rec-box {
    border-radius: 12px;
    padding: 18px 20px;
    margin-top: 16px;
    border-left: 3px solid;
}
.rec-HIGH { background: #FFF5F5; border-color: #DC2626; }
.rec-MEDIUM_HIGH { background: #FFF8F2; border-color: #EA580C; }
.rec-MEDIUM { background: #FEFCE8; border-color: #CA8A04; }
.rec-LOW { background: #F0FDF4; border-color: #16A34A; }
.rec-title { font-size: 10px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #6B7A99; margin-bottom: 6px; }
.rec-text { font-size: 13px; line-height: 1.65; color: #3D4863; }

/* Styled table */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    font-family: 'DM Mono', monospace;
}
.styled-table th {
    background: #F7F8FA;
    color: #6B7A99;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 11px 16px;
    text-align: left;
    border-bottom: 1px solid #E8EBF0;
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
}
.styled-table td {
    padding: 11px 16px;
    border-bottom: 1px solid #F0F2F7;
    color: #3D4863;
}
.styled-table tr:hover td { background: #F7F9FF; }
.styled-table tr.best td { color: #1A3A6C; font-weight: 600; }
.styled-table tr.best td:first-child::before { content: '★ '; color: #F59E0B; }

/* Form card */
.form-card {
    background: #FFFFFF;
    border: 1px solid #E8EBF0;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.form-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6B7A99;
    margin-bottom: 16px;
}

/* Risk pills */
.risk-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px; border-radius: 100px;
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.05em; text-transform: uppercase;
}
.pill-HIGH { background:#FEE2E2; color:#991B1B; }
.pill-MEDIUM_HIGH { background:#FFEDD5; color:#9A3412; }
.pill-MEDIUM { background:#FEF9C3; color:#854D0E; }
.pill-LOW { background:#DCFCE7; color:#166534; }

/* Computed badge */
.computed-badge {
    flex: 1;
    background: #F7F8FA;
    border: 1px solid #E8EBF0;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: #6B7A99;
}
.computed-key { font-family: 'DM Mono'; font-weight: 500; color: #1A3A6C; }

/* Feature pill */
.feat-pill {
    display: inline-block;
    background: #EEF2FF;
    border: 1px solid #C7D2FE;
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 12px;
    font-family: 'DM Mono';
    color: #3730A3;
    margin: 3px;
}

/* Animations */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-up { animation: fadeUp 0.45s cubic-bezier(0.16,1,0.3,1) forwards; }
@keyframes fadeIn {
    from { opacity: 0; } to { opacity: 1; }
}
.fade-in { animation: fadeIn 0.3s ease forwards; }

/* Stat row on home */
.stat-row {
    display: flex; align-items: center; gap: 8px;
    padding: 12px 0;
    border-bottom: 1px solid #F0F2F7;
}
.stat-row:last-child { border-bottom: none; }
.stat-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.stat-name { font-size: 13px; font-weight: 500; color: #3D4863; flex: 1; }
.stat-pct { font-family: 'DM Mono'; font-size: 13px; color: #6B7A99; }
.stat-bar-wrap { width: 80px; height: 5px; background: #F0F2F7; border-radius: 3px; overflow: hidden; }
.stat-bar { height: 100%; border-radius: 3px; }

/* Chart containers dengan spacing konsisten */
.chart-card {
    background: #FFFFFF;
    border: 1px solid #E8EBF0;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    min-height: 320px;
}

/* Spacing antar section */
.page-section {
    margin-bottom: 32px;
}

/* Hero section spacing */
.hero-section {
    padding: 24px 0 16px;
}

/* Info box */
.info-box {
    background: #F7F9FF;
    border: 1px solid #E0E7FF;
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 13px;
    color: #3D4863;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SVG ICONS
# ─────────────────────────────────────────────────────────────
ICONS = {
    "home":    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "predict": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    "chart":   '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "map":     '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>',
    "model":   '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
    "history": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-4.93"/></svg>',
    "star":    '<svg width="13" height="13" viewBox="0 0 24 24" fill="#F59E0B" stroke="#F59E0B" stroke-width="1"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    "alert":   '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "arrow":   '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
}

RISK_COLORS = {
    "HIGH_RISK":        "#DC2626",
    "MEDIUM_HIGH_RISK": "#EA580C",
    "MEDIUM_RISK":      "#CA8A04",
    "LOW_RISK":         "#16A34A",
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

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ─────────────────────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-wrap">
        <svg width="34" height="34" viewBox="0 0 34 34" fill="none">
            <rect width="34" height="34" rx="10" fill="#1A3A6C"/>
            <path d="M17 7L20.5 14.5H28L22 18.5L24.5 26L17 22L9.5 26L12 18.5L6 14.5H13.5L17 7Z" fill="white" opacity="0.95"/>
        </svg>
        <div>
            <div class="brand-name">CrimeScope</div>
            <div class="brand-tag">Chicago · Smart City ML</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-section">Navigasi</div>', unsafe_allow_html=True)

    pages = [
        ("Home",               "home",    "Dashboard & Overview"),
        ("Prediksi",           "predict", "Prediksi Risk Category"),
        ("Analisis Data",      "chart",   "EDA & Visualisasi"),
        ("Peta Kejahatan",     "map",     "Heatmap Distrik"),
        ("Perbandingan Model", "model",   "Scorecard & Evaluasi"),
    ]

    for name, icon_key, desc in pages:
        active = st.session_state.page == name
        label = f"{'●  ' if active else '○  '}{name}"
        if st.button(label, key=f"nav_{name}", use_container_width=True, help=desc):
            st.session_state.page = name
            st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Riwayat
    n_hist = len(st.session_state.history)
    st.markdown(f"""
    <div style="padding:0 6px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
            <span style="color:#6B7A99;">{ICONS["history"]}</span>
            <span style="font-size:11px;font-weight:700;color:#6B7A99;text-transform:uppercase;letter-spacing:0.1em;">Riwayat Sesi</span>
            <span style="margin-left:auto;background:#EEF2FF;color:#3730A3;font-size:11px;font-family:'DM Mono';padding:2px 9px;border-radius:20px;font-weight:600;">{n_hist}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if n_hist > 0:
        with st.expander("Lihat Riwayat", expanded=False):
            df_hist = pd.DataFrame(st.session_state.history)
            st.dataframe(df_hist[["waktu","distrik","hasil"]].tail(10), use_container_width=True, hide_index=True)
        csv = pd.DataFrame(st.session_state.history).to_csv(index=False).encode()
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"prediksi_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if model_ready:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding:10px 14px;background:#F0FDF4;border-radius:10px;border:1px solid #BBF7D0;">
            <svg width="10" height="10" viewBox="0 0 10 10"><circle cx="5" cy="5" r="5" fill="#16A34A"/></svg>
            <span style="font-size:12px;color:#166534;font-weight:500;">Model aktif · Gradient Boosting</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding:10px 14px;background:#FFF5F5;border-radius:10px;border:1px solid #FCA5A5;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">
                <svg width="10" height="10" viewBox="0 0 10 10"><circle cx="5" cy="5" r="5" fill="#DC2626"/></svg>
                <span style="font-size:12px;color:#991B1B;font-weight:600;">Model tidak ditemukan</span>
            </div>
            <div style="font-size:11px;color:#B91C1C;line-height:1.5;">Letakkan file .pkl &amp; .json di folder yang sama dengan app.py</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────────────────────
if st.session_state.page == "Home":

    # Hero
    col_hero, col_visual = st.columns([3, 2], gap="large")
    with col_hero:
        st.markdown("""
        <div class="fade-up hero-section">
            <div style="display:inline-flex;align-items:center;gap:8px;background:#EEF2FF;border:1px solid #C7D2FE;border-radius:100px;padding:5px 14px;margin-bottom:20px;">
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                    <circle cx="6" cy="6" r="6" fill="#4F46E5" opacity="0.15"/>
                    <circle cx="6" cy="6" r="3" fill="#4F46E5"/>
                </svg>
                <span style="font-size:11px;font-weight:700;color:#4F46E5;letter-spacing:0.1em;text-transform:uppercase;">Smart City · Machine Learning</span>
            </div>
            <h1 style="font-size:46px;font-weight:700;color:#1A1F2E;line-height:1.08;letter-spacing:-0.03em;margin:0 0 18px;">
                Crime Hotspot<br>
                <span style="color:#1A3A6C;">Prediction</span>
            </h1>
            <p style="font-size:15px;color:#3D4863;line-height:1.75;max-width:440px;margin:0 0 32px;font-weight:400;">
                Sistem prediksi berbasis <strong style="color:#1A3A6C;font-weight:600;">Gradient Boosting</strong> untuk mengidentifikasi titik rawan kejahatan di kota Chicago dari data historis 2001–2017.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Mulai Prediksi", type="primary"):
            st.session_state.page = "Prediksi"
            st.rerun()

    with col_visual:
        # Distribution mini-chart
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #E8EBF0;border-radius:18px;padding:22px 24px;box-shadow:0 4px 20px rgba(0,0,0,0.05);margin-top:12px;">
            <div style="font-size:11px;font-weight:700;color:#6B7A99;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:18px;">Distribusi Kelas Dataset</div>
            <div class="stat-row">
                <div class="stat-dot" style="background:#CA8A04;"></div>
                <span class="stat-name">Medium Risk</span>
                <div class="stat-bar-wrap"><div class="stat-bar" style="width:100%;background:#CA8A04;opacity:0.7;"></div></div>
                <span class="stat-pct">49.6%</span>
            </div>
            <div class="stat-row">
                <div class="stat-dot" style="background:#EA580C;"></div>
                <span class="stat-name">Medium High</span>
                <div class="stat-bar-wrap"><div class="stat-bar" style="width:70%;background:#EA580C;opacity:0.7;"></div></div>
                <span class="stat-pct">34.8%</span>
            </div>
            <div class="stat-row">
                <div class="stat-dot" style="background:#16A34A;"></div>
                <span class="stat-name">Low Risk</span>
                <div class="stat-bar-wrap"><div class="stat-bar" style="width:20%;background:#16A34A;opacity:0.7;"></div></div>
                <span class="stat-pct">10.0%</span>
            </div>
            <div class="stat-row">
                <div class="stat-dot" style="background:#DC2626;"></div>
                <span class="stat-name">High Risk</span>
                <div class="stat-bar-wrap"><div class="stat-bar" style="width:11%;background:#DC2626;opacity:0.7;"></div></div>
                <span class="stat-pct">5.6%</span>
            </div>
            <div style="margin-top:18px;padding-top:14px;border-top:1px solid #F0F2F7;display:flex;gap:16px;">
                <div>
                    <div style="font-size:10px;color:#6B7A99;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;">Total Baris</div>
                    <div style="font-size:16px;font-weight:700;font-family:'DM Mono';color:#1A1F2E;margin-top:2px;">107,687</div>
                </div>
                <div style="width:1px;background:#F0F2F7;"></div>
                <div>
                    <div style="font-size:10px;color:#6B7A99;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;">Periode</div>
                    <div style="font-size:16px;font-weight:700;font-family:'DM Mono';color:#1A1F2E;margin-top:2px;">2001–2017</div>
                </div>
                <div style="width:1px;background:#F0F2F7;"></div>
                <div>
                    <div style="font-size:10px;color:#6B7A99;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;">Distrik</div>
                    <div style="font-size:16px;font-weight:700;font-family:'DM Mono';color:#1A1F2E;margin-top:2px;">25</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Metric cards
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        (col1, "107,687", "Total Data",      "Baris dari 4 file Chicago",   "#1A3A6C"),
        (col2, "25",      "Distrik",         "Area kota Chicago",            "#4F46E5"),
        (col3, "59.31%",  "Best Accuracy",   "Gradient Boosting · Test set", "#059669"),
        (col4, "4",       "Kelas Risiko",    "HIGH → LOW RISK",              "#D97706"),
    ]
    for col, val, label, sub, accent in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card fade-up" style="--accent:{accent};">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="color:{accent};">{val}</div>
                <div class="metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Risk categories grid
    st.markdown('<div class="section-header">Kategori Risiko</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Klasifikasi tingkat bahaya berdasarkan jenis kejahatan historis Chicago</div>', unsafe_allow_html=True)

    risk_info = [
        ("HIGH_RISK",        "#DC2626", "#FFF5F5", "#FEE2E2", "Pembunuhan, Perkosaan, Perampokan, Penculikan, Arson, Perdagangan Manusia"),
        ("MEDIUM_HIGH_RISK", "#EA580C", "#FFF8F2", "#FFEDD5", "Penganiayaan, Penyerangan, Pencurian Kendaraan, Pelecehan Seksual, Stalking"),
        ("MEDIUM_RISK",      "#CA8A04", "#FEFCE8", "#FEF9C3", "Pencurian, Vandalisme, Narkotika, Penipuan, Pelanggaran Senjata"),
        ("LOW_RISK",         "#16A34A", "#F0FDF4", "#DCFCE7", "Pelanggaran Ringan, Perjudian, Gangguan Ketertiban, Pelanggaran Izin"),
    ]
    cols = st.columns(4)
    for col, (risk, color, bg, border_bg, desc) in zip(cols, risk_info):
        with col:
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {border_bg};border-radius:16px;padding:20px;height:100%;min-height:160px;transition:box-shadow 0.2s;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
                    <div style="width:10px;height:10px;border-radius:50%;background:{color};flex-shrink:0;box-shadow:0 0 0 3px {border_bg};"></div>
                    <span style="font-size:11px;font-weight:700;color:{color};letter-spacing:0.08em;text-transform:uppercase;">{risk.replace('_',' ')}</span>
                </div>
                <p style="font-size:12.5px;color:#3D4863;line-height:1.6;margin:0;">{desc}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Model info + features
    col_model, col_feat = st.columns([2, 3], gap="large")
    with col_model:
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #E8EBF0;border-radius:16px;padding:22px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="font-size:11px;font-weight:700;color:#6B7A99;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:16px;">Model Terbaik</div>
            <div style="font-size:20px;font-weight:700;color:#1A3A6C;margin-bottom:4px;">Gradient Boosting</div>
            <div style="font-size:13px;color:#6B7A99;margin-bottom:18px;">n_estimators=100 · max_depth=5</div>
            <div style="display:flex;flex-direction:column;gap:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #F0F2F7;">
                    <span style="font-size:12px;color:#3D4863;">Test Accuracy</span>
                    <span style="font-family:'DM Mono';font-size:13px;font-weight:600;color:#059669;">59.31%</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #F0F2F7;">
                    <span style="font-size:12px;color:#3D4863;">Precision</span>
                    <span style="font-family:'DM Mono';font-size:13px;font-weight:600;color:#1A3A6C;">59.17%</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #F0F2F7;">
                    <span style="font-size:12px;color:#3D4863;">Overfit Gap</span>
                    <span style="font-family:'DM Mono';font-size:13px;font-weight:600;color:#059669;">0.0149</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;">
                    <span style="font-size:12px;color:#3D4863;">SMOTE</span>
                    <span style="font-size:12px;font-weight:600;color:#DC2626;">Tidak digunakan</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_feat:
        st.markdown('<div style="font-size:14px;font-weight:600;color:#1A1F2E;margin-bottom:12px;">12 Fitur Input Model</div>', unsafe_allow_html=True)
        features_list = [
            ("District",   "Nomor distrik Chicago (1–25)"),
            ("Hour",       "Jam kejadian (0–23)"),
            ("Month",      "Bulan kejadian (1–12)"),
            ("DayOfWeek",  "Hari dalam seminggu (0=Senin)"),
            ("Year",       "Tahun kejadian"),
            ("is_weekend", "1 jika Sabtu/Minggu"),
            ("is_night",   "1 jika jam 22:00–05:00"),
            ("season",     "Musim (0=Winter … 3=Fall)"),
            ("Arrest",     "1 jika terjadi penangkapan"),
            ("Domestic",   "1 jika kekerasan domestik"),
            ("Latitude",   "Koordinat lintang lokasi"),
            ("Longitude",  "Koordinat bujur lokasi"),
        ]
        pairs = [features_list[i:i+2] for i in range(0, len(features_list), 2)]
        for pair in pairs:
            c1, c2 = st.columns(2)
            for col_f, (fname, fdesc) in zip([c1, c2], pair):
                with col_f:
                    st.markdown(f"""
                    <div style="display:flex;align-items:flex-start;gap:10px;padding:9px 0;border-bottom:1px solid #F0F2F7;">
                        <span style="font-family:'DM Mono';font-size:12px;font-weight:500;color:#1A3A6C;white-space:nowrap;padding-top:1px;">{fname}</span>
                        <span style="font-size:12px;color:#3D4863;line-height:1.4;">{fdesc}</span>
                    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: PREDIKSI
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "Prediksi":
    st.markdown('<div class="section-header">Prediksi Risk Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Isi parameter lokasi dan waktu untuk mendapatkan prediksi tingkat risiko kejahatan</div>', unsafe_allow_html=True)

    if not model_ready:
        st.markdown(f"""
        <div style="background:#FFF5F5;border:1px solid #FCA5A5;border-radius:14px;padding:20px 24px;display:flex;align-items:center;gap:12px;">
            {ICONS["alert"]}
            <span style="color:#991B1B;font-size:14px;"><strong>Model belum dimuat.</strong> Pastikan file .pkl dan .json ada di folder yang sama dengan app.py, lalu restart aplikasi.</span>
        </div>""", unsafe_allow_html=True)
    else:
        col_form, col_result = st.columns([1, 1], gap="large")

        with col_form:
            st.markdown('<div class="form-card">', unsafe_allow_html=True)
            st.markdown('<div class="form-label">Parameter Input</div>', unsafe_allow_html=True)

            district = st.selectbox("Distrik", list(range(1, 26)), format_func=lambda x: f"Distrik {x}")
            hour     = st.slider("Jam (Hour)", 0, 23, 12)
            day      = st.selectbox("Hari", list(range(7)), format_func=lambda x: ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][x])
            month    = st.slider("Bulan", 1, 12, 6)
            year     = st.number_input("Tahun", 2001, 2030, 2017)
            season   = st.selectbox("Musim", [0,1,2,3], format_func=lambda x: ["Winter","Spring","Summer","Fall"][x])
            arrest   = st.radio("Penangkapan (Arrest)?", [0,1], format_func=lambda x: "Ya" if x else "Tidak", horizontal=True)
            domestic = st.radio("Kekerasan Domestik?",  [0,1], format_func=lambda x: "Ya" if x else "Tidak", horizontal=True)

            district_coords = {
                1:(41.8416,-87.6268), 2:(41.7475,-87.6163), 3:(41.7558,-87.5873),
                4:(41.7623,-87.5697), 5:(41.7492,-87.5551), 6:(41.7669,-87.6536),
                7:(41.7644,-87.6664), 8:(41.8623,-87.7291), 9:(41.8147,-87.6794),
                10:(41.8544,-87.7186),11:(41.8038,-87.6584),12:(41.8649,-87.6580),
                14:(41.9150,-87.6786),15:(41.8719,-87.7196),16:(41.9561,-87.7543),
                17:(41.9726,-87.7266),18:(41.9302,-87.6602),19:(41.9862,-87.6620),
                20:(41.9727,-87.6396),22:(41.7380,-87.5620),24:(41.9006,-87.7614),
                25:(41.8466,-87.7054),
            }
            lat_def, lon_def = district_coords.get(district, (41.8781, -87.6298))
            lat = st.number_input("Latitude",  value=lat_def,  format="%.4f")
            lon = st.number_input("Longitude", value=lon_def,  format="%.4f")

            is_weekend = 1 if day >= 5 else 0
            is_night   = 1 if (hour >= 22 or hour < 5) else 0

            st.markdown(f"""
            <div style="display:flex;gap:8px;margin-top:10px;">
                <div class="computed-badge"><span class="computed-key">is_weekend</span> = {is_weekend}</div>
                <div class="computed-badge"><span class="computed-key">is_night</span> = {is_night}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            predict_btn = st.button("Jalankan Prediksi", type="primary", use_container_width=True)

        with col_result:
            if predict_btn:
                input_data = {
                    "District":   district, "Hour": hour, "Month": month,
                    "DayOfWeek":  day,      "Year": int(year),
                    "is_weekend": is_weekend, "is_night": is_night,
                    "season":     season,   "Arrest": arrest,
                    "Domestic":   domestic, "Latitude": lat, "Longitude": lon,
                }
                try:
                    df_input   = pd.DataFrame([input_data])[feature_cols]
                    scaled     = scaler.transform(df_input)
                    pred_enc   = model.predict(scaled)[0]
                    proba      = model.predict_proba(scaled)[0]
                    pred_label = encoder.inverse_transform([pred_enc])[0]
                    color      = RISK_COLORS[pred_label]
                    risk_short = pred_label.replace("_RISK","").replace("_","")

                    border_map = {
                        "HIGH_RISK":"#FCA5A5","MEDIUM_HIGH_RISK":"#FED7AA",
                        "MEDIUM_RISK":"#FDE68A","LOW_RISK":"#86EFAC"
                    }
                    bg_map = {
                        "HIGH_RISK":"#FFF5F5","MEDIUM_HIGH_RISK":"#FFF8F2",
                        "MEDIUM_RISK":"#FEFCE8","LOW_RISK":"#F0FDF4"
                    }

                    st.markdown(f"""
                    <div class="result-box fade-in" style="border-color:{border_map[pred_label]};background:{bg_map[pred_label]};">
                        <div class="result-label">Prediksi Tingkat Risiko</div>
                        <div class="result-title" style="color:{color};">{RISK_LABELS[pred_label]}</div>
                        <div style="margin-top:10px;font-size:13px;color:#6B7A99;">
                            Distrik {district} &nbsp;·&nbsp; Jam {hour:02d}:00 &nbsp;·&nbsp; {'Malam' if is_night else 'Siang'}
                        </div>
                    </div>""", unsafe_allow_html=True)

                    classes    = encoder.classes_
                    colors_bar = [RISK_COLORS.get(c, "#A8B3CC") for c in classes]
                    fig = go.Figure(go.Bar(
                        x=proba * 100,
                        y=[c.replace("_RISK","").replace("_"," ") for c in classes],
                        orientation='h',
                        marker=dict(color=colors_bar, opacity=0.75),
                        text=[f"{p*100:.1f}%" for p in proba],
                        textposition='outside',
                        textfont=dict(color='#6B7A99', size=11, family='DM Mono'),
                    ))
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#6B7A99', family='DM Sans'),
                        xaxis=dict(showgrid=False, showticklabels=False, range=[0,115]),
                        yaxis=dict(showgrid=False, tickfont=dict(size=12, color='#6B7A99')),
                        margin=dict(l=10, r=60, t=16, b=10),
                        height=175, showlegend=False,
                    )
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

                    st.markdown(f"""
                    <div class="rec-box rec-{risk_short}">
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
                <div style="height:100%;min-height:400px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:64px 20px;text-align:center;background:#FFFFFF;border:1px solid #E8EBF0;border-radius:16px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
                    <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#D1D8E0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:14px;">
                        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>
                    <div style="font-size:15px;font-weight:600;color:#6B7A99;margin-bottom:6px;">Siap untuk prediksi</div>
                    <div style="font-size:13px;color:#A8B3CC;">Isi form di sebelah kiri lalu<br>klik "Jalankan Prediksi"</div>
                </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: ANALISIS DATA
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "Analisis Data":
    st.markdown('<div class="section-header">Analisis Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Visualisasi distribusi dan pola kejahatan dari dataset Chicago 2001–2017</div>', unsafe_allow_html=True)

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

    LIGHT_BG = '#FFFFFF'
    GRID_C   = '#F0F2F7'
    TICK_C   = '#6B7A99'
    FONT_F   = 'DM Sans'

    st.markdown('<div class="page-section">', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        counts = demo_df["Risk_Category"].value_counts()
        fig = go.Figure(go.Bar(
            x=[c.replace("_RISK","").replace("_"," ") for c in counts.index],
            y=counts.values,
            marker=dict(color=[RISK_COLORS[c] for c in counts.index], opacity=0.75),
            text=counts.values, textposition='outside',
            textfont=dict(color='#6B7A99', size=12),
        ))
        fig.update_layout(
            title=dict(text="Distribusi Risk Category", font=dict(color='#1A1F2E', size=14, family=FONT_F)),
            paper_bgcolor=LIGHT_BG, plot_bgcolor=LIGHT_BG,
            font=dict(color=TICK_C, family=FONT_F),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color=TICK_C)),
            yaxis=dict(showgrid=True, gridcolor=GRID_C, tickfont=dict(size=11, color=TICK_C)),
            margin=dict(l=10,r=10,t=44,b=10), height=280, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        hour_counts = demo_df.groupby("Hour").size().reset_index(name="count")
        fig = go.Figure(go.Scatter(
            x=hour_counts["Hour"], y=hour_counts["count"],
            mode='lines+markers',
            line=dict(color='#1A3A6C', width=2.5),
            marker=dict(color='#1A3A6C', size=5),
            fill='tozeroy', fillcolor='rgba(26,58,108,0.07)',
        ))
        fig.update_layout(
            title=dict(text="Kejahatan per Jam", font=dict(color='#1A1F2E', size=14, family=FONT_F)),
            paper_bgcolor=LIGHT_BG, plot_bgcolor=LIGHT_BG,
            font=dict(color=TICK_C, family=FONT_F),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color=TICK_C), tickmode='linear', dtick=4),
            yaxis=dict(showgrid=True, gridcolor=GRID_C, tickfont=dict(size=11, color=TICK_C)),
            margin=dict(l=10,r=10,t=44,b=10), height=280, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="page-section">', unsafe_allow_html=True)
    col3, col4 = st.columns(2, gap="large")
    with col3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        month_names = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Ags","Sep","Okt","Nov","Des"]
        mc = demo_df.groupby("Month").size().reset_index(name="count")
        fig = go.Figure(go.Bar(
            x=[month_names[m-1] for m in mc["Month"]], y=mc["count"],
            marker=dict(color='#4F46E5', opacity=0.65),
        ))
        fig.update_layout(
            title=dict(text="Kejahatan per Bulan", font=dict(color='#1A1F2E', size=14, family=FONT_F)),
            paper_bgcolor=LIGHT_BG, plot_bgcolor=LIGHT_BG,
            font=dict(color=TICK_C, family=FONT_F),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color=TICK_C)),
            yaxis=dict(showgrid=True, gridcolor=GRID_C, tickfont=dict(size=11, color=TICK_C)),
            margin=dict(l=10,r=10,t=44,b=10), height=280, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        demo_df["is_night"] = ((demo_df["Hour"] >= 22) | (demo_df["Hour"] < 5)).astype(int)
        grp = demo_df.groupby(["Risk_Category","is_night"]).size().reset_index(name="count")
        fig = px.bar(grp, x="Risk_Category", y="count", color="is_night", barmode="group",
                     color_discrete_map={0:"#1A3A6C", 1:"#6366F1"},
                     labels={"is_night":"Malam", "count":"Jumlah", "Risk_Category":"Risiko"})
        fig.update_layout(
            title=dict(text="Siang vs Malam per Risiko", font=dict(color='#1A1F2E', size=14, family=FONT_F)),
            paper_bgcolor=LIGHT_BG, plot_bgcolor=LIGHT_BG,
            font=dict(color=TICK_C, family=FONT_F),
            xaxis=dict(showgrid=False, tickfont=dict(size=10, color=TICK_C),
                       ticktext=["HIGH","LOW","MED-HIGH","MEDIUM"],
                       tickvals=["HIGH_RISK","LOW_RISK","MEDIUM_HIGH_RISK","MEDIUM_RISK"]),
            yaxis=dict(showgrid=True, gridcolor=GRID_C, tickfont=dict(size=11, color=TICK_C)),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TICK_C, size=11)),
            margin=dict(l=10,r=10,t=44,b=10), height=280,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <strong style="color:#4F46E5;">Catatan:</strong> Data visualisasi menggunakan sampel representatif dari dataset Chicago 2001–2017. Distribusi kelas: MEDIUM_RISK 49.6% · MEDIUM_HIGH_RISK 34.8% · LOW_RISK 10.0% · HIGH_RISK 5.6%
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: PETA KEJAHATAN
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "Peta Kejahatan":
    st.markdown('<div class="section-header">Peta Kejahatan Chicago</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Distribusi titik rawan kejahatan berdasarkan distrik dan tingkat risiko</div>', unsafe_allow_html=True)

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

    st.markdown('<div class="page-section">', unsafe_allow_html=True)
    fc, _ = st.columns([2,3])
    with fc:
        risk_filter = st.multiselect("Filter Tingkat Risiko", options=list(RISK_LABELS.values()), default=list(RISK_LABELS.values()))
    label_to_key = {v:k for k,v in RISK_LABELS.items()}
    selected_keys = [label_to_key[r] for r in risk_filter]
    filtered = map_df[map_df["risk"].isin(selected_keys)]

    st.markdown('<div class="chart-card" style="padding:0;overflow:hidden;">', unsafe_allow_html=True)
    fig_map = go.Figure()
    for risk, color in RISK_COLORS.items():
        sub = filtered[filtered["risk"]==risk]
        if len(sub) == 0: continue
        fig_map.add_trace(go.Scattermapbox(
            lat=sub["lat"], lon=sub["lon"], mode='markers',
            marker=dict(size=sub["count"]/30, color=color, opacity=0.75, sizemode='area'),
            text=[f"Distrik {d}<br>{RISK_LABELS[r]}<br>{c} kasus" for d,r,c in zip(sub["district"],sub["risk"],sub["count"])],
            hoverinfo='text', name=RISK_LABELS[risk],
        ))
    fig_map.update_layout(
        mapbox=dict(style="carto-positron", center=dict(lat=41.8781, lon=-87.6298), zoom=10),
        paper_bgcolor='#FFFFFF', margin=dict(l=0,r=0,t=0,b=0), height=480,
        legend=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='#E8EBF0', borderwidth=1,
                    font=dict(color='#3D4863', size=12)),
    )
    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;font-weight:700;color:#6B7A99;margin-bottom:12px;letter-spacing:0.08em;text-transform:uppercase;">Ringkasan per Distrik</div>', unsafe_allow_html=True)

    risk_order = {"HIGH_RISK":0,"MEDIUM_HIGH_RISK":1,"MEDIUM_RISK":2,"LOW_RISK":3}
    fs = filtered.copy()
    fs["_order"] = fs["risk"].map(risk_order)
    fs = fs.sort_values("_order")

    bg_map_t = {"HIGH_RISK":"#FEE2E2","MEDIUM_HIGH_RISK":"#FFEDD5","MEDIUM_RISK":"#FEF9C3","LOW_RISK":"#DCFCE7"}
    rows = ""
    for _, row in fs.iterrows():
        c = RISK_COLORS[row["risk"]]
        bg = bg_map_t[row["risk"]]
        rows += f"""<tr>
            <td style="font-family:'DM Mono';color:#1A3A6C;font-weight:500;">Distrik {int(row['district'])}</td>
            <td><span style="background:{bg};color:{c};padding:3px 10px;border-radius:100px;font-size:11px;font-weight:700;">{RISK_LABELS[row['risk']]}</span></td>
            <td style="font-family:'DM Mono';">{row['count']:,}</td>
            <td style="font-family:'DM Mono';color:#6B7A99;">{row['lat']:.4f}, {row['lon']:.4f}</td>
        </tr>"""

    st.markdown(f"""
    <div style="background:#FFFFFF;border:1px solid #E8EBF0;border-radius:14px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
        <table class="styled-table">
            <thead><tr><th>Distrik</th><th>Tingkat Risiko</th><th>Est. Kasus</th><th>Koordinat</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: PERBANDINGAN MODEL
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "Perbandingan Model":
    st.markdown('<div class="section-header">Perbandingan Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Evaluasi performa tiga model ML sebelum dan sesudah penerapan SMOTE</div>', unsafe_allow_html=True)

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
        best_cls = 'class="best"' if r["best"] else ""
        gap_color = "#DC2626" if r["Gap"] > 0.1 else "#059669"
        star = f'{ICONS["star"]} ' if r["best"] else ""
        rows += f"""<tr {best_cls}>
            <td>{star}{r['Model']}</td>
            <td>{r['Train Acc']:.4f}</td><td>{r['Test Acc']:.4f}</td>
            <td>{r['Precision']:.4f}</td><td>{r['Recall']:.4f}</td><td>{r['F1']:.4f}</td>
            <td style="color:{gap_color};font-weight:600;">{r['Gap']:.4f}</td>
        </tr>"""

    st.markdown(f"""
    <div style="font-size:11px;font-weight:700;color:#6B7A99;margin-bottom:10px;letter-spacing:0.1em;text-transform:uppercase;">Scorecard {title_sfx}</div>
    <div style="background:#FFFFFF;border:1px solid #E8EBF0;border-radius:14px;overflow:auto;margin-bottom:24px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
        <table class="styled-table">
            <thead><tr><th>Model</th><th>Train Acc</th><th>Test Acc</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>Overfit Gap</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>""", unsafe_allow_html=True)

    LIGHT_BG = '#FFFFFF'; GRID_C = '#F0F2F7'; TICK_C = '#6B7A99'; FONT_F = 'DM Sans'

    st.markdown('<div class="page-section">', unsafe_allow_html=True)
    col_c1, col_c2 = st.columns(2, gap="large")
    model_names = [r["Model"] for r in data]
    f1_vals     = [r["F1"] for r in data]
    acc_vals    = [r["Test Acc"] for r in data]
    bar_colors  = ["#1A3A6C" if r["best"] else "#D1D8E0" for r in data]

    with col_c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=model_names, y=f1_vals, marker=dict(color=bar_colors, opacity=0.85),
            text=[f"{v:.4f}" for v in f1_vals], textposition='outside',
            textfont=dict(color='#6B7A99', size=12, family='DM Mono'),
        ))
        fig.update_layout(
            title=dict(text="F1-Score Perbandingan", font=dict(color='#1A1F2E', size=13, family=FONT_F)),
            paper_bgcolor=LIGHT_BG, plot_bgcolor=LIGHT_BG, font=dict(color=TICK_C, family=FONT_F),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color=TICK_C)),
            yaxis=dict(showgrid=True, gridcolor=GRID_C, range=[0,0.75], tickfont=dict(size=11, color=TICK_C)),
            margin=dict(l=10,r=10,t=44,b=10), height=260, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=model_names, y=[r["Train Acc"] for r in data], name="Train Acc", marker=dict(color='#6366F1', opacity=0.7)))
        fig.add_trace(go.Bar(x=model_names, y=acc_vals, name="Test Acc", marker=dict(color='#1A3A6C', opacity=0.8)))
        fig.update_layout(
            title=dict(text="Train vs Test Accuracy", font=dict(color='#1A1F2E', size=13, family=FONT_F)),
            paper_bgcolor=LIGHT_BG, plot_bgcolor=LIGHT_BG, barmode='group',
            font=dict(color=TICK_C, family=FONT_F),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color=TICK_C)),
            yaxis=dict(showgrid=True, gridcolor=GRID_C, tickfont=dict(size=11, color=TICK_C)),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TICK_C, size=11)),
            margin=dict(l=10,r=10,t=44,b=10), height=260,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;font-weight:700;color:#6B7A99;margin-bottom:16px;letter-spacing:0.1em;text-transform:uppercase;">Confusion Matrix — Gradient Boosting (tanpa SMOTE)</div>', unsafe_allow_html=True)

    class_names = ["HIGH_RISK","LOW_RISK","MEDIUM_HIGH_RISK","MEDIUM_RISK"]
    cm = np.array([[87,12,412,450],[15,54,598,1475],[87,36,3621,3229],[76,80,2694,9008]])
    fig_cm = go.Figure(go.Heatmap(
        z=cm,
        x=[c.replace("_RISK","").replace("_","-") for c in class_names],
        y=[c.replace("_RISK","").replace("_","-") for c in class_names],
        colorscale=[[0,"#F7F8FA"],[0.5,"#BFDBFE"],[1,"#1A3A6C"]],
        text=cm, texttemplate="%{text}",
        textfont=dict(size=13, color='#1A1F2E', family='DM Mono'),
        showscale=True,
        colorbar=dict(tickfont=dict(color=TICK_C), outlinewidth=0, bgcolor='rgba(0,0,0,0)'),
    ))
    fig_cm.update_layout(
        paper_bgcolor=LIGHT_BG, plot_bgcolor=LIGHT_BG, font=dict(color=TICK_C, family=FONT_F),
        xaxis=dict(title=dict(text="Prediksi", font=dict(color=TICK_C)), tickfont=dict(size=11, color=TICK_C), side='bottom'),
        yaxis=dict(title=dict(text="Aktual",   font=dict(color=TICK_C)), tickfont=dict(size=11, color=TICK_C), autorange='reversed'),
        margin=dict(l=10,r=10,t=20,b=10), height=350,
    )

    st.markdown('<div class="page-section">', unsafe_allow_html=True)
    col_cm, col_insight = st.columns([3,2], gap="large")
    with col_cm:
        st.markdown('<div class="chart-card" style="padding:16px;">', unsafe_allow_html=True)
        st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    with col_insight:
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #E8EBF0;border-radius:14px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.04);min-height:350px;">
            <div style="font-size:11px;font-weight:700;color:#6B7A99;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:14px;">Interpretasi</div>
            <div style="display:flex;flex-direction:column;gap:8px;">
                <div style="padding:10px 12px;background:#FEFCE8;border-left:3px solid #CA8A04;border-radius:6px;">
                    <div style="font-size:12px;color:#854D0E;font-weight:700;">MEDIUM_RISK · F1=0.71</div>
                    <div style="font-size:12px;color:#6B7A99;margin-top:3px;">Prediksi terbaik, dominasi kelas</div>
                </div>
                <div style="padding:10px 12px;background:#FFF8F2;border-left:3px solid #EA580C;border-radius:6px;">
                    <div style="font-size:12px;color:#9A3412;font-weight:700;">MEDIUM_HIGH · F1=0.51</div>
                    <div style="font-size:12px;color:#6B7A99;margin-top:3px;">Performa sedang, cukup andal</div>
                </div>
                <div style="padding:10px 12px;background:#FFF5F5;border-left:3px solid #DC2626;border-radius:6px;">
                    <div style="font-size:12px;color:#991B1B;font-weight:700;">HIGH_RISK · F1=0.17</div>
                    <div style="font-size:12px;color:#6B7A99;margin-top:3px;">Precision tinggi, Recall rendah</div>
                </div>
                <div style="padding:10px 12px;background:#F0FDF4;border-left:3px solid #16A34A;border-radius:6px;">
                    <div style="font-size:12px;color:#166534;font-weight:700;">LOW_RISK · F1=0.05</div>
                    <div style="font-size:12px;color:#6B7A99;margin-top:3px;">Terburuk, class imbalance parah</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#F7F9FF;border:1px solid #C7D2FE;border-radius:14px;padding:20px 24px;">
        <div style="font-size:11px;font-weight:700;color:#4F46E5;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:10px;">Kesimpulan SMOTE</div>
        <div style="font-size:14px;color:#3D4863;line-height:1.75;">
            SMOTE justru <strong style="color:#DC2626;">menurunkan performa</strong> semua model pada dataset Chicago ini.
            Gradient Boosting tanpa SMOTE tetap menjadi model terbaik dengan
            <strong style="color:#1A3A6C;">Test Accuracy 59.31%</strong>, Precision 59.17%, dan Overfit Gap terkecil (0.0149).
        </div>
    </div>
    """, unsafe_allow_html=True)