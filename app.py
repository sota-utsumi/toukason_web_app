import json
from pathlib import Path
import streamlit as st

# ページ設定：画面をワイドに使う
st.set_page_config(
    page_title="桃下村塾メンバー紹介",
    layout="wide",
)

DATA_PATH = Path("data/members.json")

# --- 初期メンバー（デフォルト値） ---
DEFAULT_MEMBERS = [
    {
        "id": 1,
        "name": "内海 颯太",
        "role": "学び舎",
        "grade": "B4",
        "faculty": "工学部",
        "department_course": "機械システム系 / 機械工学コース",
        "lab": "特殊加工学研究室",
        "likes": "AI / 画像認識 / カフェ巡り / カラオケ",
        "skills": "Pythonでの簡単なWebアプリ作成 / プレゼン資料作り / 引越し現場の段取り",
        "belongs": "桃下村塾 / アート引越センター(バイト)",
        "wanna_learn": "LLM応用 / 画像認識 / 生産技術 / 事業づくり",
    },
]

# 役割とカラー
ROLE_OPTIONS = {
    "代表": "#ff99cc",        # ピンク
    "開発": "#66cc66",        # 緑
    "イベント企画": "#ffeb66", # 黄色
    "SNS広報": "#ff6666",     # 赤
    "学び舎": "#6699ff",      # 青
    "外部連携": "#aaaaaa",    # グレー
}

# 表示順
ROLE_ORDER = ["代表", "開発", "イベント企画", "SNS広報", "学び舎", "外部連携"]


def load_members() -> list[dict]:
    """JSON からメンバー一覧を読み込む。なければデフォルトを返す。"""
    if DATA_PATH.exists():
        with DATA_PATH.open("r", encoding="utf-8") as f:
            members = json.load(f)
    else:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        with DATA_PATH.open("w", encoding="utf-8") as f:
            json.dump(DEFAULT_MEMBERS, f, ensure_ascii=False, indent=2)
        members = DEFAULT_MEMBERS

    # 既存データの不足キーを軽く補完（保険）
    for m in members:
        m.setdefault("role", "学び舎")
        m.setdefault("grade", "")
        m.setdefault("faculty", "")
        m.setdefault("department_course", "")
        m.setdefault("lab", "")
        m.setdefault("likes", "")
        m.setdefault("skills", "")
        m.setdefault("belongs", "")
        m.setdefault("wanna_learn", "")

    return members


def save_members(members: list[dict]) -> None:
    """メンバー一覧を JSON に保存する。"""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(members, f, ensure_ascii=False, indent=2)


def to_multiline(value: str) -> str:
    """スラッシュ区切りなどの文字列を、1行1項目の文字列に変換"""
    if not value:
        return ""
    # / や 、 で区切ってた場合をざっくり吸収
    tmp = value.replace("／", "/")
    for sep in ["/", "、", ",", "，"]:
        tmp = tmp.replace(sep, "\n")
    lines = [line.strip() for line in tmp.splitlines() if line.strip()]
    return "\n".join(lines)


def from_multiline(value: str) -> str:
    """1行1項目の複数行テキストを ' / ' 区切りの1行文字列に変換"""
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    return " / ".join(lines)


members = load_members()

# ===================== サイドバー =====================
st.sidebar.title("桃下村塾")

PAGES = ["プロフィール作成・編集", "メンバー一覧"]

# 初期ページ
if "page" not in st.session_state:
    st.session_state.page = "プロフィール作成・編集"

st.sidebar.markdown("ページ")

# 縦ボタンでページ切り替え
for label in PAGES:
    is_active = (st.session_state.page == label)
    if st.sidebar.button(
        label,
        use_container_width=True,
        type="primary" if is_active else "secondary",
        key=f"nav_{label}",
    ):
        st.session_state.page = label

page = st.session_state.page

# メンバー一覧から戻ってきたときに詳細選択状態をリセットしておく
if page != "メンバー一覧" and "selected_member_id" in st.session_state:
    st.session_state.selected_member_id = None


# ======================================================
#              プロフィール作成・編集（みんな用）
# ======================================================
if page == "プロフィール作成・編集":
    left, main, right = st.columns([0.3, 1.4, 0.3])
    with main:
        st.title("プロフィール作成・編集")

        st.caption("新しく自分のページを作るか、すでに登録されているプロフィールを編集できます。")

        # 「新規作成」か「既存メンバー編集」か
        mode = st.radio(
            "操作を選んでください",
            ["新規作成", "既存メンバーを編集"],
            horizontal=True,
        )

        target_member = None

        if mode == "新規作成":
            # 空のひな形
            target_member = {
                "id": None,
                "name": "",
                "role": "",
                "grade": "",
                "faculty": "",
                "department_course": "",
                "lab": "",
                "likes": "",
                "skills": "",
                "belongs": "",
                "wanna_learn": "",
            }

        else:
            # 既存メンバーから1人選んで編集
            name_options = [m["name"] for m in members]
            selected_name = st.selectbox("編集するメンバーを選択", name_options)
            target_member = next(m for m in members if m["name"] == selected_name)

        st.markdown("---")
        st.subheader("プロフィール入力")

        with st.form("edit_or_create_profile"):
            name = st.text_input("名前", value=target_member["name"])

            # 役割プルダウン（未設定や空文字の場合は「学び舎」をデフォルトに）
            role_keys = list(ROLE_OPTIONS.keys())
            current_role = target_member.get("role") or "学び舎"
            if current_role not in role_keys:
                current_role = "学び舎"
            role_index = role_keys.index(current_role)

            role_keys = list(ROLE_OPTIONS.keys())

            # role が "" や None のときは "学び舎" にする
            current_role = target_member.get("role")
            if not current_role:
                current_role = "学び舎"

            # 想定外の文字列が入っていた時も保険で "学び舎" に寄せる
            if current_role not in role_keys:
                current_role = "学び舎"

            role = st.selectbox(
                "桃下村塾での役割",
                role_keys,
                index=role_keys.index(current_role),
            )


            grade = st.text_input("学年（例：B4, M1 など）", value=target_member["grade"])
            faculty = st.text_input("学部", value=target_member["faculty"])
            department_course = st.text_input("学科・コース", value=target_member["department_course"])
            lab = st.text_input("研究室", value=target_member["lab"])

            st.markdown("---")

            likes_input = st.text_area(
                "好きなこと（1行につき1つ）",
                value=to_multiline(target_member["likes"]),
            )

            skills_input = st.text_area(
                "できること（1行につき1つ）",
                value=to_multiline(target_member["skills"]),
            )

            belongs_input = st.text_area(
                "所属（サークル・コミュニティなど｜1行につき1つ）",
                value=to_multiline(target_member["belongs"]),
            )

            wanna_learn_input = st.text_area(
                "学びたいこと（1行につき1つ）",
                value=to_multiline(target_member["wanna_learn"]),
            )

            submitted = st.form_submit_button("この内容で保存する")

            if submitted:
                if not name.strip():
                    st.error("名前は必須です。")
                else:
                    if mode == "新規作成":
                        # 連打 & 二重登録対策：同一人物が既にいないかチェック
                        same_members = [
                            m for m in members
                            if m["name"] == name.strip()
                            and m["grade"] == grade.strip()
                            and m["lab"] == lab.strip()
                        ]

                        if same_members:
                            st.warning(
                                "同じ名前・学年・研究室のメンバーがすでに登録されています。\n"
                                "二重登録を防ぐため、新規作成は行いませんでした。\n"
                                "プロフィールを変更したい場合は「既存メンバーを編集」を選んでください。"
                            )
                        else:
                            # 新しいIDを採番
                            new_id = max((m["id"] for m in members), default=0) + 1
                            new_member = {
                                "id": new_id,
                                "name": name.strip(),
                                "role": role.strip(),
                                "grade": grade.strip(),
                                "faculty": faculty.strip(),
                                "department_course": department_course.strip(),
                                "lab": lab.strip(),
                                "likes": from_multiline(likes_input),
                                "skills": from_multiline(skills_input),
                                "belongs": from_multiline(belongs_input),
                                "wanna_learn": from_multiline(wanna_learn_input),
                            }
                            members.append(new_member)
                            save_members(members)
                            st.success(f"新しくメンバー「{name}」を登録しました！")

                    else:
                        # 既存メンバーの情報を書き換え
                        target_member["name"] = name.strip()
                        target_member["role"] = role.strip()
                        target_member["grade"] = grade.strip()
                        target_member["faculty"] = faculty.strip()
                        target_member["department_course"] = department_course.strip()
                        target_member["lab"] = lab.strip()
                        target_member["likes"] = from_multiline(likes_input)
                        target_member["skills"] = from_multiline(skills_input)
                        target_member["belongs"] = from_multiline(belongs_input)
                        target_member["wanna_learn"] = from_multiline(wanna_learn_input)

                        save_members(members)
                        st.success(f"メンバー「{name}」のプロフィールを更新しました！")


# ======================================================
#                     メンバー一覧
# ======================================================

# 役割順でソート（ROLE_ORDER にない場合は末尾に）
def role_sort_key(m: dict) -> int:
    role = m.get("role", "学び舎")
    return ROLE_ORDER.index(role) if role in ROLE_ORDER else len(ROLE_ORDER)

members_sorted = sorted(members, key=role_sort_key)

if page == "メンバー一覧":
    # 一度も設定してなければ「一覧モード」にする
    if "selected_member_id" not in st.session_state:
        st.session_state.selected_member_id = None

    left, main, right = st.columns([0.3, 1.4, 0.3])
    with main:
        # ---------- 一覧モード ----------
        if st.session_state.selected_member_id is None:
            st.title("メンバー一覧")
            st.caption("カードをクリックすると、そのメンバーの詳細プロフィールが見られます。")

            # 3列 layout
            cols = st.columns(3)

            for i, m in enumerate(members_sorted):
                with cols[i % 3]:

                    role_color = ROLE_OPTIONS.get(m.get("role", "学び舎"), "#cccccc")

                    # カードデザイン
                    card_html = f"""
                    <div style="
                        background-color:{role_color};
                        padding:15px;
                        border-radius:12px;
                        margin-bottom:10px;
                        color:black;
                        height:180px;   /* カードの高さ固定で揃える */
                        display:flex;
                        flex-direction:column;
                        justify-content:flex-start;
                    ">
                        <b>{m['name']}（{m['grade']}・{m['faculty']}）</b><br>
                        {m['department_course']}<br>
                        研究室：{m['lab']}<br>
                        好きなこと：{m['likes']}
                    </div>
                    """

                    st.markdown(card_html, unsafe_allow_html=True)

                    # カードの下に詳細ボタン
                    if st.button(
                        "▶︎ 詳細を見る",
                        key=f"view_{m['id']}",
                        use_container_width=True
                    ):
                        st.session_state.selected_member_id = m["id"]
                        st.rerun()


        # ---------- 詳細モード ----------
        else:
            # 詳細表示するメンバーを取得
            detail_member = next(
                m for m in members if m["id"] == st.session_state.selected_member_id
            )

            # 一覧に戻るボタン
            if st.button("← 一覧に戻る", use_container_width=False):
                st.session_state.selected_member_id = None
                st.stop()

            st.title(f"{detail_member['name']} のプロフィール")

            role_color = ROLE_OPTIONS.get(detail_member.get("role", "学び舎"), "#cccccc")

            st.markdown(
                f"""
                <div style="
                    padding: 10px;
                    background-color: {role_color};
                    border-radius: 8px;
                    color: black;
                    margin-bottom: 15px;
                ">
                    役割：<b>{detail_member.get('role', '未設定')}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            # 削除 UI
            with st.expander("このメンバーを削除する（取り消し不可）", expanded=False):
                st.warning(
                    "このメンバーを削除すると、元に戻せません。\n"
                    "本当に削除する場合のみチェックを入れてください。"
                )
                confirm_delete = st.checkbox("本当に削除する", key=f"confirm_delete_{detail_member['id']}")
                if confirm_delete:
                    if st.button("このメンバーを完全に削除する", type="primary"):
                        # 該当メンバーを除外
                        members = [m for m in members if m["id"] != detail_member["id"]]
                        save_members(members)
                        st.session_state.selected_member_id = None
                        st.success("メンバーを削除しました。")
                        st.rerun()

            with st.container(border=True):
                st.subheader("基本情報")
                st.write(f"学年：{detail_member['grade']}")
                st.write(f"学部：{detail_member['faculty']}")
                st.write(f"学科・コース：{detail_member['department_course']}")
                st.write(f"役割：{detail_member.get('role', '未設定')}")

                st.markdown("---")
                st.subheader("好きなこと")
                st.write(detail_member["likes"])

                st.markdown("---")
                st.subheader("できること")
                st.write(detail_member["skills"])

                st.markdown("---")
                st.subheader("所属")
                st.write(detail_member["belongs"])

                st.markdown("---")
                st.subheader("学びたいこと")
                st.write(detail_member["wanna_learn"])
