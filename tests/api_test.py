import requests
import unittest

class sampleTest(unittest.TestCase):

    def test_sample(self):
        r = requests.get("http://127.0.0.1:5000/")
        result = r.json()
        print(result)


class SESTfulGetTest(unittest.TestCase):

    def test_sample(self):
        name = "tom"
        r = requests.get("http://127.0.0.1:5000/user/"+name)
        result = r.json()
        print(result)


class GetUserDataTest(unittest.TestCase):
    
    def test_uid_null(self):
        uid = "2"
        r = requests.get("http://127.0.0.1:5000/id/"+uid)
        result = r.json()
        print(result)

    def test_uid_exist(self):
        uid = "1"
        r = requests.get("http://127.0.0.1:5000/id/"+uid)
        result = r.json()
        print(result)


class GetSampleTest(unittest.TestCase):

    def test_sample_1(self):
        payload = {'q': 'selenium'}
        r = requests.get("http://127.0.0.1:5000/search/", params=payload)
        result = r.json()
        print(result)

    def test_sample_2(self):
        r = requests.get("http://127.0.0.1:5000/search/?q=selenium")
        result = r.json()
        print(result)


class POSTSampleTest(unittest.TestCase):

    def test_sample_1(self):
        r = requests.post("http://127.0.0.1:5000/login")
        result = r.json()
        print(result)

    def test_sample_2(self):
        payload = {'username': '', "password": ""}
        r = requests.post("http://127.0.0.1:5000/login", data=payload)
        result = r.json()
        print(result)

    def test_sample_3(self):
        payload = {'username': 'abc', "password": "123"}
        r = requests.post("http://127.0.0.1:5000/login", data=payload)
        result = r.json()
        print(result)

    def test_sample_4(self):
        payload = {'username': 'admin', "password": "a123456"}
        r = requests.post("http://127.0.0.1:5000/login", data=payload)
        result = r.json()
        print(result)


class POSTJsonTest(unittest.TestCase):

    def test_key_null(self):
        payload = {}
        r = requests.post("http://127.0.0.1:5000/add_user", json=payload)
        result = r.json()
        print(result)

    def test_name_null(self):
        payload = {"name": "", "age": 22, "height": 177}
        r = requests.post("http://127.0.0.1:5000/add_user", json=payload)
        result = r.json()
        print(result)

    def test_name_exist(self):
        payload = {"name": "tom", "age": 22, "height": 177}
        r = requests.post("http://127.0.0.1:5000/add_user", json=payload)
        result = r.json()
        print(result)

    def test_add_success(self):
        payload = {'name': 'jack', "age": 22, "height": 177}
        r = requests.post("http://127.0.0.1:5000/add_user", json=payload)
        result = r.json()
        print(result)


class HeadersTest(unittest.TestCase):

    def test_smaple(self):
        headers = {'Content-Type': 'application/json',
                   "token": "3d80caXELzU1aWmHwxl0TzW7jtterObm8l5EeAfipnhyaKmhFl8KdhFRvy4"}
        r = requests.post("http://127.0.0.1:5000/header", headers=headers)
        result = r.json()
        print(result)


class AuthTest(unittest.TestCase):

    def test_auth_none(self):
        r = requests.post("http://127.0.0.1:5000/auth")
        result = r.json()
        print(result)

    def test_auth_null(self):
        auth = ("", "")
        r = requests.post("http://127.0.0.1:5000/auth", auth=auth)
        result = r.json()
        print(result)

    def test_auth_fail(self):
        auth = ("abc", "123")
        r = requests.post("http://127.0.0.1:5000/auth", auth=auth)
        result = r.json()
        print(result)

    def test_auth_success(self):
        auth = ("admin", "admin123")
        r = requests.post("http://127.0.0.1:5000/auth", auth=auth)
        result = r.json()
        print(result)


class UploadFileTest(unittest.TestCase):

    def test_sample(self):
        files = {'file': open('D:\\log.txt', 'rb')}
        r = requests.post("http://127.0.0.1:5000/upload", files=files)
        result = r.json()
        print(result)


class MoreMethodTest(unittest.TestCase):

    def test_get_method(self):
        r = requests.get("http://127.0.0.1:5000/phone/1")
        result = r.json()
        print(result)

    def test_put_method(self):
        data = {"name": "华为手机", "price": "3999"}
        r = requests.put("http://127.0.0.1:5000/phone/1", data=data)
        result = r.json()
        print(result)

    def test_delete_method(self):
        r = requests.delete("http://127.0.0.1:5000/phone/1")
        result = r.json()
        print(result)


class SessionTest(unittest.TestCase):

    def test_sample(self):
        s = requests.Session()
        r = s.post("http://127.0.0.1:5000/user_login", data={"username": "jack", "password": "123"})
        result = r.json()
        print(result)
        r2 = s.get("http://127.0.0.1:5000/user_data")
        result2 = r2.json()
        print(result2)


if __name__ == '__main__':
    unittest.main()
