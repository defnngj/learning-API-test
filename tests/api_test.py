import requests
import unittest

class sampleTest(unittest.TestCase):

    @unittest.skip("aa")
    def test_sample(self):
        r = requests.get("http://127.0.0.1:5000/")
        result = r.json()
        print(result)


class SESTfulGetTest(unittest.TestCase):

    @unittest.skip("aa")
    def test_sample(self):
        name = "tom"
        r = requests.get("http://127.0.0.1:5000/user/"+name)
        result = r.json()
        print(result)


class GetUserDataTest(unittest.TestCase):
    
    @unittest.skip("aa")
    def test_uid_null(self):
        uid = "2"
        r = requests.get("http://127.0.0.1:5000/id/"+uid)
        result = r.json()
        print(result)

    @unittest.skip("aa")
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


@unittest.skip("aa")
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


@unittest.skip("aa")
class POSTJsonTest(unittest.TestCase):

    def test_sample_1(self):
        payload = {'name': 'jack', "age": 22, "height": 177}
        r = requests.post("http://127.0.0.1:5000/add_user", json=payload)
        result = r.json()
        print(result)


if __name__ == '__main__':
    unittest.main()
