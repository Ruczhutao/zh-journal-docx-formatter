"""
Numbering utilities for Chinese academic papers.
"""

def num_to_chinese(num):
    """Convert Arabic number to Chinese numeral."""
    chinese_nums = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    if num <= 10:
        return chinese_nums[num]
    elif num < 20:
        return '十' + chinese_nums[num % 10] if num % 10 != 0 else '十'
    elif num < 100:
        tens = num // 10
        ones = num % 10
        if ones == 0:
            return chinese_nums[tens] + '十'
        else:
            return chinese_nums[tens] + '十' + chinese_nums[ones]
    else:
        return str(num)

def format_level1_heading(num):
    """Format level 1 heading number: 一、二、三..."""
    return f"{num_to_chinese(num)}、"

def format_level2_heading(num):
    """Format level 2 heading number: （一）（二）（三）..."""
    return f"（{num_to_chinese(num)}）"

# Circled numbers ①-㊿ (1-50)
CIRCLED_NUMBERS = [
    '①','②','③','④','⑤','⑥','⑦','⑧','⑨','⑩',
    '⑪','⑫','⑬','⑭','⑮','⑯','⑰','⑱','⑲','⑳',
    '㉑','㉒','㉓','㉔','㉕','㉖','㉗','㉘','㉙','㉚',
    '㉛','㉜','㉝','㉞','㉟','㊱','㊲','㊳','㊴','㊵',
    '㊶','㊷','㊸','㊹','㊺','㊻','㊼','㊽','㊾','㊿'
]

def get_circled_number(num):
    """Get circled number for citation."""
    if 1 <= num <= 50:
        return CIRCLED_NUMBERS[num - 1]
    return f"[{num}]"
