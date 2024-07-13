def paypay_get_history(session):
    if not session.access_token:
        raise PayPayLoginError("ログインしてください")
    
    response = session.session.get("https://www.paypay.ne.jp/app/v2/bff/getPay2BalanceHistory", headers=session._headers(), proxies=session.proxy)
    data = response.json()
    if data["header"]["resultCode"] != "S0000":
        raise PayPayError(data)
    
    return data
