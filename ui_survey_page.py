import streamlit as st
from streamlit.components.v1 import html


FORM_URL = (
    "https://docs.google.com/forms/d/e/1FAIpQLSeH-0LrZNsEyoeYMguo8IGosRTslTG3mB1nYrA3NcT7RjXF-Q/viewform?usp=header"
)


def render_survey_page():
    st.header("アンケート")
    st.caption("桃下村塾に関するアンケートフォームです。")

    st.link_button("別タブで開く", FORM_URL, type="secondary")

    html(
        f"""
        <div style="max-width: 1200px; margin: 1rem auto;">
            <iframe
                src="{FORM_URL}"
                style="width: 100%; height: 900px; border: 0;"
                allowfullscreen
                loading="lazy"
            ></iframe>
        </div>
        """,
        height=940,
    )
