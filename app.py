# app.py
import streamlit as st
from repository import load_members, save_members
from ui.profile_page import render_profile_page
from ui.member_list_page import render_member_list_page

# ページ設定：画面をワイドに使う
st.set_page_config(
    page_title="桃下村塾メンバー紹介",
    layout="wide",
)

# --- メンバーの初期読み込み（Supabase or その他ストレージ） ---
if "members" not in st.session_state:
    # ここで repository.load_members() が Supabase から取得してくれる想定
    st.session_state.members = load_members()

# --- ページ定義 ---
PAGES = {
    "プロフィール作成・編集": render_profile_page,
    "メンバー一覧": render_member_list_page,
}

# --- サイドバーのナビゲーション ---
st.sidebar.title("桃下村塾")
page_name = st.sidebar.radio("ページ", list(PAGES.keys()))

# --- 選択されたページを描画 ---
PAGES[page_name](st.session_state.members, save_members)
