import json
import requests


def text_message(token, recipient):
    txt = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token},
                        data=json.dumps({
                            "recipient": {"id": recipient},
                            "message": {"text": "This is a response"}
                        }), headers={'Content-type': 'application/json'})
    if txt.status_code != requests.codes.ok:
        print(txt.text)


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
                            "text": "Pick a color:",
                            "quick_replies": [
                                {
                                "content_type": "text",
                                "title": "Red",
                                "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                                },
                                {
                                "content_type": "text",
                                "title": "Green",
                                "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
                                },
                                {
                                "content_type": "text",
                                "title": "Green",
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
    test_message = requests.post("https://graph.facebook.com/v2.6/me/messages", params={"access_token": token}, data=json.dumps({
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