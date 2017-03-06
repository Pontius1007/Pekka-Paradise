from flask import request
import json
import requests
import ime_data_fetch
from app import app


PAT = 'EAACI4GIIx08BAHwR6J1cOROTpYbE9QceOhxR08JBywhdAV6t24J70RG28YaZCzQxJGinIB6v0xy7Y7gdTVQUZCmgRwm1EVBQd05kMYCwi' \
      'kkTAtmHbxVhTUvvpMGYM9vcTKD2qPXmwcZCDgOVX1eZCUGNfzJpyifuocmDXIMElQZDZD'


@app.route('/', methods=['GET'])
def handle_verification():
    print("Handling Verification: ->")
    if request.args.get('hub.verify_token', '') == 'Heisann32141221':
        print("Verification successful!")
        return request.args.get('hub.challenge', '')
    else:
        print("Verification failed!")
        return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def handle_messages():
    print("Handling Messages")
    payload = request.get_data()
    for sender, incoming_message in messaging_events(payload):
        #TEST
        test_get_full_name(sender)
        #ENDTEST
        # Uses the ime api with the course code
        outgoing_message = ime_data_fetch.subject_exists(incoming_message.split()[0])
        # Sends the message
        send_message(PAT, sender, outgoing_message)
    return "ok"


def messaging_events(payload):
    """
    Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    #TESTTEST
    print("This is the data in the message:")
    print(data)
    #ENDTEST
    message = data["entry"][0]["messaging"]
    # Testing to see what message is
    print(message)
    # EndTest
    for event in message:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"]
        else:
            yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
    """
    Send the message text to recipient with id recipient.
    """

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token}, data=json.dumps({
        "recipient": {"id": recipient},
        "message": {"text": text}
        }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)


def test_get_full_name(sender):
    test = requests.get("https://graph.facebook.com/v2.6/" + sender + "fields=first_name,last_name&access_token=" + PAT)
    print(test)


