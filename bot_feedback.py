

def generate_percent_for_speed(feedback):
    """
    Returns feedback numbers
    :param feedback:
    :return: percentage for speed of the lecture
    """
    slow = feedback.count(0)
    ok = feedback.count(1)
    fast = feedback.count(2)
    total = float(slow + ok + fast)
    counter = [round((slow/total)*100), round((ok/total)*100), round((fast/total)*100), round(total)]

    return counter


def generate_percent_for_questions(feedbackevaluation):
    """
    Calculates percentages for feedback numbers
    :param feedbackevaluation: 
    :return: , percentage for questions
    """
    increased_knowledge = 0
    well_organized = 0
    logical = 0
    use_of_slides = 0
    use_of_time = 0
    presenter_knowledgeable = 0
    general_score = 0
    feedbackeval_total = len(feedbackevaluation)
    for feedbackeval in feedbackevaluation:
        increased_knowledge += feedbackeval[0]
        well_organized += feedbackeval[1]
        logical += feedbackeval[2]
        use_of_slides += feedbackeval[3]
        use_of_time += feedbackeval[4]
        presenter_knowledgeable += feedbackeval[5]
        general_score += feedbackeval[6]
    feedbackevaluation_counter = [round(increased_knowledge / feedbackeval_total),
                                  round(well_organized / feedbackeval_total), round(logical / feedbackeval_total),
                                  round(use_of_slides / feedbackeval_total), round(use_of_time / feedbackeval_total),
                                  round(presenter_knowledgeable / feedbackeval_total),
                                  round(general_score / feedbackeval_total)]

    return feedbackevaluation_counter
