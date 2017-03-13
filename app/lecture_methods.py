# -*- coding utf-8 -*-

import sub_info
#from app import models, db

test = ([['TDT4100', '14:15', '16:00', 2, ['2-14', '17'], '2017_VÅR', 'F1'], ['TDT4100', '12:15', '14:00', 5, ['10'], '2017_VÅR', 'F1']])


def extract_lecture_information(lecture_information):


    for i in range(0, len(lecture_information)):
        week_number = ''.join((lecture_information[i][4][0]))
        print(week_number)
        if len(week_number) > 2:
            start_week = int((week_number.split('-', 2)[0]))
            end_week = int((week_number.split('-', 2)[1]))
            year = lecture_information[i][5][:4]
            for x in range(start_week, end_week+1):
                print(x)
                #new_lecture = models.Lecture()

        else:
            print ("Lengden av test1 er: " + str(len(week_number)))


extract_lecture_information(test)




