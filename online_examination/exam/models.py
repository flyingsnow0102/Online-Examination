
from django.db import models

from college.models import Course, Semester
from academic.models import Student 

class Subject(models.Model):
	
	subject_name = models.CharField('Subject Name', null=True, blank=True, max_length=200)
	duration = models.CharField('Duration', null=True, blank=True, max_length=200)
	duration_parameter = models.CharField('Duration Parameter', null=True, blank=True, max_length=200)
	total_mark = models.CharField('Total Mark', null=True, blank=True, max_length=200)
	pass_mark = models.CharField('Pass Mark', null=True, blank=True, max_length=200)
	
	def __unicode__(self):
		return str(self.subject_name)

	class Meta:
		verbose_name = 'Subject'
		verbose_name_plural = 'Subject'

class Exam(models.Model):
	
	exam_name = models.CharField('Exam Name', null=True, blank=True, max_length=200)
	course = models.ForeignKey(Course, null=True, blank=True)
	semester = models.ForeignKey(Semester, null=True, blank=True)
	start_date = models.DateField('Start Date', null=True, blank=True)
	end_date = models.DateField('End Date', null=True, blank=True)
	no_subjects= models.IntegerField('Number of Subjects', default=0)
	exam_total= models.IntegerField('Exam Total', default=0)
	subjects = models.ManyToManyField(Subject, null=True, blank=True)

	def __unicode__(self):
		return str(self.exam_name)

	class Meta:
		verbose_name = 'Exam'
		verbose_name_plural = 'Exam'

class SubjectMark(models.Model):

	subject_name = models.ForeignKey(Subject, null=True, blank=True)
	mark = models.CharField('Mark ', null=True, blank=True, max_length=200)
	status = models.CharField('Status ', null=True, blank=True, max_length=200)

	def __unicode__(self):
		return str(self.subject_name)

	class Meta:
		verbose_name = 'SubjectMark'
		verbose_name_plural = 'SubjectMark'


class StudentMark(models.Model):
	student = models.ForeignKey(Student, null=True, blank=True)
	course = models.ForeignKey(Course, null=True, blank=True)
	semester = models.ForeignKey(Semester, null=True, blank=True)
	exam = models.ForeignKey(Exam, null=True, blank=True)
	total_mark = models.DecimalField('Total Mark Obtained',max_digits=14, decimal_places=2, default=0)
	subject_mark = models.ManyToManyField(SubjectMark, null=True, blank=True)
	status = models.CharField('Status ', null=True, blank=True, max_length=200)

	def __unicode__(self):
		return str(self.student.student_name) if self.student else 'Student'

	class Meta:
		verbose_name = 'StudentMark'
		verbose_name_plural = 'StudentMark'
