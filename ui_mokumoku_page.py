# ui_mokumoku_page.py
import streamlit as st
import streamlit.components.v1 as components

# 他のページと同じシグネチャにしておく（members, save_members は使わない）
def render_mokumoku_page(members, save_members) -> None:
    st.title("もくもく会")

    st.write(
        "桃下村塾オンラインもくもく会用のワークスペースです。"
        "下の画面がうまく表示されない場合は、下のリンクから別タブで開いてください。"
    )

    # 外部サイトを iframe で埋め込み（ブラウザ側で許可されていれば表示される）
    components.iframe(
        "https://online-workspace-1c2a4.web.app/",
        height=800,
        scrolling=True,
    )

    # 念のため別タブで開けるリンクも用意
    st.markdown(
        "[🔗 別タブでオンラインもくもく会を開く](https://online-workspace-1c2a4.web.app/)"
    )
