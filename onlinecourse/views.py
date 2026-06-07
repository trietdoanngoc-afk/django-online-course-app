from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

# Hàm hiển thị kết quả bài kiểm tra
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    earned_score = 0
    
    # Tính tổng số điểm của tất cả câu hỏi và số điểm đạt được
    for question in course.question_set.all():
        total_score += question.grade
        # Lấy danh sách ID các lựa chọn người dùng đã chọn cho câu hỏi này
        selected_ids = [choice.id for choice in submission.choices.filter(question=question)]
        if question.is_get_score(selected_ids):
            earned_score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'total_score': total_score,
        'earned_score': earned_score,
    }
    return render(request, 'onlinecourse/exam_result.html', context)

# Hàm xử lý khi người dùng ấn nút nộp bài (Submit)
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Tạo mới một lượt nộp bài gắn với user hiện tại
        submission = Submission.objects.create(user=request.user)
        
        # Duyệt qua các câu hỏi để lấy đáp án người dùng chọn từ form HTML
        for question in course.question_set.all():
            input_name = f"choice_{question.id}"
            selected_choice_ids = request.POST.getlist(input_name)
            
            for choice_id in selected_choice_ids:
                choice = get_object_or_404(Choice, pk=choice_id)
                submission.choices.add(choice)
        
        submission.save()
        # Sau khi lưu xong, chuyển hướng người dùng sang trang hiển thị kết quả vừa làm
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    
    return HttpResponseRedirect(reverse('onlinecourse:popular_course_list'))
