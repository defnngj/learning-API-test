import requests
import unittest

class BaseCase(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://127.0.0.1:5000"


class sampleTest(BaseCase):

    def test_sample(self):
        r = requests.get(self.base_url)
        result = r.json()
        print(result)


class SESTfulGetTest(BaseCase):

    def test_sample(self):
        name = "tom"
        r = requests.get(self.base_url + "/user/"+name)
        result = r.json()
        print(result)


class GetUserDataTest(BaseCase):
    
    def test_uid_null(self):
        uid = "2"
        r = requests.get(self.base_url + "/id/"+uid)
        result = r.json()
        print(result)

    def test_uid_exist(self):
        uid = "1"
        r = requests.get(self.base_url + "/id/"+uid)
        result = r.json()
        print(result)


class GetSampleTest(BaseCase):

    def test_sample_1(self):
        payload = {'q': 'selenium'}
        r = requests.get(self.base_url + "/search/", params=payload)
        result = r.json()
        print(result)

    def test_sample_2(self):
        r = requests.get(self.base_url + "/search/?q=selenium")
        result = r.json()
        print(result)


class POSTSampleTest(BaseCase):

    def test_sample_1(self):
        r = requests.post(self.base_url + "/login")
        result = r.json()
        print(result)

    def test_sample_2(self):
        payload = {'username': '', "password": ""}
        r = requests.post(self.base_url + "/login", data=payload)
        result = r.json()
        print(result)

    def test_sample_3(self):
        payload = {'username': 'abc', "password": "123"}
        r = requests.post(self.base_url + "/login", data=payload)
        result = r.json()
        print(result)

    def test_sample_4(self):
        payload = {'username': 'admin', "password": "a123456"}
        r = requests.post(self.base_url + "/login", data=payload)
        result = r.json()
        print(result)


class POSTJsonTest(BaseCase):

    def test_key_null(self):
        payload = {}
        r = requests.post(self.base_url + "/add_user", json=payload)
        result = r.json()
        print(result)

    def test_name_null(self):
        payload = {"name": "", "age": 22, "height": 177}
        r = requests.post(self.base_url + "/add_user", json=payload)
        result = r.json()
        print(result)

    def test_name_exist(self):
        payload = {"name": "tom", "age": 22, "height": 177}
        r = requests.post(self.base_url + "/add_user", json=payload)
        result = r.json()
        print(result)

    def test_add_success(self):
        payload = {'name': 'jack', "age": 22, "height": 177}
        r = requests.post(self.base_url + "/add_user", json=payload)
        result = r.json()
        print(result)


class HeadersTest(BaseCase):

    def test_smaple(self):
        headers = {'Content-Type': 'application/json',
                   "token": "3d80caXELzU1aWmHwxl0TzW7jtterObm8l5EeAfipnhyaKmhFl8KdhFRvy4"}
        r = requests.post(self.base_url + "/header", headers=headers)
        result = r.json()
        print(result)


class AuthTest(BaseCase):

    def test_auth_none(self):
        r = requests.post(self.base_url + "/auth")
        result = r.json()
        print(result)

    def test_auth_null(self):
        auth = ("", "")
        r = requests.post(self.base_url + "/auth", auth=auth)
        result = r.json()
        print(result)

    def test_auth_fail(self):
        auth = ("abc", "123")
        r = requests.post(self.base_url + "/auth", auth=auth)
        result = r.json()
        print(result)

    def test_auth_success(self):
        auth = ("admin", "admin123")
        r = requests.post(self.base_url + "/auth", auth=auth)
        result = r.json()
        print(result)


class UploadFileTest(BaseCase):

    def test_sample(self):
        with open('file.txt', 'rb') as f:
            files = {'file': f}
            r = requests.post(self.base_url + "/upload", files=files)
            result = r.json()
            print(result)


class MoreMethodTest(BaseCase):

    def test_get_method(self):
        r = requests.get(self.base_url + "/phone/1")
        result = r.json()
        print(result)

    def test_put_method(self):
        data = {"name": "华为手机", "price": "3999"}
        r = requests.put(self.base_url + "/phone/1", data=data)
        result = r.json()
        print(result)

    def test_delete_method(self):
        r = requests.delete(self.base_url + "/phone/1")
        result = r.json()
        print(result)


class SessionTest(BaseCase):

    def test_sample(self):
        s = requests.Session()
        r = s.post(self.base_url + "/user_login", data={"username": "jack", "password": "123"})
        result = r.json()
        print(result)
        r2 = s.get(self.base_url + "/user_data")
        result2 = r2.json()
        print(result2)


class DependencyTest(BaseCase):

    def test_sample(self):
        r = requests.get(self.base_url + "/get_activity")
        result = r.json()
        print(result)
        activity_id = result["data"]["id"]

        r = requests.get(self.base_url + "/get_user")
        result = r.json()
        print(result)
        user_id = result["data"]["id"]

        data = {"aid": activity_id, "uid": user_id}
        r = requests.post(self.base_url + "/lucky_number", data=data)
        result = r.json()
        print(result)


if __name__ == '__main__':
    unittest.main()
