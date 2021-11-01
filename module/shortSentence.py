from .sentence import Sentence


class ShortSentence(Sentence):
    group: int
    group_master: int
    # 所属的 段落对象
    belong_to_paragraph = None
    # 所属的整句对象
    belong_to_whole_sentence = None

    def __init__(self, param):
        super().__init__(param)
        self.group = int(param.get('group', -1))
        self.group_master = int(param.get('group_master', -1))
        self.belong_to_paragraph = param.get('belong_to_paragraph', None)
        self.belong_to_whole_sentence = param.get('belong_to_whole_sentence', None)

    def __str__(self):
        return f'时间:{self.sentence_time},句子:{self.sentence_text}'

    # 在整句中获得之前的短句
    @property
    def prev_brothers_in_whole(self):
        father_short_list = self.belong_to_whole_sentence.short_sentence_list
        return [x for index, x in enumerate(father_short_list) if father_short_list.index(self) > index]

    # 在整句中获得之后的短句
    @property
    def after_brothers_in_whole(self):
        father_short_list = self.belong_to_whole_sentence.short_sentence_list
        return [x for index, x in enumerate(father_short_list) if father_short_list.index(self) < index]

    # 在段落中获得之前的短句
    @property
    def prev_brothers_in_paragraph(self):
        father_short_list = [x for x in self.belong_to_paragraph.all_short_sentence_dict.values()]
        return [x for index, x in enumerate(father_short_list) if father_short_list.index(self) > index]

    # 在段落中获得之后的短句
    @property
    def after_brothers_in_paragraph(self):
        father_short_list = [x for x in self.belong_to_paragraph.all_short_sentence_dict.values()]
        return [x for index, x in enumerate(father_short_list) if father_short_list.index(self) < index]

    # 在整句中获得前一个短句
    @property
    def prev_brother_in_whole(self):
        prev_short_list = self.prev_brothers_in_whole
        return None if not prev_short_list else prev_short_list[-1]

    # 在整句中获得后一个短句
    @property
    def next_brother_in_whole(self):
        after_short_list = self.after_brothers_in_whole
        return None if not after_short_list else after_short_list[0]

    # 在段落中获得前一个短句
    @property
    def prev_brother_in_paragraph(self):
        prev_short_list = self.prev_brothers_in_paragraph
        return None if not prev_short_list else prev_short_list[-1]

    # 在段落中获得后一个短句
    @property
    def next_brother_short_in_paragraph(self):
        after_short_list = self.after_brothers_in_paragraph
        return None if not after_short_list else after_short_list[0]
