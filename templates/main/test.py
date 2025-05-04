
# import requests
# data = {'from': '50002710067815', 'to': f"09931567815", 'text': f'کد تایید شما: 4581 \n یونی ویز \n www UniWays ir '}
# response = requests.post('https://console.melipayamak.com/api/send/simple/7b8f36a1a1474b3cbe6a0f5374b47850', json=data)
# print(response.json())


from melipayamak import Api
username = '09931567815'
password = '6!#ML'
api = Api(username,password)
sms_soap = api.sms('soap')
to = '09123456789'
result = sms_soap.send_by_base_number("پیام تست", '09908490828', 308145)
print(result)