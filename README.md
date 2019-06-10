# learning-API-test

帮助你学习API接口测试。

## 开始


__安装__

克隆或下载项目，安装依赖。

```shell
$ pip install -r requirements.txt
```

* __启动接口服务__

```shell
$ python api_server.py

* Serving Flask app "api_server.py" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 208-740-173
```

Flask Web框架可以非常简单的方式实现API，项目中的所有API都在```api_server.py ``` 文件中。 

* __接口测试库__

[Requests](https://2.python-requests.org//zh_CN/latest/user/quickstart.html) 所有例子使用Requests库调用，你也可以使用其他API测试工具，如Postman、JMeter等。


## http接口的基本信息


* URL (http://www.xxx.com/v1/login)
* 方法：GET/POST/PUT/DELETE
* Auth 
* Header
* 参数类型（form-data/json..）
* 参数值（id=1，name=tom）
* 参数加密方式
* 返回值（错误码/提示信息/数据）


## 接口测试例子


#### 最简单的接口调用

```python
import requests

r = requests.get("http://127.0.0.1:5000/")
result = r.json()
print(result)
```

返回结果：

```json
{"code": 10200, "message": "Welcome to API testing"}
```

#### RESTful 风格的API

```python
import requests

name = "tom"
r = requests.get("http://127.0.0.1:5000/user/"+name)
result = r.json()
print(result)
```

返回结果：

```json
{"code": 10200, "message": "hello, tom"}
```

#### 根据用户id返回不同的结果

```python
import requests

uid = "1"
r = requests.get("http://127.0.0.1:5000/id/"+uid)
result = r.json()
print(result)

```

返回结果：

```json
{"code": 10101, "message": "user id null"}
{"code": 10200, "data": {"age": 22, "id": 1, "name": "tom"}, "message": "success"}

```

#### 一般GET请求

* 方法一

```python
import requests

payload = {'q': 'selenium'}
r = requests.get("http://127.0.0.1:5000/search/", params=payload)
result = r.json()
print(result)
```

* 方式二

```python
import requests

r = requests.get("http://127.0.0.1:5000/search/?q=selenium")
result = r.json()
print(result)
```

返回结果：

```json
{"code": 10200, "data": ["selenium教程", "seleniumhq.org", "selenium环境安装"], "message": "success"}
```

#### POST请求

参数类型为：```from-data```/```x-www-from-urlencode```格式

```python
import requests

payload = {'username': 'admin', "password": "a123456"}
r = requests.post("http://127.0.0.1:5000/login", data=payload)
result = r.json()
print(result)
```

返回结果：

```json
{"code": 10102, "message": "username or passwrord is None"}
{"code": 10203, "message": "username or passwrord is null"}
{"code": 10104, "message": "username or password error"}
{"code": 10200, "message": "login success"}

```

#### POST请求

参数类型为：```JSON```格式

```python
import requests

payload = {'name': 'jack', "age": 22, "height": 177}
r = requests.post("http://127.0.0.1:5000/add_user", json=payload)
result = r.json()
print(result)
```

返回结果：

```json
{"code": 10102, "message": "key null"}
{"code": 10103, "message": "name null"}
{"code": 10104, "message": "name exist"}
{"code": 10105, "message": "format error"}
{"code": 10200, "message": "add success",  
 "data": {
   "age": 22, "height": 177, "name": "jack"
   },
}

```

#### 带Header的接口

```python
import requests

headers = {"Content-Type": "application/json",
            "token": "3d80caXELzU1aWmHwxl0TzW7jtterObm8l5EeAfipnhyaKmhFl8KdhFRvy4"}
r = requests.post("http://127.0.0.1:5000/header", headers=headers)
result = r.json()
print(result)

```

返回结果：

```json
{
  "code": 10200, "message": "header ok!", 
  "data": {
    "Content-Type": "application/json",
    "token": "3d80caXELzU1aWmHwxl0TzW7jtterObm8l5EeAfipnhyaKmhFl8KdhFRvy4"
   },
}

```

#### 带Basic Auth认证的接口

```python
import requests

auth = ("admin", "admin123")
r = requests.post("http://127.0.0.1:5000/auth", auth=auth)
result = r.json()
print(result)

```

返回结果：

```json
{"code": 10200, "message": "Authorization fail!"}
{"code": 10101, "message": "Authorization None"}
{"code": 10102, "message": "Authorization null"}
{"code": 10102, "message": "Authorization success!"}
```

#### 上传文件的接口

```python
import requests

files = {'file': open('D:\\log.txt', 'rb')}
r = requests.post("http://127.0.0.1:5000/upload", files=files)
result = r.json()
print(result)

```

返回结果：

```json
{"code": 10200, "message": "upload success!"}
```
