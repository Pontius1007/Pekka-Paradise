

def generate_percent(feedback):
    """
    Returns feedback numbers
    :param feedback:
    :return: total number of persons, subject
    """
    subject = len(feedback[0])
    tot = 0
    counter = [0.0, 0.0, 0.0]  # First index shows percentage of slow, second ok, third too fast, fourth total number
    for i in range(0, len(feedback)):
        if i == 0:
            subject = feedback[i]
        else:
            if feedback[i] == 0:
                counter[0] += 1
                tot += 1
            elif feedback[i] == 1:
                counter[1] += 1
                tot += 1
            elif feedback[i] == 2:
                counter[2] += 1
                tot += 1
    counter.append(tot)
    counter[0] /= counter[3] * 100
    counter[1] /= counter[3] * 100
    counter[2] /= counter[3] * 100

    return subject, counter
