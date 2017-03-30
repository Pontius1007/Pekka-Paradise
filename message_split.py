# -*- coding utf-8 -*-


def __message_splitter(in_message):
    """
    a method only used in message_split to split strings
    formatted by the methods in subject_info such as get_schedule
    :param in_message: a formatted string containing several newlines
    :return: a list with the input string split
    on the first newline after the middle of the string
    """
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
    """
    a method that splits messages that are too long for facebook messenger into parts that are short enough to send
    :param message: the formatted message string for facebook, such as those returned from get_schedule
    :return: a list of shorter pieces of the input string that can be sent to messenger
    """
    message_list = [message]
    index = 0
    too_long = True
    while too_long:
        too_long = False
        msg = message_list.pop(index)
        message_list.extend(__message_splitter(msg))
        for msg in message_list:
            if len(msg) > 640:
                too_long = True
                index = message_list.index(msg)
                break
    return message_list


"""
import subject_info
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



