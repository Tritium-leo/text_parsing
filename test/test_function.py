from main.main_function import TextParsing
from module.config import Config

if __name__ == '__main__':
    # param 各参数可以查看 MODULE /CONFIG对象注释
    param = {"replace_last_inner_punctuation_to_out": False,
             "ignore_inner_punctuation": False,
             "get_more_time_get_paragraph": False,
             "whole_sentence_split_reg": '[。]',
             "short_sentence_split_reg": "[,，]",
             "get_sentence_time": True,
             "spilt_short_by_time_and_comma": False,
             "whole_get_last_time": False,
             "short_get_last_time": False,
             "short_time_filter_pattern": "",
             "short_extent_last_time_level": {"prefix_short_index": -1,
                                              "prefix_whole_index": -1,
                                              "get_useful": True},
             "get_time_ignore_bracket_and_other": False,
             "incomplete_time_swallow_word": "TIME_UNKNOWN",
             "default_time": "MISSING"
             }
    split_text = {
        "text": "患者自述7个月前无明显诱因出现咳嗽、咳痰，痰为白色泡沫样痰，量少易咳出。间断有痰中带血，量少。曾在当地医院就诊行胸部CT检查提示左肺包块，给予抗感染治疗咳嗽咯血症状消失。同时行纤维支气管镜检查未能明确诊断。2月前上述症状再次出现，伴有咳黄色粘痰，遂再次到四川省人民医院就诊，考虑肺脓肿给予头孢克洛口服治疗，疗程2月。11月27日复查胸部CT提示左肺块影较前明显增大，为求进一步诊断，于今日入我院就诊。患病来，患者精神状况良，大小便正常，睡眠正常，体重无明显变化。",
        "origin": "table1|column1"}
    # 抽象时间可以做时间的推断  如 7月前
    abstract_base_datetime = {"text": "2021-02-22",
                              "origin": "table1|column2"}
    result = TextParsing.execute(param, split_text, abstract_base_datetime)

    for one in result.whole_sentence_list:
        print(one)

    pass
