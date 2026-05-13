import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Bebas+Neue&display=swap');
    .stApp { background-color: #07080d; color: white; }
    .main-title { font-family: 'Bebas Neue'; font-size: 88px; color: white; letter-spacing: .1em; margin: 0; }
    .header-lines { color: #FF10F0; letter-spacing: .4em; margin-bottom: 30px; text-transform: uppercase; border-top: 1px solid #2a2040; border-bottom: 1px solid #2a2040; padding: 10px 0; text-align: center; font-size: 14px; }
    .stat-card { background: #0d0e18; border: 1px solid #2a2040; padding: 16px; border-left: 3px solid #FF10F0; }
    .stat-label { color: #7060a0; font-size: 10px; text-transform: uppercase; }
    .stat-value { color: white; font-size: 18px; font-weight: 700; }
    .stButton button { background: transparent !important; border: 1px solid #FF10F0 !important; color: #FF10F0 !important; height: 50px; border-radius: 0; width: 100%; letter-spacing: 0.2em; }
    .stButton button:hover { background: rgba(255, 16, 240, 0.1) !important; box-shadow: 0 0 15px #FF10F0; }
    .log-box { background: #030407; border: 1px solid #1a1530; padding: 20px; font-family: 'Space Mono'; font-size: 12px; margin-top: 20px; }
    [data-testid="stSidebar"] { background: #0a0b14 !important; border-right: 1px solid #2a2040 !important; }
    </style>
    """, unsafe_allow_html=True)