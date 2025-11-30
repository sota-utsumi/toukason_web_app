# ui_member_detail_page.py
import streamlit as st
from models import Member


def render_member_detail_page(member: Member) -> None:
    """選択されたメンバーの詳細ページ"""

    if member is None:
        st.error("メンバーが選択されていません。")
        return

    # ヘッダー
    st.title(member.name)
    if member.role:
        st.caption(f"役割：{member.role}")

    basics = " / ".join(
        x
        for x in [
            member.grade or "",
            member.faculty or "",
            member.department_course or "",
        ]
        if x
    )
    if basics:
        st.caption(basics)

    if member.lab:
        st.caption(f"研究室：{member.lab}")

    st.markdown("---")

    # 各セクションを1ページにまとめて表示
    if member.likes:
        st.subheader("好きなこと")
        st.write(member.likes)
        st.markdown("---")

    if member.skills:
        st.subheader("できること")
        st.write(member.skills)
        st.markdown("---")

    if member.belongs:
        st.subheader("所属")
        st.write(member.belongs)
        st.markdown("---")

    if member.wanna_learn:
        st.subheader("学びたいこと")
        st.write(member.wanna_learn)
        st.markdown("---")

    if st.button("← メンバー一覧に戻る"):
        st.session_state.view = "list"
        st.session_state.detail_member_id = None
        st.rerun()

