import requests as s
import os

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
        print("Oldest -> Newest")
        for match in matches["data"]["matches"][::-1]:
            match_id = match["id"]
            match_name = match["person"]["name"]
            print(f"{i} - Match ID:", match_name, match_id)
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
        print(match_name)
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
        for msg in messages:
            if msg['from'] == personal_id:
                print(f"[{msg['sent_date']}] You: {msg['message']}")
            else:
                print(f"[{msg['sent_date']}] {person_name}: {msg['message']}")
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
            print("You have a new message")
            print("Message: ", last_message['message'])
            print("Sending it to AI...")
            # TODO ADD AI




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



print("Made with heart by @lincolnkermit")
print("Tinder Runner")
print("1 - Get Matches")
print("2 - Get Messages")
print("3 - Send Message")

choice = int(input("attacker@tinder:~$ "))

if choice == 1:
    print("Getting matches...")
    get_matches()
    print("Done.")
elif choice == 2:
    match_id = input("Enter the match id: ")
    get_messages(match_id)
elif choice == 3:
    match_id = input("Enter the match id: ")
    message_to_send = input("Enter the message to send: ")
    send_message(match_id, message_to_send)

