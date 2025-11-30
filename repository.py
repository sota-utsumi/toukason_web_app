# repository.py
from dataclasses import asdict
from typing import List

import streamlit as st
from supabase import create_client, Client

from models import Member

TABLE_NAME = "menbers"  # Supabase のテーブル名（DDL の typo に合わせる）


@st.cache_resource
def get_supabase() -> Client:
    """Supabase クライアント（Streamlit Cloud 用にキャッシュ）。"""
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

    members: List[Member] = [Member.from_dict(row) for row in rows]
    return members


def save_members(members: List[Member]) -> None:
    """
    渡された members を Supabase に保存する。
    - id を主キーとして upsert（あれば更新、なければ挿入）
    - 削除同期は行わず、INSERT / UPDATE のみ
    """
    supabase = get_supabase()

    if not members:
        return

    payload = [asdict(m) for m in members]
    supabase.table(TABLE_NAME).upsert(payload, on_conflict="id").execute()
