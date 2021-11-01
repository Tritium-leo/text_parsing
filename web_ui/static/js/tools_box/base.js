function load_database_url_choose() {
    $.ajax({
        url: '/get_all_database_url',
        success: function (data) {
            if (data.code == 0) {
                $('#database_url_choose').select2({
                    placeholder: "请选择",
                    data: data.data
                });
                $('#database_url_choose').val(data.data[0].id).trigger('change');
            } else {
                confirmTrans('加载数据库链接出错');
            }
        }
    })

}

function load_databases() {
    $('#database_choose').empty();
    $('#paragraph_source').empty();
    var database_url = $('#database_url_choose').select2().val();
    if (!CheckIsNullOrEmpty(database_url)) {
        return
    }
    $.ajax({
        url: '/get_all_database',
        data: {"database_url": database_url},
        success: function (data) {
            if (data.code == 0) {
                $('#database_choose').select2({
                    placeholder: "请选择",
                    data: data.data
                });
                $('#database_choose').select2('val', "");
                $('#paragraph_source').select2('val', "");
                get_paragraph_source();
            } else {
                confirmTrans('加载数据库出错');
            }
        }
    })
}

function get_paragraph_source() {
    $('#paragraph_source').empty();
    var database = $('#database_choose').select2().val();
    var database_url = $('#database_url_choose').select2().val();
    if ((!CheckIsNullOrEmpty(database)) || (!CheckIsNullOrEmpty(database_url))) {
        return;
    }
    $.ajax({
        url: '/get_paragraph_source',
        data: {
            'database': database,
            "database_url": database_url
        },
        success: function (data) {
            if (data.code == 0) {
                $('#paragraph_source').select2({
                    placeholder: "选择原文",
                    data: data.paragraph
                })
                if (CheckIsNullOrEmpty($('#abstract_source'))) {
                    $('#abstract_source').select2({
                        placeholder: "选择抽象时间",
                        data: data.abstract_time
                    })
                }

            } else {
                confirmTrans('加载该数据库数据出错')
            }
        }
    })
}