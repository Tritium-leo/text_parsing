var script1 = document.createElement('script');//创建script标签节点
script1.setAttribute('type', 'text/javascript');//设置script类型
script1.setAttribute('src', '/static/js/tools_box/base.js');//设置js地址
script1.setAttribute('charset', 'utf-8');
document.body.appendChild(script1);//将js追加为body的子标签
var list_table = $("#zero_config");

function page_init() {
    $('#by_json').hide();
}

function get_param() {
    var post_data = null;
    if ($('input[name="choose_param_type"]:checked').val() == 'hand' ? true : false) {
        post_data = {
            "paragraph_source_value": $('#paragraph_source_value').val(),
            "abstract_source_value": $('#abstract_source_value').val(),
            "paragraph_source": $('#paragraph_source').val(),
            "abstract_source": $('#abstract_source').val(),

            "ignore_inner_punctuation": $('input[name="ignore_inner_punctuation"]:checked').val() == 'true' ? true : false,
            "replace_last_inner_punctuation_to_out": $('input[name="replace_last_inner_punctuation_to_out"]:checked').val() == 'true' ? true : false,
            "get_more_time_get_paragraph": $('input[name="get_more_time_get_paragraph"]:checked').val() == 'true' ? true : false,
            "whole_sentence_split_reg": $('#whole_sentence_split_reg').val(),
            "short_sentence_split_reg": $('#short_sentence_split_reg').val(),
            "get_sentence_time": $('input[name="get_sentence_time"]:checked').val() == 'true' ? true : false,
            "spilt_short_by_time_and_comma": $('input[name="spilt_short_by_time_and_comma"]:checked').val() == 'true' ? true : false,
            "whole_get_last_time": $('input[name="whole_get_last_time"]:checked').val() == 'true' ? true : false,
            "short_get_last_time": $('input[name="short_get_last_time"]:checked').val() == 'true' ? true : false,
            "short_time_filter_pattern": $('#short_time_filter_pattern').val(),
            "get_time_ignore_bracket_and_other": $('input[name="get_time_ignore_bracket_and_other"]:checked').val() == 'true' ? true : false,
            "prefix_whole_num": parseInt($('#prefix_whole_num').val()),
            "prefix_short_num": parseInt($('#prefix_short_num').val()),
            "get_useful": $('input[name="get_useful"]:checked').val() == 'true' ? true : false,
        };
    } else {
        post_data = {
            "paragraph_source_value": $('#paragraph_source_value').val(),
            "abstract_source_value": $('#abstract_source_value').val(),
            "paragraph_source": $('#paragraph_source').val(),
            "abstract_source": $('#abstract_source').val(),

            'json_data': $('#json_text_area').val().replaceAll('\n', '')
        };
    }
    return post_data;
}

function process_param() {
    var post_data = get_param();
    post_data.download_config = true
    post_data = JSON.stringify(post_data)
    $.ajax({
        url: '/data_viewer/search_text_parsing_result',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json;charset=UTF-8',
        data: post_data,
        success: function (data) {
            if (data.code == 0) {
                $('#param').JSONView(data.param);
                $('#param').JSONView('expand');
            } else {
                confirmTrans('生成失败');
            }
        }
    })
}

function find_result(element) {
    $(element).text('解析中').addClass('btn-secondary').removeClass('btn-success').attr('disabled', true)
    var post_data = get_param();
    post_data = JSON.stringify(post_data);

    $.ajax({
        url: '/data_viewer/search_text_parsing_result',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json;charset=UTF-8',
        data: post_data,
        success: function (data) {
            if (data.code === 0) {
                $('#case_id').text(data.dimension_id)
                $('#origin_text').text(data.origin_text)
                $('#abstract_time').text(data.abstract_time)

                var add_html = ''
                for (i_index in data.split_result) {
                    var _whole = data.split_result[i_index];

                    add_html += '<div class="children1" title = "' + _whole.time + '">'
                    for (_j_index in _whole.shorts) {
                        _short = _whole.shorts[_j_index]
                        add_html += "<div class='children2' title='" + _short.time + "'>" + _short.text + "</div>"
                    }
                    add_html += '</div>'
                }
                $('#json_renderer').html(add_html)
                $(element).text('解析').addClass('btn-success').removeClass('btn-secondary').attr('disabled', false);

            } else if (data.code == -1) {
                $('#case_id').text(data.dimension_id)
                $('#origin_text').text(data.origin_text)
                $('#abstract_time').text(data.abstract_time)
                $('#json_renderer').html('')
                $(element).text('解析').addClass('btn-success').removeClass('btn-secondary').attr('disabled', false)
            } else {
                $('#case_id').text('')
                $('#origin_text').text('')
                $('#abstract_time').text('')
                $('#json_renderer').html('')
                confirmTrans('缺少必要参数,请检查')
                $(element).text('解析').addClass('btn-success').removeClass('btn-secondary').attr('disabled', false)
            }

        }
    })

}

script1.onload = script1.onreadystatechange = function () {
    page_init();
}