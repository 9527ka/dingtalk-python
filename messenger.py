from alibabacloud_dingtalk.robot_1_0.client import Client as dingtalkrobot_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.robot_1_0 import models as dingtalkrobot__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
import os

def create_client() -> dingtalkrobot_1_0Client:
    """
    创建一个钉钉客户端实例。
    """
    config = open_api_models.Config()
    config.protocol = 'https'
    config.region_id = 'central'
    return dingtalkrobot_1_0Client(config)

def send_news(client, news_details):
    """
    发送新闻到钉钉。
    """
    print(os.getenv('X_ACS_DINGTALK_ACCESS_TOKEN'))
    org_group_send_headers = dingtalkrobot__1__0_models.OrgGroupSendHeaders()
    org_group_send_headers.x_acs_dingtalk_access_token = '402ce9c2416334b39b1a7bba209070f1'
    org_group_send_request = dingtalkrobot__1__0_models.OrgGroupSendRequest(
        msg_param=f'{{"title": "{news_details["title"]}","text": "{news_details["content"]}","picUrl": "{news_details["imgUrl"]}","singleTitle": "查看详情","singleURL":"{news_details["news_url"]}"}}',
        msg_key='sampleActionCard',
        robot_code=os.getenv('ROBOT_CODE'),
        open_conversation_id=os.getenv('OPEN_CONVERSATION_ID')
    )
    client.org_group_send_with_options(org_group_send_request, org_group_send_headers, util_models.RuntimeOptions())