import streamlit as st
from repository import load_members, save_members
from ui_profile_page import render_profile_page
from ui_member_list_page import render_member_list_page
from ui_member_detail_page import render_member_detail_page
from ui_mokumoku_page import render_mokumoku_page

st.set_page_config(page_title="桃下村塾", layout="wide")
st.title("桃下村塾")

# --------- セッション状態の初期化（★ここを一番最初にやる） ---------
# 1) 画面の種類
if "view" not in st.session_state:
    st.session_state.view = "profile"  # "profile" / "list" / "detail" / "mokumoku"

# 2) 詳細ページで見るメンバーID
if "detail_member_id" not in st.session_state:
    st.session_state.detail_member_id = None

# 3) メンバー一覧（Supabase からロード）
if "members" not in st.session_state:
    try:
        st.session_state.members = load_members()
    except Exception as e:
        st.error(
            "Supabase への接続に失敗しました。\n"
            "一旦空のメンバーリストで起動します。\n\n"
            f"詳細: {type(e).__name__}"
        )
        st.session_state.members = []

members = st.session_state.members

# --------- サイドバー ---------
st.sidebar.title("メニュー")

# プロフィール
if st.sidebar.button(
    "プロフィール作成・編集",
    type="primary" if st.session_state.view == "profile" else "secondary",
):
    st.session_state.view = "profile"
    st.session_state.detail_member_id = None
    st.rerun()

# メンバー一覧
if st.sidebar.button(
    "メンバー一覧",
    type="primary" if st.session_state.view == "list" else "secondary",
):
    st.session_state.view = "list"
    st.session_state.detail_member_id = None
    st.rerun()

# もくもく会
if st.sidebar.button(
    "もくもく会",
    type="primary" if st.session_state.view == "mokumoku" else "secondary",
):
    st.session_state.view = "mokumoku"
    st.session_state.detail_member_id = None
    st.rerun()

# --------- ルーティング ---------
if st.session_state.view == "detail" and st.session_state.detail_member_id is not None:
    # 詳細ページ
    target_id = st.session_state.detail_member_id
    target = next((m for m in members if m.id == target_id), None)

    if target is None:
        st.error("選択されたメンバーが見つかりません。")
        st.session_state.view = "list"
        st.session_state.detail_member_id = None
    else:
        render_member_detail_page(target)

else:
    # プロフィール / 一覧 / もくもく会
    if st.session_state.view == "profile":
        render_profile_page(members, save_members)
    elif st.session_state.view == "list":
        render_member_list_page(members, save_members)
    elif st.session_state.view == "mokumoku":
        render_mokumoku_page(members, save_members)
