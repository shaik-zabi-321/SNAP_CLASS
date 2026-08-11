import streamlit as st


def header_home():
    st.markdown("""
        <div style="display:flex; align-items:center; gap:14px; padding:10px 0 24px 0; border-bottom:1px solid #e8ddc9; margin-bottom:32px;">
            <div style="height:52px; width:52px; border-radius:12px; background:#d97b3f; display:flex; align-items:center; justify-content:center;">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 12a3 3 0 1 0 6 0a3 3 0 1 0 -6 0"></path>
                    <path d="M3 12a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"></path>
                    <path d="M12 3v2"></path>
                    <path d="M12 19v2"></path>
                </svg>
            </div>
            <div>
                <p style="margin:0; font-size:22px; font-weight:700; color:#2d2013;">AttendEase</p>
                <p style="margin:0; font-size:13px; color:#8a7862;">Face and voice attendance system</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
