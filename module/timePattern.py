from typing import *
import re

# 1800-2199年
class TimePattern(object):
    year_pattern = re.compile('(1[8-9][0-9][0-9]|2[0-1][0-9][0-9])\s{0,2}年')
    # 完整年月日
    hole_data_pattern = re.compile(
        '(1[8-9][0-9][0-9]|2[0-1][0-9][0-9])\s?[年\.\-－]{1,2}\s?(1[0-2]|[0]?[1-9])\s?[月\-－\.]{1,2}\s?([0]?3[0-1]|[0]?[12][0-9]|[0]?[1-9])(日|号)?[^\d]')
    # 有年分割符 的年月日
    hole_data_pattern2 = re.compile(
        '(1[8-9][0-9][0-9]|2[0-1][0-9][0-9])\s?[年\.\-－]{1,2}\s?(1[0-2]|[0]?[1-9])\s?(3[0-1]|[12][0-9]|[0]?[1-9])(日|号|(?!\d|[A-Z]|[a-z]))')
    # 有月分割符的年月日
    hole_data_pattern3 = re.compile(
        '(1[8-9][0-9][0-9]|2[0-1][0-9][0-9])\s?(1[0-2]|[0]?[1-9])\s?[月\-－\.]{1,2}\s?(3[0-1]|[12][0-9]|[0]?[1-9])(日|号)?[^\d]')
    # 无分隔符的年月日
    hole_data_pattern4 = re.compile(
        '(1[8-9][0-9][0-9]|2[0-1][0-9][0-9])\s?(1[0-2]|[0]?[1-9])\s?(3[0-1]|[12][0-9]|[0]?[1-9])(日|号)?[^\d]')
    # 年月
    year_month_pattern = re.compile('(1[8-9][0-9][0-9]|2[0-1][0-9][0-9])\s?[年\.\-－]\s?([0]?[1-9]|[1][0-2])\s?月?[^\d]')
    year_month_pattern2 = re.compile('(1[8-9][0-9][0-9]|2[0-1][0-9][0-9])\s?[年\.\-－]?\s?([0]?[1-9]|[1][0-2])\s?月')

    explicit_patten_list = [hole_data_pattern, hole_data_pattern2, hole_data_pattern3, year_month_pattern2,
                            year_month_pattern, year_pattern, hole_data_pattern4]
    # XX年 XX月 XX日
    month_pattern = re.compile('(,|，|、|。|^)(0[1-9]|1[0-2]|[1-9])\s{0,2}月')
    month_pattern2 = re.compile('(0[1-9]|1[0-2]|[1-9])\s{0,2}月')
    day_pattern = re.compile('(,|，|、|。|^)(3[0-1]|2[0-9]|1[0-9]|0[1-9]|[1-9])\s{0,2}(号|日)')
    # XX月XX日
    month_day_pattern = re.compile(
        '(0?[1-9]|1[0-2])\s?月\s?(3[0-1]|[12][0-9]|[0]?[1-9])\s?(号|日)?|(0?[1-9]|1[0-2])\s?(月|-{1,2}|－{1,2}|\.)\s?(3[0-1]|[12][0-9]|[0]?[1-9])\s?(号|日)|[^a-zA-Z](0?[1-9]|1[0-2])[\-月—](3[0-1]|[12][0-9]|[0]?[1-9])(号(?!基)|日|$)')
    month_day_pattern2 = re.compile(
        '((0?[1-9]|1[0-2])\s?月\s?(3[0-1]|[12][0-9]|[0]?[1-9])\s?(号|日)?|(0?[1-9]|1[0-2])\s?(月|-{1,2}|－{1,2}|\.)\s?(3[0-1]|[12][0-9]|[0]?[1-9])\s?(号|日))')
    abstract_data_pattern = re.compile(
        '近?(\d|半|一|壹|二|两|三|叁|四|肆|五|伍|六|陆|七|柒|八|捌|九|玖|十|拾)+(\+|余|个)?半?多?(年|月|周|天|日|小时)\+?(多前|余前|余|前)')
    abstract_error_pattern = re.compile('\d{4,}年|\d{3,}月|\d{4,}(天|日)')
    other_patten_list = [year_pattern, month_pattern, day_pattern, month_day_pattern]

    error_time_patten = re.compile(
        '([^\d]|^)\d{3}\s?[年\.\-－]{1,2}\s?(1[0-2]|[0]?[1-9])\s?[月\-－\.]{1,2}\s?(3[0-1]|[12][0-9]|[0]?[1-9])[^\d]')

    # 时间、时间
    # @property
    # def comma_time_pattern(self):
    #     return self._comma_time_pattern
    #
    # @comma_time_pattern.setter
    @staticmethod
    def comma_time_pattern():
        middle_pattean = ".*?、.*?"
        new_pattern_list = []
        for one in TimePattern.explicit_patten_list + [TimePattern.month_day_pattern2, TimePattern.month_pattern2]:
            for _one in TimePattern.explicit_patten_list + [TimePattern.month_day_pattern2, TimePattern.month_pattern2]:
                prefix_pattern = one.pattern if not one.pattern.endswith('[^\d]') else one.pattern[:-5]
                suffix_pattern = _one.pattern if not _one.pattern.endswith('[^\d]') else _one.pattern[:-5]
                new_pattern_list.append(f"({prefix_pattern}{middle_pattean}{suffix_pattern})")
        return re.compile('|'.join(new_pattern_list))

    @staticmethod
    def comma_time_pattern_small():
        middle_pattean = "(.)"
        new_pattern_list = []
        for one in TimePattern.explicit_patten_list:
            prefix_pattern = one.pattern if not one.pattern.endswith('[^\d]') else one.pattern[:-5]
            new_pattern_list.append(f"{prefix_pattern}{middle_pattean}\d+")
        return re.compile('|'.join(new_pattern_list))
        # self._comma_time_pattern = re.compile('|'.join(new_pattern_list))
