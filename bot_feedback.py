

def generate_percent(feedback):
    """
    Returns feedback numbers
    :param feedback:
    :return: total number of persons, subject
    """
    subject = len(feedback[0])
    print(feedback)
    slow = feedback.count(0)
    ok = feedback.count(1)
    fast = feedback.count(2)
    total = float(slow + ok + fast)
    print(total, slow, ok, fast)
    counter = [round((slow/total)*100), round((ok/total)*100), round((fast/total)*100), round(total)]
    return subject, counter
