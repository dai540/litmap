from __future__ import annotations


def build_text_template(text_fields: list[str], separator: str) -> str:
    return separator.join(f"{{{field}}}" for field in text_fields)
