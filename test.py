
from PayPay import PayPaySession, paypay_login, paypay_resend_otp, paypay_get_balance, paypay_get_profile, paypay_get_history, paypay_link_check, paypay_link_receive, paypay_link_reject, paypay_create_p2pcode, paypay_create_paymentcode

paypay = PayPaySession(phone="08012345678", password="Test-1234")
otp = input(f"SMS : :{paypay.otp_prefix}-")
paypay_login(paypay, otp)

print(paypay.access_token)
print(paypay.client_uuid)

link_info = paypay_link_check(paypay, "https://pay.paypay.ne.jp/osuvUuLmQH8WA4kW")
print(paypay.link_amount)
print(paypay.link_money_light)
print(paypay.link_money)
print(paypay.link_has_password)
print(paypay.link_chat_room_id)
print(paypay.link_status)
print(paypay.link_order_id)

paypay_link_receive(paypay, f"https://pay.paypay.ne.jp/{後半の値}", link_info=link_info)
paypay_link_reject(paypay, f"https://pay.paypay.ne.jp/{後半の値}", link_info=link_info)

paypay_get_balance(paypay)
print(paypay.all_balance)
print(paypay.useable_balance)
print(paypay.money_light)
print(paypay.money)
print(paypay.point)

paypay_get_profile(paypay)
print(paypay.name)
print(paypay.external_user_id)
print(paypay.icon)

print(paypay_get_history(paypay))
