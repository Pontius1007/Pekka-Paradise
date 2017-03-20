from app import db, models


def get_year(course):
    """
    :param course:
    :return A list in descending order containing the years of the lectures:
    """
    try:
        if models.Lecture.query.filter_by(subject=course) is not None:
            lecture_year = []
            lectures = models.Lecture.query.filter_by(subject=course)
            for lecture in lectures:
                if lecture.year not in lecture_year:
                    lecture_year.append(lecture.year)
            lecture_year.sort(reverse=True)
            return lecture_year
    except Exception as e:
        print(e)


def check_lecture_semester(course, start, end, year):
    """
    :param course:
    :param start:
    :param end:
    :param year:
    :return True or false depending on is the course has lectures in the given weeks:
    """
    try:
        if models.Lecture.query.filter_by(subject=course) is not None:
            lecture_week = []
            lectures = models.Lecture.query.filter_by(subject=course, year=year)
            for lecture in lectures:
                if lecture.week_number not in lecture_week:
                    lecture_week.append(lecture.week_number)
            for i in range(start, end):
                if i in lecture_week:
                    return True
    except Exception as e:
        print(e)
    return False


def get_lecture_weeks(subject, year, semester):
    try:
        week_list = []
        lectures = models.Lecture.query.filter_by(subject=subject, year=year)
        if semester is 'Spring':
            start = 1
            end = 18
        else:
            start = 32
            end = 49
        for lecture in lectures:
            if lecture.week_number not in week_list and start <= lecture.week_number <= end:
                week_list.append(lecture.week_number)
        return week_list.sort()
    except Exception as e:
        print(e)


def day_of_lecture_in_week(course, week, year):
    """
    :param course:
    :param week:
    :param year:
    :return A list containing the week-days of a given lecture in a given week:
    """
    try:
        if models.Lecture.query.filter_by(subject=course) is not None:
            lecture_days = []
            lectures = models.Lecture.query.filter_by(subject=course, year=year, week_number=week)
            for lecture in lectures:
                if lecture.day_number not in lecture_days:
                    lecture_days.append(lecture.day_number)
            return lecture_days
    except Exception as e:
        print(e)