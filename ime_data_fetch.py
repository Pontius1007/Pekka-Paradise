
import requests


base_url = "http://www.ime.ntnu.no/api/course/en/"


def get_subject_name(code):
    """
    method for checking if a subject exists at NTNU
    :param code: a string subject code such as TDT4145
    :return: subject name and code if it exists
    """

    try:
        course = requests.get(base_url + code).json()
        code = course['course']['code']
        name = course['course']['name']
    except TypeError:
        return 'Subject does not exist'
    return ''.join(code + ': ' + name)


def subject_exists_boolean(code):
    """
    Same as above but returns a boolean value instead
    :param code: a string subject code such as TDT4145
    :return: Boolean
    """
    try:
        if requests.get(base_url + code).json()["course"] is not None:
            return True
    except TypeError:
        return False
    return False
