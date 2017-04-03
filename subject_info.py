# -*- coding utf-8 -*-

from datetime import date

import requests

import ime_data_fetch

# a list of weekdays to use in printing course schedules
week = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag"]
# Gets the current year
current_year = str(date.today().year)


# method that return a courses schedule in JSON format if the subject exists
# the order of the elements in the returned schedule can change from call to call with the same sub_code
def get_schedule(sub_code):
    """
    method that return a courses schedule in JSON format if the subject exists
    :param sub_code: a string subject code such as TDT4145
    :return: a schedule JSON
    """
    if ime_data_fetch.subject_exists_boolean(sub_code):
        schedule = requests.get("http://www.ntnu.no/web/studier/emner?p_p_id=coursedetailsportlet_WAR_"
                                "courselistportlet&p_p_lifecycle=2&p_p_resource_id=timetable&_coursedetailsportlet_WAR_"
                                "courselistportlet_year=" + current_year + "&_c"
                                "oursedetailsportlet_WAR_courselistportlet_courseCode="
                                + sub_code.upper() + "&year=" + current_year + "&version=1").json()
        try:
            trigger_key_error = schedule['course']['summarized']
            return schedule
        except KeyError:
            return False
    else:
        return False


def printable_schedule(schedule):
    """
    pretty much the same as print_schedule except that it returns a formatted string instead of printing it
    :param schedule: a schedule JSON file
    :return: a string with the schedule
    """
    if not schedule:
        return "No schedule available"

    schedule = schedule['course']['summarized']
    schedule_string = "Timeplan for " + schedule[0]['courseName'] + ":\n"
    for i in range(0, len(schedule)):
        schedule_string += (schedule[i]['description'] + " "
                            + week[schedule[i]['dayNum'] - 1] +
                            " fra " + schedule[i]['from'] +
                            " til " + schedule[i]['to'] + "\n")
    return schedule_string


def gather_lecture_information(schedule):
    """
    Method for gathering raw data so we can add the lecture to the database
    :param schedule: a schedule JSON
    :return: Return lecture information from IMEs API.
    """
    lecture_information = []

    if not schedule:
        return "No schedule available"

    for i in range(0, len(schedule['course']['summarized'])):
        if schedule['course']['summarized'][i]['acronym'] == 'FOR' \
                or schedule['course']['summarized'][i]['acronym'] == 'F/Ø':
            print(i)
            single_lecture = []
            single_lecture.extend(
                (schedule['course']['summarized'][i]['courseCode'], schedule['course']['summarized'][i]['from'],
                 schedule['course']['summarized'][i]['to'], schedule['course']['summarized'][i]['dayNum'],
                 schedule['course']['summarized'][i]['weeks'], schedule['course']['summarized'][i]['arsterminId']))
            try:
                single_lecture.extend(schedule['course']['summarized'][i]['rooms'][0]['romNavn'])
            except IndexError:
                single_lecture.extend("")
            lecture_information.append(single_lecture)
    return lecture_information


def get_course_json(sub_code):
    """
    method that fetches the information about a subject from IMEs api in a json file
    :param sub_code: a string subject code such as TDT4145
    :return: course info JSON file
    """
    try:
        course = requests.get("http://www.ime.ntnu.no/api/course/" + sub_code).json()
        if course['course'] is None:
            return 'Subject does not exist'
    except TypeError:
        return 'Subject does not exist'
    return course


def printable_course_info(course):
    """
    method that returns information about a subject as a printable formatted string.
    :param course: A course JSON from the ime API
    :return: a string with course info
    """
    if course == 'Subject does not exist' or course == 'Not valid':
        return 'subject does not exist and thus has no information'

    course = course['course']
    if course['assessment'][0]['codeName'] == 'Skriftlig eksamen':
        info_string = ("%s %s\nStudiepoeng: %s\nStudienivå: %s\nVurderingsordning: %s\nKarakter: %s\nEksamensdato: %s" %
                       (course['code'], course['name'],
                        course['credit'], course['studyLevelName'],
                        course['assessment'][0]['codeName'], course['assessment'][0]['gradeRuleSchemeName'],
                        course['assessment'][0]['date']))
    else:
        info_string = ("%s %s\nStudiepoeng: %s\nStudienivå: %s\nVurderingsordning: %s\nKarakter: %s" %
                       (course['code'], course['name'],
                        course['credit'], course['studyLevelName'],
                        course['assessment'][0]['codeName'], course['assessment'][0]['gradeRuleSchemeName']))
    return info_string

  
def course_name(code):
    """
    A method that fetches the name of a course
    :param code: a string subject code such as TDT4145
    :return: a course name string
    """

    c = get_course_json(code)
    if c == 'Subject does not exist' or c == 'Not valid':
        return c
    return c['course']['name']

