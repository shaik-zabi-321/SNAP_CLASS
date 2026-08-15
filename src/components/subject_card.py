import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    html = (
        "<div style=\"background:#FFF6EC; border-left:8px solid #58B92E; padding:22px 25px; "
        "border-radius:20px; border:1px solid #FFE0B8; box-shadow:0 2px 0 #FFE0B8; margin-bottom:18px;\">"
        f"<h3 style=\"margin:0; color:#2F6B14; font-family:'Baloo 2', sans-serif; font-weight:800; font-size:1.4rem;\">{name}</h3>"
        "<p style=\"color:#5F5E5A; font-family:'Outfit', sans-serif; margin:8px 0 12px;\">"
        f"Code: <span style=\"background:#FFF0D6; color:#B36B00; padding:2px 10px; border-radius:8px; font-weight:600;\">{code}</span>"
        f" &nbsp;|&nbsp; Section: {section}</p>"
    )

    if stats:
        html += "<div style=\"display:flex; gap:8px; flex-wrap:wrap;\">"
        for icon, label, value in stats:
            html += (
                "<div style=\"background:#EAF7E0; color:#2F6B14; padding:5px 12px; "
                "border-radius:12px; font-size:0.85rem; font-family:'Outfit', sans-serif;\">"
                f"{icon} <b>{value}</b> {label}</div>"
            )
        html += "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
