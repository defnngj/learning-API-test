# learning-API-test

帮助你学习API接口测试。

## 开始

* __安装__

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

所有例子使用[Requests](https://2.python-requests.org//zh_CN/latest/user/quickstart.html) 库调用，你也可以使用其他API测试工具，如Postman、JMeter等。

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

### 最简单的接口调用

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

### 累加器

每次请求数字加1

```python
import requests

r = requests.get("http://127.0.0.1:5000/add_one")
result = r.json()
print(result)
```

返回结果：

```json
{"code": 10200, "data": { "number": 1 }, "message": "success"}
```


### RESTful 风格的API

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

### 根据用户id返回不同的结果

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

### 一般GET请求

* 方法一

```python
import requests

payload = {"q": "selenium"}
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

### POST请求

参数类型为：```from-data```/```x-www-from-urlencode```格式

```python
import requests

payload = {"username": "admin", "password": "a123456"}
r = requests.post("http://127.0.0.1:5000/login", data=payload)
result = r.json()
print(result)
```

返回结果：

```json
{"code": 10102, "message": "username or passwrord is None"}
{"code": 10103, "message": "username or passwrord is null"}
{"code": 10104, "message": "username or password error"}
{"code": 10200, "message": "login success"}

```

#### POST请求

参数类型为：```JSON```格式

```python
import requests

payload = {"name": "jack", "age": 22, "height": 177}
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

### 带Header的接口

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

### 带Basic Auth认证的接口

```python
import requests

auth = ("admin", "admin123")
r = requests.post("http://127.0.0.1:5000/auth", auth=auth)
result = r.json()
print(result)

```

返回结果：

```json
{"code": 10101, "message": "Authorization None"}
{"code": 10102, "message": "Authorization null"}
{"code": 10103, "message": "Authorization fail!"}
{"code": 10200, "message": "Authorization success!"}
```

### 上传文件接口

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

### 下载文件接口

```python
import requests

r = requests.get("http://127.0.0.1:5000/download", stream=True)

with open("./log.txt", "wb") as f:
    for chunk in r.iter_content(chunk_size=512):
        f.write(chunk)
```

文件默认保存在当前脚本文件所在目录，文件名为`log.txt`。

### 同一个URL，根据方法实现不同功能

* ```GET```请求，一般用作获取数据接口。

```python
import requests

r = requests.get("http://127.0.0.1:5000/phone/1")
result = r.json()
print(result)

```

返回结果：

```json
{"code": 10101, "message": "The phone id is empty"}
{"code": 10201, "message": "get success", 
 "data": {
   "id": 1, "name": "小米手机", "price": 1999
  }
}
```

* ```PUT```请求，一般用作更新数据接口。

```python
import requests

data = {"name":"华为手机", "price": "3999"}
r = requests.put("http://127.0.0.1:5000/phone/1", data=data)
result = r.json()
print(result)

```

返回结果：

```json
{"code": 10102, "message": "The updated phone id is empty"}
{"code": 10202, "message": "update success",
 "data": {
   "id": 1, "name": "华为手机", "price": "3999"
  }
}
```

* ```DELETE```请求, 一般用作删除数据接口。

```python
import requests

r = requests.delete("http://127.0.0.1:5000/phone/1")
result = r.json()
print(result)

```

返回结果：

```json
{"code": 10103, "message": "The deleted phone id is empty"}
{"code": 10203, "message": "delete success"}
```

### 通过Session记录登录状态

```python
import requests

s = requests.Session()
r = s.post("http://127.0.0.1:5000/user_login", data={"username": "jack", "password": "123"})
result = r.json()
print(result)

r2 = s.get("http://127.0.0.1:5000/user_data")
result2 = r2.json()
print(result2)
```

返回结果：

```json
{"code": 10200, "message": "login success"}
{"code": 10200, "message": "hello, jack"}
```

### 依赖接口的调用

一个获取抽奖号码的接口，需要先得到抽奖活动id 和 抽奖用户id

```python
# 获取活动id
r = requests.get("http://127.0.0.1:5000/get_activity")
result = r.json()
print(result)
activity_id = result["data"]["id"]

# 获取用户id
r = requests.get("http://127.0.0.1:5000/get_user")
result = r.json()
print(result)
user_id = result["data"]["id"]

# 调用获取抽奖号码接口
data = {"aid": activity_id, "uid": user_id}
r = requests.post("http://127.0.0.1:5000/lucky_number", data=data)
result = r.json()
print(result)
````

返回结果：

```json
{"code": 10200, "data": {"id": 1, "name": "618抽奖活动"}, "message": "success"}
{"code": 10200, "data": {"id": 1, "name": "张三"}, "message": "success"}
{"code": 10200, "data": 80092, "message": "Lucky draw number"}
```
