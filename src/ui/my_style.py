import streamlit as st


def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        .stApp {
            background-color: #fdfaf5 !important;
        }

        html, body, [class*="css"], p, label, div, span {
            font-family: 'Poppins', sans-serif !important;
            color: #2d2013 !important;
        }

        h1 {
            font-size: 2.4rem !important;
            font-weight: 700 !important;
            color: #2d2013 !important;
        }

        h2, h3 {
            color: #8a7862 !important;
            font-weight: 600 !important;
        }

        div.stButton > button {
            background-color: #d97b3f !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.7em 1.5em !important;
            width: 100% !important;
            transition: all 0.2s ease-in-out !important;
        }

        div.stButton > button:hover {
            background-color: #c1652c !important;
            transform: translateY(-1px) !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #f5efe4 !important;
            border-right: 1px solid #e8ddc9 !important;
        }

        div[data-baseweb="input"] > div {
            background-color: #ffffff !important;
            border-radius: 8px !important;
            border: 1px solid #e8ddc9 !important;
        }
        </style>
    """, unsafe_allow_html=True)
