# ui_profile_page.py
import streamlit as st
from typing import List, Callable
from models import Member, ROLE_ORDER, ROLE_COLORS  # ROLE_COLORS は今後の拡張用


def to_multiline(value: str) -> str:
    if not value:
        return ""
    tmp = value.replace("／", "/")
    for sep in ["/", "、", ",", "，"]:
        tmp = tmp.replace(sep, "\n")
    return "\n".join(line.strip() for line in tmp.splitlines() if line.strip())


def from_multiline(value: str) -> str:
    return " / ".join(
        line.strip() for line in value.splitlines() if line.strip()
    )


def render_profile_page(
    members: List[Member],
    saver: Callable[[List[Member]], None],
) -> None:
    left, main, right = st.columns([0.3, 1.4, 0.3])
    with main:
        st.title("プロフィール作成・編集")
        st.caption("新しく自分のページを作るか、すでに登録されているプロフィールを編集できます。")

        mode = st.radio("操作を選んでください", ["新規作成", "既存メンバーを編集"], horizontal=True)

        if mode == "新規作成":
            target = Member(id=-1, name="", role="学び舎")
        else:
            if not members:
                st.warning("まだメンバーが登録されていません。まずは「新規作成」から登録してください。")
                return
            name_options = [m.name for m in members]
            selected_name = st.selectbox("編集するメンバーを選択", name_options)
            target = next(m for m in members if m.name == selected_name)

        st.markdown("---")
        st.subheader("プロフィール入力")

        with st.form("edit_or_create_profile"):
            name = st.text_input("名前", value=target.name)

            role_keys = list(ROLE_ORDER)
            current_role = target.role if target.role in role_keys else "学び舎"
            role = st.selectbox(
                "桃下村塾での役割",
                role_keys,
                index=role_keys.index(current_role),
            )

            grade = st.text_input("学年（例：B4, M1 など）", value=target.grade or "")
            faculty = st.text_input("学部", value=target.faculty or "")
            department_course = st.text_input("学科・コース", value=target.department_course or "")
            lab = st.text_input("研究室", value=target.lab or "")

            st.markdown("---")

            likes = st.text_area("好きなこと（1行につき1つ）", value=to_multiline(target.likes or ""))
            skills = st.text_area("できること（1行につき1つ）", value=to_multiline(target.skills or ""))
            belongs = st.text_area("所属（1行につき1つ）", value=to_multiline(target.belongs or ""))
            wanna_learn = st.text_area(
                "学びたいこと（1行につき1つ）",
                value=to_multiline(target.wanna_learn or ""),
            )

            submitted = st.form_submit_button("この内容で保存する")

        if not submitted:
            return

        if not name.strip():
            st.error("名前は必須です。")
            return

        if mode == "新規作成":
            if any(
                (m.name == name.strip() and (m.grade or "") == grade.strip() and (m.lab or "") == lab.strip())
                for m in members
            ):
                st.warning("同じ名前・学年・研究室のメンバーが既にいます。")
                return

            new_id = max((m.id or 0 for m in members), default=0) + 1
            new_member = Member(
                id=new_id,
                name=name.strip(),
                role=role,
                grade=grade.strip(),
                faculty=faculty.strip(),
                department_course=department_course.strip(),
                lab=lab.strip(),
                likes=from_multiline(likes),
                skills=from_multiline(skills),
                belongs=from_multiline(belongs),
                wanna_learn=from_multiline(wanna_learn),
            )
            members.append(new_member)
            saver(members)
            st.success(f"新しくメンバー「{name}」を登録しました！")

        else:
            # 既存更新
            target.name = name.strip()
            target.role = role
            target.grade = grade.strip()
            target.faculty = faculty.strip()
            target.department_course = department_course.strip()
            target.lab = lab.strip()
            target.likes = from_multiline(likes)
            target.skills = from_multiline(skills)
            target.belongs = from_multiline(belongs)
            target.wanna_learn = from_multiline(wanna_learn)

            saver(members)
            st.success(f"メンバー「{name}」のプロフィールを更新しました！")
