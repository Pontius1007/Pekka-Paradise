from app import db, models

def get_year(course):
    try:
        if models.Lecture.query.filter_by(subject=course):
            
feedbacks = []
lectures = models.Lecture.query.filter_by(subject='TDT4112', year=2017, week_number=11, day_number=2)
for lecture in lectures:
    feedbacks.append(models.LectureFeedback.query.filter_by(lecture_id=lecture.id, user_id='Håvard Hellem'))
for feedback in feedbacks:
    for feed in feedback:
        print(feed)

