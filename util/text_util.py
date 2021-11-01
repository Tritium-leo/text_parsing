import re

"""
文本工具
"""


def strQ2B(ustring: str):
    # """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring

    # "中文标点转英文标点"


def C_trans_to_E(text: str):
    E_pun = u';:,!?[]()<>"\'~'
    C_pun = u'；：，！？【】（）《》“‘～'
    table = {ord(f): ord(t) for f, t in zip(C_pun, E_pun)}
    return text.translate(table)

    # 特殊字符做转化


def esc_code_change(text: str):
    special_code_map = {"&lt;": '<',
                        "&gt;": '>',
                        "&amp;": '&',
                        "&quot;": '"',
                        "&copy;": '©'}
    for old, replace in special_code_map.items():
        text = re.sub(old, replace, text)
    return text


# 连续CODE 只保留一个
def repetition_code_trans(text: str):
    # 连续重复CODE 只保留一个[,;。、?]
    filter_pattern = re.compile(',{2,}|;{2,}|。{2,}|、{2,}|\?{2,}')
    for _one in filter_pattern.finditer(text):
        replace_str = [x if index == 0 else ' ' for index, x in enumerate(_one.group())]
        _temp_list = list(text)
        text = ''.join(_temp_list[0:_one.span()[0]] + replace_str + _temp_list[_one.span()[1]:])
    filter_pattern = re.compile('[、,;。]{2,}')
    # 连续不重复CODE 按优先级保留[。?;,、]
    level_list = ['。', '\?', ';', ',', '、']
    for _one in filter_pattern.finditer(text):
        _keep_str = [x for x in level_list if x in _one.group()][0]
        replace_str = [_keep_str if index == 0 else ' ' for index, x in enumerate(_one.group())]
        _temp_list = list(text)
        text = ''.join(_temp_list[0:_one.span()[0]] + replace_str + _temp_list[_one.span()[1]:])
    return text
