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
    print(payload)
    for sender, incoming_message in messaging_events(payload):
        # Checks if subject exists
        # outgoing_message = ime_data_fetch.subject_exists(incoming_message.split()[0])
        # Sends Course name to correct user
        # send_message(PAT, sender, outgoing_message)
        # launches button test
        send_button_test(PAT, sender)
    return "ok"


def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    # Testing to see what message is
    print(messaging_events)
    # EndTest
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"]
        else:
            yield event["sender"]["id"], "I can't echo this"


def send_button_test(token, recipient):
    txt = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token}, data=json.dumps({
        "recipient": {"id": recipient},
        "message": {"text": "This is a response"}
    }), headers={'Content-type': 'application/json'})

    test_message = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token}, data=json.dumps({
         "recipient": {"id": recipient},
         "message": {
             "attachment": {
                 "type": "template",
                 "payload": {
                     "template_type": "button",
                     "text": "What can I do for you today?",
                     "buttons": [
                         {
                             "type": "web_url",
                             "url": "https://google.com",
                             "title": "Show Google"
                         },
                         {
                             "type": "postback",
                             "title": "Start Chatting",
                             "payload": txt
                         },
                     ]
                 }
             }
         }
    }), headers={'Content-type': 'application/json'})

    if test_message.status_code != requests.codes.ok:
        print(test_message.text)


def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient.
    """

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token}, data=json.dumps({
        "recipient": {"id": recipient},
        "message": {"text": text}
        }),
        headers={'Content-type': 'application/json'})

    if r.status_code != requests.codes.ok:
        print(r.text)
