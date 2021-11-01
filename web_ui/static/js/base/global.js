function get_hospitals() {
    var hospitals = new Array();
    $.ajax({
        url: base_url + "/metadata/hospital",
        xhrFields: {withCredentials: true},
        type: 'get',
        async: false,
        success: function (data) {
            if (data.code == "0") {
                hospitals = data.data
            } else {
                confirmTrans('加载医院异常')
            }

        }
    })
    return hospitals
}

function get_users() {
    var users = new Array();
    $.ajax({
        url: base_url + "/system/user",
        xhrFields: {withCredentials: true},
        type: 'get',
        async: false,
        success: function (data) {
            if (data.code == "0") {
                users = data.data
            } else {
                confirmTrans('加载用户异常')
            }
        }
    })
    return users
}

function get_projects() {
    var projects = new Array();
    $.ajax({
        url: base_url + "/metadata/project",
        xhrFields: {withCredentials: true},
        type: 'get',
        async: false,
        success: function (data) {
            if (data.code == "0") {
                projects = data.data
            } else {
                confirmTrans('加载项目异常')
            }
        }
    })
    return projects
}

function get_normal_db() {
    var normal_db_= new Array();
    $.ajax({
        url: base_url + "/metadata/normal_db",
        xhrFields: {withCredentials: true},
        type: 'get',
        async: false,
        success: function (data) {
            if (data.code == "0") {
                normal_db_ = data.data
            } else {
                confirmTrans('加载NORMAL_DB_VERISON异常')
            }
        }
    })
    return normal_db_
}

function get_diseases() {
    var diseases = new Array();
    $.ajax({
        url: base_url + "/metadata/disease",
        xhrFields: {withCredentials: true},
        type: 'get',
        async: false,
        success: function (data) {
            if (data.code == "0") {
                diseases = data.data
            } else {
                confirmTrans('加载癌种异常')
            }
        }
    });
    return diseases
}