import requests as s
import os
from openai import OpenAI


bot_name = "Louis"
bot_age = 23

"""
def send_message_to_ai(message):
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "human", "content": f"You pretend you are human. You are {bot_age} years old and your name is {bot_name}. You are on Tinder and will chat with your matches."},
        {"role": "user", "content": "Hello!"}
    ]
    )

    print(completion.choices[0].message)
send_message_to_ai("Hello, how are you?")
exit(0)
"""




personal_id=os.getenv("PERSONAL_ID", "")


headers = {
    "User-Agent": "Tinder/12.8.0 (iPhone; iOS 15.0; Scale/3.00)",
    "X-Auth-Token": os.getenv("X_AUTH_TOKEN", ""),
    "Content-Type": "application/json",
}

if headers["X-Auth-Token"] == "":
    print("Please fill the X-Auth-Token in the headers")
    headers["X-Auth-Token"] = input("X-Auth-Token: ")


def get_matches():
    i = 0
    url = "https://api.gotinder.com/v2/matches?count=100&is_tinder_u=false"
    response = s.get(url, headers=headers)
    if response.status_code == 200:
        matches = response.json()
        for match in matches["data"]["matches"][::-1]:
            match_id = match["id"]
            match_name = match["person"]["name"]
            i += 1
        return matches["data"]["matches"]
    else:
        print(f"Erreur : {response.status_code} - {response.text}")
        return []



def get_name(match_id):
    url = f"https://api.gotinder.com/v2/matches/{match_id}"
    response = s.get(url, headers=headers)
    if response.status_code == 200:
        match = response.json()
        match_name = match["data"]["person"]["name"]
        return match_name
    else:
        print(f"Erreur : {response.status_code} - {response.text}")
        return ""


def get_messages(match_id):
    url = f"https://api.gotinder.com/v2/matches/{match_id}/messages?locale=fr&count=100"
    response = s.get(url, headers=headers)
    if response.status_code == 200:
        messages = response.json()
        person_name = get_name(match_id)
        messages = messages["data"]["messages"]
        messages.reverse()
        return messages
    else:
        print(f"Erreur : {response.status_code} - {response.text}")
        return []


def check_status(match_id):
    messages_list = get_messages(match_id)
    if len(messages_list) > 0:
        last_message = messages_list[0]
        if last_message['from'] == personal_id:
            print("Nothing to see, you are updated")
        elif last_message['from'] != personal_id:
            print("----------------------------------------------")
            print("You have a new message from ", get_name(match_id))
            print("Message: ", last_message['message'])
            print("Sending it to AI...")
            # TODO ADD THIS LINE AND ADD API OF AI
            #response = send_message_to_ai(last_message['message'])
            #send_message(match_id, response)
            print("Debug : NO AI API, Skipping...")
            print("----------------------------------------------")



def send_message(match_id, message_to_send):
    url = f"https://api.gotinder.com/user/matches/{match_id}"
    payload = {
        "matchId": personal_id+match_id,
        "message": message_to_send,
        "otherId": match_id,
        "sessionId": "null",
        "userId": personal_id,
    }
    response = s.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Message envoyé : {message_to_send}")
    else:
        print(f"Erreur lors de l'envoi du message : {response.status_code} - {response.text}")





def check_status(match_id):
    messages_list = get_messages(match_id)
    if len(messages_list) > 0:
        last_message = messages_list[0]
        if last_message == []:
            print(f"Nothing to see, you are updated for {get_name(match_id)}")
        if last_message['from'] == personal_id:
            print(f"Nothing to see, you are updated for {get_name(match_id)}")
        elif last_message['from'] != personal_id:
            print(f"You have a new message from {get_name(match_id)}")
            print("Message: ", last_message['message'])
            print("Sending it to AI...")



while True:
    matches = get_matches()
    for match in matches:
        check_status(match["id"])