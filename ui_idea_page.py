# ui_idea_page.py
import streamlit as st

def render_idea_page():
    left, main, right = st.columns([0.2, 1.0, 0.2])
    with main:
        st.header("アイデア / Tokason Idea Chat")
        st.caption("桃下村塾用のアイデア出しチャット（ChatGPT）を別タブで開きます。")

        st.markdown(
            """
            <a href="https://chatgpt.com/g/g-692c67208a208191b3e37acb81d63c27-tokasonideachat"
               target="_blank"
               style="text-decoration:none;">
                <button style="
                    padding: 12px 20px;
                    font-size: 16px;
                    background: #6699ff;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                ">
                    Tokason Idea Chat を開く
                </button>
            </a>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.write("※ ボタンを押すと ChatGPT の画面が新しいタブで開きます。")
        st.write("※ 桃下村塾の企画・開発・学びのアイデア出しに自由に使ってください。")
