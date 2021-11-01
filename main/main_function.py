# 官方
import re
import time
import calendar
from typing import *
from datetime import datetime
from collections import defaultdict
# 第三方
from dateutil.relativedelta import relativedelta
# 自己
from module import *
from util.time_util import str_to_datetime


class TextParsing(object):
    """
    文本按时间解析
    param: param_init方法pip install
    """

    def __call__(self, param=None):
        for _one in param:
            split_text, abstract_base_datetime = TextParsing.source_check(self.input, _one)
            paragraph = Paragraph({"source": split_text['origin'],
                                   "paragraph_text": split_text['text']}).load_config(Config(_one))
            # 分割文本
            TextParsing.get_sentence(paragraph)
            if paragraph.config.get_sentence_time:
                # 文本提取时间
                all_whole_times = TextParsing.get_sentence_time(paragraph, abstract_base_datetime)
                # 短句时间过滤器
                TextParsing.short_sentence_filter(paragraph, all_whole_times)

            self.calc_result[_one.get('nickname', _one['split_text'])] = paragraph

    # 来源检查和获取
    @staticmethod
    def source_check(check_input: Dict, _one_config: Dict):
        table, column = _one_config['split_text'].split('|')
        split_text = {"origin": _one_config['split_text']}
        if len(check_input[table]) < 1:
            split_text.update({'text': ''})
        else:
            split_text.update({'text': check_input.get(table, [{column: ""}])[0].get(column, '')})
        abstract_base_datetime = {"origin": _one_config.get('abstract_datetime', '')}
        # table, column = _one_config['abstract_datetime'].split('|')
        if not abstract_base_datetime['origin'] or len(check_input[table]) < 1:
            abstract_base_datetime.update({'text': ''})
        else:
            table, column = _one_config['abstract_datetime'].split('|')
            abstract_base_datetime.update({'text': check_input[table][0][column]})
        return split_text, abstract_base_datetime

    # for web_server  main_function
    @staticmethod
    def execute(param, split_text, abstract_base_datetime):
        """
        单独调用 静态方法
        :param param: 一份配置文件
        :param split_text: {‘text’:"表格原文内容",“origin”：“table|column”}
        :param abstract_base_datetime: {‘text’:"表格原文内容",“origin”：“table|column”}
        :return: 段落对象
        """
        paragraph_param = {
            "source": split_text['origin'],
            "paragraph_text": split_text['text']
        }
        paragraph_obj = Paragraph(paragraph_param).load_config(Config(param))
        # 分割文本
        TextParsing.get_sentence(paragraph_obj)
        # 是否获得时间
        if paragraph_obj.config.get_sentence_time:
            # 文本提取时间
            all_whole_times = TextParsing.get_sentence_time(paragraph_obj, abstract_base_datetime)
            # 短句时间过滤器
            TextParsing.short_sentence_filter(paragraph_obj, all_whole_times)

        return paragraph_obj

    # 分长短句
    @staticmethod
    def get_sentence(paragraph: Paragraph):

        # 复原被替换的文本
        def recover_replace_item(text: str, _replace_str_dict: Dict) -> str:
            replace_pattern = re.compile('\[REPLACE\d+\]')
            take_str = text
            for _one in replace_pattern.finditer(text):
                middle = text[_one.span()[0]: _one.span()[1]]
                take_str = take_str.replace(middle, _replace_str_dict[middle])
            return take_str

        # 按顿号分割
        def split_short_by_comma(get_time_str: str, short_sentence_group_index: int):
            get_time_str = get_time_str.replace('、、', '、')
            get_time_str = get_time_str.replace('及、', '、')
            comma_index_list = []
            comma_index = set(x for x in get_comma_index_explicit_time(get_time_str))
            if comma_index:
                comma_index_list = list({0}.union(comma_index).union({len(get_time_str)}))
                comma_index_list.sort()
            comma_index_tuple_list = []
            for i, index in enumerate(comma_index_list):
                if i + 1 < len(comma_index_list):
                    comma_index_tuple_list.append((index, comma_index_list[i + 1]))
            text_list = []
            if not comma_index_tuple_list:
                pass
            else:
                short_sentence_group_index += 1
                first_special_tuple = get_time_str[:comma_index_tuple_list.pop(0)[1]]
                last_special_tuple = get_time_str[comma_index_tuple_list.pop(-1)[0] + 1:]
                if first_special_tuple == '分别于2015年3月':
                    a = 1
                prefix_str = get_prefix_except_time(first_special_tuple)
                suffix_str = get_suffix_except_time(last_special_tuple)
                # 去除时间表述的后续句子
                if not comma_index_tuple_list:
                    text_list.append(f"{first_special_tuple}{suffix_str}")
                    text_list.append(f"{prefix_str}{last_special_tuple}")
                else:
                    # 前缀纯时间添加
                    text_list.append(f"{first_special_tuple}{suffix_str}")
                    # 中间其他添加
                    for index_tuple in comma_index_tuple_list:
                        middle_text = get_time_str[index_tuple[0] + 1:index_tuple[1]]
                        if not middle_text:
                            continue
                        if prefix_str:
                            text_list.append(prefix_str + middle_text + suffix_str)
                        else:
                            text_list.append(middle_text + suffix_str)
                    # 后缀添加
                    if prefix_str:
                        text_list.append(f"{prefix_str}{last_special_tuple}")
                    else:
                        text_list.append(f"{last_special_tuple}")
            return text_list, short_sentence_group_index

        # 获得具体提及的时间所有的顿号
        def get_comma_index_explicit_time(text_replaced: str):
            all_index_list = []
            for patten in TimePattern.explicit_patten_list + \
                          [TimePattern.month_day_pattern, re.compile('\d{1,2}-\d{1,2}、'), TimePattern.month_pattern2]:
                for one in patten.finditer(text_replaced):
                    if one.group().find('、') != -1:
                        all_index_list.append(one.span()[0] + one.group().find('、'))
                    if one.group().find('及') != -1:
                        all_index_list.append(one.span()[0] + one.group().find('及'))
                    if one.group().find('\\') != -1:
                        all_index_list.append(one.span()[0] + one.group().find('\\'))
                    if text_replaced[one.span()[0] - 1] == '、':
                        all_index_list.append(one.span()[0] - 1)
                    if text_replaced[one.span()[0] + 1] == '、':
                        all_index_list.append(one.span()[0] + 1)
            return all_index_list

        # 获取除去时间的前缀
        def get_prefix_except_time(_first_special_tuple):
            """
            :param _first_special_tuple:
            :return: 纯时间文本返回 '' ,纯文本返回None,时间+文本 返回文本
            """
            prefix_str = None

            normalize_pattern = re.compile('年|月|日|号|--|—|\.')
            check_str = normalize_pattern.sub('-', _first_special_tuple)
            check_str = check_str[:-1] if check_str.endswith('-') else check_str
            # 纯时间/纯文本
            if not re.search('[^\d-]', check_str):
                return ''
            # 尝试 14位内找到 表达时间的字符串
            for i in range(15):
                if prefix_str is not None:
                    break
                start_index = len(_first_special_tuple) - 14 + i
                if start_index < 0:
                    continue
                check_str = normalize_pattern.sub('-', _first_special_tuple[start_index:])
                if re.search('[^\d-]', check_str):
                    continue
                prefix_str = _first_special_tuple[:start_index]
            prefix_str = _first_special_tuple if prefix_str is None else prefix_str
            if prefix_str == _first_special_tuple:
                prefix_str = _first_special_tuple
            return prefix_str

        # 获取除去时间的后缀
        def get_suffix_except_time(_last_special_tuple):
            """
            :param _last_special_tuple:
            :return: 纯时间文本返回 '' ,纯文本返回None,时间+文本 返回文本
            """
            suffix_str = None
            check_str = _last_special_tuple
            check_str = re.sub('年|月|日|号|--|——|\.', '-', check_str)
            # 文本为 纯时间 /纯文本
            if not re.search('[^\d-]', check_str):
                return ''
            # 尝试在14位内找到时间
            for i in range(15):
                if suffix_str is not None:
                    break
                prefix_index = 14 - i
                if prefix_index < 2:
                    continue
                check_str = _last_special_tuple[:prefix_index]
                check_str = re.sub('年|月|日|号|--|——|\.', '-', check_str)
                if re.search('[^\d-]', check_str) or len(_last_special_tuple) <= prefix_index:
                    continue
                suffix_str = _last_special_tuple[prefix_index:]
            suffix_str = _last_special_tuple if suffix_str is None else suffix_str
            if suffix_str == _last_special_tuple:
                a = 1
            return suffix_str

        source = paragraph.source
        config = paragraph.config
        # 整句分割
        whole_sentence_list = []
        paragraph.whole_sentence_list = whole_sentence_list
        last_end_index = 0
        # 短句被分组标志下表
        short_sentence_group_index = 0
        # 整句切分列表
        whole_list = [x for x in config.whole_sentence_split_reg.split(paragraph.paragraph_text_replaced) if x]
        for _whole_sentence in whole_list:
            whole_take_str = recover_replace_item(_whole_sentence, paragraph.replace_str_dict)
            start_index = last_end_index + paragraph.paragraph_text[last_end_index:].find(whole_take_str)
            whole_sentence_token_positions = {
                source: [x for x in range(start_index, start_index + len(whole_take_str))]}

            # 整句对象
            whole_obj = WholeSentence({
                "source": source,
                'sentence_text': whole_take_str,
                'token_positions': whole_sentence_token_positions,
                'sentence_start_index': min(whole_sentence_token_positions[source]),
                "belong_to_paragraph": paragraph
            })
            whole_sentence_list.append(whole_obj)
            last_end_index = max(whole_sentence_token_positions[source])
            # 获得短句
            short_sentence_list = []
            whole_obj.short_sentence_list = short_sentence_list
            short_list = [x for x in config.short_sentence_split_reg.split(_whole_sentence) if x]
            # 短句开始 时间 默认是长句的时间
            for _short_sentence in short_list:
                old_short_sentence_group_index = short_sentence_group_index
                short_take_str = recover_replace_item(_short_sentence, paragraph.replace_str_dict)
                short_start_position = start_index + whole_take_str.find(short_take_str)
                short_sentence_token_positions = {source: [x for x in range(short_start_position,
                                                                            short_start_position + len(
                                                                                short_take_str))]}
                get_time_str = _short_sentence if config.get_time_ignore_bracket_and_other else short_take_str
                get_time_str = re.sub('\s', '', get_time_str)
                # 时间表达式、时间表达式
                if config.spilt_short_by_time_and_comma and TimePattern.comma_time_pattern().search(get_time_str):
                    text_list, short_sentence_group_index = split_short_by_comma(get_time_str,
                                                                                 short_sentence_group_index)
                    # 约定匹配的文本 必有后缀 (aaa)?TIME、TIME BBB. BBB 必须存在
                    for _n_short in text_list:
                        short_sentence_list.append(ShortSentence({
                            "source": source,
                            "group": short_sentence_group_index,
                            "sentence_text": _n_short,
                            "token_positions": short_sentence_token_positions,
                            "sentence_start_index": min(short_sentence_token_positions[source]),
                            "belong_to_paragraph": paragraph,
                            "belong_to_whole_sentence": whole_obj,

                        }))
                short_add_dict = {
                    "source": source,
                    "sentence_text": short_take_str,
                    "sentence_start_index": min(short_sentence_token_positions[source]),
                    "token_positions": short_sentence_token_positions,
                    "belong_to_paragraph": paragraph,
                    "belong_to_whole_sentence": whole_obj,
                }
                # 是否被顿号分组了
                if short_sentence_group_index != old_short_sentence_group_index and config.spilt_short_by_time_and_comma:
                    short_add_dict.update({"group_master": short_sentence_group_index})
                short_sentence_list.append(ShortSentence(short_add_dict))

    # MAIN_FUNCTION 切分整句短句 并赋予句子时间
    @staticmethod
    def get_sentence_time(paragraph: Paragraph, abstract_base_time_dict: Dict):

        # 复原被替换的文本
        def recover_replace_item(text: str, _replace_str_dict: Dict) -> str:
            replace_pattern = re.compile('\[REPLACE\d+\]')
            take_str = text
            for _one in replace_pattern.finditer(text):
                middle = text[_one.span()[0]: _one.span()[1]]
                take_str = take_str.replace(middle, _replace_str_dict[middle])
            return take_str

        # 获取文本中的数字 int 或者 中文数字
        def get_num_by_number_or_chinese_to_arabic(text: str) -> int:
            # 中文数字转为数字
            def chinese_to_arabic(cn: str) -> int:
                CN_NUM = {
                    '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
                    '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
                }
                CN_UNIT = {
                    '十': 10,
                    '拾': 10,
                    '百': 100,
                    '佰': 100,
                    '千': 1000,
                    '仟': 1000,
                    '万': 10000,
                    '萬': 10000,
                    '亿': 100000000,
                    '億': 100000000,
                    '兆': 1000000000000,
                }
                unit = 0  # current
                ldig = []  # digest
                for cndig in reversed(cn):
                    if cndig in CN_UNIT:
                        unit = CN_UNIT.get(cndig)
                        if unit == 10000 or unit == 100000000:
                            ldig.append(unit)
                            unit = 1
                    else:
                        dig = CN_NUM.get(cndig)
                        if unit:
                            dig *= unit
                            unit = 0
                        ldig.append(dig)
                if unit == 10:
                    ldig.append(10)
                val, tmp = 0, 0
                for x in reversed(ldig):
                    if x == 10000 or x == 100000000:
                        val += tmp * x
                        tmp = 0
                    else:
                        tmp += x
                val += tmp
                return val

            num = 0.5 if '半' in text else 0
            try:
                num += int(re.search('\d+', text).group())
            except:
                try:
                    num += chinese_to_arabic(
                        re.search('(\d|一|壹|二|两|三|叁|四|肆|五|伍|六|陆|七|柒|八|捌|九|玖|十|拾)+', text).group())
                except:
                    num = 0.5 if '半' in text else None
            return num

        # 时间格式化
        def data_normalize(data_str: str) -> str:
            default_add_time = paragraph.config.incomplete_time_swallow_word

            data_str = re.sub("\-\-|[年月日－\.]", '-', data_str)
            data_str = data_str.replace('--', '-')
            data_str = re.sub("[^\d\-]", '', data_str)
            data_str = data_str[:-1] if data_str.endswith('-') else data_str
            if re.match('^\d{1,2}\-\d{1,2}', data_str) and len(data_str) in (4, 5):
                data_str = '-'.join([default_add_time, data_str.split('-')[0], data_str.split('-')[1]])
            elif re.match('\d{4}\-\d{2}\-\d{3}', data_str) and len(data_str) == 11:
                data_str = '-'.join([data_str[:4], data_str[5:7], data_str[9:]])
            # 20140102
            elif re.match('\d{8}', data_str) and len(data_str) == 8:
                data_str = '-'.join([data_str[:4], data_str[4:6], data_str[6:]])
            # 2014102 2014021
            elif re.match('\d{7}', data_str) and len(data_str) == 7:
                if data_str[4] == "0":
                    data_str = '-'.join([data_str[:4], data_str[4:6], data_str[6:]])
                elif data_str[5:7] <= "12" and data_str[5:7] >= "1" and data_str[6:] <= "31":
                    data_str = '-'.join([data_str[:4], data_str[4:6], data_str[6:]])
                else:
                    data_str = '-'.join([data_str[:4], data_str[4:5], data_str[5:]])
            # 201411
            elif re.match('\d{6}', data_str) and len(data_str) == 6:
                data_str = '-'.join([data_str[:4], data_str[4:5], data_str[5:]])
            # 2014-102 2014-012 2014-0102
            elif re.match('\d{4}-\d{3,4}', data_str):
                if len(data_str) == 9:
                    data_str = '-'.join([data_str[:4], data_str[5:7], data_str[7:]])
                elif data_str[5:6] == '0':
                    data_str = '-'.join([data_str[:4], data_str[5:7], data_str[7:]])
                elif data_str[5:6] <= "12" and data_str[6:] <= "31":
                    data_str = '-'.join([data_str[:4], data_str[5:6], data_str[6:]])
                else:
                    data_str = '-'.join([data_str[:4], data_str[5:7], data_str[7:]])
            # 20141-02 201401-02 20141-1 201401-1
            elif re.match('\d{5,6}-\d{1,2}', data_str) and len(data_str) in (7, 8, 9):
                other, day = data_str.split('-')
                data_str = '-'.join([other[:4], other[4:], day])
            year = data_str.split('-')[0][:4]
            month = data_str.split('-')[1] if data_str.count(
                '-') >= 1 else paragraph.config.incomplete_time_swallow_word
            day = data_str.split('-')[2] if data_str.count('-') >= 2 else paragraph.config.incomplete_time_swallow_word
            month = '0' + month if len(month) == 1 else month
            day = '0' + day if len(day) == 1 else day
            data_str = '-'.join([year, month, day])
            return data_str

        # 获得具体提及的时间
        def get_explicit_time(text_replaced: str, sentence_type: str):
            explicit_time = None
            for patten in TimePattern.explicit_patten_list:
                if patten.search(text_replaced):
                    matching_item = [x for x in patten.finditer(text_replaced)][-1] \
                        if (sentence_type == 'short' and paragraph.config.short_get_last_time) or \
                           (sentence_type == 'whole' and paragraph.config.whole_get_last_time) else \
                        [x for x in patten.finditer(text_replaced)][0]
                    area_min, area_max = matching_item.span()
                    matching_text = matching_item.group()[:-1] if not re.match('\d', matching_item.group()[
                                                                                     :-1]) else matching_item.group()
                    matching_text = data_normalize(matching_text)
                    explicit_time = {"index": area_min, 'end_index': area_max, 'value': matching_text}
                    break
            return explicit_time

        # 获得抽象时间
        def get_abstract_time(text_replaced, _abstract_base_time_dict: Dict, token_positions: Dict, token_flag=True):
            """
            仅获取第一个正确表达的抽象时间 几年前 等
            :param text_replaced:
            :param _abstract_base_time_dict:
            :param token_positions:
            :param token_flag:
            :return:
            """

            default_add_time = paragraph.config.incomplete_time_swallow_word
            _abstract_base_time, _abstract_base_time_source = _abstract_base_time_dict['text'], abstract_base_time_dict[
                'origin']
            abstract_time = None
            abstract_data_pattern = TimePattern.abstract_data_pattern
            if _abstract_base_time:
                for _one_matching in abstract_data_pattern.finditer(text_replaced):
                    # 过滤错误的抽象时间
                    if TimePattern.abstract_error_pattern.match(_one_matching.group()):
                        continue
                    # 溯源
                    area_min, area_max = _one_matching.span()
                    if token_flag:
                        token_positions[_abstract_base_time_source] = [x for x in
                                                                       range(0, len(_abstract_base_time) + 1)]
                    admission_date = str_to_datetime(_abstract_base_time)

                    matching_text = _one_matching.group()
                    num = get_num_by_number_or_chinese_to_arabic(matching_text)
                    level_down = False
                    if num != 0:
                        untime = time.mktime(admission_date.timetuple()) * 1000
                        if isinstance(num, float):
                            level_down = True
                        if '年' in matching_text:
                            admission_date = admission_date.replace(month=1)
                            admission_date = admission_date.replace(day=1)
                            subtractor = relativedelta(years=num) if not level_down else relativedelta(years=int(num),
                                                                                                       months=int(
                                                                                                           0.5 * 12))
                            untime = admission_date - subtractor
                        elif '月' in matching_text:
                            admission_date = admission_date.replace(day=1)
                            subtractor = relativedelta(months=num) if not level_down else \
                                relativedelta(months=int(num),
                                              days=int(
                                                  0.5 * calendar.monthrange(admission_date.year, admission_date.month)[
                                                      1]))
                            untime = admission_date - subtractor
                        elif '日' in matching_text or '天' in matching_text:
                            subtractor = relativedelta(days=num) if not level_down else relativedelta(days=int(num),
                                                                                                      hours=int(
                                                                                                          0.5 * 24))
                            untime = admission_date - subtractor
                        elif '周' in matching_text:
                            subtractor = relativedelta(weeks=num) if not level_down else relativedelta(weeks=int(num),
                                                                                                       days=int(
                                                                                                           0.5 * 7))
                            untime = admission_date - subtractor
                        elif '小时' in matching_text:
                            subtractor = relativedelta(hours=num) if not level_down else relativedelta(hours=int(num),
                                                                                                       minutes=int(
                                                                                                           0.5 * 60))
                            untime = admission_date - subtractor
                        else:
                            # DEBUG
                            untime = admission_date
                    else:
                        # DEBUG
                        untime = admission_date
                    abstract_time = {'index': area_min,
                                     'value': untime.strftime('%Y-%m-%d')}
                    if level_down:
                        abstract_time['value'] = list(abstract_time['value'].split('-'))
                        if '年' in matching_text:
                            abstract_time['value'][1] = default_add_time
                            abstract_time['value'][2] = default_add_time
                        elif '月' in matching_text:
                            abstract_time['value'][2] = default_add_time
                        elif '周' in matching_text:
                            abstract_time['value'][2] = default_add_time
                        abstract_time['value'] = '-'.join(abstract_time['value'])
                    if '年' in matching_text:
                        abstract_time['value'] = '-'.join(
                            [abstract_time['value'].split('-')[0], default_add_time, default_add_time])
                    elif '月' in matching_text:
                        abstract_time['value'] = '-'.join(
                            [abstract_time['value'].split('-')[0], abstract_time['value'].split('-')[1],
                             default_add_time])
                    break
            # TODO 抽象时间是否需要依赖原文进行推断
            # else:
            #     pass
            return abstract_time

        # 一个句子提及了抽象时间 和具体时间，选择
        def choose_from_time(abstract_time, explicit_time):
            default_add_time = paragraph.config.incomplete_time_swallow_word
            mention_time = paragraph.config.default_time
            if abstract_time or explicit_time:
                if abstract_time and explicit_time:
                    # 两个时间 差15位的时候 选择表达信息量更全的
                    if abs(int(abstract_time['index']) - int(explicit_time['index'])) <= 15:
                        if abstract_time['value'].count(default_add_time) < explicit_time['value'].count(
                                default_add_time):
                            mention_time = abstract_time['value']
                        else:
                            mention_time = explicit_time['value']
                    elif int(abstract_time['index']) < int(explicit_time['index']):
                        mention_time = abstract_time['value']
                    else:
                        mention_time = explicit_time['value']
                elif abstract_time:
                    mention_time = abstract_time['value']
                else:
                    mention_time = explicit_time['value']
            return mention_time

        # 一个句子提及了抽象时间 和具体时间，选择
        def choose_from_time_get_earlier(abstract_time: Dict, explicit_time: Dict):
            mention_time = None
            if abstract_time is not None or explicit_time is not None:
                if abstract_time and explicit_time:
                    # 两个时间 差15位的时候 选择表达信息量更全的
                    if int(abstract_time['index']) < int(explicit_time['index']):
                        mention_time = abstract_time['value']
                    else:
                        mention_time = explicit_time['value']
                elif abstract_time:
                    mention_time = abstract_time['value']
                else:
                    mention_time = explicit_time['value']
            return mention_time

        def time_function(last_notice_time: str,
                          get_time_str: str,
                          sentence_token_positions: List,
                          _abstract_base_time_dict: Dict,
                          _source: str,
                          sentence_type: str) -> Tuple[str, Dict[str, List[int]]]:
            mention_time, token_positions = paragraph.config.default_time, sentence_token_positions
            all_time_pattern = re.compile('|'.join(
                [x.pattern for x in TimePattern.explicit_patten_list] + [TimePattern.abstract_data_pattern.pattern] + [
                    x.pattern for x in TimePattern.other_patten_list] + [TimePattern.error_time_patten.pattern]))
            sentence_get_time_flag = True
            # 上一个句子有时间. 且这句没有提及时间,仅做推断用
            if not all_time_pattern.search(get_time_str):
                return last_notice_time, token_positions, False
            # 这句有提及时间
            else:
                # # step1 补时间,当有需要补齐的时间
                # 文本标准化
                get_time_str = re.sub('\s', '', get_time_str)
                # 找到所有可能要补齐的信息。按顺序排序
                change_item = [x for x in TimePattern.month_pattern.finditer(get_time_str)] + \
                              [x for x in TimePattern.day_pattern.finditer(get_time_str)] + \
                              [x for x in TimePattern.month_day_pattern.finditer(get_time_str)] + \
                              [x for x in TimePattern.error_time_patten.finditer(get_time_str)]
                change_item = {x.span()[0]: (x.span()[0], x.span()[1], x.group()) for x in change_item if change_item}
                key_index = [x for x in change_item.keys()]
                key_index.sort()
                _temp_list = []
                for index in key_index:
                    _temp_list.append(change_item[index])
                explicit_time = get_explicit_time(get_time_str, 'any')
                abstract_time = get_abstract_time(get_time_str, _abstract_base_time_dict, token_positions)
                # 抽象的时间,具体的时间 选择出现顺序早的一个,无时间返回None，’2014-01-01‘
                first_mention_time = choose_from_time_get_earlier(abstract_time, explicit_time)
                base_time = last_notice_time if first_mention_time is None else first_mention_time
                get_time_str_backup = get_time_str
                for x in _temp_list:
                    # 判断是否是要补的时间
                    area_min, area_max = x[0], x[1]
                    if get_time_str[area_min - 1] in [str(x) for x in range(0, 10)] + ['年', '月', '日']:
                        continue
                    area_min -= 8
                    area_max += 5
                    area_min = 0 if area_min < 0 else area_min
                    area_max = len(get_time_str) if area_max > len(get_time_str) else area_max
                    area_text = get_time_str[area_min:area_max + 1]
                    # 抽象的时间,具体的时间
                    explicit_time = get_explicit_time(area_text, 'any')
                    abstract_time = get_abstract_time(area_text, _abstract_base_time_dict, token_positions,
                                                      token_flag=False)
                    # 抽象的时间,具体的时间 选择出现顺序早的一个,无时间返回None，’2014-01-01‘
                    mention_time_check = choose_from_time_get_earlier(abstract_time, explicit_time)
                    # 上一个句子有时间,这句有提及时间
                    if mention_time_check is not None:
                        base_time = mention_time_check
                        continue
                    if TimePattern.month_day_pattern.search(x[2]) and base_time != time_default:
                        base_month = base_time.split('-')[1]
                        current_month = data_normalize(x[2]).split('-')[1]
                        if current_month < base_month:
                            base_time = str(int(base_time[:4]) + 1) + base_time[4:]

                    if base_time == time_default and _abstract_base_time_dict['text']:
                        base_time = _abstract_base_time_dict['text']

                    if base_time == time_default:
                        continue
                    area_min, area_max = x[0], x[1]
                    area_text = get_time_str_backup[
                                area_min - 2 if area_min - 2 > 0 else area_min:area_max if area_max < len(
                                    get_time_str_backup) else len(get_time_str_backup)]
                    add_pref = get_time_str_backup[area_min - 2 if area_min - 2 > 0 else area_min:area_min]
                    add_suffix = get_time_str_backup[
                                 area_max:area_max + 2 if area_max + 2 < len(get_time_str_backup) else len(
                                     get_time_str_backup)]
                    new_text = x[2]
                    if TimePattern.month_day_pattern.search(area_text) or TimePattern.month_pattern.search(area_text):
                        add_data = base_time.split("-")[0] + '-'
                    else:
                        add_data = '-'.join([base_time.split("-")[0], base_time.split("-")[1]])
                    if TimePattern.error_time_patten.search(area_text):
                        if last_notice_time != time_default:
                            new_data = data_normalize(f'{last_notice_time[:4]}{"-".join(new_text.split("-")[1:])}')
                        elif _abstract_base_time_dict['text'] != time_default and _abstract_base_time_dict['text']:
                            new_data = data_normalize(
                                f'{_abstract_base_time_dict["text"][:4]}{"-".join(new_text.split("-")[1:])}')
                        else:
                            new_data = data_normalize(f'{base_time[:4]}{"-".join(new_text.split("-")[1:])}')
                    else:
                        new_data = data_normalize(f'{add_data}{new_text}')
                    get_time_str = get_time_str.replace(area_text, f"{add_pref}{new_data}{add_suffix}")
                # step2 获取时间

                # 抽象的时间,具体的时间
                explicit_time = get_explicit_time(get_time_str, sentence_type)
                abstract_time = get_abstract_time(get_time_str, _abstract_base_time_dict, token_positions)
                # 抽象的时间,具体的时间 选择出现顺序早的一个
                mention_time = choose_from_time(abstract_time, explicit_time)
                # token_positions去重 排序
                # for _one, take_list in deepcopy(token_positions).items():
                #     _t_l = []
                #     for _t_list in take_list:
                #         _t_l += _t_list
                #
                #     n_list = list(set(_t_l))
                #     n_list.sort()
                #     token_positions[_one] = n_list
                # _new_time = []
                return mention_time, token_positions, sentence_get_time_flag

        config = paragraph.config
        default_time = config.default_time
        time_default, sentence_start_time = default_time, default_time
        last_sentence_start_time = default_time
        last_whole_short_time_dict = defaultdict(dict)
        all_whole_times = []
        for whole_index, whole_sentence_obj in enumerate(paragraph.whole_sentence_list):
            sentence_text = whole_sentence_obj.sentence_text
            whole_token_positions = whole_sentence_obj.token_positions
            source = whole_sentence_obj.source
            whole_take_str = recover_replace_item(sentence_text, paragraph.replace_str_dict)
            get_time_str = sentence_text if config.get_time_ignore_bracket_and_other else whole_take_str
            sentence_start_time, time_token_positions, sentence_get_time_flag = time_function(
                last_sentence_start_time, get_time_str,
                whole_token_positions,
                abstract_base_time_dict, source, 'whole')
            whole_sentence_obj.sentence_time = sentence_start_time
            whole_sentence_obj.time_token_positions = time_token_positions
            short_times = []
            for short_sentence_index, short_sentence in enumerate(whole_sentence_obj.short_sentence_list):
                sentence_text = short_sentence.sentence_text
                sentence_token_positions = short_sentence.token_positions
                source = short_sentence.source

                short_take_str = recover_replace_item(sentence_text, paragraph.replace_str_dict)
                get_time_str = sentence_text if config.get_time_ignore_bracket_and_other else short_take_str
                # 过滤不必要的时间
                if config.short_time_filter_pattern.pattern and config.short_time_filter_pattern.search(get_time_str):
                    get_time_str = '.'.join(
                        [x for x in re.split(
                            f'((?={config.short_time_filter_pattern.pattern})[\u4e00-\u9fa5A-Za-z\d\、\(\-\)\[\]]*(?=[^\u4e00-\u9fa5A-Za-z\d\-]))|((?={config.short_time_filter_pattern.pattern}).*$)',
                            get_time_str) if x and
                         not config.short_time_filter_pattern.search(x)])
                    if get_time_str:
                        sentence_start_time, time_token_positions, sentence_get_time_flag = time_function(
                            last_sentence_start_time,
                            get_time_str,
                            sentence_token_positions,
                            abstract_base_time_dict, source, 'short')
                    else:
                        sentence_start_time, time_token_positions, sentence_get_time_flag = time_default, sentence_token_positions, False
                else:
                    # 时间表达式、时间表达式
                    sentence_start_time, time_token_positions, sentence_get_time_flag = time_function(
                        last_sentence_start_time,
                        get_time_str,
                        sentence_token_positions,
                        abstract_base_time_dict, source, 'short')
                if sentence_get_time_flag:
                    short_times.append({'time': sentence_start_time,
                                        'lineage': time_token_positions})
                else:
                    short_times.append({'time': time_default,
                                        'lineage': time_token_positions})
                short_sentence.sentence_time = sentence_start_time
                short_sentence.time_token_positions = time_token_positions
                # 仅记上一个提及的有效时间
                if sentence_get_time_flag:
                    last_sentence_start_time = sentence_start_time
            all_whole_times.append(short_times)

        return all_whole_times

    @staticmethod
    def short_sentence_filter(paragraph: Paragraph, all_whole_times: Dict):
        def get_prefix_whole(present_index: int, prefix_index: int, present_short_index: int):
            all_short_times = []
            for _one in all_whole_times:
                all_short_times += _one
            if prefix_index < 0:
                start_index = sum([int(len(x)) for index, x in enumerate(all_whole_times) if index < present_index])
                return all_short_times[:start_index + present_short_index]
            need_index = present_index - prefix_index
            short_list = []
            if need_index >= 0:
                for i in range(need_index, present_index):
                    short_list += all_whole_times[i]
                short_list += all_whole_times[present_index][:present_short_index]
                # start_index = len(short_list)
            else:
                short_list = all_whole_times[present_index][:present_short_index + 1]
                # start_index = len(short_list)
            return short_list

        def get_prefix_short(present_index: int, prefix_index: int, all_short_times: List, get_useful: bool):
            the_time, the_lineage = None, {}
            if prefix_index < 0 and get_useful:
                the_list = [x for x in all_short_times if x['time'] != time_default]
                the_list.reverse()
                the_time = the_list[0]['time'] if the_list else time_default
                the_lineage = the_list[0]['lineage'] if the_list else {}
            elif prefix_index < 0:
                prefix_index = 1
                need_index = present_index - prefix_index
                the_time = all_short_times[need_index]['time'] if need_index >= 0 else \
                    all_short_times[present_index]['time']
                the_lineage = all_short_times[need_index]['lineage'] if need_index >= 0 else \
                    all_short_times[present_index]['lineage']
            elif prefix_index > 0 and not get_useful:
                the_time, the_lineage = all_short_times[-1]['time'], all_short_times[-1]['lineage']
            elif prefix_index > 0 and get_useful:
                the_list = [x for x in all_short_times if x['time'] != time_default]
                the_list.reverse()
                for _one in the_list:
                    the_time = _one['time']
                    the_lineage = _one['lineage']
                    break
                if the_time is None:
                    the_time = time_default
                    the_lineage = {}
            else:
                the_time = time_default
                the_lineage = {}
            return the_time, the_lineage

        def get_prefix_whole_and_short(present_whole_index: int, prefix_whole_index: int, present_short_index: int,
                                       prefix_short_index: int, get_useful: bool):
            if prefix_whole_index == 0:
                the_time, the_lineage = get_prefix_short(present_short_index, prefix_short_index,
                                                         all_whole_times[present_whole_index][:present_short_index + 1],
                                                         get_useful)
            else:
                short_list = get_prefix_whole(present_whole_index, prefix_whole_index,
                                              present_short_index)
                the_time, the_lineage = get_prefix_short(present_short_index, prefix_short_index, short_list,
                                                         get_useful)
            return the_time, the_lineage

        config = paragraph.config
        level = config.short_extent_last_time_level
        if isinstance(level, str):
            # prefix_short prefix_on_whole across_whole whole_first_time whole_last_time
            assert level in ['prefix_short', 'prefix_on_whole', 'across_whole', 'whole_first_time',
                             'whole_last_time'], f'配置的不存在等级:{level}'
            if level == 'prefix_short':
                prefix_whole_num = -1
                prefix_short_num = 1
                get_useful = False
            elif level == 'prefix_on_whole':
                prefix_whole_num = 1
                prefix_short_num = -1
                get_useful = True

        elif isinstance(level, dict):
            prefix_whole_num = level.get('prefix_whole_num', 0)
            prefix_short_num = level.get('prefix_short_num', 1)
            get_useful = level.get('get_useful', False)
        time_default = paragraph.config.default_time
        # 有序的所有时间短句

        for w_index, _whole in enumerate(paragraph.whole_sentence_list):
            for s_index, _short in enumerate(_whole.short_sentence_list):
                if (s_index == 0 and w_index == 0) or all_whole_times[w_index][s_index]['time'] != time_default:
                    continue
                time, lineage = get_prefix_whole_and_short(int(w_index), int(prefix_whole_num),
                                                           int(s_index), int(prefix_short_num), get_useful)
                _short.sentence_time = time
                # for x, data in lineage.items():
                #     if x in _short['token_positions']:
                #         _short['token_positions'][x] += data
                #         _short['token_positions'][x] = list(set(_short['token_positions'][x]))
                #         _short['token_positions'][x].sort()
                # _short['token_position'] = []
