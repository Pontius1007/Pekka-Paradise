# -*- coding utf-8 -*-

import subject_info


def message_splitter(in_message):
    if len(in_message) <= 640:
        return [in_message]
    else:
        for i in range(int(len(in_message)/2)-2, len(in_message)-1):
            if in_message[i] == "\n":
                left = in_message[:i]
                right = in_message[i+1:]
                message_list = [left, right]
                return message_list
        return [in_message]


def message_split(message):
    message_list = [message]
    index = 0
    too_long = True
    while too_long:
        too_long = False
        msg = message_list.pop(index)
        message_list.extend(message_splitter(msg))
        for msg in message_list:
            if len(msg) > 640:
                too_long = True
                index = message_list.index(msg)
                break
    return message_list


"""
schedule = subject_info.printable_schedule(subject_info.get_schedule("tma4115"))
if len(schedule) > 640:
    print(len(schedule))
    sch_list = message_split(schedule)
    for msg in sch_list:
        print(msg)
else:
    print(len(schedule))
    print(schedule)
"""
