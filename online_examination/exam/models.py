
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

    def get_json_data(self):
        subjects_data = []
        for subject in self.subjects.all():
            subjects_data.append({
                'subject_id': subject.id if subject.id else '',
                'subject': subject.subject_name if subject.subject_name else '',
                'duration': subject.duration + '-' +subject.duration_parameter,
                'duration_parameter': subject.duration_parameter,
                'duration_no': subject.duration,
                'total_mark': subject.total_mark if subject.total_mark else '',
                'pass_mark': subject.pass_mark if subject.pass_mark else '',
            })
        exam_data = {
            'exam_name':self.exam_name,
            'exam': self.id,
            'course': self.course.course,
            'semester': self.semester.semester,
            'start_date': self.start_date.strftime('%d/%m/%Y') ,
            'end_date': self.end_date.strftime('%d/%m/%Y') ,
            'no_subjects': self.no_subjects,
            'exam_total': self.exam_total,
            'subjects_data': subjects_data,
        }
        return exam_data

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

class Choice(models.Model):

    choice = models.CharField('Choice', null=True, blank=True, max_length=200)
    correct_answer = models.BooleanField('Correct Answer', default=False)

    def __unicode__(self):
        return str(self.choice) if self.choice else 'Choice'

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choice'

class Question(models.Model):

    exam = models.ForeignKey(Exam, null=True, blank=True)
    question = models.TextField('Question', null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, blank=True)
    choices = models.ManyToManyField(Choice, null=True, blank=True)
    mark = models.DecimalField(' Mark ',max_digits=14, decimal_places=2, default=0)

    def __unicode__(self):
        return str(self.question) if self.question else 'Question'

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Question'

    def set_attributes(self, question_data):
        print question_data
        self.question = question_data['question']
        self.mark = question_data['mark']
        choices = question_data['choices']
        for choice_data in choices:
            choice = Choice.objects.create(choice=choice_data['choice'],correct_answer=choice_data['correct_answer'])
            self.choices.add(choice)
        self.save()
        return self

    def get_json_data(self):
        choices = []
        if self.choices:
            if self.choices.all().count() > 0:
                for choice in self.choices.all().order_by('-id'):
                    choices.append({
                        'id': choice.id,
                        'choice': choice.choice,
                        })
        question_data = {
            'question': self.question ,
            'choices': choices,
        }
        return question_data

class StudentAnswer(models.Model):

    question = models.ForeignKey(Question, null=True, blank=True)
    choosen_choice = models.BooleanField('Correct Answer', default=False)


    def __unicode__(self):
        return str(self.question.question) if self.question else 'Student'

    class Meta:
        verbose_name = 'StudentAnswer'
        verbose_name_plural = 'StudentAnswer'

class AnswerSheet(models.Model):

    is_attempted = models.BooleanField('Is attempted',default=False)
    student = models.ForeignKey(Student, null=True, blank=True)
    exam = models.ForeignKey(Exam, null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, blank=True)
    student_answer = models.ManyToManyField(StudentAnswer, null=True, blank=True)
    is_completed = models.BooleanField('Is Completed',default=False)

    def __unicode__(self):
        return str(self.student.student_name) if self.student else 'Student'

    class Meta:
        verbose_name = 'AnswerSheet'
        verbose_name_plural = 'AnswerSheet'

