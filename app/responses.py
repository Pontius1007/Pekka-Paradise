import json
import requests


def greeting_message(token, recipient):
    message = "Hello! \n What can I do for you today?"
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


def supp_message(token, recipient):
    supp = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                                  data=json.dumps({
                                      "recipient": {"id": recipient},
                                      "message": {
                                          "text": "Pick a color:",
                                          "quick_replies": [
                                              {
                                                  "content_type": "text",
                                                  "title": "Yes",
                                                  "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                                              },
                                              {
                                                  "content_type": "text",
                                                  "title": "Quit Course",
                                                  "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
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


def quick_reply(token, recipient):
    quick_message = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                                  data=json.dumps({
                                      "recipient": {"id": recipient},
                                      "message": {
                                          "text": "What do you need?",
                                          "quick_replies": [
                                              {
                                                  "content_type": "text",
                                                  "title": "Schedule",
                                                  "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                                              },
                                              {
                                                  "content_type": "text",
                                                  "title": "Info",
                                                  "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
                                              },
                                              {
                                                  "content_type": "text",
                                                  "title": "Secret",
                                                  "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
                                              }
                                          ]
                                      }
                                  }),
                                  headers={'Content-type': 'application/json'})
    if quick_message.status_code != requests.codes.ok:
        print(quick_message.text)


def send_button_test(token, recipient):
    # I wonder if each separate message to be sent must be in its own method
    # As of now the bot seems to send all JSON objects in this method
    test_message = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                                 data=json.dumps({
                                     "recipient": {"id": recipient},
                                     "message": {
                                         "attachment": {
                                             "type": "template",
                                             "payload": {
                                                 "template_type": "button",
                                                 "text": "What can I do for you today?",
                                                 "buttons": [
                                                     {
                                                         "type": "web_url",
                                                         "url": "https://google.com",
                                                         "title": "Show Google"
                                                     },
                                                     {
                                                         "type": "postback",
                                                         "title": "Press this button",
                                                         "payload": "Herro? \n Herro? \n"
                                                     },
                                                 ]
                                             }
                                         }
                                     }
                                 }), headers={'Content-type': 'application/json'})

    if test_message.status_code != requests.codes.ok:
        print(test_message.text)
