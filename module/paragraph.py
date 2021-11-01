import re
from typing import *
from .wholeSentence import WholeSentence
from .config import Config
from .timePattern import TimePattern
from copy import deepcopy
from util.text_util import *


class Paragraph(object):
    source: str
    paragraph_text: str

    paragraph_text_replaced: str
    replace_str_dict: Dict

    config: Config
    whole_sentence_list: List[WholeSentence]

    def __init__(self, param):
        self.source = param['source']
        self.paragraph_text = param['paragraph_text']
        self.paragraph_text_replaced = self.paragraph_text
        self.replace_str_dict = {}

    # 替换被“”（）包含的词语
    def _replace_paragraph(self, patten_list: List):
        _replace_tuple_list = []
        for reg_str in patten_list:
            split_index_list = []
            for one_matching in re.finditer(reg_str, self.paragraph_text):
                split_index_list.append(one_matching.span()[0])
            split_index_list.sort()
            for index, num in enumerate(split_index_list):
                if index % 2 == 0 and len(split_index_list) > index + 1:
                    _replace_tuple_list.append((split_index_list[index], split_index_list[index + 1] + 1))
        replace_index = 0
        for _tuple in _replace_tuple_list:
            replace_index += 1
            self.replace_str_dict[f'[REPLACE{replace_index}]'] = self.paragraph_text[_tuple[0]:_tuple[1]]
        for find_str, replace_str in {v: k for k, v in self.replace_str_dict.items()}.items():
            self.paragraph_text_replaced = self.paragraph_text_replaced.replace(find_str, replace_str)

    def load_config(self, config: Config):
        self.config = config
        self.paragraph_init()
        self.paragraph_text_replaced = self.paragraph_text
        # 括号，单双引号不会分隔子句
        if self.config.ignore_inner_punctuation:
            patten_list = ['[\(\)（）]', '[‘’]', '[“"”\']']
            self._replace_paragraph(patten_list)
        # 获得更好时间 时间.时间 都变为 时间、时间.
        # TODO 存在逻辑问题 XXX时间，时间BBB 也会被替换
        if self.config.get_more_time_get_paragraph:
            for _one in TimePattern.comma_time_pattern_small().finditer(self.paragraph_text):
                start_index = _one.span()[0]
                for _i in range(0, len(_one.group())):
                    if not re.search('[\d年月日号天\.\-]', _one.group()[_i]):
                        start_index += _i
                        break
                to_list_paragraph = list(self.paragraph_text)
                if start_index != _one.span()[0]:
                    to_list_paragraph[start_index] = '、'
                    self.paragraph_text = ''.join(to_list_paragraph)
        return self

    # 段落初始化
    def paragraph_init(self):
        # 全半角转化
        self.paragraph_text = strQ2B(self.paragraph_text)
        # 中英文标点转化
        self.paragraph_text = C_trans_to_E(self.paragraph_text)
        # 转义字符的处理
        self.paragraph_text = esc_code_change(self.paragraph_text)
        # 。" 替换为 "。 内置的最后的标点外置
        if self.config.replace_last_inner_punctuation_to_out:
            _patten = re.compile('[。,，；;][”\')）"]')
            for one in _patten.finditer(deepcopy(self.paragraph_text)):
                matching_text = one.group()
                assert len(matching_text) == 2, '匹配错误'
                matching_text = list(matching_text)
                matching_text.reverse()
                matching_text = ''.join(matching_text)
                self.paragraph_text = re.sub(_patten, matching_text, self.paragraph_text)

        self.paragraph_text = repetition_code_trans(self.paragraph_text)

    @property
    def all_short_sentence_dict(self):
        short_dict = {}
        for whole_index, whole in enumerate(self.whole_sentence_list):
            for short_index, short in enumerate(whole.short_sentence_list):
                short_dict[(whole_index, short_index)] = short
        return short_dict

    @property
    def all_whole_sentence_dict(self):
        whole_dict = {}
        for whole_index, whole in enumerate(self.whole_sentence_list):
            whole_dict[whole_index] = whole
        return whole_dict
