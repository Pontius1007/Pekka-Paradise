import json
import requests


def greeting_message(token, recipient, user_name):
    message = "Hello" + user_name[0] + "!\n What can I do for you today?"
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

# To be used later
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
                      "payload": "Change subject"
                  }
              ]
          }
        }),
        headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)


# If needed it is possible to send subject back to the user in the payload without saving in db
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
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
      data=json.dumps({
          "recipient": {"id": recipient},
          "message": {
              "text": "How do you think this lecture is going:",
              "quick_replies": [
                  {
                      "content_type": "text",
                      "title": "Too fast!!",
                      "payload": "fast"
                  },
                  {
                      "content_type": "text",
                      "title": "It's All Right",
                      "payload": "ok"
                  },
                  {
                      "content_type": "text",
                      "title": "Too slow",
                      "payload": "slow"
                  }
              ]
          }
        }),
        headers={'Content-type': 'application/json'})
    if supp.status_code != requests.codes.ok:
        print(supp.text)
