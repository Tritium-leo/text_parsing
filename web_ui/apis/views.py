# 官方
import json, re
# 第三方
from flask import render_template, request, jsonify
# 自己
from web_ui.core.buleprint import api
from main.main_function import TextParsing


# INDEX
@api.route('/data_viewer')
def data_viewer_index1():
    return render_template('/data_viewer/data_viewer.html')


# INDEX
@api.route('/index')
def data_viewer_index():
    return render_template('/data_viewer/data_viewer.html')


# INDEX
@api.route('/')
def index():
    return render_template('/data_viewer/data_viewer.html')


@api.route('/data_viewer/search_text_parsing_result', methods=['POST'])
def search_text_parsing_result():
    code, msg = 0, 'ok'
    origin_text = ''
    abstract_time = ''
    dimension_id = ''
    _filter_result = []
    try:

        paragraph_source_value = request.json.get('paragraph_source_value')
        paragraph_source = request.json.get('paragraph_source')
        abstract_source_value = request.json.get('abstract_source_value')
        abstract_source = request.json.get('abstract_source')

        if 'json_data' in request.json:
            param = json.loads(request.json['json_data'])
            if paragraph_source:
                param.update({"split_text": paragraph_source,
                              "abstract_datetime": abstract_source})
        else:
            param = {"split_text": paragraph_source,
                     "abstract_datetime": abstract_source}
            param.update(request.json)
            if param.get('get_sentence_time', False):
                param['short_extent_last_time_level'] = {"prefix_whole_num": int(param.pop('prefix_whole_num', -1)),
                                                         "prefix_short_num": int(param.pop('prefix_short_num', -1)),
                                                         "get_useful": param.pop('get_useful', True)}
            else:
                param['short_extent_last_time_level'] = {"prefix_whole_num": -1,
                                                         "prefix_short_num": -1,
                                                         "get_useful": True}

        # 生成配置文件
        if param.pop('download_config', False) or request.json.pop('download_config', False):
            for pop_key in (
                    'database', 'database_url', 'dimension_id', 'paragraph_source_value', 'abstract_source_value'):
                if pop_key in param:
                    param.pop(pop_key)
            return jsonify({"code": code, "param": param})
        # param check
        for key in ('split_text', 'abstract_datetime'):
            if not request.json.get(key) and not param.get(key):
                return jsonify({"code": -2})

        split_text = {"origin": paragraph_source,
                      "text": paragraph_source_value}
        abstract_base_datetime = {"origin": abstract_source,
                                  "text": abstract_source_value}

        def esc_code_change(string: str):
            special_code_map = {"&lt;": '<',
                                "&gt;": '>',
                                "&amp;": '&',
                                "&quot;": '"',
                                "&copy;": '©'}
            for old, replace in special_code_map.items():
                string = re.sub(old, replace, string)
            return string

        origin_text = esc_code_change(paragraph_source_value)
        _filter_result = []
        for _whole in TextParsing.execute(param, split_text, abstract_base_datetime).whole_sentence_list:
            _n_short = []
            for _short in _whole.short_sentence_list:
                _n_short.append({"text": _short.sentence_text,
                                 "time": _short.sentence_time})
            _filter_result.append({"text": _whole.sentence_text,
                                   'time': _whole.sentence_time,
                                   'shorts': _n_short})
    except:
        code = -1

    return jsonify(
        {"code": code,
         'origin_text': origin_text,
         "abstract_time": abstract_source_value,
         "split_result": _filter_result,
         "dimension_id": dimension_id})
