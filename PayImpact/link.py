def paypay_link_check(session, url):
    if "https://" in url:
        url = url.replace("https://pay.paypay.ne.jp/", "")

    params = {
        "verificationCode": url
    }
    response = session.session.get("https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo", headers=session._headers(), params=params, proxies=session.proxy)
    data = response.json()
    if data["header"]["resultCode"] != "S0000":
        raise PayPayError(data)
    
    session.link_sender_name = data["payload"]["sender"]["displayName"]
    session.link_sender_external_id = data["payload"]["sender"]["externalId"]
    session.link_sender_icon = data["payload"]["sender"]["photoUrl"]
    session.link_order_id = data["payload"]["pendingP2PInfo"]["orderId"]
    session.link_chat_room_id = data["payload"]["message"]["chatRoomId"]
    session.link_amount = data["payload"]["pendingP2PInfo"]["amount"]
    session.link_status = data["payload"]["message"]["data"]["status"]
    session.link_money_light = data["payload"]["message"]["data"]["subWalletSplit"]["senderPrepaidAmount"]
    session.link_money = data["payload"]["message"]["data"]["subWalletSplit"]["senderEmoneyAmount"]
    session.link_has_password = data["payload"]["pendingP2PInfo"]["isSetPasscode"]

    return data

def paypay_link_receive(session, url, password=None, link_info=None):
    if not session.access_token:
        raise PayPayLoginError("まずはログインしてください")
    
    if "https://" in url:
        url = url.replace("https://pay.paypay.ne.jp/", "")
    
    if not link_info:
        params = {
            "verificationCode": url
        }
        response = session.session.get("https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo", headers=session._headers(), params=params, proxies=session.proxy)
        link_info = response.json()
        if link_info["header"]["resultCode"] != "S0000":
            raise PayPayError(link_info)
    
    if link_info["payload"]["orderStatus"] != "PENDING":
        raise PayPayError("すでに 受け取り / 辞退 / キャンセル されているリンクです")
    
    if link_info["payload"]["pendingP2PInfo"]["isSetPasscode"] and not password:
        raise PayPayError("このリンクにはパスワードが設定されています")
    
    payload = {
        "verificationCode": url,
        "client_uuid": session.client_uuid,
        "passcode": password
    }
    
    response = session.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/completeP2PLink", json=payload, headers=session._headers(), proxies=session.proxy)
    data = response.json()
    if data["header"]["resultCode"] != "S0000":
        raise PayPayError(data)
    
    return data

def paypay_link_reject(session, url, link_info=None):
    if not session.access_token:
        raise PayPayLoginError("まずはログインしてください")
    
    if "https://" in url:
        url = url.replace("https://pay.paypay.ne.jp/", "")
    
    if not link_info:
        params = {
            "verificationCode": url
        }
        response = session.session.get("https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo", headers=session._headers(), params=params, proxies=session.proxy)
        link_info = response.json()
        if link_info["header"]["resultCode"] != "S0000":
            raise PayPayError(link_info)
    
    if link_info["payload"]["orderStatus"] != "PENDING":
        raise PayPayError("すでに 受け取り / 辞退 / キャンセル されているリンクです")
    
    payload = {
        "verificationCode": url,
        "client_uuid": session.client_uuid
    }
    
    response = session.session.post("https://www.paypay.ne.jp/app/v2/p2p-api/cancelP2PLink", json=payload, headers=session._headers(), proxies=session.proxy)
    data = response.json()
    if data["header"]["resultCode"] != "S0000":
        raise PayPayError(data)
    
    return data
