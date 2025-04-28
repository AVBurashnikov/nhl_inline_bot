from typing import Any


def bold(value: Any) -> str:
    return f"<b>{value}</b>"


def italic(value: Any) -> str:
    return f"<i>{value}</i>"


def underline(value: Any) -> str:
    return f"<u>{value}</u>"


def strike(value: Any) -> str:
    return f"<s>{value}</s>"


def cite(value: Any) -> str:
    return f"<blockquote>{value}</blockquote>"


def code(value: Any) -> str:
    return f"<code>{value}</code>"


def spoiler(value: Any) -> str:
    return f"<span class='tg-spoiler'>{value}</span>"


def link(value: Any, anchor: str) -> str:
    return f"<a href='{anchor}'>{value}</a>"
