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


def test_graph(token, recipient):
    """
    Sends the feedback as a graph(?) to the user in this case lecturer
    :param token:
    :param recipient:
    :param image:
    :return:
    """
    img = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                        data=json.dumps({
                            "recipient": {"id": recipient},
                            "message": {
                                "attachment": {
                                  "type": "image",
                                  "payload": {
                                      "url": "lordi_lead.jpg"
                                  }
                                }
                              }
                        }), headers={'Content-type': 'application/json'})
    if img.status_code != requests.codes.ok:
        print(img.text)


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
