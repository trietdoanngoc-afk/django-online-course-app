from django.contrib import admin
from .models import Course, Lesson, Instructor, Enrollment, Question, Choice, Submission

# 1. Cấu hình hiển thị Choice lồng trong Question (ChoiceInline)
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4  # Hiển thị sẵn 4 ô nhập đáp án mặc định

# 2. Cấu hình hiển thị Question lồng trong Course/Lesson (QuestionInline)
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

# 3. Cấu hình giao diện tùy biến cho Câu hỏi (QuestionAdmin)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]  # Nhúng Choice vào giao diện Question
    list_display = ['question_text', 'grade', 'course']
    list_filter = ['course']
    search_fields = ['question_text']

# 4. Cấu hình giao diện tùy biến cho Bài học (LessonAdmin)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'course']

# Tùy biến giao diện Khóa học có sẵn để hiển thị lồng cả Câu hỏi
class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

# Đăng ký các class với hệ thống Django Admin
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
