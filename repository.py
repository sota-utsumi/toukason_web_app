# repository.py
from dataclasses import asdict
from typing import List

import streamlit as st
from supabase import create_client, Client

from models import Member

TABLE_NAME = "menbers"  # Supabase のテーブル名


@st.cache_resource
def get_supabase() -> Client:
    """Supabase クライアントを生成（Streamlit のリソースキャッシュ付き）"""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["anon_key"]

    # デバッグ用：URL を軽くチェック（必要なくなったら消してOK）
    clean_url = url.strip()
    if not clean_url.startswith("https://") or ".supabase.co" not in clean_url:
        # ここでエラーを投げると、Cloud のログに URL の repr が出る
        raise RuntimeError(f"Supabase URL looks wrong: {repr(clean_url)}")

    return create_client(clean_url, key)


def load_members() -> List[Member]:
    """
    Supabase から members をロード。
    失敗したときは例外を投げるので、呼び出し側で try/except する。
    """
    supabase = get_supabase()
    res = supabase.table(TABLE_NAME).select("*").order("id").execute()

    rows = res.data or []
    members: List[Member] = []

    for row in rows:
        # DB のカラムと Member のフィールド名は一致している前提
        members.append(Member(**row))

    return members


def save_members(members: List[Member]) -> None:
    """
    渡された members を Supabase に保存。
    - id を主キーとして upsert（あれば更新、なければ挿入）
    """
    supabase = get_supabase()

    if not members:
        return

    payload = [asdict(m) for m in members]
    supabase.table(TABLE_NAME).upsert(payload, on_conflict="id").execute()
