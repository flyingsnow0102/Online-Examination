from django.contrib import admin
from exam.models import *

admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(SubjectMark)
admin.site.register(StudentMark)