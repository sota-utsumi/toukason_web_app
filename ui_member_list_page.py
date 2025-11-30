# ui_member_list_page.py
from typing import List, Callable

import streamlit as st

from models import Member, ROLE_ORDER, ROLE_COLORS


def render_member_list_page(
    members: List[Member],
    save_members: Callable[[List[Member]], None],  # 使ってないがシグネチャ合わせ
) -> None:
    """メンバー一覧ページを描画"""

    st.title("メンバー一覧")

    if not members:
        st.info("まだメンバーが登録されていません。")
        return

    # 役割ごとにグルーピングして表示
    for role in ROLE_ORDER:
        group = [m for m in members if m.role == role]
        if not group:
            continue

        st.markdown(f"## {role}")

        cols = st.columns(3)  # 3列カード

        for i, m in enumerate(group):
            col = cols[i % 3]
            with col:
                with st.container(border=True):
                    # 色付き役割バッジ
                    color = ROLE_COLORS.get(role, "#ccc")
                    st.markdown(
                        f"""
                        <div style="
                            display:inline-block;
                            padding:2px 8px;
                            border-radius:12px;
                            background-color:{color};
                            color:#000;
                            font-size:0.75rem;
                            margin-bottom:4px;
                        ">
                            {role}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # 名前
                    st.markdown(f"### {m.name}")

                    # 基本情報（学年 / 学部 / コース）
                    basics = " / ".join(
                        x for x in [
                            m.grade or "",
                            m.faculty or "",
                            m.department_course or "",
                        ] if x
                    )
                    if basics:
                        st.caption(basics)

                    # 🔽 ここが修正：詳細を expander にまとめる
                    with st.expander("詳細を表示"):
                        if m.lab:
                            st.write("**研究室**")
                            st.write(m.lab)

                        if m.likes:
                            st.write("**好きなこと**")
                            st.write(m.likes)

                        if m.skills:
                            st.write("**できること**")
                            st.write(m.skills)

                        if m.belongs:
                            st.write("**所属**")
                            st.write(m.belongs)

                        if m.wanna_learn:
                            st.write("**学びたいこと**")
                            st.write(m.wanna_learn)
# ui_member_list_page.py
from typing import List, Callable
import streamlit as st
from models import Member, ROLE_ORDER, ROLE_COLORS


def render_member_list_page(members: List[Member], save_members: Callable[[List[Member]], None]):
    st.title("メンバー一覧")

    if not members:
        st.info("まだメンバーが登録されていません。")
        return

    for role in ROLE_ORDER:
        group = [m for m in members if m.role == role]
        if not group:
            continue

        st.markdown(f"## {role}")

        cols = st.columns(3)

        for i, m in enumerate(group):
            col = cols[i % 3]
            with col:
                with st.container(border=True):
                    color = ROLE_COLORS.get(role, "#cccccc")
                    st.markdown(
                        f"""
                        <div style="
                            display:inline-block;
                            padding:2px 8px;
                            border-radius:12px;
                            background-color:{color};
                            color:#000;
                            font-size:0.75rem;
                            margin-bottom:4px;
                        ">
                            {role}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(f"### {m.name}")

                    basics = " / ".join(
                        x
                        for x in [
                            m.grade or "",
                            m.faculty or "",
                            m.department_course or "",
                        ]
                        if x
                    )
                    if basics:
                        st.caption(basics)

                    if m.lab:
                        st.caption(f"研究室：{m.lab}")

                    # ★ 詳細ページへ飛ぶボタン
                    if st.button("このメンバーの詳細を見る", key=f"detail_{m.id}"):
                        st.session_state.view = "detail"
                        st.session_state.detail_member_id = m.id
                        st.rerun()

