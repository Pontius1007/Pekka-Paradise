from app import db, models

def get_year(course):
    try:
        if models.Lecture.query.filter_by(subject=course):
            
