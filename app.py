# app.py
import streamlit as st
from repository import load_members, save_members

# ui のファイル名に合わせて変えてね：
# ui_profile_page.py なら ↓ こう
from ui_profile_page import render_profile_page
#from ui_member_list_page import render_member_list_page  # ← まだ無ければコメントアウトでOK

st.set_page_config(page_title="桃下村塾メンバー紹介", layout="wide")

if "members" not in st.session_state:
    st.session_state.members = load_members()

PAGES = {
    "プロフィール作成・編集": render_profile_page,
    # "メンバー一覧": render_member_list_page,  # 実装済みなら有効化
}

st.sidebar.title("桃下村塾")
page_name = st.sidebar.radio("ページ", list(PAGES.keys()))

PAGES[page_name](st.session_state.members, save_members)
