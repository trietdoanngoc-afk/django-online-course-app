from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Thêm 2 path quy định đường dẫn cho submit và show_exam_result theo đúng yêu cầu đề bài
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    path('course/<int:course_id>/submission/<int:submission_id>/show_exam_result/', views.show_exam_result, name='show_exam_result'),
]
