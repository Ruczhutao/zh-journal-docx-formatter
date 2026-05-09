"""Numbering helpers for Chinese academic manuscript headings and citations."""

from __future__ import annotations


CHINESE_NUMS = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
CIRCLED_NUMBERS = [
    "①",
    "②",
    "③",
    "④",
    "⑤",
    "⑥",
    "⑦",
    "⑧",
    "⑨",
    "⑩",
    "⑪",
    "⑫",
    "⑬",
    "⑭",
    "⑮",
    "⑯",
    "⑰",
    "⑱",
    "⑲",
    "⑳",
    "㉑",
    "㉒",
    "㉓",
    "㉔",
    "㉕",
    "㉖",
    "㉗",
    "㉘",
    "㉙",
    "㉚",
    "㉛",
    "㉜",
    "㉝",
    "㉞",
    "㉟",
    "㊱",
    "㊲",
    "㊳",
    "㊴",
    "㊵",
    "㊶",
    "㊷",
    "㊸",
    "㊹",
    "㊺",
    "㊻",
    "㊼",
    "㊽",
    "㊾",
    "㊿",
]


def num_to_chinese(num: int) -> str:
    """Convert an integer to a simple Chinese numeral for manuscript headings."""

    if num < 0:
        raise ValueError("num must be non-negative")
    if num < 10:
        return CHINESE_NUMS[num]
    if num == 10:
        return "十"
    if num < 20:
        return "十" + CHINESE_NUMS[num % 10]
    if num < 100:
        tens, ones = divmod(num, 10)
        return CHINESE_NUMS[tens] + "十" + (CHINESE_NUMS[ones] if ones else "")
    return str(num)


def format_number(num: int, numbering: str) -> str:
    if numbering == "chinese":
        return f"{num_to_chinese(num)}、"
    if numbering == "chinese_paren":
        return f"（{num_to_chinese(num)}）"
    if numbering == "arabic":
        return f"{num}."
    if numbering == "arabic_full_stop":
        return f"{num}．"
    if numbering == "arabic_paren":
        return f"({num})"
    return ""


def circled_number(num: int) -> str:
    if 1 <= num <= len(CIRCLED_NUMBERS):
        return CIRCLED_NUMBERS[num - 1]
    return f"[{num}]"
