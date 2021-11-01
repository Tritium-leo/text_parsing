var script1 = document.createElement('script');//创建script标签节点
script1.setAttribute('type', 'text/javascript');//设置script类型
script1.setAttribute('src', '/static/js/base/global.js');//设置js地址
script1.setAttribute('charset', 'utf-8');
document.body.appendChild(script1);//将js追加为body的子标签
function get_user_unread_message() {
    var user_id = $('#nickname').attr('value')
    if (!CheckIsNullOrEmpty(user_id)) {
        return
    }
    $.ajax({
        url: base_url + "/user_center/get_user_unread_message",
        xhrFields: {withCredentials: true},
        data: {"user_id": user_id.trim()},
        success: function (data) {
            if (data.code == '0') {
                var add_flag = false
                $('a[href="/user_center/message_list"][class="dropdown-item"]').each(function () {
                    var inner_html = $(this).html()
                    if (inner_html.startsWith('未读消息') && data.unread_num != 0) {
                        add_flag = true
                        var add_html = "<span class=\"layui-badge\">" + data.unread_num + "</span>"
                        $(this).html('未读消息' + add_html)
                    } else if (inner_html.startsWith('未读错误消息') && data.unread_error_num != 0) {
                        add_flag = true
                        var add_html = "<span class=\"layui-badge\">" + data.unread_error_num + "</span>"
                        $(this).html('未读错误消息' + add_html)
                    }
                })
                if ($('#message_bell').next('span').length > 0 && add_flag) {

                } else if (add_flag) {
                    add_html = '<span class="layui-badge-dot"></span>'
                    $('#message_bell').after(add_html)
                }
            } else {
                confirmTrans('查询消息出错')
            }
        }
    })

}

function reset_global_normal() {
    var can_change_url_reg = new RegExp('query_list|list_page|index|^\/$')
    if (can_change_url_reg.test(window.location.pathname)) {
        let normal_open = layer.open({
            type: 1
            , title: '重新选择项目'
            , offset: '50px'
            , shadeClose: true
            , area: ['650px', '800px']
            , id: 'project_list_form'
            , btnAlign: 'c'
            , moveType: 1
            , content: $('#reset_project_hide_form')
        });
    } else {
        confirmTrans('当前页面不支持切换数据库')
    }
}

function change_db_choose() {
    script1.onload = script1.onreadystatechange = function () {
        var data = get_projects();
        layui.use(['table', 'form'], function () {
            var table = layui.table, layer = layui.layer;
            var normal_db_table = table.render({
                elem: '#project_list'
                , data: data
                , loading: true
                , cols: [[
                    {field: "project_id", title: "hide_column", hide: true, width: 0}
                    , {type: 'numbers', title: '序号', width: 30, minWidth: 30}
                    , {field: 'project_name', title: '项目名称'}
                ]]
            });
            var current_project = getCookie('project_id');
            // 没有选择项目，默认用第一个
            if (!CheckIsNullOrEmpty(current_project)) {
                var row_data = data[0];
                current_project = row_data.project_id;
                set_project(row_data.project_name, current_project);
            } else {
                for (var i = 0; i < data.length; i++) {
                    var row_data = data[i];
                    if (row_data.project_id == current_project) {
                        current_project = row_data.project_id;
                        set_project(row_data.project_name, row_data.project_id);
                    }
                }
                if (!CheckIsNullOrEmpty(current_project)) {
                    delCookie('project_id');
                    change_db_choose();
                    return;
                }
            }
            table.on('row(project_list_filter)', function (obj) {
                var project_id = obj.data.project_id;
                var project_name = obj.data.project_name;
                layer.closeAll()
                layer.open({
                    type: 1,
                    title: false,
                    closeBtn: false,
                    area: '300px;',
                    shade: 0.8,
                    id: 'LAY_layuipro',
                    btn: ['确认切换', '取消'],
                    btnAlign: 'c',
                    moveType: 1,
                    content: '<div style="padding: 50px; line-height: 22px; background-color: #393D49; color: #fff; font-weight: 300;">是否切换到项目:' + obj.data.project_name + '<br><br></div>',
                    success: function (layero) {
                        var btn = layero.find('.layui-layer-btn');
                        btn.find('.layui-layer-btn0').click(function () {
                            set_project(project_name, project_id);
                            layer.closeAll();
                            page_init();
                        })
                    }
                });
            })
        })
    }
}

function set_project(project_name, project_id) {
    delCookie('project_id');
    setCookie('project_id', project_id, new Date(new Date().getTime() + 30 * 24 * 60 * 60 * 1000));
    $('#current_project').html('当前项目:' + project_name + ' <i class="fa fa-angle-down"></i>');
    $('#current_project').attr('project_id', project_id);
    $('div[lay-id="project_list"] .layui-btn-success').each(function () {
        $(this).removeClass('layui-btn-success')
    });
    $('div[lay-id="project_list"] td[data-field="project_id"] div:contains("' + project_id.toString() + '")').eq(0).parents('tr').addClass('layui-btn-success')
    return project_id
}

function base_page_init() {
    // get_user_unread_message();
    // change_db_choose();
    layui.use('element', function () {
        var element = layui.element; //导航的hover效果、二级菜单等功能，需要依赖element模块

        //监听导航点击
        element.on('nav(demo)', function (elem) {
            //console.log(elem)
            layer.msg(elem.text());
        });
    });
    $('.head_navigation').each(function () {
        if (window.location.pathname.indexOf($(this).children('a').eq(0).attr('href')) >= 0) {
            $(this).addClass('layui-this')
        }
    })
}

base_page_init()