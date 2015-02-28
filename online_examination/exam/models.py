
from django.db import models

from college.models import Course, Semester
from academic.models import Student 

class Subject(models.Model):
    
    subject_name = models.CharField('Subject Name', null=True, blank=True, max_length=200)
    duration = models.CharField('Duration', null=True, blank=True, max_length=200)
    duration_parameter = models.CharField('Duration Parameter', null=True, blank=True, max_length=200)
    total_mark = models.CharField('Total Mark', null=True, blank=True, max_length=200)
    pass_mark = models.DecimalField('Pass Mark', max_digits=14, decimal_places=2, default=0)
    
    def __unicode__(self):
        return str(self.subject_name)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subject'

class Exam(models.Model):
    
    student = models.ForeignKey(Student, null=True, blank=True)
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

    def get_json_data(self, x=None):
        subjects_data = []
        for subject in self.subjects.all():
            subject_dict = {
                'subject_id': subject.id if subject.id else '',
                'subject': subject.subject_name if subject.subject_name else '',
                'subject_name' : subject.subject_name if subject.subject_name else '',
                'Duration': subject.duration + '-' +subject.duration_parameter,
                'duration': subject.duration,
                'duration_parameter': subject.duration_parameter,
                'duration_no': subject.duration,
                'total_mark': subject.total_mark if subject.total_mark else '',
                'pass_mark': subject.pass_mark if subject.pass_mark else '',
            }
            question = Question.objects.filter(exam__id=self.id,subject__id=subject.id)
            question = question[0] if question.count() > 0 else None
            if x:
                if question:
                    subjects_data.append(subject_dict)
            else:
                subjects_data.append(subject_dict) 
            
        exam_data = {
            'exam_name':self.exam_name,
            'exam': self.id,
            'course': self.course.id,
            'semester': self.semester.id,
            'course_name': self.course.course,
            'semester_name': self.semester.semester,
            'start_date': self.start_date.strftime('%d/%m/%Y') ,
            'end_date': self.end_date.strftime('%d/%m/%Y') ,
            'no_subjects': self.no_subjects,
            'exam_total': self.exam_total,
            'subjects_data': subjects_data,
        }
        return exam_data



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
        print choices
        for choice_data in choices:
            choice = Choice.objects.create(choice=choice_data['choice'])
            if choice_data['correct_answer'] == 'true':
                choice.correct_answer = True
            else:
                choice.correct_answer = False
            choice.save()
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
            'id': self.id,
            'choices': choices,
        }
        return question_data

class StudentAnswer(models.Model):

    question = models.ForeignKey(Question, null=True, blank=True)
    choosen_choice = models.ForeignKey(Choice, null=True, blank=True)
    is_correct = models.BooleanField('Is Answer Correct', default=False)
    mark = models.DecimalField('Mark', max_digits=14, decimal_places=2, default=0 )


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
    student_answers = models.ManyToManyField(StudentAnswer, null=True, blank=True)
    is_completed = models.BooleanField('Is Completed',default=False)
    total_mark = models.DecimalField('Total Mark Obtained',max_digits=14, decimal_places=2, default=0)
    status = models.CharField('Status ', null=True, blank=True, max_length=200)

    def __unicode__(self):
        return str(self.student.student_name) if self.student else 'Student'

    class Meta:
        verbose_name = 'AnswerSheet'
        verbose_name_plural = 'AnswerSheet'

    def set_attributes(self, answer_data):   
        questions = answer_data['questions']
        total = 0
        for question_data in questions:
            student_answer = StudentAnswer()
            question = Question.objects.get(id=question_data['id'])
            choosen_choice = Choice.objects.get(id=question_data['chosen_answer'])
            
            student_answer.question = question
            student_answer.choosen_choice = choosen_choice
            student_answer.save()
            self.student_answers.add(student_answer)
            for correct_choice in question.choices.all().order_by('id'):
                if correct_choice.choice == choosen_choice.choice:
                    if correct_choice.correct_answer == True:
                        student_answer.mark = question.mark
                        student_answer.is_correct = True
                        total = float(total) + float(student_answer.mark)
                        student_answer.save()
        self.total_mark = total
        self.save()
        if self.total_mark >= self.subject.pass_mark:
            self.status = 'Pass'
        else:
            self.status = 'Fail'
        self.save()

    def get_json_data(self):
        student_answers = []
        if self.student_answers:
            if self.student_answers.all().count() > 0:
                for student_answer in self.student_answers.all().order_by('-id'):
                    student_answers.append({
                        'id': student_answer.id,
                        'question': student_answer.question.id,
                        'choosen_choice': student_answer.choosen_choice.id,
                        'is_correct':student_answer.is_correct if student_answer.is_correct else '',
                        'mark': student_answer.mark if student_answer.mark else '',
                        })
        answer_sheet_data = {
            'student': self.student.id,
            'student_name': self.student.student_name,
            'fathers_name': self.student.father_name if self.student.father_name else '',
            'specialization': self.student.specialization if self.student.specialization else '',
            'exam': self.exam.id,
            'exam_name':self.exam.exam_name,
            'subject_name': self.subject.subject_name,
            'status':self.status if self.status else 'Fail',
            'total_mark': self.total_mark if self.total_mark else 0,
            'subject' : self.subject.id,
            'student_answers': student_answers,
            'is_completed': self.is_completed if self.is_completed else '',
            'is_attempted': self.is_attempted if self.is_attempted else '',
        }
        return answer_sheet_data