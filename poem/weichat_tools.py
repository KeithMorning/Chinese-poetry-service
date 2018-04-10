from weixin import WXAPPAPI
from rest_framework_jwt.settings import api_settings
import random
from WXBizDataCrypt.WXBizDataCrypt import WXBizDataCrypt

def get_session_info(appcode,appid,appsecret):

    api = WXAPPAPI(appid=appid,app_secret=appsecret)
    session_info = api.exchange_code_for_session_key(code=appcode)

    session_key = session_info.get('session_key')
    open_id = session_info.get('openid')
    print("sessionid=%s openid=%s" %(session_key,open_id))

    return (session_key,open_id)

def to_weichat_jwt(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token

def random_passwd():
    return ''.join(str(random.choice(range(10))) for _ in range(10))

def get_user_info(session_key,appid,encryptdata,iv):
    crypt = WXBizDataCrypt(appid,session_key)
    userinfo = crypt.decrypt(encryptdata,iv)
    return userinfo
