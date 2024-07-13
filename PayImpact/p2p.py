def paypay_create_p2pcode(session, amount):
    if not session.access_token:
        raise PayPayLoginError("まずはログインしてください")
    
    payload = {
        "amount": amount,
        "order_description": "P2P送金",
        "client_uuid": session.client_uuid,
        "is_not_use_p2p_url_schema": True
    }
    
    response = session.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/getP2PCode", json=payload, headers=session._headers(), proxies=session.proxy)
    data = response.json()
    if data["header"]["resultCode"] != "S0000":
        raise PayPayError(data)
    
    session.created_p2pcode = data["payload"]["p2pUrl"]

    return data

def paypay_create_paymentcode(session, amount, description=""):
    if not session.access_token:
        raise PayPayLoginError("まずはログインしてください")
    
    payload = {
        "amount": amount,
        "order_description": description,
        "client_uuid": session.client_uuid
    }
    
    response = session.session.post("https://www.paypay.ne.jp/app/v2/bff/paymentcode/getPaymentCode", json=payload, headers=session._headers(), proxies=session.proxy)
    data = response.json()
    if data["header"]["resultCode"] != "S0000":
        raise PayPayError(data)
    
    session.created_paymentcode = data["payload"]["paymentCode"]

    return data
