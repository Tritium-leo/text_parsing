from datetime import timedelta
from flask import Flask, jsonify
from web_ui.core.buleprint import api
import os


def create_app():
    os.environ['PYTHONHASHSEED'] = '0'
    init_app = Flask(__name__,
                     template_folder='templates',
                     static_folder="static")
    init_app.config.update(
        JSON_AS_ASCII=False
    )
    # CORS(init_app, supports_credentials=True)  # 设置跨域
    # 设置缓存保存时间
    init_app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=0)
    return init_app


if __name__ == '__main__':
    # 初始化
    app = create_app()
    app.register_blueprint(api)

    app.run(
        host='0.0.0.0',
        port=os.environ.get('APP_PORT', 8200),
        debug=True)
