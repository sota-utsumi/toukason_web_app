import streamlit as st
from repository import load_members, save_members
from ui_profile_page import render_profile_page
from ui_member_list_page import render_member_list_page
from ui_member_detail_page import render_member_detail_page

st.set_page_config(page_title="桃下村塾メンバー紹介", layout="wide")

# --------- セッション状態の初期化 ---------
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

# view: "profile" | "list" | "detail"
if "view" not in st.session_state:
    st.session_state.view = "profile"

if "detail_member_id" not in st.session_state:
    st.session_state.detail_member_id = None

members = st.session_state.members

# --------- サイドバー（ラジオやめてボタンだけ） ---------
st.sidebar.title("桃下村塾")

if st.sidebar.button(
    "プロフィール作成・編集",
    type="primary" if st.session_state.view == "profile" else "secondary",
):
    st.session_state.view = "profile"
    st.session_state.detail_member_id = None
    st.rerun()

if st.sidebar.button(
    "メンバー一覧",
    type="primary" if st.session_state.view == "list" else "secondary",
):
    st.session_state.view = "list"
    st.session_state.detail_member_id = None
    st.rerun()

st.title("桃下村塾メンバー紹介")
st.markdown("---")

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
    # 一覧 or プロフィール
    if st.session_state.view == "profile":
        render_profile_page(members, save_members)
    else:  # "list"
        render_member_list_page(members, save_members)
