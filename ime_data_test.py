
import requests


base_url = "http://www.ime.ntnu.no/api/course/en/"
# method for checking if a subject exists at NTNU


def subject_exists(code):

    try:
        course = requests.get(base_url + code).json()
        code = course['course']['code']
        name = course['course']['name']
    except TypeError:
        return 'Subject does not exist'
    except ValueError:
        return 'Not valid'
    return ''.join(code + ': ' + name)
