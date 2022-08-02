# LOGIN 
import requests
import json

url = "http://localhost:8000/api/auth/token/"

payload = json.dumps({
  "username": "driox",
  "password": "12345678"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

# REGISTER
import requests
import json

url = "http://localhost:8000/api/auth/register"

payload = json.dumps({
  "user": {
    "username": "usr123",
    "email": "usr123@hotmail.com",
    "password": "12345678"
  },
  "company": {
    "name": "Bidi",
    "ein": "481234567",
    "structure": "PARTNER",
    "cellphone": "5051234123",
    "address": {
      "zip": "12345",
      "street": "Golden Avenue",
      "city": "Orlando",
      "state": "FL"
    }
  }
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

# /INVOICE
import requests
import json

url = "http://localhost:8000/api/invoice/"

payload = json.dumps({
  "userID": 9,
  "product": {
    "name": "Product A",
    "price": 12,
    "tax": 0.05
  },
  "productAmount": 10
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

# refresh
import requests
import json

url = "http://localhost:8000/api/auth/token/refresh/"

payload = json.dumps({
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2NzE4MDgxMCwiaWF0IjoxNjU5NDA0ODEwLCJqdGkiOiI2Y2UwZDFjZGQ3YWI0MzRmOWM0NzdjY2FkZDY1MjdjMCIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoiZHJpb3gifQ.ZbUa7FnIfxGJno2KGBW_QFfruiqpMi6urCePD1Tcuh0"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
