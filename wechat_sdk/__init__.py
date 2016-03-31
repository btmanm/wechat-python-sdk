# -*- coding: utf-8 -*-

__all__ = ['WechatConf', 'WechatBasic', 'WechatCorp', 'WechatExt']

try:
    from wechat_sdk.core.conf import WechatConf
    from wechat_sdk.basic import WechatBasic
    from wechat_sdk.corp import WechatCorp
    from wechat_sdk.ext import WechatExt
except ImportError:
    pass
