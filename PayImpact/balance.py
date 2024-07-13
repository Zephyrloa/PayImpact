def paypay_get_balance(session):
    if not session.access_token:
        raise PayPayLoginError("ログインしてください")
    
    response = session.session.get("https://www.paypay.ne.jp/app/v1/bff/getBalanceInfo", headers=session._headers(), proxies=session.proxy)
    data = response.json()
    if data["header"]["resultCode"] != "S0000":
        raise PayPayError(data)
    
    session.money = data["payload"]["walletDetail"]["emoneyBalanceInfo"]["balance"]
    session.money_light = data["payload"]["walletDetail"]["prepaidBalanceInfo"]["balance"]
    session.all_balance = data["payload"]["walletSummary"]["allTotalBalanceInfo"]["balance"]
    session.useable_balance = data["payload"]["walletSummary"]["usableBalanceInfoWithoutCashback"]["balance"]
    session.point = data["payload"]["walletDetail"]["cashBackBalanceInfo"]["balance"]

    return data
