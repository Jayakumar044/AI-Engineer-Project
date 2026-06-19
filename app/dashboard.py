import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Sales Intelligence Platform",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DESIGN TOKENS
# ============================================================
NAVY = "#0F172A"
SLATE_DARK = "#1E293B"
SLATE = "#334155"
MUTED = "#64748B"
BORDER = "#E2E8F0"
CANVAS = "#F8FAFC"
WHITE = "#FFFFFF"
INDIGO = "#4F46E5"
INDIGO_LIGHT = "#EEF2FF"
EMERALD = "#10B981"
EMERALD_LIGHT = "#ECFDF5"
AMBER = "#F59E0B"
AMBER_LIGHT = "#FFFBEB"
RED = "#EF4444"

CHART_PALETTE = ["#4F46E5", "#10B981", "#F59E0B", "#EF4444", "#06B6D4", "#8B5CF6"]

# ============================================================
# GLOBAL STYLES
# ============================================================
st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">

<style>
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, sans-serif;
    }}

    * {{
        scroll-behavior: smooth;
    }}

    /* ---- Base canvas ---- */
    .stApp {{
        background-color: {CANVAS};
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        max-width: 1180px;
    }}

    /* ---- Hide default Streamlit chrome ---- */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{
        background: transparent;
    }}
    /* Hide ONLY the "Deploy" button — NOT the whole toolbar, since the
       sidebar reopen button (stExpandSidebarButton) also lives inside the
       toolbar and must stay visible and clickable. */
    .stAppDeployButton {{
        display: none !important;
    }}

    /* ---- Entrance animation for the whole app ---- */
    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .main .block-container > div {{
        animation: fadeUp 0.45s ease-out;
    }}

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {{
        background-color: {NAVY};
        border-right: none;
    }}
    section[data-testid="stSidebar"] > div {{
        padding-top: 1.4rem;
    }}
    section[data-testid="stSidebar"] * {{
        color: #E2E8F0 !important;
    }}
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] small {{
        color: #94A3B8 !important;
    }}
    section[data-testid="stSidebar"] hr {{
        border-color: #283548 !important;
        margin: 1.4rem 0 !important;
    }}
    section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {{
        background-color: #1A2436 !important;
        border-color: #2D3B52 !important;
        border-radius: 9px !important;
        transition: border-color 0.15s ease;
    }}
    section[data-testid="stSidebar"] [data-baseweb="select"]:hover > div {{
        border-color: {INDIGO} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {{
        background-color: #1A2436 !important;
        border: 1.5px dashed #344256 !important;
        border-radius: 12px !important;
        transition: border-color 0.2s ease, background-color 0.2s ease;
    }}
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]:hover {{
        border-color: {INDIGO} !important;
        background-color: #1E2A40 !important;
    }}
    section[data-testid="stSidebar"] [data-baseweb="tag"] {{
        background-color: {INDIGO} !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
    }}
    .sidebar-eyebrow {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 600;
        color: #5B6B85 !important;
        letter-spacing: 0.12em;
        margin-bottom: 0.55rem;
        margin-top: 0.2rem;
    }}

    /* ---- Headings ---- */
    h1 {{
        font-weight: 800 !important;
        letter-spacing: -0.025em !important;
        color: {NAVY} !important;
    }}
    h2 {{
        font-weight: 700 !important;
        letter-spacing: -0.015em !important;
        color: {NAVY} !important;
        font-size: 1.35rem !important;
    }}
    h3, h4 {{
        font-weight: 600 !important;
        color: {SLATE} !important;
        letter-spacing: -0.005em;
    }}
    p, label, .stMarkdown {{
        color: {SLATE};
    }}

    /* ---- Section header with accent bar ---- */
    .section-label {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 3rem;
        margin-bottom: 1.1rem;
        animation: fadeUp 0.4s ease-out;
    }}
    .section-label .bar {{
        width: 5px;
        height: 24px;
        background: linear-gradient(180deg, {INDIGO}, #7C73F0);
        border-radius: 3px;
    }}
    .section-label .num {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        color: #A5ADBB;
        letter-spacing: 0.08em;
        background: {WHITE};
        border: 1px solid {BORDER};
        padding: 2px 8px;
        border-radius: 6px;
    }}
    .section-label h2 {{
        margin: 0 !important;
    }}

    /* ---- Hero header ---- */
    .hero {{
        background:
            radial-gradient(circle at 15% 20%, rgba(99, 102, 241, 0.18), transparent 45%),
            linear-gradient(135deg, {NAVY} 0%, #16213A 55%, {SLATE_DARK} 100%);
        border-radius: 20px;
        padding: 2.6rem 2.8rem;
        margin-bottom: 2.2rem;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(15, 23, 42, 0.18);
    }}
    .hero .eyebrow {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        color: #A5B4FC;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .hero .eyebrow .dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: {EMERALD};
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6);
        animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.55); }}
        70% {{ box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
    }}
    .hero h1 {{
        color: white !important;
        font-size: 2.25rem !important;
        margin-bottom: 0.6rem !important;
        line-height: 1.15 !important;
    }}
    .hero p {{
        color: #B9C2D4;
        font-size: 1.02rem;
        margin: 0;
        max-width: 620px;
        line-height: 1.55;
    }}

    /* ---- Metric cards ---- */
    div[data-testid="stMetric"] {{
        background-color: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        transition: box-shadow 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.09);
        transform: translateY(-2px);
        border-color: #C7D2FE;
    }}
    div[data-testid="stMetricLabel"] {{
        font-size: 0.76rem !important;
        font-weight: 600 !important;
        color: {MUTED} !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    div[data-testid="stMetricValue"] {{
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        color: {NAVY} !important;
        font-size: 1.65rem !important;
    }}

    /* ---- Tabs ---- */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        border-bottom: 1px solid {BORDER};
    }}
    .stTabs [data-baseweb="tab"] {{
        font-weight: 600;
        font-size: 0.9rem;
        color: {MUTED};
        padding: 11px 18px;
        border-radius: 8px 8px 0 0;
        transition: color 0.15s ease, background-color 0.15s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: {INDIGO};
        background-color: {INDIGO_LIGHT};
    }}
    .stTabs [aria-selected="true"] {{
        color: {INDIGO} !important;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        background-color: {INDIGO} !important;
        height: 3px;
        border-radius: 3px 3px 0 0;
    }}

    /* ---- Buttons ---- */
    .stButton > button {{
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        border: 1px solid {BORDER};
        transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .stButton > button[kind="primary"] {{
        background-color: {INDIGO};
        border: none;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.28);
    }}
    .stButton > button[kind="primary"]:hover {{
        background-color: #4338CA;
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.38);
        transform: translateY(-1px);
    }}
    .stButton > button[kind="primary"]:active {{
        transform: translateY(0px) scale(0.98);
    }}
    .stDownloadButton > button {{
        border-radius: 10px;
        font-weight: 600;
        border: 1px solid {BORDER};
        background-color: {WHITE};
        color: {SLATE};
        transition: all 0.18s ease;
    }}
    .stDownloadButton > button:hover {{
        border-color: {INDIGO};
        color: {INDIGO};
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.12);
        transform: translateY(-1px);
    }}

    /* ---- Expander ---- */
    div[data-testid="stExpander"] {{
        border: 1px solid {BORDER} !important;
        border-radius: 13px !important;
        background-color: {WHITE};
        transition: border-color 0.15s ease;
        overflow: hidden;
    }}
    div[data-testid="stExpander"]:hover {{
        border-color: #C7D2FE !important;
    }}

    /* ---- Dataframe ---- */
    div[data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid {BORDER};
    }}

    /* ---- Alerts ---- */
    div[data-testid="stAlert"] {{
        border-radius: 12px;
        border: none;
    }}

    /* ---- Selectbox / number input ---- */
    div[data-baseweb="select"] > div {{
        border-radius: 9px !important;
        border-color: {BORDER} !important;
        transition: border-color 0.15s ease;
    }}
    div[data-baseweb="select"]:hover > div {{
        border-color: #A5B4FC !important;
    }}
    div[data-testid="stNumberInput"] input {{
        border-radius: 9px !important;
        font-family: 'JetBrains Mono', monospace;
    }}
    div[data-testid="stNumberInput"]:hover input {{
        border-color: #A5B4FC !important;
    }}

    /* ---- Result panel ---- */
    .result-panel {{
        background: linear-gradient(135deg, {EMERALD_LIGHT} 0%, #F0FDF9 100%);
        border: 1px solid #A7F3D0;
        border-radius: 14px;
        padding: 1.3rem 1.6rem;
        margin: 0.6rem 0 1.2rem 0;
        animation: fadeUp 0.3s ease-out;
    }}
    .result-panel .label {{
        font-size: 0.78rem;
        color: #047857;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 4px;
    }}
    .result-panel .value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.9rem;
        font-weight: 700;
        color: #065F46;
    }}

    /* ---- Sidebar stat card ---- */
    .sidebar-stat {{
        background: #1A2436;
        border: 1px solid #2D3B52;
        border-radius: 12px;
        padding: 12px 16px;
        transition: border-color 0.2s ease;
    }}
    .sidebar-stat:hover {{
        border-color: {INDIGO};
    }}
    .sidebar-stat .label {{
        font-size: 0.72rem;
        color: #7C8AA3;
        margin-bottom: 3px;
        letter-spacing: 0.03em;
    }}
    .sidebar-stat .value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.25rem;
        font-weight: 700;
        color: white;
    }}
    .sidebar-stat .value .of {{
        font-size: 0.85rem;
        font-weight: 500;
        color: #5B6B85;
    }}

    /* ---- Brand mark ---- */
    .brand-row {{
        display: flex;
        align-items: center;
        gap: 11px;
        margin-bottom: 5px;
    }}
    .brand-mark {{
        width: 34px;
        height: 34px;
        background: linear-gradient(135deg, {INDIGO}, #7C73F0);
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: white;
        font-size: 16px;
        box-shadow: 0 2px 10px rgba(79, 70, 229, 0.4);
    }}
    .brand-name {{
        font-weight: 700;
        font-size: 1.12rem;
        color: white;
        letter-spacing: -0.01em;
    }}

    /* ---- Footer ---- */
    .footer {{
        text-align: center;
        color: {MUTED};
        font-size: 0.82rem;
        padding-top: 1.8rem;
        border-top: 1px solid {BORDER};
        margin-top: 3rem;
    }}

    /* ---- Native Streamlit sidebar toggle ----
       We deliberately leave Streamlit's own built-in collapse/expand arrow
       alone (just keep the header from collapsing to zero height so it
       stays clickable). Our own single "Menu" button below handles the
       guaranteed, good-looking version of this control. ---- */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        min-height: 48px !important;
    }}

    /* ---- Our single custom "Menu" button (mobile/tablet only) ---- */
    .menu-fallback-btn button {{
        background-color: {INDIGO} !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4) !important;
        padding: 0.5rem 1.1rem !important;
        animation: menuPulse 2.2s ease-in-out infinite;
    }}
    .menu-fallback-btn button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.5) !important;
        animation: none;
    }}
    @keyframes menuPulse {{
        0%, 100% {{ box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4); }}
        50% {{ box-shadow: 0 4px 22px rgba(79, 70, 229, 0.85); }}
    }}

    /* This custom button is only meant for small screens — hide it on desktop,
       where the sidebar is open by default and Streamlit's native arrow
       (top-left, small and unobtrusive) is enough to collapse/reopen it. */
    @media (min-width: 769px) {{
        .menu-fallback-btn {{ display: none !important; }}
    }}

    /* ---- Responsive system: tablet ---- */
    @media (max-width: 1024px) {{
        .block-container {{ max-width: 100%; padding-left: 1.4rem; padding-right: 1.4rem; }}
        .hero {{ padding: 2rem 1.8rem; }}
        div[data-testid="stMetric"] {{ padding: 1rem 1.1rem; }}
    }}

    /* ---- Responsive system: mobile ---- */
    @media (max-width: 768px) {{
        .hero {{ padding: 1.6rem 1.3rem; border-radius: 16px; margin-bottom: 1.5rem; }}
        .hero h1 {{ font-size: 1.45rem !important; line-height: 1.25 !important; }}
        .hero p {{ font-size: 0.88rem; line-height: 1.5; }}
        .hero .eyebrow {{ font-size: 0.64rem; }}

        .block-container {{ padding-left: 0.9rem; padding-right: 0.9rem; padding-top: 1rem; }}

        .section-label {{ margin-top: 2rem; gap: 8px; }}
        .section-label h2 {{ font-size: 1.1rem !important; }}
        .section-label .num {{ font-size: 0.65rem; padding: 1px 6px; }}

        div[data-testid="stMetric"] {{ padding: 0.85rem 1rem; }}
        div[data-testid="stMetricValue"] {{ font-size: 1.3rem !important; }}

        .stTabs [data-baseweb="tab"] {{ padding: 9px 12px; font-size: 0.82rem; }}

        .result-panel {{ padding: 1rem 1.2rem; }}
        .result-panel .value {{ font-size: 1.5rem; }}

        .stButton > button, .stDownloadButton > button {{
            width: 100%;
            padding: 0.65rem 1rem;
        }}
    }}

    /* ---- Responsive system: very small phones ---- */
    @media (max-width: 480px) {{
        .hero h1 {{ font-size: 1.25rem !important; }}
        .brand-name {{ font-size: 1rem; }}
        div[data-testid="column"] {{ min-width: 100% !important; }}
    }}
</style>
""", unsafe_allow_html=True)


def section_header(number: str, title: str):
    st.markdown(f"""
        <div class="section-label">
            <div class="bar"></div>
            <span class="num">{number}</span>
            <h2>{title}</h2>
        </div>
    """, unsafe_allow_html=True)


# ============================================================
# MATPLOTLIB GLOBAL THEME (so all charts look consistent + clean)
# ============================================================
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "axes.edgecolor": BORDER,
    "axes.labelcolor": SLATE,
    "axes.titlecolor": NAVY,
    "axes.titleweight": "bold",
    "axes.titlesize": 13,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "grid.color": "#F1F5F9",
    "axes.grid": True,
    "axes.grid.axis": "y",
})

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
        <div class="brand-row">
            <div class="brand-mark">◆</div>
            <div class="brand-name">Sales Intelligence</div>
        </div>
    """, unsafe_allow_html=True)
    st.caption("AI-powered analytics for retail sales data")

    st.divider()
    st.markdown('<div class="sidebar-eyebrow">DATA SOURCE</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

    use_sample = uploaded_file is None
    if use_sample:
        st.markdown(
            '<span class="badge indigo" style="background-color:#1A2436;color:#A5B4FC;border:1px solid #2D3B52;">● Using sample dataset</span>',
            unsafe_allow_html=True
        )

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# Resolve the sample CSV path relative to THIS script's location,
# so it works no matter which folder you run `streamlit run` from.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_CSV_PATH = os.path.join(SCRIPT_DIR, "..", "data", "sales_data.csv")

if uploaded_file is not None:
    df_raw = load_data(uploaded_file)
elif os.path.exists(SAMPLE_CSV_PATH):
    df_raw = load_data(SAMPLE_CSV_PATH)
else:
    st.error(
        f"Sample data file not found at `{SAMPLE_CSV_PATH}`. "
        "Please upload a CSV file using the sidebar, or make sure "
        "`sales_data.csv` exists inside the `data` folder."
    )
    st.stop()

# ============================================================
# CLEANING (flexible — works on any CSV)
# ============================================================
df = df_raw.copy()
initial_rows = df.shape[0]
duplicates_removed = df.duplicated().sum()
df = df.drop_duplicates()
missing_before = int(df.isnull().sum().sum())

for col in df.columns:
    if df[col].isnull().sum() > 0:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            mode_vals = df[col].mode()
            if len(mode_vals) > 0:
                df[col] = df[col].fillna(mode_vals[0])

numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = [c for c in df.columns if c not in numeric_cols]

date_col = None
for c in df.columns:
    if "date" in c.lower():
        try:
            df[c] = pd.to_datetime(df[c])
            date_col = c
            break
        except Exception:
            pass

# ============================================================
# SIDEBAR FILTERS
# ============================================================
with st.sidebar:
    st.divider()
    st.markdown('<div class="sidebar-eyebrow">FILTERS</div>', unsafe_allow_html=True)

    filtered_df = df.copy()
    filter_candidates = [c for c in categorical_cols if 1 < df[c].nunique() <= 15]

    if filter_candidates:
        for fc in filter_candidates[:3]:
            options = sorted(df[fc].dropna().unique().tolist())
            selected = st.multiselect(fc, options, default=options)
            if selected:
                filtered_df = filtered_df[filtered_df[fc].isin(selected)]
    else:
        st.caption("No filterable columns found.")

    st.divider()
    pct = int(100 * filtered_df.shape[0] / df.shape[0]) if df.shape[0] else 0
    st.markdown(f"""
        <div class="sidebar-stat">
            <div class="label">ROWS IN VIEW</div>
            <div class="value">{filtered_df.shape[0]:,} <span class="of">/ {df.shape[0]:,} ({pct}%)</span></div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# GUARANTEED SIDEBAR REOPEN BUTTON
# (Always works, regardless of Streamlit version/internal DOM names)
# ============================================================
menu_col, _ = st.columns([1, 8])
with menu_col:
    st.markdown('<div class="menu-fallback-btn">', unsafe_allow_html=True)
    menu_clicked = st.button("☰  Menu", key="open_sidebar_btn", help="Open the sidebar (upload data & filters)")
    st.markdown('</div>', unsafe_allow_html=True)

if menu_clicked:
    st.markdown("""
        <script>
            const selectors = [
                'button[data-testid="stExpandSidebarButton"]',
                'button[data-testid="stSidebarCollapsedControl"]',
                '[data-testid="stSidebarCollapsedControl"] button',
                '[data-testid="collapsedControl"] button',
                '[data-testid="collapsedControl"]'
            ];
            for (const sel of selectors) {
                const el = window.parent.document.querySelector(sel);
                if (el) { el.click(); break; }
            }
        </script>
    """, unsafe_allow_html=True)

st.markdown(
    '<p class="menu-fallback-btn" style="font-size:0.82rem;color:#64748B;margin-top:-0.4rem;">'
    'Tap <strong>☰ Menu</strong> to open data upload &amp; filters.</p>',
    unsafe_allow_html=True
)

# ============================================================
# HERO HEADER
# ============================================================
st.markdown("""
    <div class="hero">
        <div class="eyebrow"><span class="dot"></span>SALES ANALYTICS · MACHINE LEARNING</div>
        <h1>Sales Intelligence Platform</h1>
        <p>Upload any sales dataset, clean it automatically, explore it visually,
        and forecast outcomes with a live AI model — no setup required.</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 1 — DATA OVERVIEW
# ============================================================
section_header("01", "Data Overview & Cleaning")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rows", f"{initial_rows:,}")
col2.metric("Duplicates Removed", int(duplicates_removed))
col3.metric("Missing Values Fixed", missing_before)
col4.metric("Columns", df.shape[1])

with st.expander("View cleaned data"):
    st.dataframe(filtered_df.head(10), use_container_width=True)

st.download_button(
    "↓  Download cleaned data (CSV)",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="cleaned_data.csv",
    mime="text/csv"
)

# ============================================================
# SECTION 2 — VISUAL EXPLORATION
# ============================================================
section_header("02", "Visual Exploration")

if filtered_df.empty:
    st.warning("No data matches the current filters. Adjust filters in the sidebar.")
else:
    tab_labels = []
    if categorical_cols and numeric_cols:
        tab_labels.append("Category Breakdown")
    if date_col and numeric_cols:
        tab_labels.append("Trend Over Time")
    if len(numeric_cols) > 1:
        tab_labels.append("Correlation")
    if numeric_cols:
        tab_labels.append("Distribution")

    if tab_labels:
        tabs = st.tabs(tab_labels)
        idx = 0

        if "Category Breakdown" in tab_labels:
            with tabs[idx]:
                # Exclude columns that look like unique identifiers (too many unique values to group meaningfully)
                sensible_group_cols = [c for c in categorical_cols if df[c].nunique() <= max(20, int(len(df) * 0.5))]
                if not sensible_group_cols:
                    sensible_group_cols = categorical_cols

                c1, c2 = st.columns(2)
                cat_col = c1.selectbox("Group by", sensible_group_cols, key="cat_select")
                val_col = c2.selectbox("Measure", numeric_cols, key="val_select")

                avg_signals = ["age", "score", "rating", "price", "pct", "percent", "ratio", "years", "hours"]
                use_average = any(k in val_col.lower() for k in avg_signals)
                agg_label = "Average" if use_average else "Total"

                if use_average:
                    grouped = filtered_df.groupby(cat_col)[val_col].mean().sort_values(ascending=False)
                else:
                    grouped = filtered_df.groupby(cat_col)[val_col].sum().sort_values(ascending=False)

                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(grouped.index.astype(str), grouped.values, color=INDIGO, width=0.6)
                ax.set_title(f"{agg_label} {val_col} by {cat_col}", pad=12)
                ax.set_ylabel(val_col)
                plt.xticks(rotation=25, ha="right")
                fig.tight_layout()
                st.pyplot(fig)
            idx += 1

        if "Trend Over Time" in tab_labels:
            with tabs[idx]:
                trend_val = st.selectbox("Measure over time", numeric_cols, key="trend_select")

                # Decide aggregation: averages make more sense for attributes like
                # age, score, rating, price, percentage; sums make sense for
                # quantities like sales, revenue, quantity, count.
                avg_signals = ["age", "score", "rating", "price", "pct", "percent", "ratio", "years", "hours"]
                use_average = any(k in trend_val.lower() for k in avg_signals)
                agg_label = "Average" if use_average else "Total"

                if use_average:
                    trend_data = filtered_df.groupby(date_col)[trend_val].mean().sort_index()
                else:
                    trend_data = filtered_df.groupby(date_col)[trend_val].sum().sort_index()

                fig, ax = plt.subplots(figsize=(9, 4))
                ax.plot(trend_data.index, trend_data.values, color=EMERALD, linewidth=2)
                ax.fill_between(trend_data.index, trend_data.values, color=EMERALD, alpha=0.08)
                ax.set_title(f"{agg_label} {trend_val} Over Time", pad=12)
                ax.set_ylabel(trend_val)
                fig.tight_layout()
                st.pyplot(fig)
            idx += 1

        if "Correlation" in tab_labels:
            with tabs[idx]:
                fig, ax = plt.subplots(figsize=(7, 5))
                custom_cmap = sns.light_palette(INDIGO, as_cmap=True)
                sns.heatmap(filtered_df[numeric_cols].corr(), annot=True, cmap="coolwarm",
                            fmt=".2f", ax=ax, linewidths=0.5, linecolor="white", cbar_kws={"shrink": 0.8})
                ax.set_title("Correlation Matrix", pad=12)
                fig.tight_layout()
                st.pyplot(fig)
            idx += 1

        if "Distribution" in tab_labels:
            with tabs[idx]:
                dist_col = st.selectbox("Column", numeric_cols, key="dist_select")
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(filtered_df[dist_col].dropna(), bins=20, color=AMBER, edgecolor="white", linewidth=0.6)
                ax.set_title(f"Distribution of {dist_col}", pad=12)
                fig.tight_layout()
                st.pyplot(fig)

# ============================================================
# SECTION 3 — AI PREDICTOR
# ============================================================
section_header("03", "AI Predictor")

if len(numeric_cols) < 2:
    st.warning("Need at least 2 numeric columns to train a prediction model.")
else:
    likely_targets = [c for c in numeric_cols if any(k in c.lower() for k in ["total", "sales", "amount", "price", "revenue"])]
    default_target = likely_targets[0] if likely_targets else numeric_cols[-1]
    default_index = numeric_cols.index(default_target)

    target_col = st.selectbox(
        "What do you want to predict?",
        numeric_cols,
        index=default_index,
        help="Pick a column that is logically influenced by the others — predicting an unrelated column (like an ID) gives a poor model."
    )
    feature_candidates = [c for c in numeric_cols if c != target_col]

    if filtered_df.shape[0] < 20:
        st.warning("Not enough rows (need at least 20) to train a reliable model with current filters.")
    else:
        X = filtered_df[feature_candidates]
        y = filtered_df[target_col]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        m1, m2, m3 = st.columns(3)
        m1.metric("R² Score", f"{r2:.3f}")
        m2.metric("Mean Absolute Error", f"{mae:,.2f}")
        quality = "Excellent" if r2 > 0.85 else "Good" if r2 > 0.6 else "Weak" if r2 > 0.3 else "Poor"
        m3.metric("Model Quality", quality)

        if r2 < 0.3:
            st.warning(
                f"R² is low ({r2:.2f}) — the selected features don't explain '{target_col}' well. "
                "Try a different target column, ideally one logically related to the available features."
            )

        st.markdown("#### Try a live prediction")
        input_values = {}
        input_cols = st.columns(len(feature_candidates))
        for i, feature in enumerate(feature_candidates):
            max_val = float(filtered_df[feature].max())
            mean_val = float(filtered_df[feature].mean())
            input_values[feature] = input_cols[i].number_input(
                feature, min_value=0.0, max_value=max_val * 2 if max_val > 0 else 100.0, value=mean_val
            )

        if st.button("Predict", type="primary"):
            input_df = pd.DataFrame([input_values])
            prediction = model.predict(input_df)[0]
            st.markdown(f"""
                <div class="result-panel">
                    <div class="label">Predicted {target_col}</div>
                    <div class="value">{prediction:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("#### What drives this prediction?")
        importance_df = pd.DataFrame({
            "Feature": feature_candidates,
            "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=False)

        fig, ax = plt.subplots(figsize=(7, max(2, len(feature_candidates) * 0.5)))
        ax.barh(importance_df["Feature"], importance_df["Importance"], color=INDIGO, height=0.55)
        ax.set_xlabel("Importance")
        ax.invert_yaxis()
        fig.tight_layout()
        st.pyplot(fig)

        results_df = X_test.copy()
        results_df["Actual"] = y_test.values
        results_df["Predicted"] = preds
        st.download_button(
            "↓  Download test predictions (CSV)",
            data=results_df.to_csv(index=False).encode("utf-8"),
            file_name="predictions.csv",
            mime="text/csv"
        )

st.markdown("""
    <div class="footer">
        Sales Intelligence Platform · Built with Python, Pandas, scikit-learn &amp; Streamlit
    </div>
""", unsafe_allow_html=True)
