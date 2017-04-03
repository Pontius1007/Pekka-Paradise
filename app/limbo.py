import json
import requests
from flask import request
import bot_feedback
import feedback_methods
import ime_data_fetch
import lecture_methods
import subject_info
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


# The wonderful logic that decides which response is sent is placed in this function
@app.route('/', methods=['POST'])
def handle_messages():
    print("Handling Messages")
    # IMPORTANT remember to add all new quick-reply titles to this list!
    # titles = ["Change subject", "Get info", "Select Course", "Get schedule", "Lecture Feedback",
    #           "Too slow", "It's all right", "Too fast"]
    payload = request.get_data()
    for sender, incoming_message, payload in messaging_events(payload):
        # The following statements check which options the user selected
        # Response handler contains "templates" for the various messages
        # Start test
        print(payload)
        # End test
        user_name = get_full_name(sender, PAT)
        if "hei" in incoming_message.lower() or "hallo" in incoming_message.lower() or "yo" in incoming_message.lower()\
                or "hi" in incoming_message.lower():
            response_handler.greeting_message(PAT, sender, user_name)
            if user_methods.has_user(user_name):
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))
            else:
                response_handler.no_course(PAT, sender)

        elif payload == "change subject" or "change subject" in incoming_message.lower():
            response_handler.text_message(PAT, sender, "You can change course at any time simply by "
                                                       "writing the course code on the form [TAG][CODE]\n"
                                                       "ex. TDT4120")
            response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif "help" in incoming_message.lower():

            response_handler.text_message(PAT, sender, "Are you lost ...? ")
            response_handler.text_message(PAT, sender, "You can change course at any time simply by "
                                                       "writing the course code on the form: [TAG][CODE]\n"
                                                       "ex. TDT4120")
            response_handler.text_message(PAT, sender, "If you want to see your currently selected course "
                                                       "and other information type 'Status'.")
            response_handler.text_message(PAT, sender, "You can also type 'Hei' or 'Hallo' at any time "
                                                       "to receive a greeting that shows your options.")
            response_handler.text_message(PAT, sender, "Here is a list of commands you can use. This is "
                                                       "recommended for the experienced user:\n"
                                                       "Change subject\n"
                                                       "Give feedback\n"
                                                       "How did today's lecture go?\n"
                                                       "Get schedule\n"
                                                       "Get info\n"
                                                       "All lectures\n"
                                                       "A specific lecture\n"
                                                       "You can type most of the commands in chat. Just give it a try!")
            response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif "status" in incoming_message.lower():
            subject = user_methods.get_subject_from_user(user_name)
            year = feedback_methods.get_year()
            week = feedback_methods.get_week()
            day = feedback_methods.get_day()
            user = get_full_name(sender, PAT)
            lecture_id_current = lecture_methods.get_lecture_from_date(year, week, day, subject)
            lecture = feedback_methods.get_lecture_object(lecture_id_current)

            if user_methods.has_user(user_name):
                sub = user_methods.get_subject_from_user(user_name) + " : " + \
                      subject_info.course_name(user_methods.get_subject_from_user(user_name))
                response_handler.user_info(PAT, sender, user_name, sub)
                if feedback_methods.user_has_feedback_for_lecture(user, lecture):
                    response_handler.text_message(PAT, sender, "You have given feedback for "
                                                  + subject + " today. Well done! Be proud of yourself and "
                                                              "remember to check in tomorrow.")
                    response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))
                else:
                    response_handler.text_message(PAT, sender, "No feedback for the given lecture on this date. "
                                                               "Please press 'Give Feedback' or write it in the "
                                                               "chat to do so.")
                    response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))
            else:
                response_handler.text_message(PAT, sender, "We seem to not be able to detect you in the database. "
                                                           "Please report this to the staff!")
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        # Checks if the subject has lectures in the database, adds them if not.

        elif payload == "give feedback" or "give feedback" in incoming_message.lower():
            response_handler.give_feedback_choice(PAT, sender)

        elif payload == "lecture speed" or "lecture speed" in incoming_message.lower():

            subject = user_methods.get_subject_from_user(user_name)

            if lecture_methods.check_lecture_in_db(subject):
                response_handler.lec_feed(PAT, sender)
            else:
                schedule = subject_info.get_schedule(subject)
                if schedule:
                    database_entry = subject_info.gather_lecture_information(schedule)
                    lecture_methods.add_lecture_information_db(database_entry)
                    response_handler.text_message(PAT, sender, "Lectures for the subject " + subject +
                                                  " were not in the database. It is now added.")
                    response_handler.lec_feed(PAT, sender)
                else:
                    response_handler.text_message(PAT, sender, "Lectures for the subject " + subject +
                                                  " does not exist. Likely due to the subject having no "
                                                  "lectures this semester.")
                    response_handler.has_course(PAT, sender, subject)

        elif payload == "evaluation_questions" or "lecture questions" in incoming_message.lower():
            # User wants to give feedback for a lecture.
            subject = user_methods.get_subject_from_user(user_name)
            payload = "evaluation_questions"  # if user typed 'lecture questions' the payload will be None

            if lecture_methods.check_lecture_in_db(subject):
                if feedback_methods.user_can_give_feedback_evaluation(user_name,
                                                                      user_methods.get_subject_from_user(user_name)):
                    response_handler.lecture_feedback_questions(PAT, sender, payload)
                else:
                    response_handler.text_message(PAT, sender, "Feedback can not be given either because there is no "
                                                               "lecture today, or because you have already "
                                                               "given feedback for this lecture.")
                    response_handler.has_course(PAT, sender, subject)
            else:
                schedule = subject_info.get_schedule(subject)
                if schedule:
                    database_entry = subject_info.gather_lecture_information(schedule)
                    lecture_methods.add_lecture_information_db(database_entry)
                    response_handler.text_message(PAT, sender, "Lectures for the subject " + subject +
                                                  " were not in the database. It is now added")
                    if feedback_methods.user_can_give_feedback_evaluation(user_name,
                                                                          user_methods.get_subject_from_user(
                                                                              user_name)):
                        response_handler.lecture_feedback_questions(PAT, sender, payload)
                    else:
                        response_handler.text_message(PAT, sender, "Feedback can not be given either because there is "
                                                                   "no lecture today, or because you have already "
                                                                   "given feedback for this lecture.")
                        response_handler.has_course(PAT, sender, subject)
                else:
                    response_handler.text_message(PAT, sender, "Lectures for the subject " + subject +
                                                  " does not exist. Likely due to the subject having no "
                                                  "lectures this semester.")
                    response_handler.has_course(PAT, sender, subject)

        elif "too slow" in incoming_message.lower():
            # Adds feedback if the subject has a lecture on the given day
            # and if the user has not already given feedback
            payload = '0'
            message_response = "too slow"
            if feedback_methods.add_entry(user_name, user_methods.get_subject_from_user(user_name), payload):
                response_handler.text_message(PAT, sender, "You chose: " + "'" +
                                              message_response + "'" + "\nFeedback Received!")
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))
            else:
                response_handler.text_message(PAT, sender, "There is either no lecture active in the selected"
                                                           " subject, or you have already given feedback"
                                                           " to the active lecture.\nFeedback denied!")
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif "it's all right" in incoming_message.lower() or "its all right" in incoming_message.lower():
            # Adds feedback if the subject has a lecture on the given day
            # and if the user has not already given feedback
            payload = '1'
            message_response = "It's all right"
            if feedback_methods.add_entry(user_name, user_methods.get_subject_from_user(user_name), payload):
                response_handler.text_message(PAT, sender, "You chose: " + "'" +
                                              message_response + "'" + "\nFeedback Received!")
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))
            else:
                response_handler.text_message(PAT, sender, "There is either no lecture active in the selected"
                                                           " subject, or you have already given feedback"
                                                           " to the active lecture.\nFeedback denied!")
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif "too fast" in incoming_message.lower():
            # Adds feedback if the subject has a lecture on the given day
            # and if the user has not already given feedback
            payload = '2'
            message_response = "too fast"
            if feedback_methods.add_entry(user_name, user_methods.get_subject_from_user(user_name), payload):
                response_handler.text_message(PAT, sender, "You chose: " + "'" +
                                              message_response + "'" + "\nFeedback Received!")
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))
            else:
                response_handler.text_message(PAT, sender, "There is either no lecture active in the selected"
                                                           " subject, or you have already given feedback"
                                                           " to the active lecture.\nFeedback denied!")
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif ("today" in incoming_message.lower() and "lecture" in incoming_message.lower()) or \
                ("todays" in incoming_message.lower() and "lecture" in incoming_message.lower()) or \
                ("today's" in incoming_message.lower() and "lecture" in incoming_message.lower()):
            # Gathers the correct information about the date.
            year = feedback_methods.get_year()
            week = feedback_methods.get_week()
            day = feedback_methods.get_day()
            subject = user_methods.get_subject_from_user(user_name)

            # Gathers the feedback from today's lecture:
            if lecture_methods.check_lecture_in_db(subject):
                feedback_list = feedback_methods.get_single_lecture_feed(year, week, day, subject)
                if feedback_list[0] is not None:
                    response_handler.present_single_lecture_feedback(PAT, sender, feedback_list)
                    response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))
                else:
                    response_handler.text_message(PAT, sender, "No feedback for the given lecture on this date. "
                                                               "Please try again at a later date.")
                    response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))
            else:
                response_handler.text_message(PAT, sender, "No  lecture present in the database. "
                                                           "Please provide some feedback and try again.")
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif payload == "get schedule" or "get schedule" in incoming_message.lower():
            subject = user_methods.get_subject_from_user(user_name)
            response_handler.text_message(PAT, sender,
                                          subject_info.printable_schedule(subject_info.get_schedule(subject)))
            response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif payload == "get info" or "get info" in incoming_message.lower():
            subject = user_methods.get_subject_from_user(user_name)
            response_handler.text_message(PAT, sender,
                                          subject_info.printable_course_info(subject_info.get_course_json(subject)))
            response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif payload == "get feedback" or "get feedback" in incoming_message.lower():
            response_handler.get_feedback_specific_or_all(PAT, sender)

        elif payload == "all_lectures" or "all lectures" in incoming_message.lower():
            # The user wants to see feedback for all lectures in the selected subject
            subject = user_methods.get_subject_from_user(user_name)
            if not lecture_methods.check_lecture_in_db(subject):
                response_handler.text_message(PAT, sender, "Course has no feedback.")
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))
            else:
                feedback, feedbackevaluation = feedback_methods.get_all_subject_feed(subject)
                if len(feedback) > 0:
                    percent_list = bot_feedback.generate_percent_for_speed(feedback)
                    response_handler.all_feedback_speed(PAT, sender, subject, percent_list)
                else:
                    response_handler.text_message(PAT, sender, "Course has no feedback for lecture speed.")
                if len(feedbackevaluation) > 0:
                    percent_list_questions = bot_feedback.generate_percent_for_questions(feedbackevaluation)

                    response_handler.all_feedback_questions(PAT, sender, subject, percent_list_questions)
                else:
                    response_handler.text_message(PAT, sender, "Course has no feedback for lecture questions.")
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif payload == "a_specific_lecture" or "a specific lecture" in incoming_message.lower():
            # Let the user choose what year to get feedback from.
            years = lecture_feedback_db_methods.get_year(user_methods.get_subject_from_user(user_name))
            if len(years) > 0:
                response_handler.get_feedback_year(PAT, sender, years)
            else:
                response_handler.text_message(PAT, sender, 'No feedback for the selected subject.')
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif payload is not None:
            # Underneath are check that use .split() on the payload.
            if "evaluation_questions" in payload.split()[0]:
                payload_split = payload.split()
                if len(payload_split) == 1:
                    # 1st question
                    response_handler.lecture_feedback_questions(PAT, sender, payload)
                elif len(payload_split) == 2:
                    # 2nd question
                    response_handler.lecture_feedback_questions(PAT, sender, payload)
                elif len(payload_split) == 3:
                    # 3rd question
                    response_handler.lecture_feedback_questions(PAT, sender, payload)
                elif len(payload_split) == 4:
                    # 4th question
                    response_handler.lecture_feedback_questions(PAT, sender, payload)
                elif len(payload_split) == 5:
                    # 5th question
                    response_handler.lecture_feedback_questions(PAT, sender, payload)
                elif len(payload_split) == 6:
                    # 6th question
                    response_handler.lecture_feedback_questions(PAT, sender, payload)
                elif len(payload_split) == 7:
                    # 7th question
                    response_handler.lecture_feedback_questions(PAT, sender, payload)
                elif len(payload_split) == 8:
                    # store feedback.
                    subject = user_methods.get_subject_from_user(user_name)
                    if feedback_methods.add_feedback_evaluation(user_name, subject, int(payload_split[1]),
                                                                int(payload_split[2]), int(payload_split[3]),
                                                                int(payload_split[4]), int(payload_split[5]),
                                                                int(payload_split[6]), int(payload_split[7])):
                        # Storing the feedback succeeded.
                        response_handler.text_message(PAT, sender, 'Feedback received!')
                        response_handler.has_course(PAT, sender, subject)
                    else:
                        # Storing the feedback failed.
                        response_handler.text_message(PAT, sender, "There is either no lecture active in the selected "
                                                                   "subject, or you have already given feedback to the "
                                                                   "active lecture.\nFeedback denied!")
                        response_handler.has_course(PAT, sender, subject)
                    pass

            elif "get_lecture_feedback_year" in payload.split()[0]:
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

            elif "get_lecture_feedback_month" in payload.split()[0]:
                # Let the user select week
                week_list = []
                payload_split = payload.split()
                for i in range(2, len(payload_split)):
                    week_list.append(int(payload_split[i].rstrip(',')))

                response_handler.get_feedback_week(PAT, sender, payload_split[1], week_list)

            elif "get_lecture_feedback_week" in payload.split()[0]:
                # Lets the user select day
                lecture_days = lecture_feedback_db_methods.get_day_of_lecture_in_week(
                    user_methods.get_subject_from_user(user_name), payload.split()[1], payload.split()[2])

                response_handler.get_feedback_day(PAT, sender, payload.split()[1], lecture_days, payload.split()[2])

            elif "get_lecture_feedback_day" in payload.split()[0]:
                subject = user_methods.get_subject_from_user(user_name)
                # Gives the user feedback from the selected day.
                feedback_list = feedback_methods.get_single_lecture_feed(payload.split()[1],
                                                                         payload.split()[2],
                                                                         payload.split()[3],
                                                                         subject)
                feedback_questions_list = feedback_methods.get_single_lecture_feedback_questions(payload.split()[1],
                                                                                                 payload.split()[2],
                                                                                                 payload.split()[3],
                                                                                                 subject)
                if len(feedback_list[1]) > 0:  # Checks if there is feedback in the variable.
                    response_handler.present_single_lecture_feedback(PAT, sender, feedback_list)
                else:
                    response_handler.text_message(PAT, sender, "This lecture has no feedback for lecture speed.")
                if len(feedback_questions_list) > 0:  # Checks if there is feedback in the variable.
                    feedback_questions = bot_feedback.generate_percent_for_questions(feedback_questions_list)
                    response_handler.present_single_lecture_feedback_questions(PAT, sender, feedback_questions)
                else:
                    response_handler.text_message(PAT, sender, "This lecture has no feedback for lecture questions.")

                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        elif ime_data_fetch.subject_exists_boolean(incoming_message.upper().split()[0]):
            if user_methods.has_user(user_name):
                user_methods.add_subject(user_name, incoming_message.split()[0])
            else:
                user_methods.add_user(user_name, incoming_message.split()[0])
            response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))

        else:
            response_handler.text_message(PAT, sender, "Type 'help' to see what you can do with L.I.M.B.O.\nIf you "
                                                       "tried to enter a subject-code and got this message, you "
                                                       "either misspelled it or the subject you are looking for is "
                                                       "not a subject at NTNU.")
            if user_methods.has_user(user_name):
                response_handler.has_course(PAT, sender, user_methods.get_subject_from_user(user_name))
            else:
                response_handler.no_course(PAT, sender)

    return "ok"


def messaging_events(payload):
    """
    Generate tuples of (sender_id, message_text, payload) from the
    provided payload.
    :param payload: String
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
    :param token: String
    :param recipient: int
    :param text: String
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
    :param sender: int
    :param token: String
    :return: full name. String
    """
    url = "https://graph.facebook.com/v2.6/" + sender + "?fields=first_name,last_name&access_token=" + token
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    return ''.join(data['first_name'] + ' ' + data['last_name'])
