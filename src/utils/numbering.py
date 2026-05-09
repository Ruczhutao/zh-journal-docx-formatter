"""Compatibility wrapper for numbering helpers."""

from chinese_paper_formatter.numbering import CIRCLED_NUMBERS, circled_number, format_number, num_to_chinese


def format_level1_heading(num):
    return format_number(num, "chinese")


def format_level2_heading(num):
    return format_number(num, "chinese_paren")


def get_circled_number(num):
    return circled_number(num)
