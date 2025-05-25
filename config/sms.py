import requests

data = {'from': '5000xxx', 'to': '09123456789', 'text': 'test sms'}
response = requests.post('https://console.melipayamak.com/api/send/simple/7b8f36a1a1474b3cbe6a0f5374b47850', json=data)
print(response.json())