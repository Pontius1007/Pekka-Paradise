# -*- coding utf-8 -*-

import requests
import ime_data_fetch
from datetime import date

# a list of weekdays to use in printing course schedules
week = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag"]
# Gets the current year
current_year = str(date.today().year)

# method that return a courses schedule in JSON format if the subject exists
def get_schedule(sub_code):
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


# method that prints a courses schedule to the console from a JSON schedule file
def print_schedule(schedule):
    if not schedule:
        print("No schedule available")

    print("Timeplan for " + schedule['course']['summarized'][0]['courseName'] + ":")
    for i in range(0, len(schedule['course']['summarized'])):
        print(schedule['course']['summarized'][i]['description'] + " "
              + week[schedule['course']['summarized'][i]['dayNum'] - 1] +
              " fra " + schedule['course']['summarized'][i]['from'] +
              " til " + schedule['course']['summarized'][i]['to'])


# pretty much the same as print_schedule except that it returns a formatted string instead of printing it
def printable_schedule(schedule):
    if not schedule:
        return "No schedule available"

    schedule_string = "Timeplan for " + schedule['course']['summarized'][0]['courseName'] + ":\n"
    for i in range(0, len(schedule['course']['summarized'])):
        schedule_string += (schedule['course']['summarized'][i]['description'] + " "
                            + week[schedule['course']['summarized'][i]['dayNum'] - 1] +
                            " fra " + schedule['course']['summarized'][i]['from'] +
                            " til " + schedule['course']['summarized'][i]['to'] + "\n")
    return schedule_string


# Method for gathering raw data so we can add the lecture to the database

def gather_lecture_information(schedule):
    lecture_information = []

    if not schedule:
        return "No schedule available"

    for i in range(0, len(schedule['course']['summarized'])):
        if schedule['course']['summarized'][i]['acronym'] == 'FOR':
            single_lecture = []
            single_lecture.extend(
                (schedule['course']['summarized'][i]['courseCode'], schedule['course']['summarized'][i]['from'],
                 schedule['course']['summarized'][i]['to'], schedule['course']['summarized'][i]['dayNum'],
                 schedule['course']['summarized'][i]['weeks'],
                 schedule['course']['summarized'][i]['rooms'][0]['romNavn']))
            lecture_information.append(single_lecture)

    return lecture_information


# method that fetches the information about a subject from IMEs api in a json file
def get_course_json(sub_code):
    try:
        course = requests.get("http://www.ime.ntnu.no/api/course/" + sub_code).json()
    except TypeError:
        return 'Subject does not exist'
    except ValueError:
        return 'Not valid'
    return course


# method that returns information about a subject as a printable formatted string.
# TODO fullføre metode, hente mer info fra API
def printable_course_info(course):
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
