# 同步调用 
import time
import httpx


def make_request(client):
    resp = client.get('http://192.168.0.7:5000')
    result = resp.json()
    # print(result)
    assert result["code"] == 10200

def main():
    session = httpx.Client()
        
    # 1000 次调用
    for _ in range(1000):
        make_request(session)


if __name__ == '__main__':
    # 开始
    start = time.time()
    main()
    # 结束
    end = time.time()
    print(f'同步：发送1000次请求，耗时：{end - start}')
