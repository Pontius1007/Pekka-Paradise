
import requests


base_url = "http://www.ime.ntnu.no/api/course/en/"


# method for checking if a subject exists at NTNU
def get_subject_name(code):

    try:
        course = requests.get(base_url + code).json()
        code = course['course']['code']
        name = course['course']['name']
    except TypeError:
        return 'Subject does not exist'
    except ValueError:
        return 'Not valid'
    return ''.join(code + ': ' + name)


# same as above but returns a boolean value instead
def subject_exists_boolean(code):

    try:
        if requests.get(base_url + code).json()["course"] is not None:
            return True
    except TypeError:
        return False
    except ValueError:
        return False
    return False

