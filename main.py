import os
from dotenv import load_dotenv
from news_fetcher import fetch_news_details
from token_manager import get_access_token, update_env_file
from messenger import create_client, send_news
from alibabacloud_tea_util.client import Client as UtilClient

def load_sent_urls(filepath):
    """
    从文件加载已发送新闻的URL，以避免重复发送。
    """
    if not os.path.exists(filepath):
        return set()
    with open(filepath, 'r') as f:
        return set(line.strip() for line in f)

def save_sent_url(filepath, url):
    """
    将已发送的URL保存到文件中。
    """
    with open(filepath, 'a') as f:
        f.write(f'{url}\n')

def main():
    """
    主函数执行脚本逻辑。
    """
    load_dotenv()

    sent_urls_filepath = '/Users/admin/Documents/Project/Python/dingding/sent_urls.txt'
    sent_urls = load_sent_urls(sent_urls_filepath)
    
    news_list = fetch_news_details()  # 获取新闻列表
    client = create_client()
    for news_details in news_list:
        if news_details['news_url'] not in sent_urls:
            try:
                send_news(client, news_details)
                save_sent_url(sent_urls_filepath, news_details['news_url'])
            except Exception as err:
                if not UtilClient.empty(err.code) and err.code == 'InvalidAuthentication':
                    print("令牌过期。获取新令牌...")
                    app_key = os.getenv('ROBOT_CODE')
                    app_secret = os.getenv('APP_SECRET')  # 确保APP_SECRET存储在.env中
                    new_token = get_access_token(app_key, app_secret)
                    update_env_file(new_token)
                    print("令牌已更新在.env文件中...")
                elif not UtilClient.empty(err.message):
                    print(f"错误: {err.code} - {err.message}")

if __name__ == '__main__':
    main()