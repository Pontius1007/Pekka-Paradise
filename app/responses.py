import json
import requests


def greeting_message(token, recipient):
    message = "Hello !\n What can I do for you today?"
    txt = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                        data=json.dumps({
                            "recipient": {"id": recipient},
                            "message": {"text": message}
                        }), headers={'Content-type': 'application/json'})
    if txt.status_code != requests.codes.ok:
        print(txt.text)


def text_message(token, recipient, message):
    txt = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                        data=json.dumps({
                            "recipient": {"id": recipient},
                            "message": {"text": message}
                        }), headers={'Content-type': 'application/json'})
    if txt.status_code != requests.codes.ok:
        print(txt.text)

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
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
      data=json.dumps({
          "recipient": {"id": recipient},
          "message": {
              "text": "You have not chosen a subject \n What would you like to do?:",
              "quick_replies": [
                  {
                      "content_type": "text",
                      "title": "Select Course",
                      "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_Course"
                  },
                  {
                      "content_type": "text",
                      "title": "Something else?",
                      "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_SOMETHING_ELSE"
                  }
              ]
          }
        }),
        headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)


def has_course(token, recipient, subject):
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
      data=json.dumps({
          "recipient": {"id": recipient},
          "message": {
              "text": "You have chosen: " + subject + "\n What would you like to do?:",
              "quick_replies": [
                  {
                      "content_type": "text",
                      "title": "Get info",
                      "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_Course"
                  },
                  {
                      "content_type": "text",
                      "title": "Get schedule",
                      "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_SOMETHING_ELSE"
                  },
                  {
                      "content_type": "text",
                      "title": "Change subject",
                      "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_Course"
                  },
                  {
                      "content_type": "text",
                      "title": "Lecture Feedback",
                      "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_SOMETHING_ELSE"
                  }
              ]
          }
        }),
        headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)


def course_info(token, recipient, message):
    """Send the message text to recipient with id recipient.
    """

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": recipient},
                          "message": {"text": message}
                      }),
                      headers={'Content-type': 'application/json'})

    if r.status_code != requests.codes.ok:
        print(r.text)


def lec_feed(token, recipient):
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
      data=json.dumps({
          "recipient": {"id": recipient},
          "message": {
              "text": "How do you think this lecture is going:",
              "quick_replies": [
                  {
                      "content_type": "text",
                      "title": "Too fast!!",
                      "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_FAST"
                  },
                  {
                      "content_type": "text",
                      "title": "It's All Right",
                      "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_OK"
                  },
                  {
                      "content_type": "text",
                      "title": "Too slow",
                      "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_SLOW"
                  }
              ]
          }
        }),
        headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)