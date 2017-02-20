
import requests

base_url = "http://www.ime.ntnu.no/api/course/en/"
searchcode = "-"

allCourses = requests.get(base_url + searchcode).json()

# print(allCourses["course"][0]["code"])

# method for checking if a subject exists at NTNU


def subject_exists(code, courses):
    exists = False

    for i in range(0, len(courses["course"])):
        if courses["course"][i]["code"] == code:
            exists = True
            print(i)
            break

    return exists

print(subject_exists("AM304016", allCourses))
