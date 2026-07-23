# ============================================
# app.py - Stock Direction Predictor Pro
# ULTRA PREMIUM ENTERPRISE EDITION v6.0
# Corporate-Grade UI | Premium Design | Error-Proof
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================
# HELPER FUNCTION: Safe Scalar Extraction
# ============================================
def safe_float(value, default=0.0):
    """Safely convert pandas Series/DataFrame to float"""
    try:
        if hasattr(value, 'item'):
            value = value.item()
        elif hasattr(value, 'values'):
            if len(value.values) > 0:
                value = value.values[0]
            else:
                return default
        if pd.isna(value):
            return default
        return float(value)
    except:
        return default

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Stock Predictor Pro | Enterprise",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ULTRA PREMIUM ENTERPRISE CSS
# ============================================
st.markdown("""
<style>
    /* ===== IMPORT PREMIUM FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=Playfair+Display:wght@700;900&display=swap');
    
    /* ===== GLOBAL RESET ===== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* ===== MAIN BACKGROUND ===== */
    .stApp {
        background: #060b18;
        background-image: 
            radial-gradient(ellipse at 5% 20%, rgba(139, 92, 246, 0.05) 0%, transparent 50%),
            radial-gradient(ellipse at 95% 80%, rgba(52, 211, 153, 0.03) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(255, 255, 255, 0.01) 0%, transparent 70%);
    }
    
    /* ==========================================
       SIDEBAR - ULTRA PREMIUM DESIGN
       ========================================== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c1322 0%, #0f1a2e 40%, #0a1528 100%) !important;
        border-right: 1px solid rgba(139, 92, 246, 0.08) !important;
        box-shadow: 4px 0 60px rgba(0, 0, 0, 0.5) !important;
    }
    
    section[data-testid="stSidebar"] .css-1d391kg {
        background: transparent !important;
    }
    
    /* Sidebar Brand Header */
    .sidebar-brand {
        text-align: center;
        padding: 28px 0 20px 0;
        border-bottom: 1px solid rgba(139, 92, 246, 0.06);
        margin-bottom: 20px;
    }
    
    .sidebar-brand .logo-icon {
        font-size: 32px;
        margin-bottom: 4px;
    }
    
    .sidebar-brand .brand-name {
        font-size: 22px;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 60%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    
    .sidebar-brand .brand-sub {
        font-size: 9px;
        font-weight: 600;
        color: #4b5563;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        margin-top: 2px;
        -webkit-text-fill-color: #4b5563;
    }
    
    .sidebar-brand .brand-line {
        width: 40px;
        height: 2px;
        background: linear-gradient(90deg, #8b5cf6, #6d28d9);
        margin: 10px auto 0 auto;
        border-radius: 2px;
        opacity: 0.5;
    }
    
    /* Sidebar Section Labels */
    .sidebar-label {
        color: #6b7280;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        padding: 12px 0 8px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        margin-bottom: 12px;
    }
    
    /* Sidebar Input Labels */
    .sidebar-input-label {
        color: #9ca3af;
        font-size: 12px;
        font-weight: 500;
        letter-spacing: 0.04em;
        margin-bottom: 6px;
    }
    
    /* Sidebar Input Styling */
    section[data-testid="stSidebar"] .stTextInput input {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 10px !important;
        color: #e5e7eb !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput input:focus {
        border-color: rgba(139, 92, 246, 0.3) !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.08) !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput input::placeholder {
        color: #4b5563;
    }
    
    /* Sidebar Date Inputs */
    section[data-testid="stSidebar"] .stDateInput input {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 10px !important;
        color: #e5e7eb !important;
        padding: 8px 12px !important;
        font-size: 13px !important;
    }
    
    section[data-testid="stSidebar"] .stDateInput input:focus {
        border-color: rgba(139, 92, 246, 0.3) !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.08) !important;
    }
    
    /* Sidebar Checkboxes */
    section[data-testid="stSidebar"] .stCheckbox label {
        color: #9ca3af !important;
        font-size: 13px !important;
        font-weight: 400 !important;
    }
    
    section[data-testid="stSidebar"] .stCheckbox label span {
        color: #9ca3af !important;
    }
    
    section[data-testid="stSidebar"] .stCheckbox input:checked + label {
        color: #e5e7eb !important;
    }
    
    /* Sidebar About Box */
    .sidebar-about {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 14px;
        padding: 18px 20px;
        margin: 8px 0;
        transition: all 0.3s ease;
    }
    
    .sidebar-about:hover {
        background: rgba(255, 255, 255, 0.03);
        border-color: rgba(139, 92, 246, 0.08);
    }
    
    .sidebar-about .title {
        color: #e5e7eb;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.04em;
        margin-bottom: 4px;
    }
    
    .sidebar-about .desc {
        color: #6b7280;
        font-size: 11px;
        line-height: 1.6;
        margin-top: 4px;
    }
    
    .sidebar-about .stats {
        color: #4b5563;
        font-size: 10px;
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    .sidebar-about .stats span {
        color: #8b5cf6;
        font-weight: 600;
    }
    
    /* Sidebar Divider */
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.08), transparent);
        margin: 16px 0;
    }
    
    /* Sidebar Caption */
    .sidebar-caption {
        text-align: center;
        color: #374151;
        font-size: 10px;
        letter-spacing: 0.08em;
        padding: 12px 0 4px 0;
    }
    
    /* ==========================================
       MAIN CONTENT - ENTERPRISE DESIGN
       ========================================== */
    
    /* Main Title */
    .main-title {
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 40%, #8b5cf6 80%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
        line-height: 1.1;
    }
    
    .main-title .accent {
        background: linear-gradient(135deg, #34d399, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .main-subtitle {
        color: #6b7280;
        font-size: 15px;
        font-weight: 400;
        letter-spacing: 0.04em;
        margin-top: 4px;
    }
    
    .main-subtitle .highlight-text {
        color: #8b5cf6;
        font-weight: 500;
        -webkit-text-fill-color: #8b5cf6;
    }
    
    /* Enterprise Badge */
    .enterprise-badge {
        display: inline-block;
        background: rgba(139, 92, 246, 0.08);
        border: 1px solid rgba(139, 92, 246, 0.12);
        border-radius: 30px;
        padding: 2px 16px;
        font-size: 9px;
        font-weight: 600;
        color: #8b5cf6;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-left: 12px;
        -webkit-text-fill-color: #8b5cf6;
        vertical-align: middle;
    }
    
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.12), rgba(52, 211, 153, 0.08), transparent);
        margin: 24px 0 28px 0;
    }
    
    /* Section Title */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.01em;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .section-title .highlight {
        background: linear-gradient(135deg, #a78bfa, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .section-title .badge {
        background: rgba(139, 92, 246, 0.08);
        border: 1px solid rgba(139, 92, 246, 0.1);
        border-radius: 30px;
        padding: 1px 12px;
        font-size: 8px;
        font-weight: 600;
        color: #8b5cf6;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        -webkit-text-fill-color: #8b5cf6;
    }
    
    /* ===== METRIC CARDS - ENTERPRISE ===== */
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 18px;
        padding: 22px 16px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
        cursor: default;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #8b5cf6, #6d28d9, #8b5cf6);
        background-size: 200% 100%;
        opacity: 0;
        transition: opacity 0.5s ease;
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(139, 92, 246, 0.12);
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-card .label {
        color: #6b7280;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 6px;
    }
    
    .metric-card .value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 4px 0;
    }
    
    .metric-card .sub {
        color: #4b5563;
        font-size: 11px;
        font-weight: 400;
        margin-top: 2px;
    }
    
    .metric-card .change-positive {
        color: #34d399;
        font-weight: 600;
        font-size: 12px;
    }
    
    .metric-card .change-negative {
        color: #f87171;
        font-weight: 600;
        font-size: 12px;
    }
    
    /* ===== PREDICTION CARDS ===== */
    .prediction-up {
        background: linear-gradient(145deg, rgba(52, 211, 153, 0.06), rgba(16, 185, 129, 0.01));
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(52, 211, 153, 0.1);
        border-radius: 24px;
        padding: 40px 32px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.5s ease;
    }
    
    .prediction-up:hover {
        border-color: rgba(52, 211, 153, 0.25);
        transform: translateY(-2px);
        box-shadow: 0 12px 48px rgba(52, 211, 153, 0.05);
    }
    
    .prediction-up::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -30%;
        width: 60%;
        height: 100%;
        background: radial-gradient(circle, rgba(52, 211, 153, 0.04) 0%, transparent 70%);
        animation: pulse-glow 4s ease-in-out infinite;
    }
    
    .prediction-down {
        background: linear-gradient(145deg, rgba(248, 113, 113, 0.06), rgba(239, 68, 68, 0.01));
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(248, 113, 113, 0.1);
        border-radius: 24px;
        padding: 40px 32px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.5s ease;
    }
    
    .prediction-down:hover {
        border-color: rgba(248, 113, 113, 0.25);
        transform: translateY(-2px);
        box-shadow: 0 12px 48px rgba(248, 113, 113, 0.05);
    }
    
    .prediction-down::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -30%;
        width: 60%;
        height: 100%;
        background: radial-gradient(circle, rgba(248, 113, 113, 0.04) 0%, transparent 70%);
        animation: pulse-glow 4s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { transform: scale(1); opacity: 0.3; }
        50% { transform: scale(1.2); opacity: 0.6; }
    }
    
    .prediction-up .icon, .prediction-down .icon {
        font-size: 56px;
        position: relative;
        z-index: 1;
        display: block;
        margin-bottom: 4px;
    }
    
    .prediction-up h1 {
        font-size: 48px;
        font-weight: 900;
        margin: 4px 0;
        letter-spacing: -0.03em;
        position: relative;
        z-index: 1;
        color: #34d399;
        font-family: 'Inter', sans-serif;
    }
    
    .prediction-down h1 {
        font-size: 48px;
        font-weight: 900;
        margin: 4px 0;
        letter-spacing: -0.03em;
        position: relative;
        z-index: 1;
        color: #f87171;
        font-family: 'Inter', sans-serif;
    }
    
    .prediction-up .subtitle, .prediction-down .subtitle {
        font-size: 14px;
        font-weight: 400;
        opacity: 0.6;
        margin: 4px 0;
        position: relative;
        z-index: 1;
        color: #9ca3af;
        letter-spacing: 0.02em;
    }
    
    /* ===== CONFIDENCE CONTAINER ===== */
    .confidence-container {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 18px;
        padding: 22px 24px;
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .confidence-container:hover {
        border-color: rgba(139, 92, 246, 0.08);
    }
    
    .confidence-container .label {
        color: #6b7280;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
    
    .confidence-container .value {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 4px 0;
    }
    
    .confidence-bar-bg {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.04);
        border-radius: 4px;
        overflow: hidden;
        margin-top: 8px;
    }
    
    .confidence-bar-fill {
        height: 100%;
        border-radius: 4px;
        background: linear-gradient(90deg, #8b5cf6, #6d28d9);
        transition: width 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.1);
    }
    
    .confidence-detail {
        color: #4b5563;
        font-size: 11px;
        margin-top: 10px;
        letter-spacing: 0.02em;
    }
    
    /* ===== INFO BOX ===== */
    .info-box {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-left: 3px solid #8b5cf6;
        border-radius: 14px;
        padding: 18px 24px;
        margin: 10px 0;
        color: #d1d5db;
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        background: rgba(255, 255, 255, 0.03);
    }
    
    /* ===== FEATURE IMPORTANCE ===== */
    .feature-box {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 16px;
        padding: 18px 22px;
        transition: all 0.3s ease;
    }
    
    .feature-box:hover {
        border-color: rgba(139, 92, 246, 0.06);
    }
    
    .feature-box .header {
        color: #6b7280;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 12px;
    }
    
    .feature-item {
        margin: 6px 0;
    }
    
    .feature-item .row {
        display: flex;
        justify-content: space-between;
        color: #d1d5db;
        font-size: 12px;
    }
    
    .feature-item .row .name {
        color: #9ca3af;
    }
    
    .feature-item .row .value {
        color: #6b7280;
        font-weight: 500;
    }
    
    .feature-item .bar {
        width: 100%;
        height: 2px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 2px;
        margin-top: 3px;
        overflow: hidden;
    }
    
    .feature-item .bar .fill {
        height: 100%;
        border-radius: 2px;
        background: linear-gradient(90deg, #8b5cf6, #6d28d9);
        transition: width 0.8s ease;
    }
    
    /* ===== PERFORMANCE BADGE ===== */
    .perf-badge {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 14px;
        padding: 14px 18px;
        margin-top: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .perf-badge .label {
        color: #6b7280;
        font-size: 11px;
    }
    
    .perf-badge .value {
        color: #34d399;
        font-weight: 700;
        font-size: 15px;
    }
    
    .perf-badge .sub {
        color: #4b5563;
        font-size: 10px;
    }
    
    /* ===== DISCLAIMER ===== */
    .disclaimer {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(253, 203, 110, 0.04);
        border-left: 3px solid rgba(253, 203, 110, 0.12);
        border-radius: 14px;
        padding: 16px 24px;
        margin-top: 32px;
    }
    
    .disclaimer p {
        color: #6b7280;
        font-size: 12px;
        margin: 0;
        line-height: 1.6;
    }
    
    .disclaimer strong {
        color: #9ca3af;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        color: #2d3748;
        font-size: 11px;
        padding: 24px 0 8px 0;
        letter-spacing: 0.06em;
        border-top: 1px solid rgba(255, 255, 255, 0.02);
        margin-top: 32px;
    }
    
    .footer .brand {
        color: #4b5563;
        font-weight: 500;
    }
    
    .footer .brand .highlight {
        background: linear-gradient(135deg, #a78bfa, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    .footer .version {
        color: #2d3748;
        font-size: 10px;
    }
    
    /* ==========================================
       RESPONSIVE
       ========================================== */
    @media (max-width: 768px) {
        .main-title { font-size: 26px; }
        .metric-card .value { font-size: 20px; }
        .prediction-up h1, .prediction-down h1 { font-size: 32px; }
        .prediction-up .icon, .prediction-down .icon { font-size: 36px; }
        .prediction-up, .prediction-down { padding: 24px 16px; }
        .enterprise-badge { font-size: 7px; padding: 1px 10px; margin-left: 6px; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# EXACT FEATURE NAMES - LOCKED (DO NOT CHANGE)
# ============================================
EXPECTED_FEATURES = [
    'SMA_10', 'SMA_20', 'SMA_50',
    'Return_1d', 'Return_5d', 'Return_10d',
    'Volatility_10', 'Volatility_20',
    'High_Low_ratio', 'Close_Open_ratio',
    'Volume_Change', 'Volume_Ratio'
]

# ============================================
# LOAD TRAINED MODELS
# ============================================
@st.cache_resource
def load_models():
    try:
        model_path = 'models/best_model.pkl'
        scaler_path = 'models/scaler.pkl'
        features_path = 'models/feature_columns.pkl'
        
        if not os.path.exists(model_path):
            return None, None, None, "Model files not found"
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        feature_columns = joblib.load(features_path)
        
        return model, scaler, feature_columns, None
    except Exception as e:
        return None, None, None, str(e)

model, scaler, feature_columns, load_error = load_models()

# ============================================
# SIDEBAR - ULTRA PREMIUM ENTERPRISE
# ============================================
with st.sidebar:
    # Brand Header
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo-icon">🏢</div>
        <div class="brand-name">PRO</div>
        <div class="brand-sub">Enterprise Edition</div>
        <div class="brand-line"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stock Selection
    st.markdown('<div class="sidebar-label">📈 Portfolio</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-input-label">Symbol</div>', unsafe_allow_html=True)
    ticker = st.text_input("", "AAPL", label_visibility="collapsed").upper()
    st.caption("AAPL · MSFT · GOOGL · TSLA")
    
    st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-input-label">Date Range</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From", datetime.now() - timedelta(days=365), label_visibility="collapsed")
    with col2:
        end_date = st.date_input("To", datetime.now(), label_visibility="collapsed")
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Display Options
    st.markdown('<div class="sidebar-label">🎨 Display</div>', unsafe_allow_html=True)
    show_ma = st.checkbox("Moving Averages", True)
    show_confidence = st.checkbox("Confidence Analysis", True)
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # About Section
    st.markdown("""
    <div class="sidebar-about">
        <div class="title">About</div>
        <div class="desc">
            Predicts whether a stock will go <span style="color: #34d399;">UP</span> or <span style="color: #f87171;">DOWN</span> tomorrow using ensemble ML.
        </div>
        <div class="stats">
            <span>●</span> Random Forest &nbsp;·&nbsp; <span>●</span> 12 Indicators &nbsp;·&nbsp; <span>●</span> ~67% Accuracy
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-caption">⚡ v6.0 · Enterprise</div>', unsafe_allow_html=True)

# ============================================
# MAIN CONTENT
# ============================================
st.markdown("""
<div class="main-title">
    Stock Direction <span class="accent">Predictor</span>
    <span class="enterprise-badge">Enterprise</span>
</div>
<div class="main-subtitle">
    Institutional-grade machine learning for <span class="highlight-text">market direction</span> forecasting
</div>
<div class="custom-divider"></div>
""", unsafe_allow_html=True)

# ============================================
# FETCH STOCK DATA
# ============================================
@st.cache_data
def fetch_stock_data(ticker, start, end):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(start=start, end=end)
        if df.empty:
            return None, None
        info = stock.info
        company_info = {
            'name': info.get('longName', ticker),
            'sector': info.get('sector', 'N/A'),
            'pe_ratio': info.get('trailingPE', 0),
            'beta': info.get('beta', 0)
        }
        return df, company_info
    except:
        return None, None

with st.spinner(f"Loading {ticker} data..."):
    df, company_info = fetch_stock_data(ticker, start_date, end_date)

if df is None or df.empty:
    st.error(f"❌ Could not fetch data for {ticker}")
    st.stop()

# ============================================
# METRICS ROW
# ============================================
st.markdown('<div class="section-title">📊 <span class="highlight">Market Overview</span> <span class="badge">Live</span></div>', unsafe_allow_html=True)

current_price = float(df['Close'].iloc[-1])
prev_price = float(df['Close'].iloc[-2])
price_change = ((current_price - prev_price) / prev_price) * 100
volume = float(df['Volume'].iloc[-1])
avg_volume = float(df['Volume'].mean())
high_52w = float(df['High'].max())
low_52w = float(df['Low'].min())

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Current Price</div>
        <div class="value">${current_price:.2f}</div>
        <div class="{'change-positive' if price_change >= 0 else 'change-negative'}">
            {price_change:+.2f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Volume</div>
        <div class="value">{volume/1e6:.1f}M</div>
        <div class="sub">Avg {avg_volume/1e6:.1f}M</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">52-Week High</div>
        <div class="value" style="color: #34d399;">${high_52w:.2f}</div>
        <div class="sub">+{((high_52w - current_price)/current_price*100):.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">52-Week Low</div>
        <div class="value" style="color: #f87171;">${low_52w:.2f}</div>
        <div class="sub">-{((current_price - low_52w)/current_price*100):.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    pe_ratio = company_info.get('pe_ratio', 0)
    beta = company_info.get('beta', 0)
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Valuation</div>
        <div class="value">P/E {pe_ratio:.1f}</div>
        <div class="sub">Beta {beta:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================
# PRICE CHART
# ============================================
st.markdown(f'<div class="section-title">📉 <span class="highlight">{ticker}</span> Price Action</div>', unsafe_allow_html=True)

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.04,
    row_heights=[0.7, 0.3],
    subplot_titles=(f'{company_info.get("name", ticker)} · Daily Candles', 'Volume')
)

fig.add_trace(
    go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        name='Price',
        increasing_line_color='#34d399',
        decreasing_line_color='#f87171'
    ),
    row=1, col=1
)

if show_ma:
    ma20 = df['Close'].rolling(20).mean()
    ma50 = df['Close'].rolling(50).mean()
    ma200 = df['Close'].rolling(200).mean()
    
    fig.add_trace(go.Scatter(x=df.index, y=ma20, name='SMA 20', line=dict(color='#fbbf24', width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=ma50, name='SMA 50', line=dict(color='#a78bfa', width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=ma200, name='SMA 200', line=dict(color='#f472b6', width=1.5)), row=1, col=1)

colors = ['#34d399' if close >= open else '#f87171' for close, open in zip(df['Close'], df['Open'])]
fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color=colors, opacity=0.6), row=2, col=1)

fig.update_layout(
    height=550,
    template='plotly_dark',
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#6b7280', size=11)),
    hovermode='x unified',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=40, b=20)
)

fig.update_xaxes(gridcolor='rgba(255,255,255,0.02)')
fig.update_yaxes(gridcolor='rgba(255,255,255,0.02)')

st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================
# PREDICTION SECTION
# ============================================
st.markdown('<div class="section-title">🔮 <span class="highlight">Tomorrow\'s Prediction</span> <span class="badge">AI Powered</span></div>', unsafe_allow_html=True)

if model is None or scaler is None or feature_columns is None:
    st.error(f"❌ Model loading error: {load_error}")
    st.info("Please make sure all model files are in the 'models' folder.")
    st.stop()

try:
    # ==========================================
    # CREATE FEATURES - SAFE VERSION
    # ==========================================
    
    close_series = df['Close']
    high_series = df['High']
    low_series = df['Low']
    open_series = df['Open']
    volume_series = df['Volume']
    
    n = len(close_series)
    last_close = safe_float(close_series.iloc[-1])
    last_high = safe_float(high_series.iloc[-1])
    last_low = safe_float(low_series.iloc[-1])
    last_open = safe_float(open_series.iloc[-1])
    last_volume = safe_float(volume_series.iloc[-1])
    prev_close = safe_float(close_series.iloc[-2]) if n > 1 else last_close
    
    returns_values = close_series.pct_change().values
    
    feature_values = {}
    
    # 1. Moving Averages
    feature_values['SMA_10'] = safe_float(close_series.rolling(10).mean().iloc[-1]) if n >= 10 else safe_float(close_series.mean())
    feature_values['SMA_20'] = safe_float(close_series.rolling(20).mean().iloc[-1]) if n >= 20 else safe_float(close_series.mean())
    feature_values['SMA_50'] = safe_float(close_series.rolling(50).mean().iloc[-1]) if n >= 50 else safe_float(close_series.mean())
    
    # 2. Returns
    feature_values['Return_1d'] = safe_float(returns_values[-1]) if n > 1 else 0.0
    feature_values['Return_5d'] = safe_float(close_series.pct_change(5).iloc[-1]) if n > 5 else 0.0
    feature_values['Return_10d'] = safe_float(close_series.pct_change(10).iloc[-1]) if n > 10 else 0.0
    
    # 3. Volatility
    if n >= 10:
        vol_10 = np.std(returns_values[-10:]) if len(returns_values[-10:]) > 0 else 0.01
        feature_values['Volatility_10'] = safe_float(vol_10)
    else:
        feature_values['Volatility_10'] = 0.01
    
    if n >= 20:
        vol_20 = np.std(returns_values[-20:]) if len(returns_values[-20:]) > 0 else 0.01
        feature_values['Volatility_20'] = safe_float(vol_20)
    else:
        feature_values['Volatility_20'] = 0.01
    
    # 4. Ratios
    feature_values['High_Low_ratio'] = last_high / last_low if last_low != 0 else 1.0
    feature_values['Close_Open_ratio'] = last_close / last_open if last_open != 0 else 1.0
    
    # 5. Volume
    feature_values['Volume_Change'] = safe_float(volume_series.pct_change().iloc[-1]) if n > 1 else 0.0
    
    if n >= 20:
        volume_sma = np.mean(volume_series.values[-20:]) if len(volume_series.values[-20:]) > 0 else last_volume
    else:
        volume_sma = np.mean(volume_series.values) if len(volume_series.values) > 0 else 1.0
    
    feature_values['Volume_Ratio'] = last_volume / volume_sma if volume_sma != 0 else 1.0
    
    # 6. Extra features (for debugging)
    feature_values['Daily_Range'] = (last_high - last_low) / last_close if last_close != 0 else 0.01
    feature_values['Gap'] = (last_open - prev_close) / prev_close if prev_close != 0 else 0.0
    
    # Convert to DataFrame
    latest_df = pd.DataFrame([feature_values])
    
    # Check ALL features exist
    missing_features = []
    for col in EXPECTED_FEATURES:
        if col not in latest_df.columns:
            missing_features.append(col)
    
    if missing_features:
        st.error(f"❌ Missing features: {missing_features}")
        with st.expander("🔍 Debug Information"):
            st.write("**Features Created:**", list(feature_values.keys()))
            st.write("**Expected Features:**", EXPECTED_FEATURES)
        st.stop()
    
    # Select features in correct order
    latest_features = latest_df[EXPECTED_FEATURES].values.reshape(1, -1)
    latest_scaled = scaler.transform(latest_features)
    
    # ==========================================
    # MAKE PREDICTION
    # ==========================================
    prediction = model.predict(latest_scaled)[0]
    probabilities = model.predict_proba(latest_scaled)[0]
    confidence = probabilities[prediction]
    
    # ==========================================
    # DISPLAY PREDICTION
    # ==========================================
    col1, col2, col3 = st.columns([2, 1.2, 1])
    
    with col1:
        if prediction == 1:
            st.markdown("""
            <div class="prediction-up">
                <span class="icon">📈</span>
                <h1>UP</h1>
                <div class="subtitle">Stock is forecasted to rise tomorrow</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="prediction-down">
                <span class="icon">📉</span>
                <h1>DOWN</h1>
                <div class="subtitle">Stock is forecasted to decline tomorrow</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="confidence-container">
            <div class="label">Model Confidence</div>
            <div class="value">{confidence:.1%}</div>
            <div class="confidence-bar-bg">
                <div class="confidence-bar-fill" style="width: {confidence*100:.1f}%;"></div>
            </div>
            <div class="confidence-detail">Based on {n} days of data</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="confidence-container">
            <div class="label">Current Snapshot</div>
            <div style="margin-top: 10px;">
                <div style="color: #ffffff; font-size: 22px; font-weight: 700;">${last_close:.2f}</div>
                <div style="color: #6b7280; font-size: 12px;">{datetime.now().strftime('%B %d, %Y')}</div>
                <div style="margin-top: 14px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.03);">
                    <div style="display: flex; justify-content: space-between; color: #6b7280; font-size: 12px;">
                        <span>Range</span>
                        <span style="color: #d1d5db;">${last_low:.2f} - ${last_high:.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #6b7280; font-size: 12px; margin-top: 6px;">
                        <span>Volume</span>
                        <span style="color: #d1d5db;">{last_volume/1e6:.1f}M</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ==========================================
    # CONFIDENCE BREAKDOWN
    # ==========================================
    if show_confidence:
        st.markdown("---")
        st.markdown('<div class="section-title">📊 <span class="highlight">Confidence Analysis</span> <span class="badge">Probability</span></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            prob_down, prob_up = probabilities
            
            st.markdown(f"""
            <div class="info-box">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #34d399; font-weight: 600;">📈 UP Probability</span>
                    <span style="color: #ffffff; font-weight: 700; font-size: 18px;">{prob_up:.1%}</span>
                </div>
                <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.04); border-radius: 4px; overflow: hidden; margin-top: 8px;">
                    <div style="width: {prob_up*100:.1f}%; height: 100%; background: linear-gradient(90deg, #34d399, #10b981);"></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px;">
                    <span style="color: #f87171; font-weight: 600;">📉 DOWN Probability</span>
                    <span style="color: #ffffff; font-weight: 700; font-size: 18px;">{prob_down:.1%}</span>
                </div>
                <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.04); border-radius: 4px; overflow: hidden; margin-top: 8px;">
                    <div style="width: {prob_down*100:.1f}%; height: 100%; background: linear-gradient(90deg, #f87171, #ef4444);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                top_features = pd.DataFrame({
                    'Feature': EXPECTED_FEATURES,
                    'Importance': importances
                }).sort_values('Importance', ascending=False).head(5)
                
                st.markdown("""
                <div class="feature-box">
                    <div class="header">Top Predictive Indicators</div>
                """, unsafe_allow_html=True)
                
                for idx, row in top_features.iterrows():
                    st.markdown(f"""
                    <div class="feature-item">
                        <div class="row">
                            <span class="name">{row['Feature']}</span>
                            <span class="value">{row['Importance']:.1%}</span>
                        </div>
                        <div class="bar">
                            <div class="fill" style="width: {row['Importance']*100:.1f}%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Performance Badge
                st.markdown(f"""
                <div class="perf-badge">
                    <div>
                        <div class="label">Model Performance</div>
                        <div class="sub">Accuracy on test data</div>
                    </div>
                    <div>
                        <div class="value">~67%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Prediction Error: {str(e)}")
    st.info("💡 This could be due to insufficient historical data. Try using a longer date range (at least 200 days).")
    
    with st.expander("🔍 Debug Information"):
        st.write("**📊 Data Shape:**", df.shape)
        st.write("**📅 Date Range:**", df.index[0].strftime('%Y-%m-%d'), "to", df.index[-1].strftime('%Y-%m-%d'))
        st.write("**🔢 Expected Features:**", EXPECTED_FEATURES)
        
        if 'feature_values' in locals():
            st.write("**📋 Features Created:**", list(feature_values.keys()))
            missing = set(EXPECTED_FEATURES) - set(feature_values.keys())
            if missing:
                st.write("**❌ Missing Features:**", missing)

# ============================================
# DISCLAIMER & FOOTER
# ============================================
st.markdown("""
<div class="disclaimer">
    <p>
        <strong>⚠️ Disclaimer:</strong> This tool is for educational and informational purposes only. 
        Stock market predictions are inherently uncertain. Always conduct your own research before 
        making investment decisions.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <span class="brand"><span class="highlight">Stock Predictor Pro</span></span>
    <span class="version">· Enterprise Edition v6.0</span>
</div>
""", unsafe_allow_html=True)