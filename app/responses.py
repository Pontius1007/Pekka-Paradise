import json
import random
import ime_data_fetch


# This file consists of responses sent to the user as JSON objects


# The following methods generates the message as a JSON object
def greeting_message(recipient, user_name):
    """
    Sends personal greeting message to the user
    :param recipient: int
    :param user_name: String
    :return: None
    """
    message = "Hello " + user_name.split()[0] + "!\nWhat can I do for you today?" + \
              "\nIf you are new to the bot and would like some help, please press 'Help' in chat"
    data = json.dumps({
            "recipient": {"id": recipient},
            "message": {"text": message}})
    return data


def text_message(recipient, message):
    """
    Sends any string(message) to the user
    :param recipient: int
    :param message: String
    :return: None
    """
    data = json.dumps({
        "recipient": {"id": recipient},
        "message": {"text": message}})
    return data


def user_info(recipient, user_name, sub):
    """
    Shows our information about the user to the user
    :param recipient: int
    :param user_name: String
    :param sub: String
    :return: None
    """
    message = "Hello " + user_name + "!\nYou currently have " + sub + " selected"
    data = json.dumps({
        "recipient": {"id": recipient},
        "message": {"text": message}})
    return data


def all_feedback_speed(recipient, subject, percent):
    """
    Presents feedback from all lectures from LectureFeedback of a subject to the user.
    :param recipient: int
    :param subject: String
    :param percent: index 0-2 contains percents of slow, ok and fast index 3 contains total number
    :return: None
    """
    url_slow = ["http://www.bbcactive.com/BBCActiveIdeasandResources/Tenwaystomakelecturesmoredynamic.aspx",
                "http://www.bbcactive.com/BBCActiveIdeasandResources/Tenwaystomakelecturesmoredynamic.aspx",
                "https://www.missouristate.edu/chhs/4256.htm"]
    url_fast = ["https://tomprof.stanford.edu/posting/491",
                "www.montana.edu%2Ffacultyexcellence%2FPapers%2Flecture.pdf&h=ATOoZvoecXZQokiY2ApCWeP4lMK1h-aZIF3"
                "rC6XU_dOtRdx4vBn9fBEcSJMA3i40D5P-QOrdve6qFCxX6rD1MhNwD7VkXnYpyhMRJD8RFnR6zc35vSjRjOBXh0G5ag5C"
                "K3zQd1WkxbY98LjG1nQo18bAc0I",
                "http://www.bbcactive.com/BBCActiveIdeasandResources/Tenwaystomakelecturesmoredynamic.aspx"]
    print('percent for speed:', str(percent))
    if percent[0] >= 25:
        extra_string = "A lot of students thinks the lecture is moving too slow, maybe you should check out this: " + \
                       url_slow[random.randrange(0, len(url_slow))]
    elif percent[2] >= 25:
        extra_string = "A lot of students thinks the lecture is moving too fast, maybe you should check out this: " + \
                       url_fast[random.randrange(0, len(url_fast))]
    else:
        extra_string = "Your students are happy and you are doing a good job, keep it up!"
    data = json.dumps({
        "recipient": {"id": recipient},
        "message": {"text": "Feedback for " + subject + ":\n" +
                            "Total number of participants: " + str(percent[3]) + "\n"
                            + str(percent[0]) + "% of participants thinks the lectures are too slow.\n"
                            + str(percent[1]) + "% of participants thinks the lectures are OK.\n"
                            + str(percent[2]) + "% of participants thinks the lectures are too fast.\n\n" +
                            extra_string
                    }
    })

    return data


def all_feedback_questions(recipient, subject, percent_questions):
    """
    Presents feedback from all lectures from LectureFeedbackEvaluation of a subject to the user.
    :param recipient: int
    :param subject: String
    :param percent_questions: list[int]
    :return: None
    """

    data = json.dumps({
        "recipient": {"id": recipient},
        "message": {"text": "Feedback for " + subject + ":\n"
                    + "Average score for the following categories.\n"
                    + str(percent_questions[0]) + " increased knowledge\n"
                    + str(percent_questions[1]) + " well organized\n"
                    + str(percent_questions[2]) + " use of slides\n"
                    + str(percent_questions[3]) + " use of time\n"
                    + str(percent_questions[4]) + " presenters knowledge\n"
                    + str(percent_questions[5]) + " general score\n"
                    + str(percent_questions[6]) + " interest in next lecture"
                    }
    })

    return data


def no_course(recipient):
    """
    Sends quick replies available to the user without a course selected
    :param recipient: int
    """
    data = json.dumps({
        "recipient": {"id": recipient},
        "message": {
            "text": "You have not chosen a subject \n What would you like to do?:",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Select Course",
                    "payload": "change subject"
                }
            ]
        }
    })
    return data


def has_course(recipient, subject):
    """
    Sends quick replies available to the user with a course selected
    :param recipient: int
    :param subject: String
    :return: None
    """
    subject_name = ime_data_fetch.get_subject_name(subject)
    data = json.dumps({
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
                    "title": "Give Feedback",
                    "payload": "give feedback"
                },
                {
                    "content_type": "text",
                    "title": "Get feedback",
                    "payload": "get feedback"
                }
            ]
        }
    })
    return data


def lec_feed(recipient):
    """
    Lets the user choose whether a lecture is too fast, slow or ok
    :param recipient: int
    :return: None
    """
    data = json.dumps({
        "recipient": {"id": recipient},
        "message": {
            "text": "How do you think this lecture is going:",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Too slow",
                    "payload": "0"
                },
                {
                    "content_type": "text",
                    "title": "It's all right",
                    "payload": "1"
                },
                {
                    "content_type": "text",
                    "title": "Too fast",
                    "payload": "2"
                }
            ]
        }
    })
    return data


def lecture_feedback_questions(recipient, payload):
    """
    Let the user give feedback from 1 to 5 on 6 different questions, given in order.
    :param recipient: int
    :param payload: String
    :return: None
    """
    text_list = ['How much did the lecture increase your knowledge?',
                 'How organized was the lecture?',
                 'How good was the use of slides?',
                 'How good was the use of time?',
                 'How knowledgeable did the lecturer seem?',
                 'How good did you think the lecture was overall?',
                 'How likely are you to go to the next lecture?'
                 ]
    payload_split = payload.split()
    text = text_list[len(payload_split) - 1]
    payload_string = ''
    for i in range(1, len(payload_split)):
        payload_string = payload_string + ' ' + payload_split[i]
    json_message = {
        "recipient": {"id": recipient},
        "message": {
            "text": text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "1",
                    "payload": "evaluation_questions" + payload_string + " 1"
                },
                {
                    "content_type": "text",
                    "title": "2",
                    "payload": "evaluation_questions" + payload_string + " 2"
                },
                {
                    "content_type": "text",
                    "title": "3",
                    "payload": "evaluation_questions" + payload_string + " 3"
                },
                {
                    "content_type": "text",
                    "title": "4",
                    "payload": "evaluation_questions" + payload_string + " 4"
                },
                {
                    "content_type": "text",
                    "title": "5",
                    "payload": "evaluation_questions" + payload_string + " 5"
                }
            ]
        }
    }
    data = json.dumps(json_message)
    return data


def give_feedback_choice(recipient):
    """
    Gives the user the choice to select what feedback to give.
    :param recipient: int
    """
    data = json.dumps({
        "recipient": {"id": recipient},
        "message": {
            "text": "What kind of feedback do want to give?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Lecture speed",
                    "payload": "lecture speed"
                },
                {
                    "content_type": "text",
                    "title": "Lecture questions",
                    "payload": "evaluation_questions"
                }
            ]
        }
    })
    return data


"""
THIS SECTION FOR GIVING FEEDBACK FOR LECTURES
"""


def get_feedback_specific_or_all(recipient):
    """
    Lets the user choose to get feedback for a specific lecture or all lectures.
    :param recipient: int
    """
    data = json.dumps({
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
    })
    return data


def get_feedback_year(recipient, years):
    """
    Lets the user choose to get feedback for a specific lecture or all lectures.
    :param recipient: int
    :param years: list[int]
    """

    # Makes initial json object.
    json_message = {
        "recipient": {"id": recipient},
        "message": {
            "text": "Select what year you want feedback from:",
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
    return data


def get_feedback_semester(recipient, year, semesters):
    """
    Lets the user choose to get feedback for a specific lecture or all lectures.
    :param recipient: int
    :param year: int
    :param semesters: list[String]
    """

    # Makes initial json object.
    json_message = {
        "recipient": {"id": recipient},
        "message": {
            "text": "Select what semester you want feedback from:",
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
    return data


def get_feedback_month(recipient, year, weeks_list):
    """
    Lets the user choose to get feedback for a specific lecture or all lectures.
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
    return data


def get_feedback_week(recipient, year, week_list):
    """
    Sends a message to recipient with buttons for selecting what week to feedback from.
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
    return data


def get_feedback_day(recipient, year, days, week):
    """
    :param recipient: int
    :param year: String
    :param days: List[int]
    :param week: String
    :return: None
    """

    # Makes initial json object.
    json_message = {
        "recipient": {"id": recipient},
        "message": {
            "text": "Select what day you want feedback from:",
            "quick_replies": [
            ]
        }
    }

    # Adds buttons to the json object depending on how many semesters in arg.
    for day in days:
        add_days_to_json(day, json_message, year, week)

    # Sends message.
    data = json.dumps(json_message)
    return data


def present_single_lecture_feedback(recipient, feedback_list):
    """
    feedback for one lecture
    :param recipient int
    :param feedback_list list[lecture_id, [feedbacks]]
    """

    slow = feedback_list[1].count(0)
    normal = feedback_list[1].count(1)
    fast = feedback_list[1].count(2)
    total = slow + normal + fast
    slow = round(slow / total * 100)
    normal = round(normal / total * 100)
    fast = round(fast / total * 100)

    data = json.dumps({
        "recipient": {"id": recipient},
        "message": {"text": 'A total of ' + str(total) + ' students have given their response.\n'
                    + str(slow) + '% of students thought the lecture was too slow.\n'
                    + str(normal) + '% of students thought the lecture was OK.\n'
                    + str(fast) + '% of students thought the lecture was too fast.'
                    }
    })

    return data


def present_single_lecture_feedback_questions(recipient, feedback_questions):
    """
    feedback for one lecture
    :param recipient: int
    :param feedback_questions: list[]
    """

    data = json.dumps({
        "recipient": {"id": recipient},
        "message": {"text": "Average score for the following categories.\n"
                    + " Increased knowledge: " + str(feedback_questions[0]) + "\n"
                    + " Organization: " + str(feedback_questions[1]) + "\n"
                    + " Use of slides: " + str(feedback_questions[2]) + "\n"
                    + " Use of time: " + str(feedback_questions[3]) + "\n"
                    + " Presenters knowledge: " + str(feedback_questions[4]) + "\n"
                    + " General score: " + str(feedback_questions[5]) + "\n"
                    + " Interest in the next lecture: " + str(feedback_questions[6])
                    }
    })
    return data


"""
HELPING METHODS FOR CREATING JSON OBJECT
"""


def add_weeks_to_json(weeks, weeks_string, json_message, year):
    """
    Adds buttons for several weeks to the json message
    :param weeks: list[int]
    :param weeks_string: String
    :param json_message: json
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


def add_days_to_json(day, json_message, year, week):
    """
    Adds buttons with the name of a day on it.
    :param day: int
    :param json_message: json
    :param year: String
    :param week: String
    """
    lecture_day = ''
    if day == 1:
        lecture_day = 'Monday'
    elif day == 2:
        lecture_day = 'Tuesday'
    elif day == 3:
        lecture_day = 'Wednesday'
    elif day == 4:
        lecture_day = 'Thursday'
    elif day == 5:
        lecture_day = 'Friday'
    elif day == 6:
        lecture_day = 'Saturday'
    elif day == 7:
        lecture_day = 'Sunday'
    else:
        print("Could not find the lecture day")

    json_message["message"]["quick_replies"].append({
        "content_type": "text",
        "title": lecture_day,
        "payload": "get_lecture_feedback_day " + str(year) + ' ' + str(week) + ' ' + str(day)
    })
