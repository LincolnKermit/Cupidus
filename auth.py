import requests

phone_number = ""

url = "https://api.gotinder.com/v2/auth/sms/send"
headers = {
    "content-type": "application/json",
    "User-Agent": "Tinder/14.6.0 (iPhone; iOS 14.6; Scale/2.00)",
    "platform": "ios",
    "app-version": "14.6.0"
}
data = {"phone_number": phone_number, "auth_type": "sms"}

response = requests.post(url, json=data, headers=headers)

print(response.text)
print(response.status_code)

try:
    print(response.json())  # Vérifie la réponse JSON
except requests.exceptions.JSONDecodeError:
    print("Erreur: La réponse n'est pas en JSON.")
