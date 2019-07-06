import json
import os
import base64
import hashlib
import time
from flask import Flask
from flask import jsonify
from flask import request
from flask import session
from flask import escape
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES    # 请安装 Crypto


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = BASE_PATH + '/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "json"])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'please-generate-a-random-secret_key'


# 最简单的json格式返回
@app.route('/')
def hello_world():
    return jsonify({"code": 10200, "message": "Welcome to API testing"})


# 通过 URI 传参
@app.route('/user/<username>')
def user(username):
    msg = "hello, {}".format(username)
    return jsonify({"code": 10200, "message": msg})


# 根据用户id返回数据
@app.route('/id/<int:uid>',  methods=["GET", "POST"])
def get_uid(uid):
    if request.method == "GET":
        user_info = {"id": 1, "name": "tom", "age": 22}
        if uid != 1:
            response = {"code": 10101, "message": "user id null"}
        else:
            response = {"code": 10200, "message": "success", "data": user_info}
        return jsonify(response)
    else:
        return jsonify({"code": 10101, "message": "request method error"})


# 一般的get传参方式,
@app.route("/search/", methods=["GET", "POST"])
def get_search():
    if request.method == "GET":
        search_word = request.args.get('q', '')
        if search_word == "selenium":
            data_list = ["selenium教程", "seleniumhq.org", "selenium环境安装"]
        else:
            data_list = []
        return jsonify({"code": 10200, "message": "success", "data": data_list})
    else:
        return jsonify({"code": 10101, "message": "request method error"})


# post请求， from-data/x-www-from-urlencode参数方式
@app.route('/login',  methods=["GET", "POST"])
def post_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username is None or password is None:
            response = {"code": 10102, "message": "username or passwrord is None"}
        
        elif username == "" or password == "":
            response = {"code": 10203, "message": "username or passwrord is null"}
        
        elif username == "admin" and password == "a123456":
            response = {"code": 10200, "message": "login success"}
        
        else:
            response = {"code": 10104, "message": "username or password error"}
        return jsonify(response)
    else:
        return jsonify({"code": 10101, "message": "request method error"})


# post请求，json参数方式
@app.route('/add_user',  methods=["GET", "POST"])
def post_add_user():
    if request.method == "POST":
        try:
            data = json.loads(request.get_data())
        except json.decoder.JSONDecodeError:
            return jsonify({"code": 10105, "message": "format error"})
        
        try:
            name = data["name"]
            age = data["age"]
            height = data["height"]
        except KeyError:
            response = {"code": 10102, "message": "key null"}
        else:
            if name == "":
                response = {"code": 10103, "message": "name null"}
            elif name == "tom":
                response = {"code": 10104, "message": "name exist"}
            else:
                data = {"name": name, "age": age, "height": height}
                response = {"code": 10200, "message": "add success", "data": data}
        return jsonify(response)
    else:
        return jsonify({"code": 10101, "message": "request method error"})


# 获取 header 信息处理
@app.route('/header', methods=['GET', 'POST'])
def post_header():
    if request.method == 'POST':
        token = request.headers.get("token")
        ct = request.headers.get("Content-Type")
        response = {"code": 10200, "message": "header ok!",
                    "data": {"token": token, "Content-Type": ct}}
        return jsonify(response)
    else:
        return jsonify({"code": 10101, "message": "request method error"})


# Base Auth认证  ["Basic","YWRtaW46YWRtaW4xMjM="]
@app.route('/auth', methods=['GET', 'POST'])
def post_auth():
    if request.method == 'POST':
        auth = request.headers.get("Authorization")
        if auth is None:
            return jsonify({"code": 10101, "message": "Authorization None"})
        else:
            auth = auth.split()
            auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
            userid, password = auth_parts[0], auth_parts[2]
            if userid == "" or password == "":
                return jsonify({"code": 10102, "message": "Authorization null"})
            
            if userid == "admin" and password == "admin123":
                return jsonify({"code": 10200, "message": "Authorization success!"})
            else:
                return jsonify({"code": 10103, "message": "Authorization fail!"})
    else:
        return jsonify({"code": 10101, "message": "request method error"})


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
            response = {"code": 10200, "message": "upload success!"} 
        else:
            response = {"code": 10102, "message": "file type error!"}
        return jsonify(response)

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
            response = {"code": 10201, "message": "get success", "data": phone_info}
        else:
            response = {"code": 10101, "message": "The phone id is empty"}
        return jsonify(response)

    elif request.method == "PUT":
        if pid == 1:
            name = request.form.get('name')
            price = request.form.get('price')
            phone_info = {
                "id": pid,
                "name": name,
                "price": price
            }
            response = {"code": 10202, "message": "update success", "data": phone_info}
        else:
            response = {"code": 10102, "message": "The updated phone id is empty"}
        return jsonify(response)

    elif request.method == "DELETE":
        if pid == 1:
            response = {"code": 10203, "message": "delete success"}
        else:
            response = {"code": 10103, "message": "The deleted phone id is empty"}
        return jsonify(response)


# 通过Session 记录登录状态
@app.route("/user_login", methods=['POST'])
def session_login():
    username = request.form['username']
    password = request.form['password']
    if username != "" and password != "":
        session['username'] = username
        return jsonify({"code": 10200, "message": 'login success'})
    else:
        return jsonify({"code": 10200, "message": 'login faile'})


@app.route("/user_data")
def session_user_data():
    if 'username' in session:
        username = format(escape(session['username']))
        return jsonify({"code": 10200, "message": 'hello, {}'.format(username)})
    return jsonify({"code": 10200, "message": 'hello, stranger'})


from random import randint


# 接口的依赖
@app.route('/get_activity',  methods=["GET", "POST"])
def get_activity():
    if request.method == "GET":
        activity_info = {"id": 1, "name": "618抽奖活动"}
        return jsonify({"code": 10200, "message": "success", "data": activity_info})
    else:
        return jsonify({"code": 10101, "message": "request method error"})


@app.route('/get_user',  methods=["GET", "POST"])
def get_user():
    if request.method == "GET":
        user_info = {"id": 1, "name": "张三"}
        return jsonify({"code": 10200, "message": "success", "data": user_info})
    else:
        return jsonify({"code": 10101, "message": "request method error"})


@app.route('/lucky_number', methods=["GET", "POST"])
def get_lucky_number():
    if request.method == "POST":
        activity_id = request.form.get('aid')
        user_id = request.form.get('uid')

        if activity_id is None or user_id is None:
            return jsonify({"code": 10102, "message": "username or password is None"})

        elif activity_id == "" or user_id == "":
            return jsonify({"code": 10103, "message": "username or password is null"})

        if int(activity_id) != 1:
            return jsonify({"code": 10104, "message": "activity id exist"})

        if int(user_id) != 1:
            return jsonify({"code": 10105, "message": "user id not exist"})

        number = randint(10000, 99999)
        return jsonify({"code": 10200, "message": "Lucky draw number", "data": number})

    else:
        return jsonify({"code": 10101, "message": "request method error"})


# 签名的接口 时间戳+ MD5加密
@app.route('/sign/', methods=['GET', 'POST'])
def post_sign():
    if request.method == 'POST':
        client_time = request.form.get('time')  # 客户端时间戳
        client_sign = request.form.get('sign')  # 客户端签名 

        if client_time is None or client_sign is None:
            return jsonify({"code": 10102, "message": "time or sign is None"})

        elif client_time == "" or client_sign == "":
            return jsonify({"code": 10103, "message": "time or sign is null"})
        
        else:
            # 服务器时间
            now_time = time.time()    # 例：1466426831
            server_time = str(now_time).split('.')[0]
            # 获取时间差
            time_difference = int(server_time) - int(client_time)
            if time_difference >= 60:
                return jsonify({"code": 10104, "message": "timeout"})

            # 签名检查
            md5 = hashlib.md5()
            sign_str = client_time + "&Guest-Bugmaster"
            sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
            md5.update(sign_bytes_utf8)
            sever_sign = md5.hexdigest()
            if sever_sign != client_sign:
                return jsonify({"code": 10105, "message": "sign error!"})
            else:
                return jsonify({"code": 10200, "message": "sign success!", "data": []})

    else:
        return jsonify({"code": 10101, "message": "request method error"})


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
           return jsonify({"code": 10102, "message": "data is None"})

        # 解密
        decode = decryptAES(data)
        # 转化为字典
        dict_data = json.loads(decode)
        return jsonify({"code": 10200, "message": "success", "data": dict_data})

    else:
        return jsonify({"code": 10101, "message": "request method error"})

############ end #############




if __name__ == '__main__':
    app.debug = True
    app.run()

