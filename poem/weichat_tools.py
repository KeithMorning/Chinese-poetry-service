from weixin import WXAPPAPI


def get_user_info(appcode,appid,appsecret):

    api = WXAPPAPI(appid=appid,app_secret=appsecret)
    session_info = api.exchange_code_for_session_key(code=appcode)

    session_key = session_info.get('session_key')


