# repository.py
from dataclasses import asdict
from typing import List

import streamlit as st
from supabase import create_client, Client

from models import Member

TABLE_NAME = "menbers"  # Supabase 側のテーブル名


@st.cache_resource
def get_supabase() -> Client:
    """Supabase クライアントを生成（Streamlit のリソースキャッシュ付き）"""
    # secrets.toml / Cloud の Secrets に入れた値を読む
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["anon_key"]
    return create_client(url, key)


def load_members() -> List[Member]:
    """Supabase からメンバー一覧を取得"""
    supabase = get_supabase()
    res = supabase.table(TABLE_NAME).select("*").order("id").execute()
    rows = res.data or []
    return [Member.from_dict(row) for row in rows]


def save_members(members: List[Member]) -> None:
    """
    渡された members を Supabase に保存する。
    - id を主キーとして upsert（あれば更新、なければ挿入）
    """
    supabase = get_supabase()

    if not members:
        return

    payload = [asdict(m) for m in members]
    supabase.table(TABLE_NAME).upsert(payload, on_conflict="id").execute()
