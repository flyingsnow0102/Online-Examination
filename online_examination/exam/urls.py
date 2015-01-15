
from django.conf.urls import patterns, url

from exam.views import (ScheduleExam, ViewExamSchedule, EditExamSchedule, \
	SaveExamSchedule, DeleteExamSchedule, Marks, GetExams, SaveMarks, CreateExam)

urlpatterns = patterns('',	
	url(r'^schedule_exam/$', ScheduleExam.as_view(), name='schedule_exam'),
	url(r'^view_exam_schedule/(?P<exam_schedule_id>\d+)/$', ViewExamSchedule.as_view(), name="view_exam_schedule"),
	url(r'^edit_exam_schedule/(?P<exam_schedule_id>\d+)/$', EditExamSchedule.as_view(), name="edit_exam_schedule"),
	url(r'^save_new_exam_schedule/$', SaveExamSchedule.as_view(), name='save_new_exam_schedule'),
	url(r'^delete_exam_schedule/(?P<exam_schedule_id>\d+)/$', DeleteExamSchedule.as_view(), name="delete_exam_schedule"),
	url(r'^marks/$', Marks.as_view(), name='marks'),
	url(r'^get_exam/(?P<course_id>\d+)/(?P<batch_id>\d+)/(?P<semester_id>\d+)/$', GetExams.as_view(), name="get_exam"),
	url(r'^save_marks/$', SaveMarks.as_view(), name='save_marks'),
	url(r'^create_exam/$', CreateExam.as_view(), name='create_exam')
)