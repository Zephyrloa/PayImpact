def paypay_login(session, otp):
    payload = {
        "scope": "SIGN_IN",
        "client_uuid": session.client_uuid,
        "grant_type": "otp",
        "otp_prefix": session.otp_prefix,
        "otp": otp,
        "otp_reference_id": session.otp_reference_id,
        "username_type": "MOBILE",
        "language": "ja"
    }
    
    response = session.session.post("https://www.paypay.ne.jp/app/v1/oauth/token", json=payload, headers=session._headers(), proxies=session.proxy)
    data = response.json()
    if "access_token" in data:
        session.access_token = data["access_token"]
    else:
        raise PayPayLoginError(data)
    
    return data

def paypay_resend_otp(session, otp_reference_id):
    payload = {
        "add_otp_prefix": "true"
    }
    response = session.session.post(f"https://www.paypay.ne.jp/app/v1/otp/mobile/resend/{otp_reference_id}", json=payload, headers=session._headers(), proxies=session.proxy)
    data = response.json()
    if "otp_prefix" in data and "otp_reference_id" in data:
        session.otp_prefix = data["otp_prefix"]
        session.otp_reference_id = data["otp_reference_id"]
    else:
        raise PayPayLoginError(data)
    
    return data
