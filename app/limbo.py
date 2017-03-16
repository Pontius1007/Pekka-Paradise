import json

import requests
from flask import request

import feedback_methods
import ime_data_fetch
import lecture_methods
import sub_info
import user_methods
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
    # IMPORTANT remember to add all new quick-reply titles to this list!
    titles = ["Change subject", "Get info", "Select Course", "Get schedule", "Lecture Feedback",
              "Too slow", "It's all right", "Too fast"]
    payload = request.get_data()
    for sender, incoming_message, payload in messaging_events(payload):
        # The following statements check which options the user selected
        # Response handler contains "templates" for the various messages
        user_name = get_full_name(sender, PAT)
        if "hei" in incoming_message.lower() or "hallo" in incoming_message.lower() or "yo" in incoming_message.lower():
            response_handler.greeting_message(PAT, sender, user_name)
            if user_methods.has_user(user_name):
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))
            else:
                response_handler.no_course(PAT, sender)

        elif payload == "change subject":
            response_handler.text_message(PAT, sender, "You can change course at any time simply by "
                                                       "writing the course code on the form [TAG][CODE]\n"
                                                       "ex. TDT4120")
        elif incoming_message == "help":
            response_handler.text_message(PAT, sender, "Are you lost ...? ")
            response_handler.text_message(PAT, sender, "You can change course at any time simply by "
                                                       "writing the course code on the form: [TAG][CODE]\n"
                                                       "ex. TDT4120")
            response_handler.text_message(PAT, sender, "If you want to see your currently selected course "
                                                       "and other information type 'Status'.")
            response_handler.text_message(PAT, sender, "You can also type 'Hei' or 'Hallo' at any time "
                                                       "to receive a greeting that shows your options.")
        elif incoming_message == "status":
            if user_methods.has_user(user_name):
                sub = user_methods.get_subject_from_user(user_name) + " : " + \
                      sub_info.course_name(user_methods.get_subject_from_user(user_name))
            else:
                sub = "no subject"
            response_handler.user_info(PAT, sender, user_name, sub)

        # Checks if the subject has lectures in the database, adds them if not.

        elif payload == "lecture feedback":
            subject = user_methods.get_subject_from_user(user_name)

            if lecture_methods.check_lecture_in_db(subject):
                response_handler.lec_feed(PAT, sender)
            else:
                schedule = sub_info.get_schedule(subject)
                if schedule:
                    database_entry = sub_info.gather_lecture_information(schedule)
                    lecture_methods.add_lecture_information_db(database_entry)
                    response_handler.text_message(PAT, sender, "Lectures for the subject " + subject +
                                                  " were not in the database. It is now added")
                    response_handler.lec_feed(PAT, sender)
                else:
                    response_handler.text_message(PAT, sender, "Lectures for the subject " + subject +
                                                  " does not exist. Likely due to the subject having no "
                                                  "lectures this semester.")
                    response_handler.has_course(PAT, sender, subject)

        elif payload == "Too fast" or payload == "It's all right" or payload == "Too slow":
            # Adds feedback if the subject has a lecture on the given day
            # and if the user has not already given feedback
            print('I was here')
            if feedback_methods.add_entry(user_name, user_methods.get_subject_from_user(user_name), payload):
                response_handler.text_message(PAT, sender, "You chose: " + "'" + payload + "'" + "\nFeedback Received!")
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))
            else:
                response_handler.text_message(PAT, sender, "There is either no lecture active in the selected"
                                                           " subject, or you have already given feedback"
                                                           " to the active lecture.\nFeedback denied!")
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif payload == "get schedule":
            subject = user_methods.get_subject_from_user(user_name)
            response_handler.text_message(PAT, sender, sub_info.printable_schedule(sub_info.get_schedule(subject)))
            response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif payload == "get info":
            subject = user_methods.get_subject_from_user(user_name)
            response_handler.text_message(PAT, sender,
                                          sub_info.printable_course_info(sub_info.get_course_json(subject)))
            response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif payload == "get feedback":
            subject = user_methods.get_subject_from_user(user_name)
            response_handler.get_feedback_specific_or_all(PAT, sender)

        elif payload == "all lectures":
            # TODO: call method with subject as arg.
            pass

        elif payload == "a specific lecture":
            # TODO: Find the weeks that have lectures. And let the user choose what week to get feedback from.
            pass

        elif payload == "":
            # TODO: take in what weeks to present the user if possible? present the remaining weeks to user.
            pass

        elif payload == "":
            # TODO:
            pass

        elif ime_data_fetch.subject_exists_boolean(incoming_message.upper().split()[0]):
            if user_methods.has_user(user_name):
                user_methods.add_subject(user_name, incoming_message.split()[0])
            else:
                user_methods.add_user(user_name, incoming_message.split()[0])
            response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif incoming_message not in titles:
            response_handler.text_message(PAT, sender, "Type 'help' to see what you can do with L.I.M.B.O.")

    return "ok"


def messaging_events(payload):
    """
    Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    message = data["entry"][0]["messaging"]
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
    :param token:
    :return: full name. String
    """
    url = "https://graph.facebook.com/v2.6/" + sender + "?fields=first_name,last_name&access_token=" + token
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    return ''.join(data['first_name'] + ' ' + data['last_name'])
