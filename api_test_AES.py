
from Crypto.Cipher import AES
import base64
import requests
import unittest
import json


class AESTest(unittest.TestCase):

    def setUp(self):
        # 字符串自动补全16倍数
        BS = 16
        self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

        self.base_url = "http://127.0.0.1:5000/aes/"

    def encryptBase64(self,src):
        """
        生成 base64 字符串
        """
        return base64.urlsafe_b64encode(src)

    def encryptAES(self, src):
        """
        生成AES密文
        """
        key = b'W7v4D60fds2Cmk2U'
        iv = b"1172311105789011"
        cryptor = AES.new(key, AES.MODE_CBC, iv)
        src_str = self.pad(src)
        src_byte = src_str.encode('utf-8')
        ciphertext = cryptor.encrypt(src_byte)  # AES加密
        aes_base64 = self.encryptBase64(ciphertext)  # base64 二次加密
        return aes_base64

    def test_aes_interface(self):
        '''test AES interface'''
        payload = {'eid':1, 'phone':'18611001100'}
        data = json.dumps(payload)
        # 加密
        encoded = self.encryptAES(data).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        print(result)


if __name__ == '__main__':
    unittest.main()