import requests
from flask import request
import json
import sub_info
from app import app
from app import responses


PAT = 'EAACI4GIIx08BAHwR6J1cOROTpYbE9QceOhxR08JBywhdAV6t24J70RG28YaZCzQxJGinIB6v0xy7Y7gdTVQUZCmgRwm1EVBQd05kMYCwi' \
      'kkTAtmHbxVhTUvvpMGYM9vcTKD2qPXmwcZCDgOVX1eZCUGNfzJpyifuocmDXIMElQZDZD'
response_handler = responses


@app.route('/', methods=['GET'])
def handle_verification():
    print("Handling Verification: ->")
    if request.args.get('hub.verify_token', '') == 'Heisann32141221':
        print("Verification successful!")
        return request.args.get('hub.challenge', '')
    else:
        print("Verification failed!")
        return 'Error, wrong validation token'


# The wonderful logic that decides which response is sent should be placed in this function
@app.route('/', methods=['POST'])
def handle_messages():
    print("Handling Messages")
    payload = request.get_data()
    # Remove this one day...
    print(payload)
    for sender, incoming_message in messaging_events(payload):
        # TODO Figure out how to access payload content
        # This solution is not very good, we must learn to use payload

            # The following statements check which options the user selected
            # Response handler contains "templates" for the various messages
            if "yes" in incoming_message.lower():
                response_handler.quick_reply(PAT, sender)
            if "hei" in incoming_message.lower() or "hallo" in incoming_message.lower():
                response_handler.greeting_message(PAT, sender)
            elif incoming_message == "Schedule":
                response_handler.text_message(PAT, sender, sub_info.printable_schedule(sub_info.get_schedule("tdt4145")))
                response_handler.supp_message(PAT, sender)

            elif incoming_message == "Info":
                response_handler.text_message(PAT, sender, sub_info.printable_course_info(sub_info.get_course_json("tdt4145")))
                response_handler.supp_message(PAT, sender)

            elif incoming_message == "Secret":
                response_handler.text_message(PAT, sender, "Pekka is love, Pekka is life")
                response_handler.supp_message(PAT, sender)
            else:
                response_handler.quick_reply(PAT, sender)

            # TEST
            # get_full_name(sender)

    return "ok"


def messaging_events(payload):
    """
    Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    # TESTTEST
    print("This is the data in the message:")
    print(data)
    # ENDTEST
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


def get_full_name(sender):
    """
    Gets the full name of sender.
    Uses a get request.
    :param sender:
    :return: full name. String
    """
    url = "https://graph.facebook.com/v2.6/" + sender + "?fields=first_name,last_name&access_token=" + PAT
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    print(data)
    print(''.join(data['first_name'] + ' ' + data['last_name']))
    return ''.join(data['first_name'] + ' ' + data['last_name'])
