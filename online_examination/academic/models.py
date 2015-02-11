
from django.db import models
from django.contrib.auth.models import User
from college.models import Course, Semester


class Student(models.Model):

	student_name = models.CharField('Student Name', null=True, blank=True, max_length=200)
	user = models.ForeignKey(User, null=True, blank=True)
	is_curently_logged_in = models.BooleanField('Currently Logged In',default=False)
	student_password = models.CharField('Student Password', null=True, blank=True, max_length=200)
	registration_no = models.CharField('Roll Number', null=True, blank=True, max_length=200 )
	hall_ticket_no = models.CharField('Roll Number', null=True, blank=True, max_length=200 )
	address = models.CharField('Student Address', null=True, blank=True, max_length=200 )
	course = models.ForeignKey(Course, null=True, blank=True)
	semester = models.ForeignKey(Semester, null=True, blank=True)
	dob = models.DateField('Date of Birth',null=True, blank=True)
	age = models.CharField('Age',null=True, blank=True, max_length=200 )
	permanent_address= models.CharField('Permanent Address',null=True, blank=True, max_length=200)
	mobile_number= models.CharField('Mobile Number',null=True, blank=True, max_length=200)
	email = models.CharField('Email',null=True, blank=True, max_length=200)
	photo = models.ImageField(upload_to = "uploads/photos/", null=True, blank=True)
	guardian_mobile_number= models.CharField('Guardian Mobile Number',null=True, blank=True, max_length=200)
	

	def __unicode__(self):
		return str(self.student_name)
		
	class Meta:
		verbose_name = 'Student'
		verbose_name_plural = 'Student'

