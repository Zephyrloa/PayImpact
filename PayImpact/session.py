import requests
from uuid import uuid4

class PayPaySession:
    def __init__(self, phone=None, password=None, client_uuid=str(uuid4()).upper(), access_token=None, proxy=None):
        self.session = requests.Session()
        self.proxy = proxy
        self.client_uuid = client_uuid
        self.phone = phone
        self.password = password
        self.access_token = access_token
        self.otp_prefix = None
        self.otp_reference_id = None
        
        if access_token:
            self.session.cookies.set("token", access_token)
        else:
            payload = {
                "scope": "SIGN_IN",
                "client_uuid": self.client_uuid,
                "grant_type": "password",
                "username": self.phone,
                "password": self.password,
                "add_otp_prefix": True,
                "language": "ja"
            }
            self._initial_login(payload)
    
    def _initial_login(self, payload):
        try:
            response = self.session.post("https://www.paypay.ne.jp/app/v1/oauth/token", json=payload, headers=self._headers(), proxies=self.proxy)
            data = response.json()
            if "access_token" in data:
                self.access_token = data["access_token"]
            else:
                if data.get("response_type") == "ErrorResponse":
                    raise PayPayLoginError(data)
                else:
                    self.otp_prefix = data.get("otp_prefix")
                    self.otp_reference_id = data.get("otp_reference_id")
        except Exception as e:
            raise NetWorkError(e)

    def _headers(self):
        return {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Content-Type": "application/json"
        }
