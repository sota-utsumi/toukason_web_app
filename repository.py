# repository.py
from dataclasses import asdict
from typing import List

import streamlit as st
from supabase import create_client, Client

from models import Member  # ← 自分（repository）は import しないこと！


TABLE_NAME = "menbers"  # Supabase のテーブル名（typo に合わせている）


@st.cache_resource
def get_supabase() -> Client:
    """Supabase クライアントを生成（Streamlit のリソースキャッシュ付き）"""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["anon_key"]
    return create_client(url, key)


def load_members() -> List[Member]:
    """
    Supabase の public.menbers からメンバー一覧を取得して、
    Member のリストとして返す。
    """
    supabase = get_supabase()
    res = supabase.table(TABLE_NAME).select("*").order("id").execute()

    rows = res.data or []

    # Supabase から返ってきた dict を Member に変換
    members: List[Member] = [Member.from_dict(row) for row in rows]

    return members


def save_members(members: List[Member]) -> None:
    """
    渡された members を Supabase に保存する。
    - id を主キーとして upsert（あれば更新、なければ挿入）
    - 削除同期は行わず、あくまで insert / update のみ
    """
    supabase = get_supabase()

    if not members:
        return

    payload = [asdict(m) for m in members]

    supabase.table(TABLE_NAME).upsert(payload, on_conflict="id").execute()
