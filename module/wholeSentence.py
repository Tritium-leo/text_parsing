from .sentence import Sentence
from .shortSentence import ShortSentence
from typing import *


class WholeSentence(Sentence):
    short_sentence_list: List[ShortSentence]
    # 所属的 段落对象
    belong_to_paragraph = None

    def __init__(self, param):
        super().__init__(param)
        self.short_sentence_list = param.get('short_sentence_list', [])
        self.belong_to_paragraph = param.get('belong_to_paragraph', None)

    def __str__(self):
        return f'时间:{self.sentence_time},句子:{self.sentence_text}'

    # 在段落中获得之前的整句
    @property
    def prev_brothers(self):
        father_whole_list = [x for x in self.belong_to_paragraph.all_whole_sentence_dict.values()]
        return [x for index, x in enumerate(father_whole_list) if father_whole_list.index(self) > index]

    # 在段落中获得之后的整句
    @property
    def after_brothers(self):
        father_whole_list = [x for x in self.belong_to_paragraph.all_whole_sentence_dict.values()]
        return [x for index, x in enumerate(father_whole_list) if father_whole_list.index(self) < index]

    # 在段落中获得前一个整句
    @property
    def prev_brother(self):
        prev_whole_list = self.prev_brothers
        return None if not prev_whole_list else prev_whole_list[-1]

    # 在段落中获得后一个整句
    @property
    def next_brother(self):
        after_whole_list = self.after_brothers
        return None if not after_whole_list else after_whole_list[0]
