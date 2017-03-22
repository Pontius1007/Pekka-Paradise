import json

import requests
from flask import request

import feedback_methods
import ime_data_fetch
import lecture_methods
import sub_info
import user_methods
import lecture_feedback_db_methods
from app import app
from app import responses
from config import PAT
from config import VERIFY_TOKEN

response_handler = responses


@app.route('/', methods=['GET'])
def handle_verification():
    print("Handling Verification: ->")
    if request.args.get('hub.verify_token', '') == VERIFY_TOKEN:
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
        # Start test
        print(payload)
        # End test
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
            response_handler.get_feedback_specific_or_all(PAT, sender)

        elif payload == "all_lectures":
            # TODO: call method with subject as arg.
            pass

        elif payload == "a_specific_lecture":
            # Let the user choose what year to get feedback from.
            years = lecture_feedback_db_methods.get_year(user_methods.get_subject_from_user(user_name))
            response_handler.get_feedback_year(PAT, sender, years)

        elif payload is not None:

            if "get_lecture_feedback_year" in payload.split()[0]:
                # Let the user choose what semester to get feedback from.
                semesters = []
                if lecture_feedback_db_methods.check_lecture_semester(user_methods.get_subject_from_user(user_name),
                                                                      1, 17, int(payload.split()[1])):
                    semesters.append('Spring')
                elif lecture_feedback_db_methods.check_lecture_semester(user_methods.get_subject_from_user(user_name),
                                                                        32, 49, int(payload.split()[1])):
                    semesters.append('Fall')
                if len(semesters) > 0:
                    response_handler.get_feedback_semester(PAT, sender, payload.split()[1], semesters)
                else:
                    # Take the user one step up to choose a different year.
                    years = lecture_feedback_db_methods.get_year(user_methods.get_subject_from_user(user_name))
                    response_handler.get_feedback_year(PAT, sender, years)

            elif "get_lecture_feedback_semester" in payload.split()[0]:
                # Let the user choose what weeks to get feedback from.

                week_list = lecture_feedback_db_methods.get_lecture_weeks(user_methods.get_subject_from_user(user_name),
                                                                          int(payload.split()[1]), payload.split()[2])
                print(week_list)
                if len(week_list) > 8:
                    response_handler.get_feedback_month(PAT, sender, payload.split()[1], week_list)
                else:
                    response_handler.get_feedback_week(PAT, sender, payload.split()[1], week_list)

            # Let the user select week
            elif "get_lecture_feedback_month" in payload.split()[0]:
                # TODO: test.
                week_list = []
                payload_split = payload.split()
                for i in range(2, len(payload_split)):
                    week_list.append(int(payload_split[i].rstrip(',')))

                response_handler.get_feedback_week(PAT, sender, payload_split[1], week_list)

            # Lets the user select day
            elif "get_lecture_feedback_week" in payload.split()[0]:
                lecture_days = lecture_feedback_db_methods.get_day_of_lecture_in_week(user_methods.get_subject(user_name),
                                                                                  payload.split()[1], payload.split()[2])

                response_handler.get_feedback_day(PAT, sender, payload.split()[1], lecture_days, payload.split()[2])

                # TODO: take in year, month and week. Let the user choose what day to get feedback from.
                pass

            # Lets the user select a lecture
            elif "get_lecture_feedback_day" in payload.split()[0]:
                # TODO: take in year, month, week and day. present the user with information from the lecture feedback.
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
    Generate tuples of (sender_id, message_text, payload) from the
    provided payload.
    """
    data = json.loads(payload)
    message = data["entry"][0]["messaging"]
    for event in message:
        if "message" in event and "text" in event["message"]:
            # if message in event and text in message set id and text
            sender_id = event["sender"]["id"]
            text = event["message"]["text"]
            quick_reply_payload = None

            if "quick_reply" in event["message"]:
                # if quick_reply i message set payload
                quick_reply_payload = event["message"]["quick_reply"]["payload"]
            yield sender_id, text, quick_reply_payload
        else:
            yield event["sender"]["id"], "I can't echo this", None


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
