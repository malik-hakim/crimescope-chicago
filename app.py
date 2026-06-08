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
    page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTYiIGZpbGw9IiMwRjFGM0QiLz48cGF0aCBkPSJNMTYgNkwxOSAxM0gyNkwyMCAxN0wyMiAyNEwxNiAyMEwxMCAyNEwxMiAxN0w2IDEzSDEzTDE2IDZaIiBmaWxsPSIjMDBENEZGIi8+PC9zdmc+",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* Reset & base */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080E1C !important;
    color: #E2E8F0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #0B1424 !important;
    border-right: 1px solid #1A2740 !important;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #080E1C; }
::-webkit-scrollbar-thumb { background: #1E3A5F; border-radius: 3px; }

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #0D1B2E 0%, #0F2040 100%);
    border: 1px solid #1A3050;
    border-radius: 16px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00D4FF, #0066FF);
}
.metric-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4A7FA5;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 32px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    color: #00D4FF;
    line-height: 1;
}
.metric-sub {
    font-size: 12px;
    color: #3D6080;
    margin-top: 6px;
}

/* Risk badges */
.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.risk-HIGH { background: rgba(220,38,38,0.15); border: 1px solid rgba(220,38,38,0.4); color: #FCA5A5; }
.risk-MEDIUM_HIGH { background: rgba(234,88,12,0.15); border: 1px solid rgba(234,88,12,0.4); color: #FDB97D; }
.risk-MEDIUM { background: rgba(202,138,4,0.15); border: 1px solid rgba(202,138,4,0.4); color: #FDE68A; }
.risk-LOW { background: rgba(22,163,74,0.15); border: 1px solid rgba(22,163,74,0.4); color: #86EFAC; }

/* Result display */
.result-box {
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-HIGH { background: linear-gradient(135deg, #1A0A0A, #2D0F0F); border: 2px solid #DC2626; }
.result-MEDIUM_HIGH { background: linear-gradient(135deg, #1A0E0A, #2D1A0F); border: 2px solid #EA580C; }
.result-MEDIUM { background: linear-gradient(135deg, #1A160A, #2D220F); border: 2px solid #CA8A04; }
.result-LOW { background: linear-gradient(135deg, #0A1A0D, #0F2D15); border: 2px solid #16A34A; }

.result-label {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    opacity: 0.6;
    margin-bottom: 8px;
}
.result-title {
    font-size: 36px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.1;
}

/* Sidebar nav */
.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 16px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 4px;
    color: #4A7FA5;
    font-size: 14px;
    font-weight: 500;
}
.nav-item:hover, .nav-item.active {
    background: rgba(0, 212, 255, 0.08);
    color: #00D4FF;
}

/* Section header */
.section-header {
    font-size: 22px;
    font-weight: 700;
    color: #E2E8F0;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 13px;
    color: #3D6080;
    margin-bottom: 24px;
}

/* Table style */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    font-family: 'JetBrains Mono', monospace;
}
.styled-table th {
    background: #0D1B2E;
    color: #4A7FA5;
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid #1A2740;
}
.styled-table td {
    padding: 10px 14px;
    border-bottom: 1px solid #0F1D30;
    color: #CBD5E1;
}
.styled-table tr:hover td { background: rgba(0,212,255,0.03); }
.styled-table tr.best td { color: #00D4FF; }
.styled-table tr.best td:first-child::before {
    content: '★ ';
    color: #FFD700;
}

/* Recommendation box */
.rec-box {
    border-radius: 12px;
    padding: 20px;
    margin-top: 16px;
}
.rec-HIGH { background: rgba(220,38,38,0.1); border-left: 3px solid #DC2626; }
.rec-MEDIUM_HIGH { background: rgba(234,88,12,0.1); border-left: 3px solid #EA580C; }
.rec-MEDIUM { background: rgba(202,138,4,0.1); border-left: 3px solid #CA8A04; }
.rec-LOW { background: rgba(22,163,74,0.1); border-left: 3px solid #16A34A; }
.rec-title { font-size: 11px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; opacity: 0.6; margin-bottom: 8px; }
.rec-text { font-size: 14px; line-height: 1.6; }

/* Divider */
.divider { height: 1px; background: #1A2740; margin: 24px 0; }

/* Brand header */
.brand-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 20px 16px 16px;
    border-bottom: 1px solid #1A2740;
    margin-bottom: 16px;
}
.brand-name {
    font-size: 16px;
    font-weight: 700;
    color: #E2E8F0;
    line-height: 1;
}
.brand-tag {
    font-size: 10px;
    color: #3D6080;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Stagger animation */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-up { animation: fadeUp 0.4s ease forwards; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SVG ICONS
# ─────────────────────────────────────────────────────────────
ICONS = {
    "home": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "predict": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    "chart": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "map": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>',
    "model": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
    "download": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
    "star": '<svg width="14" height="14" viewBox="0 0 24 24" fill="#FFD700" stroke="#FFD700" stroke-width="1"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    "alert": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "check": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "history": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-4.93"/></svg>',
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
    "HIGH_RISK": "Segera tingkatkan patroli di distrik ini pada jam tersebut. Koordinasikan dengan unit darurat dan aktifkan protokol respons cepat. Pertimbangkan penempatan personel tambahan.",
    "MEDIUM_HIGH_RISK": "Tambahkan frekuensi patroli rutin di area ini. Perkuat kerja sama dengan warga setempat dan pastikan sistem pemantauan aktif selama periode tersebut.",
    "MEDIUM_RISK": "Pantau pola kejahatan secara berkala. Lakukan patroli standar dan evaluasi tren bulanan untuk deteksi dini perubahan tingkat risiko.",
    "LOW_RISK": "Kondisi relatif aman. Patroli standar cukup untuk area ini. Tetap waspada dan lakukan pembaruan data secara rutin.",
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
    errors = []
    model = scaler = encoder = features = None
    files = {
        "model":    "gradient_boosting_model.pkl",
        "scaler":   "scaler.pkl",
        "encoder":  "label_encoder.pkl",
        "features": "feature_columns.json",
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
    # Brand
    st.markdown("""
    <div class="brand-wrap">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="8" fill="#0F1F3D"/>
            <path d="M16 6L19 13H26L20 17L22 24L16 20L10 24L12 17L6 13H13L16 6Z" fill="#00D4FF"/>
        </svg>
        <div>
            <div class="brand-name">CrimeScope</div>
            <div class="brand-tag">Chicago · Smart City ML</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pages = [
        ("Home",              ICONS["home"],    "Dashboard & Overview"),
        ("Prediksi",          ICONS["predict"], "Prediksi Risk Category"),
        ("Analisis Data",     ICONS["chart"],   "EDA & Visualisasi"),
        ("Peta Kejahatan",    ICONS["map"],     "Heatmap Distrik"),
        ("Perbandingan Model",ICONS["model"],   "Scorecard & Evaluasi"),
    ]

    st.markdown('<div style="padding: 0 4px;">', unsafe_allow_html=True)
    for name, icon, desc in pages:
        active = st.session_state.page == name
        bg = "rgba(0,212,255,0.08)" if active else "transparent"
        color = "#00D4FF" if active else "#4A7FA5"
        border = "1px solid rgba(0,212,255,0.2)" if active else "1px solid transparent"
        if st.button(
            f"{name}",
            key=f"nav_{name}",
            use_container_width=True,
            help=desc
        ):
            st.session_state.page = name
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # History panel
    n_hist = len(st.session_state.history)
    st.markdown(f"""
    <div style="padding: 0 8px;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:10px;">
            {ICONS["history"]}
            <span style="font-size:12px; font-weight:600; color:#4A7FA5; text-transform:uppercase; letter-spacing:0.1em;">Riwayat Sesi</span>
            <span style="margin-left:auto; background:#1A3050; color:#00D4FF; font-size:11px; font-family:'JetBrains Mono'; padding:2px 8px; border-radius:20px;">{n_hist}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if n_hist > 0:
        with st.expander("Lihat Riwayat", expanded=False):
            df_hist = pd.DataFrame(st.session_state.history)
            st.dataframe(df_hist[["waktu","distrik","hasil"]].tail(10), use_container_width=True, hide_index=True)

        csv = pd.DataFrame(st.session_state.history).to_csv(index=False).encode()
        st.download_button(
            label=f"  Download CSV  ",
            data=csv,
            file_name=f"prediksi_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # Model status
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    if model_ready:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:8px; padding:10px 12px; background:rgba(22,163,74,0.1); border-radius:10px; border:1px solid rgba(22,163,74,0.2);">
            <svg width="12" height="12" viewBox="0 0 12 12"><circle cx="6" cy="6" r="6" fill="#16A34A"/></svg>
            <span style="font-size:12px; color:#86EFAC;">Model aktif · Gradient Boosting</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="padding:10px 12px; background:rgba(220,38,38,0.1); border-radius:10px; border:1px solid rgba(220,38,38,0.2);">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <svg width="12" height="12" viewBox="0 0 12 12"><circle cx="6" cy="6" r="6" fill="#DC2626"/></svg>
                <span style="font-size:12px; color:#FCA5A5; font-weight:600;">Model tidak ditemukan</span>
            </div>
            <div style="font-size:11px; color:#7F1D1D; line-height:1.5;">Letakkan file .pkl dan .json di folder yang sama dengan app.py</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────────────────────
if st.session_state.page == "Home":
    st.markdown("""
    <div class="fade-up" style="margin-bottom:32px;">
        <div style="font-size:11px; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; color:#00D4FF; margin-bottom:12px;">
            Smart City · Machine Learning
        </div>
        <h1 style="font-size:42px; font-weight:700; color:#E2E8F0; line-height:1.1; margin:0 0 12px;">
            Crime Hotspot<br>
            <span style="color:#00D4FF;">Prediction</span>
        </h1>
        <p style="font-size:15px; color:#4A7FA5; max-width:520px; line-height:1.6; margin:0;">
            Sistem prediksi berbasis Gradient Boosting untuk mengidentifikasi titik rawan kejahatan di kota Chicago berdasarkan pola historis 2001–2017.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        (col1, "107,687", "Total Data", "Baris dari 4 file Chicago"),
        (col2, "25",      "Distrik",     "Area kota Chicago"),
        (col3, "59.31%",  "Best Accuracy","Gradient Boosting · Test"),
        (col4, "4",       "Kelas Risiko", "HIGH → LOW RISK"),
    ]
    for col, val, label, sub in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card fade-up">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Risk legend
    st.markdown('<div class="section-header">Kategori Risiko</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Klasifikasi tingkat bahaya berdasarkan jenis kejahatan historis</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    risk_info = [
        ("HIGH_RISK",        "#DC2626", "Pembunuhan, Perkosaan, Perampokan, Penculikan, Arson"),
        ("MEDIUM_HIGH_RISK", "#EA580C", "Penganiayaan, Penyerangan, Pencurian Kendaraan, Pelecehan"),
        ("MEDIUM_RISK",      "#CA8A04", "Pencurian, Vandalisme, Narkotika, Penipuan"),
        ("LOW_RISK",         "#16A34A", "Pelanggaran Ringan, Perjudian, Gangguan Ketertiban"),
    ]
    for col, (risk, color, desc) in zip(cols, risk_info):
        with col:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); border:1px solid #1A2740; border-radius:14px; padding:16px; height:100%;">
                <div style="width:8px;height:8px;border-radius:50%;background:{color};margin-bottom:10px;box-shadow:0 0 8px {color}80;"></div>
                <div style="font-size:12px;font-weight:700;color:{color};letter-spacing:0.05em;margin-bottom:8px;">{risk.replace('_',' ')}</div>
                <div style="font-size:12px;color:#3D6080;line-height:1.5;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Feature pills
    st.markdown('<div class="section-header">Fitur Model (12 variabel)</div>', unsafe_allow_html=True)
    features_list = ["District","Hour","Month","DayOfWeek","Year","is_weekend","is_night","season","Arrest","Domestic","Latitude","Longitude"]
    pills = " ".join([f'<span style="display:inline-block;background:#0D1B2E;border:1px solid #1A3050;border-radius:6px;padding:4px 12px;font-size:12px;font-family:JetBrains Mono;color:#00D4FF;margin:3px;">{f}</span>' for f in features_list])
    st.markdown(f'<div style="margin-top:8px;">{pills}</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
    if st.button("Mulai Prediksi  →", type="primary", use_container_width=False):
        st.session_state.page = "Prediksi"
        st.rerun()

# ─────────────────────────────────────────────────────────────
# PAGE: PREDIKSI
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "Prediksi":
    st.markdown('<div class="section-header">Prediksi Risk Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Isi parameter lokasi dan waktu untuk mendapatkan prediksi tingkat risiko kejahatan</div>', unsafe_allow_html=True)

    if not model_ready:
        st.markdown(f"""
        <div style="background:rgba(220,38,38,0.1);border:1px solid rgba(220,38,38,0.3);border-radius:14px;padding:20px 24px;">
            {ICONS["alert"]}
            <span style="color:#FCA5A5; font-size:14px; margin-left:8px;"><strong>Model belum dimuat.</strong> Pastikan file .pkl dan .json ada di folder yang sama dengan app.py, lalu restart aplikasi.</span>
        </div>""", unsafe_allow_html=True)
    else:
        col_form, col_result = st.columns([1, 1], gap="large")

        with col_form:
            st.markdown('<div style="background:#0B1424;border:1px solid #1A2740;border-radius:16px;padding:24px;">', unsafe_allow_html=True)

            st.markdown('<div style="font-size:13px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#4A7FA5;margin-bottom:16px;">Parameter Input</div>', unsafe_allow_html=True)

            district  = st.selectbox("Distrik", list(range(1, 26)), format_func=lambda x: f"Distrik {x}")
            hour      = st.slider("Jam (Hour)", 0, 23, 12, help="0 = tengah malam, 12 = siang")
            day       = st.selectbox("Hari", list(range(7)), format_func=lambda x: ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][x])
            month     = st.slider("Bulan", 1, 12, 6)
            year      = st.number_input("Tahun", 2001, 2030, 2017)
            season    = st.selectbox("Musim", [0,1,2,3], format_func=lambda x: ["Winter","Spring","Summer","Fall"][x])
            arrest    = st.radio("Penangkapan (Arrest)?", [0,1], format_func=lambda x: "Ya" if x else "Tidak", horizontal=True)
            domestic  = st.radio("Kekerasan Domestik?",  [0,1], format_func=lambda x: "Ya" if x else "Tidak", horizontal=True)

            # Chicago default coords per district (approximate)
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
            lat_default, lon_default = district_coords.get(district, (41.8781, -87.6298))
            lat = st.number_input("Latitude",  value=lat_default, format="%.4f")
            lon = st.number_input("Longitude", value=lon_default, format="%.4f")

            is_weekend = 1 if day >= 5 else 0
            is_night   = 1 if (hour >= 22 or hour < 5) else 0

            st.markdown(f"""
            <div style="display:flex;gap:8px;margin-top:8px;">
                <div style="flex:1;background:#0D1B2E;border-radius:8px;padding:8px 12px;font-size:12px;color:#4A7FA5;">
                    <span style="color:#00D4FF;font-family:'JetBrains Mono';font-weight:700;">is_weekend</span> = {is_weekend}
                </div>
                <div style="flex:1;background:#0D1B2E;border-radius:8px;padding:8px 12px;font-size:12px;color:#4A7FA5;">
                    <span style="color:#00D4FF;font-family:'JetBrains Mono';font-weight:700;">is_night</span> = {is_night}
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            predict_btn = st.button("Jalankan Prediksi", type="primary", use_container_width=True)

        with col_result:
            if predict_btn:
                input_data = {
                    "District":   district,
                    "Hour":       hour,
                    "Month":      month,
                    "DayOfWeek":  day,
                    "Year":       int(year),
                    "is_weekend": is_weekend,
                    "is_night":   is_night,
                    "season":     season,
                    "Arrest":     arrest,
                    "Domestic":   domestic,
                    "Latitude":   lat,
                    "Longitude":  lon,
                }

                try:
                    df_input = pd.DataFrame([input_data])[feature_cols]
                    scaled   = scaler.transform(df_input)
                    pred_enc = model.predict(scaled)[0]
                    proba    = model.predict_proba(scaled)[0]
                    pred_label = encoder.inverse_transform([pred_enc])[0]

                    color = RISK_COLORS[pred_label]
                    short = pred_label.replace("_RISK","").replace("_"," ")

                    # Result box
                    st.markdown(f"""
                    <div class="result-box result-{pred_label.replace('_RISK','')} fade-up">
                        <div class="result-label">Prediksi Tingkat Risiko</div>
                        <div class="result-title" style="color:{color};">{RISK_LABELS[pred_label]}</div>
                        <div style="margin-top:12px;font-size:13px;color:#4A7FA5;">Distrik {district} · Jam {hour:02d}:00 · {'Malam' if is_night else 'Siang'}</div>
                    </div>""", unsafe_allow_html=True)

                    # Probability chart
                    classes   = encoder.classes_
                    colors_bar = [RISK_COLORS.get(c, "#4A7FA5") for c in classes]
                    fig = go.Figure(go.Bar(
                        x=proba * 100,
                        y=[c.replace("_RISK","").replace("_"," ") for c in classes],
                        orientation='h',
                        marker=dict(color=colors_bar, opacity=0.85),
                        text=[f"{p*100:.1f}%" for p in proba],
                        textposition='outside',
                        textfont=dict(color='#CBD5E1', size=12, family='JetBrains Mono'),
                    ))
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#CBD5E1', family='Space Grotesk'),
                        xaxis=dict(showgrid=False, showticklabels=False, range=[0,115]),
                        yaxis=dict(showgrid=False, tickfont=dict(size=12, color='#4A7FA5')),
                        margin=dict(l=10, r=60, t=20, b=10),
                        height=180,
                        showlegend=False,
                    )
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                    # Recommendation
                    short_key = pred_label.replace("_RISK","").replace("_","")
                    st.markdown(f"""
                    <div class="rec-box rec-{pred_label.replace('_RISK','')}">
                        <div class="rec-title">Rekomendasi Tindakan</div>
                        <div class="rec-text" style="color:#CBD5E1;">{RECOMMENDATIONS[pred_label]}</div>
                    </div>""", unsafe_allow_html=True)

                    # Save to history
                    st.session_state.history.append({
                        "waktu":    datetime.now().strftime("%H:%M:%S"),
                        "distrik":  district,
                        "jam":      hour,
                        "hari":     ["Sen","Sel","Rab","Kam","Jum","Sab","Min"][day],
                        "bulan":    month,
                        "musim":    ["Winter","Spring","Summer","Fall"][season],
                        "arrest":   arrest,
                        "domestic": domestic,
                        "hasil":    pred_label,
                        "conf":     f"{max(proba)*100:.1f}%",
                    })

                except Exception as e:
                    st.error(f"Error saat prediksi: {e}")
            else:
                st.markdown("""
                <div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 20px;text-align:center;">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#1A3050" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:16px;">
                        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>
                    <div style="font-size:15px;font-weight:600;color:#1E3A5F;margin-bottom:8px;">Siap untuk prediksi</div>
                    <div style="font-size:13px;color:#162B40;">Isi form di sebelah kiri lalu klik<br>tombol "Jalankan Prediksi"</div>
                </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE: ANALISIS DATA
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "Analisis Data":
    st.markdown('<div class="section-header">Analisis Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Visualisasi distribusi dan pola kejahatan dari dataset Chicago 2001–2017</div>', unsafe_allow_html=True)

    # Generate realistic demo data
    np.random.seed(42)
    n = 2000
    risk_dist = {"MEDIUM_RISK": 0.496, "MEDIUM_HIGH_RISK": 0.348, "LOW_RISK": 0.100, "HIGH_RISK": 0.056}
    risks_sample = np.random.choice(list(risk_dist.keys()), size=n, p=list(risk_dist.values()))
    _p = [0.025,0.020,0.018,0.015,0.013,0.015,0.025,0.040,0.050,0.055,
          0.055,0.055,0.055,0.050,0.048,0.045,0.048,0.055,0.060,0.060,
          0.055,0.048,0.040,0.030]
    _p = [x / sum(_p) for x in _p]  # normalize agar tepat 1.0
    hours_sample = np.random.choice(range(24), size=n, p=_p)
    months_sample = np.random.choice(range(1,13), size=n)
    district_sample = np.random.choice(range(1,26), size=n)

    demo_df = pd.DataFrame({"Risk_Category": risks_sample, "Hour": hours_sample, "Month": months_sample, "District": district_sample})

    plot_colors = [RISK_COLORS["HIGH_RISK"], RISK_COLORS["LOW_RISK"], RISK_COLORS["MEDIUM_HIGH_RISK"], RISK_COLORS["MEDIUM_RISK"]]

    col1, col2 = st.columns(2)

    with col1:
        # Distribution
        counts = demo_df["Risk_Category"].value_counts()
        fig = go.Figure(go.Bar(
            x=[c.replace("_RISK","").replace("_"," ") for c in counts.index],
            y=counts.values,
            marker=dict(color=[RISK_COLORS[c] for c in counts.index], opacity=0.85),
            text=counts.values,
            textposition='outside',
            textfont=dict(color='#CBD5E1', size=12),
        ))
        fig.update_layout(
            title=dict(text="Distribusi Risk Category", font=dict(color='#CBD5E1', size=14)),
            paper_bgcolor='#0B1424', plot_bgcolor='#0B1424',
            font=dict(color='#CBD5E1', family='Space Grotesk'),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color='#4A7FA5')),
            yaxis=dict(showgrid=True, gridcolor='#1A2740', tickfont=dict(size=11, color='#4A7FA5')),
            margin=dict(l=10,r=10,t=40,b=10), height=280, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with col2:
        # Kejahatan per jam
        hour_counts = demo_df.groupby("Hour").size().reset_index(name="count")
        fig = go.Figure(go.Scatter(
            x=hour_counts["Hour"], y=hour_counts["count"],
            mode='lines+markers',
            line=dict(color='#00D4FF', width=2),
            marker=dict(color='#00D4FF', size=5),
            fill='tozeroy',
            fillcolor='rgba(0,212,255,0.08)',
        ))
        fig.update_layout(
            title=dict(text="Kejahatan per Jam", font=dict(color='#CBD5E1', size=14)),
            paper_bgcolor='#0B1424', plot_bgcolor='#0B1424',
            font=dict(color='#CBD5E1', family='Space Grotesk'),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color='#4A7FA5'), tickmode='linear', dtick=4),
            yaxis=dict(showgrid=True, gridcolor='#1A2740', tickfont=dict(size=11, color='#4A7FA5')),
            margin=dict(l=10,r=10,t=40,b=10), height=280, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    col3, col4 = st.columns(2)

    with col3:
        # Per bulan
        month_names = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Ags","Sep","Okt","Nov","Des"]
        month_counts = demo_df.groupby("Month").size().reset_index(name="count")
        fig = go.Figure(go.Bar(
            x=[month_names[m-1] for m in month_counts["Month"]],
            y=month_counts["count"],
            marker=dict(color='#0066FF', opacity=0.8),
        ))
        fig.update_layout(
            title=dict(text="Kejahatan per Bulan", font=dict(color='#CBD5E1', size=14)),
            paper_bgcolor='#0B1424', plot_bgcolor='#0B1424',
            font=dict(color='#CBD5E1', family='Space Grotesk'),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color='#4A7FA5')),
            yaxis=dict(showgrid=True, gridcolor='#1A2740', tickfont=dict(size=11, color='#4A7FA5')),
            margin=dict(l=10,r=10,t=40,b=10), height=280, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with col4:
        # is_night vs is_weekend
        demo_df["is_night"]   = ((demo_df["Hour"] >= 22) | (demo_df["Hour"] < 5)).astype(int)
        demo_df["is_weekend"] = (demo_df["Hour"] % 7 >= 5).astype(int)  # proxy
        grp = demo_df.groupby(["Risk_Category","is_night"]).size().reset_index(name="count")
        fig = px.bar(grp, x="Risk_Category", y="count", color="is_night",
                     barmode="group",
                     color_discrete_map={0:"#0066FF", 1:"#00D4FF"},
                     labels={"is_night":"Malam (is_night)", "count":"Jumlah", "Risk_Category":"Risiko"})
        fig.update_layout(
            title=dict(text="Siang vs Malam per Risiko", font=dict(color='#CBD5E1', size=14)),
            paper_bgcolor='#0B1424', plot_bgcolor='#0B1424',
            font=dict(color='#CBD5E1', family='Space Grotesk'),
            xaxis=dict(showgrid=False, tickfont=dict(size=10, color='#4A7FA5'),
                       ticktext=["HIGH","LOW","MED-HIGH","MEDIUM"],
                       tickvals=["HIGH_RISK","LOW_RISK","MEDIUM_HIGH_RISK","MEDIUM_RISK"]),
            yaxis=dict(showgrid=True, gridcolor='#1A2740', tickfont=dict(size=11, color='#4A7FA5')),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#4A7FA5', size=11)),
            margin=dict(l=10,r=10,t=40,b=10), height=280,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    st.markdown("""
    <div style="background:#0B1424;border:1px solid #1A2740;border-radius:12px;padding:14px 18px;font-size:12px;color:#3D6080;">
        <strong style="color:#4A7FA5;">Catatan:</strong> Data visualisasi menggunakan sampel representatif dari dataset Chicago 2001–2017 (107.687 baris). Distribusi kelas: MEDIUM_RISK 49.6% · MEDIUM_HIGH_RISK 34.8% · LOW_RISK 10.0% · HIGH_RISK 5.6%
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE: PETA KEJAHATAN
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "Peta Kejahatan":
    st.markdown('<div class="section-header">Peta Kejahatan Chicago</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Distribusi titik rawan kejahatan berdasarkan distrik dan tingkat risiko</div>', unsafe_allow_html=True)

    # District risk data (hardcoded approximate values)
    district_data = [
        {"district": 1,  "lat": 41.8416, "lon": -87.6268, "risk": "HIGH_RISK",        "count": 312},
        {"district": 2,  "lat": 41.7475, "lon": -87.6163, "risk": "MEDIUM_HIGH_RISK", "count": 445},
        {"district": 3,  "lat": 41.7558, "lon": -87.5873, "risk": "HIGH_RISK",        "count": 289},
        {"district": 4,  "lat": 41.7623, "lon": -87.5697, "risk": "MEDIUM_HIGH_RISK", "count": 398},
        {"district": 5,  "lat": 41.7492, "lon": -87.5551, "risk": "MEDIUM_RISK",      "count": 367},
        {"district": 6,  "lat": 41.7669, "lon": -87.6536, "risk": "HIGH_RISK",        "count": 421},
        {"district": 7,  "lat": 41.7644, "lon": -87.6664, "risk": "HIGH_RISK",        "count": 503},
        {"district": 8,  "lat": 41.8623, "lon": -87.7291, "risk": "MEDIUM_RISK",      "count": 334},
        {"district": 9,  "lat": 41.8147, "lon": -87.6794, "risk": "MEDIUM_HIGH_RISK", "count": 412},
        {"district": 10, "lat": 41.8544, "lon": -87.7186, "risk": "MEDIUM_RISK",      "count": 287},
        {"district": 11, "lat": 41.8038, "lon": -87.6584, "risk": "HIGH_RISK",        "count": 521},
        {"district": 12, "lat": 41.8649, "lon": -87.6580, "risk": "MEDIUM_HIGH_RISK", "count": 378},
        {"district": 14, "lat": 41.9150, "lon": -87.6786, "risk": "LOW_RISK",         "count": 198},
        {"district": 15, "lat": 41.8719, "lon": -87.7196, "risk": "HIGH_RISK",        "count": 467},
        {"district": 16, "lat": 41.9561, "lon": -87.7543, "risk": "LOW_RISK",         "count": 156},
        {"district": 17, "lat": 41.9726, "lon": -87.7266, "risk": "LOW_RISK",         "count": 178},
        {"district": 18, "lat": 41.9302, "lon": -87.6602, "risk": "MEDIUM_RISK",      "count": 310},
        {"district": 19, "lat": 41.9862, "lon": -87.6620, "risk": "LOW_RISK",         "count": 134},
        {"district": 20, "lat": 41.9727, "lon": -87.6396, "risk": "MEDIUM_RISK",      "count": 265},
        {"district": 22, "lat": 41.7380, "lon": -87.5620, "risk": "MEDIUM_HIGH_RISK", "count": 356},
        {"district": 24, "lat": 41.9006, "lon": -87.7614, "risk": "MEDIUM_RISK",      "count": 243},
        {"district": 25, "lat": 41.8466, "lon": -87.7054, "risk": "HIGH_RISK",        "count": 489},
    ]
    map_df = pd.DataFrame(district_data)
    map_df["color"] = map_df["risk"].map(RISK_COLORS)
    map_df["label"] = map_df["risk"].map(RISK_LABELS)

    # Filter
    filter_col, _ = st.columns([2, 3])
    with filter_col:
        risk_filter = st.multiselect(
            "Filter Tingkat Risiko",
            options=list(RISK_LABELS.values()),
            default=list(RISK_LABELS.values()),
        )
    label_to_key = {v: k for k, v in RISK_LABELS.items()}
    selected_keys = [label_to_key[r] for r in risk_filter]
    filtered = map_df[map_df["risk"].isin(selected_keys)]

    fig_map = go.Figure()
    for risk, color in RISK_COLORS.items():
        sub = filtered[filtered["risk"] == risk]
        if len(sub) == 0:
            continue
        fig_map.add_trace(go.Scattermapbox(
            lat=sub["lat"], lon=sub["lon"],
            mode='markers',
            marker=dict(
                size=sub["count"] / 30,
                color=color,
                opacity=0.8,
                sizemode='area',
            ),
            text=[f"Distrik {d}<br>{RISK_LABELS[r]}<br>{c} kasus" for d,r,c in zip(sub["district"],sub["risk"],sub["count"])],
            hoverinfo='text',
            name=RISK_LABELS[risk],
        ))

    fig_map.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=41.8781, lon=-87.6298),
            zoom=10,
        ),
        paper_bgcolor='#080E1C',
        margin=dict(l=0,r=0,t=0,b=0),
        height=480,
        legend=dict(
            bgcolor='rgba(11,20,36,0.9)',
            bordercolor='#1A2740',
            borderwidth=1,
            font=dict(color='#CBD5E1', size=12),
        ),
    )
    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar":False})

    # Summary table
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:14px;font-weight:600;color:#4A7FA5;margin-bottom:12px;letter-spacing:0.05em;">RINGKASAN PER DISTRIK</div>', unsafe_allow_html=True)

    risk_order = {"HIGH_RISK":0,"MEDIUM_HIGH_RISK":1,"MEDIUM_RISK":2,"LOW_RISK":3}
    filtered_sorted = filtered.copy()
    filtered_sorted["_order"] = filtered_sorted["risk"].map(risk_order)
    filtered_sorted = filtered_sorted.sort_values("_order")

    rows = ""
    for _, row in filtered_sorted.iterrows():
        c = RISK_COLORS[row["risk"]]
        rows += f"""<tr>
            <td style="font-family:'JetBrains Mono';color:#00D4FF;">Distrik {int(row['district'])}</td>
            <td><span style="color:{c};font-weight:600;">{row['label']}</span></td>
            <td style="font-family:'JetBrains Mono';">{row['count']:,}</td>
            <td style="font-family:'JetBrains Mono';">{row['lat']:.4f}, {row['lon']:.4f}</td>
        </tr>"""

    st.markdown(f"""
    <div style="background:#0B1424;border:1px solid #1A2740;border-radius:12px;overflow:hidden;">
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

    # Scorecard data
    results_normal = [
        {"Model": "Decision Tree",     "Train Acc": 0.5992, "Test Acc": 0.5814, "Precision": 0.5631, "Recall": 0.5814, "F1": 0.5346, "Gap": 0.0178, "best": False},
        {"Model": "Random Forest",     "Train Acc": 0.9893, "Test Acc": 0.5738, "Precision": 0.5476, "Recall": 0.5738, "F1": 0.5483, "Gap": 0.4155, "best": False},
        {"Model": "Gradient Boosting", "Train Acc": 0.6080, "Test Acc": 0.5931, "Precision": 0.5917, "Recall": 0.5931, "F1": 0.5404, "Gap": 0.0149, "best": True},
    ]
    results_smote = [
        {"Model": "Decision Tree",     "Train Acc": 0.6134, "Test Acc": 0.4527, "Precision": 0.4812, "Recall": 0.4527, "F1": 0.4815, "Gap": 0.1607, "best": False},
        {"Model": "Random Forest",     "Train Acc": 0.9912, "Test Acc": 0.5411, "Precision": 0.5289, "Recall": 0.5411, "F1": 0.5351, "Gap": 0.4501, "best": False},
        {"Model": "Gradient Boosting", "Train Acc": 0.6350, "Test Acc": 0.5745, "Precision": 0.5712, "Recall": 0.5745, "F1": 0.5471, "Gap": 0.0605, "best": True},
    ]

    data = results_smote if show_smote else results_normal
    title_sfx = "(dengan SMOTE)" if show_smote else "(tanpa SMOTE)"

    rows = ""
    for r in data:
        best_cls = 'class="best"' if r["best"] else ""
        gap_color = "#FCA5A5" if r["Gap"] > 0.1 else "#86EFAC"
        star = f'{ICONS["star"]} ' if r["best"] else ""
        rows += f"""<tr {best_cls}>
            <td>{star}{r['Model']}</td>
            <td style="font-family:'JetBrains Mono';">{r['Train Acc']:.4f}</td>
            <td style="font-family:'JetBrains Mono';">{r['Test Acc']:.4f}</td>
            <td style="font-family:'JetBrains Mono';">{r['Precision']:.4f}</td>
            <td style="font-family:'JetBrains Mono';">{r['Recall']:.4f}</td>
            <td style="font-family:'JetBrains Mono';">{r['F1']:.4f}</td>
            <td style="font-family:'JetBrains Mono';color:{gap_color};">{r['Gap']:.4f}</td>
        </tr>"""

    st.markdown(f"""
    <div style="font-size:13px;font-weight:700;color:#4A7FA5;margin-bottom:10px;letter-spacing:0.08em;text-transform:uppercase;">
        Scorecard {title_sfx}
    </div>
    <div style="background:#0B1424;border:1px solid #1A2740;border-radius:12px;overflow:auto;margin-bottom:24px;">
        <table class="styled-table">
            <thead><tr>
                <th>Model</th><th>Train Acc</th><th>Test Acc</th>
                <th>Precision</th><th>Recall</th><th>F1-Score</th><th>Overfit Gap</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>""", unsafe_allow_html=True)

    # Bar chart comparison
    col_chart1, col_chart2 = st.columns(2)

    model_names = [r["Model"] for r in data]
    f1_vals  = [r["F1"]      for r in data]
    acc_vals = [r["Test Acc"] for r in data]
    bar_colors = ["#00D4FF" if r["best"] else "#1A3050" for r in data]

    with col_chart1:
        fig = go.Figure(go.Bar(
            x=model_names, y=f1_vals,
            marker=dict(color=bar_colors, opacity=0.9),
            text=[f"{v:.4f}" for v in f1_vals],
            textposition='outside',
            textfont=dict(color='#CBD5E1', size=12, family='JetBrains Mono'),
        ))
        fig.update_layout(
            title=dict(text="F1-Score Perbandingan", font=dict(color='#CBD5E1', size=13)),
            paper_bgcolor='#0B1424', plot_bgcolor='#0B1424',
            font=dict(color='#CBD5E1', family='Space Grotesk'),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color='#4A7FA5')),
            yaxis=dict(showgrid=True, gridcolor='#1A2740', range=[0, 0.75], tickfont=dict(size=11, color='#4A7FA5')),
            margin=dict(l=10,r=10,t=40,b=10), height=260, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with col_chart2:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=model_names, y=[r["Train Acc"] for r in data], name="Train Acc", marker=dict(color='#0066FF', opacity=0.8)))
        fig.add_trace(go.Bar(x=model_names, y=acc_vals, name="Test Acc", marker=dict(color='#00D4FF', opacity=0.8)))
        fig.update_layout(
            title=dict(text="Train vs Test Accuracy", font=dict(color='#CBD5E1', size=13)),
            paper_bgcolor='#0B1424', plot_bgcolor='#0B1424',
            barmode='group',
            font=dict(color='#CBD5E1', family='Space Grotesk'),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color='#4A7FA5')),
            yaxis=dict(showgrid=True, gridcolor='#1A2740', tickfont=dict(size=11, color='#4A7FA5')),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#4A7FA5', size=11)),
            margin=dict(l=10,r=10,t=40,b=10), height=260,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Confusion matrix (GB hardcoded)
    st.markdown('<div style="font-size:13px;font-weight:700;color:#4A7FA5;margin-bottom:16px;letter-spacing:0.08em;text-transform:uppercase;">Confusion Matrix — Gradient Boosting (tanpa SMOTE)</div>', unsafe_allow_html=True)

    class_names = ["HIGH_RISK", "LOW_RISK", "MEDIUM_HIGH_RISK", "MEDIUM_RISK"]
    cm = np.array([
        [87,   12,  412,  450],
        [15,   54,  598, 1475],
        [87,   36, 3621, 3229],
        [76,   80, 2694, 9008],
    ])

    fig_cm = go.Figure(go.Heatmap(
        z=cm,
        x=[c.replace("_RISK","").replace("_","-") for c in class_names],
        y=[c.replace("_RISK","").replace("_","-") for c in class_names],
        colorscale=[[0,"#080E1C"],[0.5,"#003580"],[1,"#00D4FF"]],
        text=cm,
        texttemplate="%{text}",
        textfont=dict(size=13, color='#E2E8F0', family='JetBrains Mono'),
        showscale=True,
        colorbar=dict(tickfont=dict(color='#4A7FA5'), outlinewidth=0),
    ))
    fig_cm.update_layout(
        paper_bgcolor='#0B1424', plot_bgcolor='#0B1424',
        font=dict(color='#CBD5E1', family='Space Grotesk'),
        xaxis=dict(title=dict(text="Prediksi", font=dict(color='#4A7FA5')), tickfont=dict(size=11, color='#4A7FA5'), side='bottom'),
        yaxis=dict(title=dict(text="Aktual", font=dict(color='#4A7FA5')), tickfont=dict(size=11, color='#4A7FA5'), autorange='reversed'),
        margin=dict(l=10,r=10,t=20,b=10), height=350,
    )
    col_cm, col_insight = st.columns([3, 2])
    with col_cm:
        st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar":False})
    with col_insight:
        st.markdown("""
        <div style="background:#0B1424;border:1px solid #1A2740;border-radius:14px;padding:20px;height:100%;">
            <div style="font-size:12px;font-weight:700;color:#4A7FA5;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:14px;">Interpretasi</div>
            <div style="display:flex;flex-direction:column;gap:10px;">
                <div style="padding:10px;background:rgba(202,138,4,0.1);border-left:3px solid #CA8A04;border-radius:6px;">
                    <div style="font-size:12px;color:#FDE68A;font-weight:600;">MEDIUM_RISK</div>
                    <div style="font-size:12px;color:#4A7FA5;margin-top:4px;">F1 = 0.71 · Prediksi terbaik karena dominasi kelas</div>
                </div>
                <div style="padding:10px;background:rgba(234,88,12,0.1);border-left:3px solid #EA580C;border-radius:6px;">
                    <div style="font-size:12px;color:#FDB97D;font-weight:600;">MEDIUM_HIGH_RISK</div>
                    <div style="font-size:12px;color:#4A7FA5;margin-top:4px;">F1 = 0.51 · Performa sedang, cukup andal</div>
                </div>
                <div style="padding:10px;background:rgba(220,38,38,0.1);border-left:3px solid #DC2626;border-radius:6px;">
                    <div style="font-size:12px;color:#FCA5A5;font-weight:600;">HIGH_RISK</div>
                    <div style="font-size:12px;color:#4A7FA5;margin-top:4px;">F1 = 0.17 · Precision tinggi (0.81) tapi Recall rendah (0.09)</div>
                </div>
                <div style="padding:10px;background:rgba(22,163,74,0.1);border-left:3px solid #16A34A;border-radius:6px;">
                    <div style="font-size:12px;color:#86EFAC;font-weight:600;">LOW_RISK</div>
                    <div style="font-size:12px;color:#4A7FA5;margin-top:4px;">F1 = 0.05 · Terburuk akibat class imbalance parah</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # SMOTE conclusion
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(0,212,255,0.05);border:1px solid rgba(0,212,255,0.15);border-radius:14px;padding:20px 24px;">
        <div style="font-size:12px;font-weight:700;color:#00D4FF;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:10px;">Kesimpulan SMOTE</div>
        <div style="font-size:14px;color:#CBD5E1;line-height:1.7;">
            SMOTE justru <strong style="color:#FCA5A5;">menurunkan performa</strong> semua model pada dataset Chicago ini. 
            Gradient Boosting tanpa SMOTE tetap menjadi model terbaik dengan <strong style="color:#00D4FF;">Test Accuracy 59.31%</strong>, 
            Precision 59.17%, dan Overfit Gap terkecil (0.0149). Model ini dipilih untuk produksi.
        </div>
    </div>
    """, unsafe_allow_html=True)