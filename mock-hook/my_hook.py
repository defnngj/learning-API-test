from seldom.testdata import get_date

def response_hook(request, response):
    print("hook request", request)
    print("hook response", response)
    
    
    # 判断请求头 token 为空，返回失败
    token = request["header"]["token"]
    if token == "":
        response["error"]["code"] = "100501"
        response["error"]["message"] = "token is null"
        return response

    # 自定义数据，插入到reponse中
    response["result"] = {"total": 100, "project_list": []}
    
    # 把 header请求头的数据，插入到reponse中
    response["result"]["token"] = token
    
    # 把 随机生成 的数据，插入到 reponse中
    response["result"]["today"] = get_date()

    return  response

