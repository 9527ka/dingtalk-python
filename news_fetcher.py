import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def is_webp_image(url):
    """
    检查图片是否为WebP格式。
    可以通过图片URL的扩展名或下载图片的头信息进行检查。
    """
    # 检查URL中的文件扩展名
    if url.lower().endswith('.webp'):
        return True
    
    # 下载图片的头信息进行进一步检查
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # 使用Pillow库检查图片格式
            img = Image.open(BytesIO(response.content))
            return img.format.lower() == 'webp'
    except Exception as e:
        print(f"Error checking image format: {e}")
    
    return False

#/www/wwwroot/gwtest.joowill.com/ai-img
def download_and_convert_image(img_url, local_dir='images'):
    """
    下载WebP格式的图片并转换为JPEG格式保存到本地。
    """
    try:
        # 下载图片
        response = requests.get(img_url)
        if response.status_code == 200:
            # 创建存储目录
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)

            # 打开下载的图片
            img = Image.open(BytesIO(response.content))
            # 检查图片格式并转换
            if img.format.lower() == 'webp':
                # 转换为JPEG
                img = img.convert('RGB')

            # 构造本地文件路径
            local_filename = os.path.join(local_dir, os.path.basename(img_url).split('.')[0] + '.jpg')
            # 保存为JPEG格式
            img.save(local_filename, 'JPEG')
            return img_url
    except Exception as e:
        print(f"Error downloading or converting image: {e}")
    return None

def fetch_news_from_ai_bot():
    """
    从 ai-bot.cn 获取新闻详情。
    """
    url = 'https://ai-bot.cn/daily-ai-news/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        first_news_item = soup.find('div', class_='news-item')

        if first_news_item:
            a_tag = first_news_item.find('h2').find('a')
            news_url = a_tag['href']
            title = a_tag.get_text(strip=True)
            content = first_news_item.find('p').get_text(strip=True)
            img_url = 'https://gwtest.joowill.com/ai-img/ai.png'
            return {
                'title': title,
                'content': content,
                'news_url': news_url,
                'imgUrl': img_url
            }
        else:
            return None
    else:
        return None

def fetch_news_from_xiaohu():
    """
    从 xiaohu.ai 获取新闻详情。
    """
    url = 'https://xiaohu.ai/c/ainews'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('article', class_='jeg_post')  # 获取第一个文章项

        if article:
            # 获取标题
            title_tag = article.find('h3', class_='jeg_post_title').find('a')
            title = title_tag.get_text(strip=True) if title_tag else '无标题'

            # 获取发布日期
            # date_tag = article.find('div', class_='jeg_meta_date').find('a')
            # date = date_tag.get_text(strip=True) if date_tag else '无日期'

            # 获取链接
            link = title_tag['href'] if title_tag else '#'

            # 获取图片
            img_tag = article.find('img', class_='wp-post-image')
            img_url = img_tag['data-src'] if img_tag else ''

            # 返回第一个新闻的信息
            return {
                'title': title,
                'content': title,
                'news_url': link,
                'imgUrl': img_url
            }
    return None

def fetch_news_from_toolify():
    """
    从 toolify.ai 获取新闻详情。
    """
    url = 'https://www.toolify.ai/zh/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('div', class_='tool-item')  # 获取所有工具项

        if article:
            # 获取标题
            title_div = article.find('div', class_='text-xl font-semibold text-gray-1000 flex-1 truncate break-words hover:text-purple-1300')
            title = title_div.get_text(strip=True) if title_div else '无标题'

            # 获取描述
            description_div = article.find('div', class_='mt-2.5 text-sm text-gray-1500 break-words tool-desc leading-6 go-tool-detail-description')
            description = description_div.get_text(strip=True) if description_div else '无描述'

            # 获取链接
            link_tag = article.find('a', class_='go-tool-detail-name')
            link = link_tag['href'] if link_tag else '#'

            # 获取图片
            # img_tag = article.find('img', class_='w-full object-cover')
            img_url = 'https://gwtest.joowill.com/ai-img/default.jpg'
            # img_url = img_tag['src'] if img_tag else ''
            # local_img_url = None

            # # 检查图片格式
            # if img_url and is_webp_image(img_url):
            #     local_img_url = download_and_convert_image(img_url)
            # else:
            #     local_img_url = img_url  # 如果不是WebP格式，直接使用原始链接

            return {
                'title': title,
                'content': description,
                'news_url': link,
                'imgUrl': img_url
            }
    return None

def fetch_news_details():
    """
    从多个新闻来源获取新闻详情。
    """
    news_list = []
    # 添加来自不同网站的新闻
    news_detail = fetch_news_from_ai_bot()
    if news_detail:
        news_list.append(news_detail)
        
    news_detail = fetch_news_from_xiaohu()
    if news_detail:
        news_list.append(news_detail)
        
    news_detail = fetch_news_from_toolify()
    if news_detail:
        news_list.append(news_detail)
    
    return news_list