import requests
from dotenv import load_dotenv
import os

def get_access_token(app_key, app_secret):
    """
    使用应用的app key和secret从钉钉API获取新的访问令牌。
    """
    url = 'https://oapi.dingtalk.com/gettoken'
    params = {
        'appkey': app_key,
        'appsecret': app_secret
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['errcode'] == 0:
        print("访问令牌:", data['access_token'])
        return data['access_token']
    else:
        print("错误:", data['errmsg'])
        raise Exception(f"获取访问令牌失败: {data['errmsg']}")

def update_env_file(token):
    """
    更新.env文件中的访问令牌。
    """
    with open('.env', 'r') as file:
        data = file.readlines()

    with open('.env', 'w') as file:
        for line in data:
            if line.startswith("X_ACS_DINGTALK_ACCESS_TOKEN"):
                file.write(f"X_ACS_DINGTALK_ACCESS_TOKEN={token}\n")
            else:
                file.write(line)