import requests, time, openai



def setup():
    global config
    config = {
        "years": 23,
        "country": "France",
        "field": "arts",
        "social": "very comfortable",
        "tinder": "always respond to Tinder matches",
        "privacy_age": "only reveal age if asked",
        "privacy_ai": "never say you're AI, Act like Human always",
    }




# ---------------------------------------------------------------- CONTEXT START ----------------------------------------------------------------
context = (
    f"Tu es un humain de {config['years']} ans, étudiant en {config['field']}. "
    f"Tu es socialement {config['social']} et répondras aux matchs Tinder à chaque fois. "
    f"Concernant ta vie privée, tu révéleras ton âge uniquement si on te le demande."
    f"Tu es en {config['country']} et tu es très à l'aise avec la culture de la région."
)
# ---------------------------------------------------------------- CONTEXT END ----------------------------------------------------------------

private_endpoint = "https://127.0.0.1/"

openai.api_key = "<votre_clé_API_OpenAI>"

auth_token = ""


headers = {
    "X-Auth-Token": auth_token,
    "Content-Type": "application/json",
    "User-Agent": "Tinder/11.12.0 (iPhone; iOS 14.0; Scale/3.00)"
}


def get_matches():
    url = "https://api.gotinder.com/v2/matches?count=100"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        matches = response.json()
        return matches["data"]["matches"]
    else:
        print(f"Erreur : {response.status_code} - {response.text}")
        return []


def get_messages(match_id):
    url = f"https://api.gotinder.com/v2/matches/{match_id}/messages"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        messages = response.json()
        return messages["data"]["messages"]
    else:
        print(f"Erreur : {response.status_code} - {response.text}")
        return []


def send_message(match_id, message):
    url = f"https://api.gotinder.com/user/matches/{match_id}"
    payload = {"message": message}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Message envoyé : {message}")
    else:
        print(f"Erreur lors de l'envoi du message : {response.status_code} - {response.text}")


def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response['choices'][0]['message']['content']


matches = get_matches()
messages_cache = {}

while True:
    time.sleep(60)
    for match in matches:
        match_id = match["_id"]
        name = match['person']['name']


        messages = get_messages(match_id)
        new_messages = [
            msg for msg in messages
            if msg["_id"] not in messages_cache.get(match_id, [])
        ]


        messages_cache[match_id] = [msg["_id"] for msg in messages]


        for message in new_messages:
            if message["from"] != match["person"]["_id"]:
                prompt = message["message"]
                print(f"Message reçu de {name} : {prompt}")
                response = generate_response(prompt)
                if response == "help-assistance:questions" or "help-assistance" in response:
                    requests.post(private_endpoint, json={"question": "Assistance demandée"})
                else:
                    send_message(match_id, response)
                
