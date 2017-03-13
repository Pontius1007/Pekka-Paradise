# -*- coding utf-8 -*-

from app import db, models

test = ([['TDT4100', '14:15', '16:00', 2, ['2-14', '17'], '2017_VÅR', 'F1'], ['TDT4100', '12:15', '14:00', 5, ['10'], '2017_VÅR', 'F1']])


def extract_lecture_information(lecture_information):


    for i in range(0, len(lecture_information)):
        week_number = ''.join((lecture_information[i][4][0]))
        if len(week_number) > 2:
            start_week = int((week_number.split('-', 2)[0]))
            end_week = int((week_number.split('-', 2)[1]))
            year = lecture_information[i][5][:4]
            for x in range(start_week, end_week+1):
                new_lecture = models.Lecture(lecture_information[i][0], year, x, lecture_information[i][3], lecture_information[i][1],
                lecture_information[i][2], lecture_information[i][6])
                db.session.add(new_lecture)
        else:
            year = lecture_information[i][5][:4]
            new_lecture_under_2 = models.Lecture(lecture_information[i][0], year, week_number, lecture_information[i][3],
                                         lecture_information[i][1],
                                         lecture_information[i][2], lecture_information[i][6])
            db.session.add(new_lecture_under_2)
    db.session.commit()
    print("Lectures added successfully")

extract_lecture_information(test)

