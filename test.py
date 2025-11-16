import requests

chat_id = 1111250499  # from @userinfobot
token = "8541693339:AAGXmigJDLG1R0vO9SEb6kOlMJqX1rhSttg"

url = f"https://api.telegram.org/bot{token}/sendMessage"
r = requests.post(url, data={"chat_id": chat_id, "text": "Test message"})
print(r.status_code, r.text)
