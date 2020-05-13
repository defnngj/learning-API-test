# 异步调用
import httpx
import asyncio
import time

async def request(client):
    resp = await client.get('http://192.168.0.7:5000')
    result = resp.json()
    # print(result)
    assert result["code"] == 10200


async def main():
    async with httpx.AsyncClient() as client:
        # # 开始
        # start = time.time()

        # 1000 次调用
        task_list = []
        for _ in range(1000):
            req = request(client)
            task = asyncio.create_task(req)
            task_list.append(task)
        await asyncio.gather(*task_list)


if __name__ == "__main__":
    #开始
    start = time.time()
    asyncio.run(main())
    # 结束
    end = time.time()
    print(f'异步：发送1000次请求，耗时：{end - start}')