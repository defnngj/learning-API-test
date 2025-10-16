import base64
import hashlib
import json
import os
import time
from html import escape
from random import randint
from time import sleep

from Crypto.Cipher import AES  # 请安装 Crypto
from flask import Flask
from flask import jsonify
from flask import request
from flask import send_from_directory
from flask import session
from werkzeug.utils import secure_filename

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = BASE_PATH + '/uploads'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "json"]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'please-generate-a-random-secret_key'


# === 实现 httpbin 风格的接口 ===

@app.route('/get', methods=['GET'])
def httpbin_get():
    return jsonify({
        "args": dict(request.args),  # 查询参数
        "headers": dict(request.headers),  # 请求头（去掉末尾空行）
        "method": request.method,
        "origin": request.remote_addr,  # 客户端 IP
        "url": request.url
    })


@app.route('/post', methods=['POST'])
def httpbin_post():
    # 区分 form-data/x-www-form-urlencoded 和 JSON
    if request.is_json:
        json_data = request.get_json()
    else:
        json_data = None

    return jsonify({
        "args": dict(request.args),
        "data": request.get_data(as_text=True),  # 原始请求体字符串
        "form": dict(request.form),  # 表单数据
        "json": json_data,  # JSON 数据（如果存在）
        "headers": dict(request.headers),
        "method": request.method,
        "origin": request.remote_addr,
        "url": request.url
    })


@app.route('/put', methods=['PUT'])
def httpbin_put():
    if request.is_json:
        json_data = request.get_json()
    else:
        json_data = None

    return jsonify({
        "args": dict(request.args),
        "data": request.get_data(as_text=True),
        "json": json_data,
        "headers": dict(request.headers),
        "method": request.method,
        "origin": request.remote_addr,
        "url": request.url
    })


@app.route('/delete', methods=['DELETE'])
def httpbin_delete():
    if request.is_json:
        json_data = request.get_json()
    else:
        json_data = None

    return jsonify({
        "args": dict(request.args),
        "data": request.get_data(as_text=True),
        "json": json_data,
        "headers": dict(request.headers),
        "method": request.method,
        "origin": request.remote_addr,
        "url": request.url
    })


def response(code=None, message=None, data=None):
    """
    定义返回参数统一格式
    """
    if data is None:
        data = []
    if code is None:
        code = 10200
    if message is None:
        message = "success"
    sleep(2)
    return jsonify({"code": code, "message": message, "data": data})


class Number:
    n = 0


# 最简单的json格式返回
@app.route('/')
def hello_world():
    return response(message="Welcome to API testing")


# 简单的计数器, 每次请求+1
@app.route('/add_one')
def add_one():
    Number.n = Number.n + 1
    return response(data={"number": Number.n})


# 通过 URI 传参
@app.route('/user/<username>')
def user(username):
    msg = "hello, {}".format(username)
    return response(message=msg)


# 根据用户id返回数据
@app.route('/id/<int:uid>', methods=["GET", "POST"])
def get_uid(uid):
    if request.method == "GET":
        user_info = {"id": 1, "name": "tom", "age": 22}
        if uid != 1:
            return response(10102, "user id null")
        else:
            return response(data=user_info)
    else:
        return response(10101, "request method error")


# 一般的get传参方式,
@app.route("/search/", methods=["GET", "POST"])
def get_search():
    if request.method == "GET":
        search_word = request.args.get('q', '')
        if search_word == "selenium":
            data_list = ["selenium教程", "seleniumhq.org", "selenium环境安装"]
        else:
            data_list = []
        return response(data=data_list)
    else:
        return response(10101, "request method error")


# post请求， from-data/x-www-from-urlencode参数方式
@app.route('/login', methods=["GET", "POST"])
def post_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username is None or password is None:
            return response(10102, "username or password is None")
        elif username == "" or password == "":
            return response(10103, "username or password is null")
        elif username == "admin" and password == "a123456":
            return response(10200, "login success")
        else:
            return response(10104, "username or password error")
    else:
        return response(10101, "request method error")


# post请求，json参数方式
@app.route('/add_user', methods=["GET", "POST"])
def post_add_user():
    if request.method == "POST":
        try:
            data = json.loads(request.get_data())
        except json.decoder.JSONDecodeError:
            return response(10105, "format error")

        try:
            name = data["name"]
            age = data["age"]
            height = data["height"]
        except KeyError:
            return response(10102, "key null")
        else:
            if name == "":
                return response(10103, "name null")
            elif name == "tom":
                return response(10104, "name exist")
            else:
                data = {"name": name, "age": age, "height": height}
                return response(10200, "add success", data)
    else:
        return response(10101, "request method error")


# 获取 header 信息处理
@app.route('/header', methods=['GET', 'POST'])
def post_header():
    if request.method == 'POST':
        token = request.headers.get("token")
        ct = request.headers.get("Content-Type")
        return response(10200, "header ok!", {"token": token, "Content-Type": ct})
    else:
        return response(10101, "request method error")


# Base Auth认证  ["Basic","YWRtaW46YWRtaW4xMjM="]
@app.route('/auth', methods=['GET', 'POST'])
def post_auth():
    if request.method == 'POST':
        auth = request.headers.get("Authorization")
        if auth is None:
            return response(10101, "Authorization None")
        else:
            auth = auth.split()
            auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
            userid, password = auth_parts[0], auth_parts[2]
            if userid == "" or password == "":
                return response(10102, "Authorization null")

            if userid == "admin" and password == "admin123":
                return response(10200, "Authorization success!")
            else:
                return response(10103, "Authorization fail!")
    else:
        return response(10101, "request method error")


# 文件后缀名的判断
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 文件上传的接口
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return response(10200, "upload success!")
        else:
            return response(10102, "file type error!")

    else:
        return response(10101, "request method error")


# 文件下载接口
@app.route("/download", methods=['GET'])
def download_file():
    if request.method == "GET":
        return send_from_directory("./uploads", filename="log.txt", as_attachment=True)

    else:
        return jsonify({"code": 10101, "message": "request method error"})


# 一个URL, 根据不同的方法做不同的处理
@app.route('/phone/<int:pid>', methods=['GET', 'POST', "PUT", "DELETE"])
def more_used(pid):
    if request.method == 'GET':
        if pid == 1:
            phone_info = {
                "id": pid,
                "name": "小米手机",
                "price": 1999
            }
            return response(10201, "get success", phone_info)
        else:
            return response(10101, "The phone id is empty")

    elif request.method == "PUT":
        if pid == 1:
            name = request.form.get('name')
            price = request.form.get('price')
            phone_info = {
                "id": pid,
                "name": name,
                "price": price
            }
            return response(10202, "update success", phone_info)
        else:
            return response(10102, "The updated phone id is empty")

    elif request.method == "DELETE":
        if pid == 1:
            return response(10203, "delete success")
        else:
            return response(10103, "The deleted phone id is empty")

    return response(10104, "request method error")


# 通过Session 记录登录状态
@app.route("/user_login", methods=['POST'])
def session_login():
    username = request.form['username']
    password = request.form['password']
    if username != "" and password != "":
        session['username'] = username
        return response(10200, 'login success')
    else:
        return response(10200, 'login faile')


@app.route("/user_data")
def session_user_data():
    if 'username' in session:
        username = format(escape(session['username']))
        return response(10200, 'hello, {}'.format(username))
    return response(10200, 'hello, stranger')


# 接口的依赖
@app.route('/get_activity', methods=["GET", "POST"])
def get_activity():
    if request.method == "GET":
        activity_info = {"id": 1, "name": "618抽奖活动"}
        return response(10200, "success", activity_info)
    else:
        return response(10101, "request method error")


@app.route('/get_user', methods=["GET", "POST"])
def get_user():
    if request.method == "GET":
        user_info = {"id": 1, "name": "张三"}
        return response(10200, "success", user_info)
    else:
        return response(10101, "request method error")


@app.route('/lucky_number', methods=["GET", "POST"])
def get_lucky_number():
    if request.method == "POST":
        activity_id = request.form.get('aid')
        user_id = request.form.get('uid')

        if activity_id is None or user_id is None:
            return response(10102, "username or password is None")

        elif activity_id == "" or user_id == "":
            return response(10103, "username or password is null")

        if int(activity_id) != 1:
            return response(10104, "activity id exist")

        if int(user_id) != 1:
            return response(10105, "user id not exist")

        number = randint(10000, 99999)
        return response(10200, "Lucky draw number", number)

    else:
        return response(10101, "request method error")


# 签名的接口 时间戳+ MD5加密
@app.route('/sign/', methods=['GET', 'POST'])
def post_sign():
    if request.method == 'POST':
        client_time = request.form.get('time')  # 客户端时间戳
        client_sign = request.form.get('sign')  # 客户端签名 

        if client_time is None or client_sign is None:
            return response(10102, "time or sign is None")

        elif client_time == "" or client_sign == "":
            return response(10103, "time or sign is null")

        else:
            # 服务器时间
            now_time = time.time()  # 例：1466426831
            server_time = str(now_time).split('.')[0]
            # 获取时间差
            time_difference = int(server_time) - int(client_time)
            if time_difference >= 60:
                return response(10104, "timeout")

            # 签名检查
            md5 = hashlib.md5()
            sign_str = client_time + "&Guest-Bugmaster" + "a=1&b=2"
            sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
            md5.update(sign_bytes_utf8)
            sever_sign = md5.hexdigest()
            if sever_sign != client_sign:
                return response(10105, "sign error!")
            else:
                return response(10200, "sign success!")

    else:
        return response(10101, "request method error")


############ AES加密的接口 #############

BS = 16


def unpad(s): return s[0: - ord(s[-1])]


def decryptBase64(src):
    return base64.urlsafe_b64decode(src)


def decryptAES(src):
    """
    解析AES密文
    """
    src = decryptBase64(src)
    key = b'W7v4D60fds2Cmk2U'
    iv = b"1172311105789011"
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    text = cryptor.decrypt(src).decode()
    return unpad(text)


@app.route('/aes/', methods=['GET', 'POST'])
def post_aes():
    if request.method == 'POST':
        data = request.form.get('data')  # AES加密的数据

        if data is None or data == "":
            return response(10102, "data is None")

        # 解密
        decode = decryptAES(data)
        # 转化为字典
        dict_data = json.loads(decode)
        return response(10200, "success", dict_data)

    else:
        return response(10101, "request method error")


############ end #############


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)  # 设置端口
