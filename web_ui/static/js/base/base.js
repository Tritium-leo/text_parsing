layui.use('layer', function () {
    var $ = layui.jquery, layer = layui.layer, upload = layui.upload;
});
String.prototype.format = function (args) {
    if (arguments.length > 0) {
        var result = this;
        if (arguments.length == 1 && typeof (args) == "object") {
            for (var key in args) {
                var reg = new RegExp("({" + key + "})", "g");
                result = result.replace(reg, args[key]);
            }
        } else {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i] == undefined) {
                    return "";
                } else {
                    var reg = new RegExp("({[" + i + "]})", "g");
                    result = result.replace(reg, arguments[i]);
                }
            }
        }
        return result;
    } else {
        return this;
    }
};
//替换全部
String.prototype.replaceAll = function (s1, s2) {
    return this.replace(new RegExp(s1.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&'), "gm"), s2);
};

//省略号的内容出现
function show_hide(element) {
    layer.open({
        type: 1,
        offset: 'auto',
        title: false,
        id: 'hide_msg',
        content: '<div style="padding: 50px; line-height: 22px; background-color: #393D49; color: #fff; font-weight: 300;">' + $(element).text() + '</div>',
        scrollbar: true,
        area: ['1500px'],
        shade: 0,
        yes: function () {
            layer.closeAll();
        }
    });
    $('#hide_msg').attr('contenteditable', true).focus();
    $('#hide_msg').blur(function () {
        layer.closeAll();
    })
}

// 弹窗提示
function confirmTrans(msg) {
    layui.use('layer', function () {
        var $ = layui.jquery, layer = layui.layer;
        layer.msg(msg + "（5s自动关闭）", {
            time: 5000,
            btn: ['明白了'],
            end: function (index, layero) {
                layer.close()
            }
        });
    });
}

function reversal_show_status(obj_id) {
    $('#search_condition').toggle()
}

function centerTrans(msg, width = 700, height = 300) {
    layui.use('layer', function () {
        layer.open({
            type: 1
            , offset: 'auto'
            , id: 'layerDemo' + 1
            , content: '<div style="padding: 20px 100px;">' + msg + '</div>'
            , btn: '关闭全部'
            , area: [width + 'px', height + 'px;']
            , btnAlign: 'c' //按钮居中
            , shade: 0 //不显示遮罩
            , yes: function () {
                layer.closeAll();
            }
        });
    });
}

function create_a(href, target = '_blank', id = 'js_a') {
    var a = document.createElement("a");
    a.setAttribute('href', href);
    a.setAttribute('target', target);
    a.setAttribute('id', id);
    //防止反复添加
    if (document.getElementById(id)) {
        document.body.removeChild(document.getElementById(id));
    }
    document.body.appendChild(a);
    return a
}


// 时钟方法
function check(val) {
    if (val < 10) {
        return ("0" + val);
    } else {
        return (val);
    }
}

function displayTime(timeDiv) {
    //获取div元素
    //获取系统当前的年、月、日、小时、分钟、毫秒
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var hour = date.getHours();
    var minutes = date.getMinutes();
    var second = date.getSeconds();
    var timestr = year + "年" + month + "月" + day + "日  " + check(hour)
        + ":" + check(minutes) + ":" + check(second);
    //将系统时间设置到div元素中
    timeDiv.innerHTML = timestr;
}

//判断数据是否为Null或者undefined或者为空字符串
function CheckIsNullOrEmpty(value) {
    //正则表达式用于判斷字符串是否全部由空格或换行符组成
    var reg = /^\s*$/
    //返回值为true表示不是空字符串
    return (value != null && value != undefined && !reg.test(value))

}

//每隔1秒调用一次displayTime函数
function start() {
    var timeDiv = document.getElementById("timeDiv");
    if (CheckIsNullOrEmpty(timeDiv)) {
        window.setInterval("displayTime(timeDiv)", 1000)
    }
}//单位是毫秒


// 全选功能 根据ID,name 将CHECKED变成TRUE
function all_select(ele_id) {
    $('#' + ele_id).click(function () {
        var father_status = $(this).prop('checked');
        var name = $(this).attr('name');
        $('input[name=' + name + ']').each(function () {
            $(this).prop('checked', father_status)
        })
    })
}

// 模拟Post 提交
function post(URL, PARAMS) {
    var temp_form = document.createElement("form");
    temp_form.action = URL;
    temp_form.target = "_blank";
    temp_form.method = "post";
    temp_form.style.display = "none";
    for (var x in PARAMS) {
        var opt = document.createElement("textarea");
        opt.name = x;
        opt.value = PARAMS[x];
        temp_form.appendChild(opt);
    }
    document.body.appendChild(temp_form);
    temp_form.submit();
}

// 时间戳转字符串
function getLocalTime(nS) {
    var the_data_str = new Date(parseInt(nS)).toLocaleString().replace(/:\d{1,2}$/, ' ');
    if ('Invalid Date' === the_data_str) {
        return ''
    } else {
        return the_data_str;
    }
}

// 获得COOKIE
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//删除cookies
function delCookie(name) {
    var exp = new Date();
    // $.cookie(name,null,{ path: '/'});
    exp.setTime(exp.getTime() - 1);
    if (getCookie(name) != null) {
        var cval = getCookie(name);
        document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
    }
}

//写cookies
function setCookie(name, value, time) {
    // $.cookie(name,value, {path:'/',expires:time});
    var exp = time;
    document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString() + ";path=/";
}

// 获取当前时间
function getCurrentDate(format) {
    var now = new Date();
    var year = now.getFullYear(); //得到年份
    var month = now.getMonth();//得到月份
    var date = now.getDate();//得到日期
    var day = now.getDay();//得到周几
    var hour = now.getHours();//得到小时
    var minu = now.getMinutes();//得到分钟
    var sec = now.getSeconds();//得到秒
    month = month + 1;
    if (month < 10) month = "0" + month;
    if (date < 10) date = "0" + date;
    if (hour < 10) hour = "0" + hour;
    if (minu < 10) minu = "0" + minu;
    if (sec < 10) sec = "0" + sec;
    var time = "";
    //精确到天
    if (format == 1) {
        time = year + "-" + month + "-" + date;
    }
    //精确到分
    else if (format == 2) {
        time = year + "-" + month + "-" + date + " " + hour + ":" + minu + ":" + sec;
    }
    return time;
}

//参数n为休眠时间，单位为毫秒:
function sleep(n) {
    var start = new Date().getTime();
    //  console.log('休眠前：' + start);
    while (true) {
        if (new Date().getTime() - start > n) {
            break;
        }
    }
    // console.log('休眠后：' + new Date().getTime());
}

var base_url = 'http://10.25.99.231:9001';
// if (!CheckIsNullOrEmpty(getCookie('JSESSIONID'))) {
//     $.ajax({
//         url: base_url + "/cas_check",
//         async: false,
//         xhrFields: {withCredentials: true},
//         success: function (data) {
//             setCookie('ticket', data.ticket)
//         }
//     })
// }
//
// if (typeof ($('#nickname')) != "undefined" && getCookie('JSESSIONaID') != null) {
//     $.ajax({
//         type: 'post',
//         url: base_url + "/get_user_by_ticket",
//         // dataType: 'jsonp',
//         xhrFields: {withCredentials: true},
//         data: {'ticket': getCookie('JSESSIONID')},
//         async: false,
//         success: function (data) {
//             // console.log(data)
//             if (data.code == '0') {
//                 $('#nickname').attr('value', data.user_id);
//                 $('#nickname').html(data.nickname);
//                 // $('#nickname').after('<div class="dropdown-divider"></div><a class="dropdown-item" href="/background"><i class="ti-settings m-r-5 m-l-5" aria-disabled="true"></i>后台管理</a>')
//                 $('#author').parent().prev().hide();
//                 $('#author').parent().hide();
//                 $('#author').val(data.nickname)
//                 $('#head_portrait').attr('src', data.head_portrait)
//             }
//         }
//     })
// }
window.onload = function () {
    start()
};