def paypay_get_profile(session):
    if not session.access_token:
        raise PayPayLoginError("まずはログインしてください")
    
    response = session.session.get("https://www.paypay.ne.jp/app/v1/getUserProfile", headers=session._headers(), proxies=session.proxy)
    data = response.json()
    if data["header"]["resultCode"] != "S0000":
        raise PayPayError(data)
    
    session.name = data["payload"]["userProfile"]["nickName"]
    session.external_user_id = data["payload"]["userProfile"]["externalUserId"]
    session.icon = data["payload"]["userProfile"]["avatarImageUrl"]

    return data
