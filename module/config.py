import re
from typing import *


class Config(object):
    # 初始化
    # 是否将 。"。)替换为"。)。
    replace_last_inner_punctuation_to_out: bool
    # 是否切分引号括号里面的分隔符
    ignore_inner_punctuation: bool
    # 是否获得更好的时间提取文本2014.01.02;2014.02.03 替换为2014.01.02、2014.02.03 配合spilt_short_by_time_and_comma使用
    get_more_time_get_paragraph: bool

    # 文本切分
    # 整句的切分正则
    whole_sentence_split_reg: re.Pattern
    # 短句切分的正则
    short_sentence_split_reg: re.Pattern

    # 时间提取
    # 是否提取时间
    get_sentence_time: bool
    # 时间默认值
    default_time: str
    # 时间年月日补齐默认值: 2021-01-UNKNOWN
    incomplete_time_swallow_word: str
    # 是否为短句切分时间顿号时间 2015年1月、2016年2月做了AAA -> 2015年1月做了AAA ，2016年2月做了AAA
    spilt_short_by_time_and_comma: bool
    # 短句是否获取最后一个提及的时间,True为提取 仅为具体时间,非抽象时间
    short_get_last_time: bool
    # 整句是否获取最后一个提及的时间,True为提取 仅为具体时间,非抽象时间
    whole_get_last_time: bool
    # 不提取时间的短句正则
    short_time_filter_pattern: re.Pattern
    # 短句能够继承的时间的范围  prefix_short_index prefix_whole_index，get_useful
    short_extent_last_time_level: Dict
    # 是否忽略[括号][引号]里的时间,配合ignore_inner_punctuation:False才有效
    get_time_ignore_bracket_and_other: bool

    def __init__(self, param):
        self.replace_last_inner_punctuation_to_out = param.get('replace_last_inner_punctuation_to_out', False)
        self.ignore_inner_punctuation = param.get('ignore_inner_punctuation', False)
        self.get_more_time_get_paragraph = param.get('get_more_time_get_paragraph', False)
        self.whole_sentence_split_reg = re.compile(param.get('whole_sentence_split_reg', ''))
        self.short_sentence_split_reg = re.compile(param.get('short_sentence_split_reg', ''))
        self.get_sentence_time = param.get('get_sentence_time', False)
        self.spilt_short_by_time_and_comma = param.get('spilt_short_by_time_and_comma', False)
        self.whole_get_last_time = param.get('whole_get_last_time', False)
        self.short_get_last_time = param.get('short_get_last_time', False)
        self.short_time_filter_pattern = re.compile(param.get('short_time_filter_pattern', ''))
        self.short_extent_last_time_level = param.get('short_extent_last_time_level',
                                                      {"prefix_short_index": -1, "prefix_whole_index": -1,
                                                       "get_useful": True})
        self.get_time_ignore_bracket_and_other = param.get('get_time_ignore_bracket_and_other', False)
        self.incomplete_time_swallow_word = param.get('incomplete_time_swallow_word', 'UNKNOWN')
        self.default_time = param.get('default_time', 'MISSING')

    @property
    def default_param(self):
        return {"replace_last_inner_punctuation_to_out": False,
                "ignore_inner_punctuation": False,
                "get_more_time_get_paragraph": False,
                "whole_sentence_split_reg": '',
                "short_sentence_split_reg": "",
                "get_sentence_time": False,
                "spilt_short_by_time_and_comma": False,
                "whole_get_last_time": False,
                "short_get_last_time": False,
                "short_time_filter_pattern": "",
                "short_extent_last_time_level": {"prefix_short_index": -1,
                                                 "prefix_whole_index": -1,
                                                 "get_useful": True},
                "get_time_ignore_bracket_and_other": False,
                "incomplete_time_swallow_word": "UNKNOWN",
                "no_mention_time_default": "MISSING"
                }
