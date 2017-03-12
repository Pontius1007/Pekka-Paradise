import requests
from app import feedback_methods
import user_methods
import ime_data_fetch
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
    for sender, incoming_message, payload in messaging_events(payload):
            # The following statements check which options the user selected
            # Response handler contains "templates" for the various messages
            user_name = get_full_name(sender, PAT)
            if "hei" in incoming_message.lower() or "hallo" in incoming_message.lower() or "yo" in incoming_message.lower():
                response_handler.greeting_message(PAT, sender)
                if user_methods.has_user(user_name):
                    response_handler.has_course(PAT, sender, user_methods.get_subject(user_name))
                else:
                    response_handler.no_course(PAT, sender)

            # TODO Add some sort of feedback #
            elif "Select Course" in incoming_message:
                pass

            elif incoming_message == "Change subject":
                response_handler.text_message(PAT, sender, "Pekka is love, Pekka is life")
            # These options should have similar("The same??") feedback #

            elif payload == "lecture_feedback":
                # TODO Check if there is an ongoing lecture somehow?
                response_handler.lec_feed(PAT, sender)

            elif payload == "Fast" or payload == "Ok" or payload == "Slow":
                feedback_methods.add_entry(user_name, user_methods.get_subject(user_name), payload)
                response_handler.text_message(PAT, sender, "You chose " + payload + "\n Feedback Received!")
                response_handler.has_course(PAT, sender, user_methods.get_subject(user_name))

            elif payload == "get_schedule":
                subject = user_methods.get_subject(user_name)
                response_handler.text_message(PAT, sender, sub_info.printable_schedule(sub_info.get_schedule(subject)))
                response_handler.has_course(PAT, sender, user_methods.get_subject(user_name))

            elif payload == "get_info":
                subject = user_methods.get_subject(user_name)
                response_handler.text_message(PAT, sender, sub_info.printable_course_info(sub_info.get_course_json(subject)))
                response_handler.has_course(PAT, sender, user_methods.get_subject(user_name))

            elif ime_data_fetch.subject_exists_boolean(incoming_message.split()[0]):
                if user_methods.has_user(user_name):
                    user_methods.add_subject(user_name, incoming_message.split()[0])
                else:
                    user_methods.add_user(user_name, incoming_message.split()[0])
                response_handler.has_course(PAT, sender, user_methods.get_subject(user_name))

            # TODO Find out why this does not work
            # else:
            #    response_handler.text_message(PAT, sender, "TIP! \n You can change course at any time simply by "
            #                                               "writing the course code on the form [TAG][CODE] \n "
            #                                               "ex. TDT4120")

    return "ok"


def messaging_events(payload):
    """
    Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    # TEST TEST
    print("This is the data in the message:")
    print(data)
    # END TEST
    message = data["entry"][0]["messaging"]
    # Testing to see what message is
    print(message)
    # EndTest
    for event in message:
        # if message in bla and text and payload bla yield payload as well
        if "message" in event and "quick_reply" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"], event["message"]["quick_reply"]["payload"]
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"], None
            # Yield path to payload
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


def get_full_name(sender, token):
    """
    Gets the full name of sender.
    Uses a get request.
    :param sender:
    :return: full name. String
    """
    url = "https://graph.facebook.com/v2.6/" + sender + "?fields=first_name,last_name&access_token=" + token
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    print(data)
    print(''.join(data['first_name'] + ' ' + data['last_name']))
    return ''.join(data['first_name'] + ' ' + data['last_name'])
