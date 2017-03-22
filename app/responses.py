import json
import requests
import ime_data_fetch



# This file consists of responses sent to the user as JSON objects


def greeting_message(token, recipient, user_name):
    """
    Sends personal greeting message to the user
    :param token:
    :param recipient:
    :param user_name:
    :return:
    """
    message = "Hello " + user_name.split()[0] + "!\nWhat can I do for you today?"
    txt = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                        data=json.dumps({
                            "recipient": {"id": recipient},
                            "message": {"text": message}
                        }), headers={'Content-type': 'application/json'})
    if txt.status_code != requests.codes.ok:
        print(txt.text)


def text_message(token, recipient, message):
    """
    Sends any string(message) to the user
    :param token:
    :param recipient:
    :param message:
    :return:
    """
    txt = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                        data=json.dumps({
                            "recipient": {"id": recipient},
                            "message": {"text": message}
                        }), headers={'Content-type': 'application/json'})
    if txt.status_code != requests.codes.ok:
        print(txt.text)


def user_info(token, recipient, user_name, sub):
    """
    Shows our information about the user to the user
    :param token:
    :param sub:
    :param recipient:
    :param user_name:
    :return:
    """
    message = "Hello " + user_name + " !\n You currently have " + sub + " selected"
    txt = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                        data=json.dumps({
                            "recipient": {"id": recipient},
                            "message": {"text": message}
                        }), headers={'Content-type': 'application/json'})
    if txt.status_code != requests.codes.ok:
        print(txt.text)


# This is a greeting message for first time users and will be a part of later user stories
# We will probably use it as is, so we let it stay as a comment for now
# def greeting_message(token, recipient):
#    greet = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
#                          data=json.dumps({
#                              "recipient": {"id": recipient},
#                              "message": {{
#                                  "setting_type": "greeting",
#                                  "greeting": {
#                                      "text": "Hi {{user_first_name}}, welcome to L.I.M.B.O."
#                                  }
#                              }}
#                          }), headers={'Content-type': 'application/json'})
#    if greet.status_code != requests.codes.ok:
#        print(greet.text)


def no_course(token, recipient):
    """
    Sends quick replies available to the user without a course selected
    :param token:
    :param recipient:
    :return:
    """
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                         data=json.dumps({
                             "recipient": {"id": recipient},
                             "message": {
                                 "text": "You have not chosen a subject \n What would you like to do?:",
                                 "quick_replies": [
                                     {
                                         "content_type": "text",
                                         "title": "Select Course",
                                         "payload": "Change subject"
                                     }
                                 ]
                             }
                         }),
                         headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)


def has_course(token, recipient, subject):
    """
    Sends quick replies available to the user with a course selected
    :param token:
    :param recipient:
    :param subject:
    :return:
    """
    subject_name = ime_data_fetch.get_subject_name(subject)
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                         data=json.dumps({
                             "recipient": {"id": recipient},
                             "message": {
                                 "text": "You have chosen: " + subject_name + "\nWhat would you like to do?:",
                                 "quick_replies": [
                                     {
                                         "content_type": "text",
                                         "title": "Get info",
                                         "payload": "get info"
                                     },
                                     {
                                         "content_type": "text",
                                         "title": "Get schedule",
                                         "payload": "get schedule"
                                     },
                                     {
                                         "content_type": "text",
                                         "title": "Change subject",
                                         "payload": "change subject"
                                     },
                                     {
                                         "content_type": "text",
                                         "title": "Lecture Feedback",
                                         "payload": "lecture feedback"
                                     },
                                     {
                                         "content_type": "text",
                                         "title": "Get feedback",
                                         "payload": "get feedback"
                                     }
                                 ]
                             }
                         }),
                         headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)


def lec_feed(token, recipient):
    """
    Lets the user choose whether a lecture is too fast, slow or ok
    :param token:
    :param recipient:
    :return:
    """
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                         data=json.dumps({
                             "recipient": {"id": recipient},
                             "message": {
                                 "text": "How do you think this lecture is going:",
                                 "quick_replies": [
                                     {
                                         "content_type": "text",
                                         "title": "Too slow",
                                         "payload": "Too slow"
                                     },
                                     {
                                         "content_type": "text",
                                         "title": "It's all right",
                                         "payload": "It's all right"
                                     },
                                     {
                                         "content_type": "text",
                                         "title": "Too fast",
                                         "payload": "Too fast"
                                     }
                                 ]
                             }
                         }),
                         headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)


"""
THIS SECTION FOR FEEDBACK FROM LECTURES
"""


def get_feedback_specific_or_all(token, recipient):
    """
    Lets the user choose to get feedback for a specific lecture or all lectures.
    :param token:
    :param recipient:
    :return:
    """
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                         data=json.dumps({
                             "recipient": {"id": recipient},
                             "message": {
                                 "text": "Do you want feedback from all the lectures or a specific lecture?",
                                 "quick_replies": [
                                     {
                                         "content_type": "text",
                                         "title": "All lectures",
                                         "payload": "all_lectures"
                                     },
                                     {
                                         "content_type": "text",
                                         "title": "A specific lecture",
                                         "payload": "a_specific_lecture"
                                     }
                                 ]
                             }
                         }),
                         headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)


def get_feedback_year(token, recipient, years):
    """
    Lets the user choose to get feedback for a specific lecture or all lectures.
    :param token:
    :param recipient:
    :param years:
    """

    # Makes initial json object.
    json_message = {
        "recipient": {"id": recipient},
        "message": {
            "text": "Select what year you want feedback from",
            "quick_replies": [
            ]
        }
    }

    # Adds buttons to the json object depending on how many years in arg.
    for year in years:
        json_message["message"]["quick_replies"].append({
            "content_type": "text",
            "title": str(year),
            "payload": "get_lecture_feedback_year " + str(year)
        })

    # Sends message.
    data = json.dumps(json_message)
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                         data=data,
                         headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)


def get_feedback_semester(token, recipient, year, semesters):
    """
    Lets the user choose to get feedback for a specific lecture or all lectures.
    :param token: String
    :param recipient: int
    :param year: int
    :param semesters: list[String]
    """

    # Makes initial json object.
    json_message = {
        "recipient": {"id": recipient},
        "message": {
            "text": "Select what semester you want feedback from",
            "quick_replies": [
            ]
        }
    }

    # Adds buttons to the json object depending on how many semesters in arg.
    for semester in semesters:
        json_message["message"]["quick_replies"].append({
            "content_type": "text",
            "title": semester,
            "payload": "get_lecture_feedback_semester " + str(year) + ' ' + semester
        })

    # Sends message.
    data = json.dumps(json_message)
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                         data=data,
                         headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)


def get_feedback_month(token, recipient, year, weeks_list):
    """
    Lets the user choose to get feedback for a specific lecture or all lectures.
    :param token: String
    :param recipient: int
    :param year: String
    :param weeks_list: list[int]
    """

    # Makes initial json object.
    json_message = {
        "recipient": {"id": recipient},
        "message": {
            "text": "Select what weeks you want feedback from:",
            "quick_replies": [
            ]
        }
    }

    # Adds buttons to the json object depending on how many groups of weeks in arg.
    weeks = []
    weeks_string = str(weeks_list[0])
    for i in range(len(weeks_list)):
        if len(weeks) > 3:
            add_weeks_to_json(weeks, weeks_string, json_message, year)
            weeks = [weeks_list[i]]
            weeks_string = str(weeks_list[i])
        else:
            weeks.append(weeks_list[i])
    if len(weeks) > 0:
        add_weeks_to_json(weeks, weeks_string, json_message, year)

    # Sends message.
    data = json.dumps(json_message)
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                         data=data,
                         headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)


def get_feedback_week(token, recipient, year, week_list):
    """
    Sends a message to recipient with buttons for selecting what week to feedback from.
    :param token: String
    :param recipient: int
    :param year: String
    :param week_list: lint[int]
    """

    # Makes initial json object.
    json_message = {
        "recipient": {"id": recipient},
        "message": {
            "text": "Select what week you want feedback from:",
            "quick_replies": [
            ]
        }
    }

    # Adds buttons to the json object depending on how many weeks in arg.
    for week in week_list:
        json_message["message"]["quick_replies"].append({
            "content_type": "text",
            "title": 'Week: ' + str(week),
            "payload": "get_lecture_feedback_week " + year + ' ' + str(week)
        })

    # Sends message.
    data = json.dumps(json_message)
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                         data=data,
                         headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)


def get_feedback_day(token, recipient, year, days, week):
    """
    :param token: String
    :param recipient: int
    :param year: String
    :param days: List[int]
    :param week: String
    :return:
    """

    # Makes initial json object.
    json_message = {
        "recipient": {"id": recipient},
        "message": {
            "text": "Select what day you want feedback from",
            "quick_replies": [
            ]
        }
    }

    # Adds buttons to the json object depending on how many semesters in arg.
    for day in days:
        add_days_to_json(days, json_message, year, week)

    # Sends message.
    data = json.dumps(json_message)
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                         data=data,
                         headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)


def add_weeks_to_json(weeks, weeks_string, json_message, year):
    """
    Adds buttons for several weeks to the json message
    :param weeks: list[int]
    :param weeks_string: String
    :param json_message:
    :param year: String
    """

    if len(weeks) == 1:
        json_message["message"]["quick_replies"].append({
            "content_type": "text",
            "title": 'Week: ' + weeks_string,
            "payload": "get_lecture_feedback_week " + year + ' ' + weeks_string
        })
    else:
        for j in range(1, len(weeks)):
            weeks_string += ', ' + str(weeks[j])
        json_message["message"]["quick_replies"].append({
            "content_type": "text",
            "title": weeks_string,
            "payload": "get_lecture_feedback_month " + year + ' ' + weeks_string
        })


def add_days_to_json(days, json_message, year, week):

    for i in range(0, len(days)):
        lecture_day = ''
        if days[i] == 1:
            lecture_day = 'Monday'
        elif days[i] == 2:
            lecture_day = 'Tuesday'
        elif days[i] == 3:
            lecture_day = 'Wednesday'
        elif days[i] == 4:
            lecture_day = 'Thursday'
        elif days[i] == 5:
            lecture_day = 'Friday'

        json_message["message"]["quick_replies"].append({
            "content_type": "text",
            "title": lecture_day,
            "payload": "get_lecture_feedback_day " + str(year) + ' ' + str(week) + ' ' + str(lecture_day)
        })
