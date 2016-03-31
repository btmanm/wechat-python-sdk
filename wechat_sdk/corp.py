# -*- coding: utf-8 -*-

import time

from .base import WechatBase
from .core.conf import WechatConf
from .lib.request import WechatRequest

class WechatCorpAccessTokenManager(object):
    def __init__(self, corpid, corpsecret):
        self.__corpid = corpid
        self.__corpsecret = corpsecret
        
        self.__access_token = None
        self.__access_token_expires_at = None

        self.__request = WechatRequest()
    
    def refresh_access_token(self):
        response_json = self.__request.get(
            url="https://qyapi.weixin.qq.com/cgi-bin/gettoken",
            params={
                "corpid": self.__corpid,
                "corpsecret": self.__corpsecret,
            },
        )

        self.__access_token = response_json['access_token']
        self.__access_token_expires_at = int(time.time()) + response_json['expires_in']

        return (self.__access_token, self.__access_token_expires_at)

    def get_access_token(self):
        if self.__access_token:
            now = time.time()
            if self.__access_token_expires_at - now > 60:
                return (self.__access_token, self.__access_token_expires_at)

        return self.refresh_access_token()

class WechatCorp(WechatBase):
    """微信企业号基本功能类

    仅包含部分官方 API 中所包含的内容
    """
    def __init__(self, conf):
        """
        :param corpid: 企业ID
        :param corpsecret: 管理组的凭证密钥
        """

        self.__conf = conf
        self.__request = WechatRequest(conf=self.__conf)

    @property
    def request(self):
        """ 获取当前 WechatConf 配置实例 """
        return self.__request

    @request.setter
    def request(self, request):
        """ 设置当前 WechatConf 实例  """
        self.__request = request

    def send_text_message(self, agentid, content, touser=None, toparty=None, totag=None, safe=0):
        """
        发送文本消息
        详情请参考 http://qydev.weixin.qq.com/wiki/index.php?title=%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F
        :param agentid: 企业应用的id，整型。可在应用的设置页面查看
        :param content: 消息内容（主页型应用消息文本长度不超过20个字）
        :param touser: 成员ID列表（消息接收者，多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为@all，则向关注该企业应用的全部成员发送
        :param toparty: 部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
        :param totag: 标签ID列表，多个接收者用‘|’分隔。当touser为@all时忽略本参数
        :param safe: 表示是否是保密消息，0表示否，1表示是，默认0 
        :return: 返回的 JSON 数据包
        """
        return self.request.post(
            url='https://qyapi.weixin.qq.com/cgi-bin/message/send',
            data={
                'touser': touser,
                'toparty': toparty,
                'totag': totag,
                'msgtype': 'text',
                'agentid': agentid,
                'text': {
                    'content': content,
                },
                'safe': safe,
            }
        )
