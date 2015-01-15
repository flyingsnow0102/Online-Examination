
import simplejson
import ast
from datetime import datetime

from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from exam.models import *
from academic.models import Student


class ScheduleExam(View):
    def get(self, request, *args, **kwargs):
        course = request.GET.get('course', '')
        if course :
            exams = Exam.objects.filter(course__id=course)
        else:
            exams = Exam.objects.all()
        if request.is_ajax():
            exam_list = []
            for exam in exams:
                exam_list.append({
                    'id': exam.id,
                    'name': exam.exam_name,
                    'course': exam.course.course,
                    'start_date': exam.start_date.strftime('%d/%m/%Y') if exam.start_date else '',
                    'end_date': exam.end_date.strftime('%d/%m/%Y') if exam.end_date else '',
                })
            res = {
                'result': 'Ok',
                'exams':  exam_list
            }
            status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

        ctx = {
            'exams': exams
        }
        return render(request, 'list_exam_schedule.html',ctx)

class CreateExam(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_exam_schedule_details.html',{})


class Marks(View):
    def get(self, request, *args, **kwargs):             
        return render(request, 'marks.html', {})

class SaveMarks(View):
    def post(self, request, *args, **kwargs):
        students = ast.literal_eval(request.POST['student'])
        course = Course.objects.get(id = request.POST['course'])
        semester = Semester.objects.get(id = request.POST['semester'])
        total_mark = 0
        if request.is_ajax():                                               
            for student_detail in students:
                student = Student.objects.get(id = student_detail['student_id'])
                for exam_detail in student_detail['exam_marks']:
                    exam = Exam.objects.get(id = exam_detail['id']) 
                    try:
                        mark = StudentMark.objects.get(course=course,semester=semester,exam=exam,student=student)
                        for subject_mark in mark.subject_mark.all():
                            subject_mark.delete()
                    except:
                        mark = StudentMark() 
                        mark.course=course
                        mark.semester=semester
                        mark.exam=exam
                        mark.student=student           
                    for subject_detail in exam_detail['subjects']:
                        try:
                            subject = SubjectMark.objects.get(subject_name = subject_detail['subject_name'])
                        except:
                            subject = SubjectMark()                                    
                        subject.subject_name = Subject.objects.get(subject_name = subject_detail['subject'])
                        subject.mark = subject_detail['mark']
                        status = ''
                        if subject_detail['mark'] and subject_detail['minimum']:                         
                            if int(subject_detail['mark']) < int(subject_detail['minimum']):
                                status = "FAIL"
                            else:
                                status = "PASS"
                        subject.status = status
                        if subject_detail['mark']:
                            total_mark = total_mark + int(subject_detail['mark'])
                        subject.save()
                        mark.save()
                        mark.subject_mark.add(subject)
                    mark.total_mark = total_mark
                    mark.save()                                          
                    total_mark = 0
                    res = {
                        'result': 'ok',
                    }  
            status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")
        return render(request, 'marks.html', {})


def save_exam_schedule_details(exam, request):
    exam.start_date = datetime.strptime(request.POST['start_date'], '%d/%m/%Y')
    exam.end_date = datetime.strptime(request.POST['end_date'], '%d/%m/%Y')
    course = Course.objects.get(id = request.POST['course'])
    semester = Semester.objects.get(id = request.POST['semester'])
    exam.exam_name = course.course + '-' +semester.semester
    exam.no_subjects = request.POST['no_subjects']
    exam.exam_total = request.POST['exam_total']
    subjects = ast.literal_eval(request.POST['subjects'])
    exam.save()
    for subject in subjects:        
        sub, created = Subject.objects.get_or_create(subject_name=subject['subject_name'])
        sub.duration = subject['duration']
        sub.duration_parameter = subject['duration_parameter']
        sub.total_mark = subject['total_mark']
        sub.pass_mark = subject['pass_mark']
        sub.save()
        exam.subjects.add(sub)
    exam.save()

class SaveExamSchedule(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                course = Course.objects.get(id = request.POST['course'])
                semester = Semester.objects.get(id = request.POST['semester'])
                exam_name = ''
                exam_name = course.course + '-' +semester.semester
                exam = Exam.objects.get(course=course,semester=semester,exam_name=exam_name)
                res = {
                    'result': 'error',
                    'message': 'Exams Scheduled Already'
                }
                status_code = 200
            except Exception as ex:
                print str(ex), "Exception ===="
                exam_name = ''
                exam_name = course.course + '-' +semester.semester
                exam = Exam.objects.create(course=course,semester=semester,exam_name=exam_name)
                print exam
                save_exam_schedule_details(exam, request)                     
                res = {
                    'result': 'Ok',
                }
                status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

class ViewExamSchedule(View):

    def get(self, request, *args, **kwargs):
        exam_schedule_id = kwargs['exam_schedule_id']
        ctx_exam_schedule = []
        ctx_subjects = []
        if request.is_ajax():
            try:
                exam = Exam.objects.get(id = exam_schedule_id)
                subjects = exam.subjects.all()
                for subject in subjects:
                    ctx_subjects.append({
                        'subject_id': subject.id if subject.id else '',
                    	'subject_name': subject.subject_name if subject.subject_name else '',
                    	'duration': subject.duration if subject.duration else '',
                        'duration_parameter': subject.duration_parameter if subject.duration_parameter else '',
                        'total_mark': subject.total_mark if subject.total_mark else '',
                        'pass_mark': subject.pass_mark if subject.pass_mark else '',
                        'date': subject.date.strftime('%d/%m/%Y') if subject.date else '',
                    })               
                ctx_exam_schedule.append({
                    
                    'exam_name': exam.exam_name if exam.exam_name else '',
                    'start_date': exam.start_date.strftime('%d/%m/%Y') if exam.start_date else '',
                    'end_date': exam.end_date.strftime('%d/%m/%Y') if exam.end_date else '',
                    'course': exam.course.course if exam.course.course else '',
                    'exam_total': exam.exam_total if exam.exam_total else '',
                    'no_subjects': exam.no_subjects if exam.no_subjects else '',
                    'subjects':ctx_subjects,
                })
                res = {
                    'result': 'ok',
                    'exam_schedule': ctx_exam_schedule,
                }
                status = 200
            except Exception as ex:
                print "Exception == ", str(ex)
                res = {
                    'result': 'error',
                    'exam_schedule': str(ex),
                }
                status = 500
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class GetExams(View):

    def get(self, request, *args, **kwargs):
        
        course_id = kwargs['course_id']
        semester_id = kwargs['semester_id']
        ctx_exam_marks = []
        ctx_subjects = []
        ctx_student = []
        if request.is_ajax():
            try:
                exams = Exam.objects.filter(course=course_id, semester=semester_id)              
                students = Student.objects.filter(course=course_id).order_by('roll_number')
                for student in students:
                    for exam in exams:
                        try:
                            for subject in exam.subjects.all():
                                try:
                                    student_marks = StudentMark.objects.get(course=course_id, student=student.id, exam=exam.id)
                                    subject = student_marks.subject_mark.get(subject_name=subject)
                                    ctx_subjects.append({
                                        'subject_id': subject.id if subject.id else '',
                                        'subject': subject.subject_name.subject_name if subject.subject_name.subject_name else '',
                                        'maximum': subject.subject_name.total_mark if subject.subject_name.total_mark else '',
                                        'minimum': subject.subject_name.pass_mark if subject.subject_name.pass_mark else '',
                                        'mark': subject.mark if subject.mark else '',
                                        'status': subject.status if subject.status else '',
                                    })
                                except:
                                    ctx_subjects.append({
                                        'subject_id': subject.id if subject.id else '',
                                        'subject': subject.subject_name,
                                        'maximum':str(subject.total_mark),
                                        'minimum':subject.pass_mark,
                                        'mark': '',
                                        'status': ''
                                    })
                            ctx_exam_marks.append({
                                'exam_name': exam.exam_name,
                                'id': exam.id,
                                'subjects': ctx_subjects,                                
                                })
                            ctx_subjects = []
                        except:
                            for subject in exam.subjects.all():
                                ctx_subjects.append({
                                    'subject_id': subject.id if subject.id else '',
                                    'subject': subject.subject_name,
                                    'maximum':str(subject.total_mark),
                                    'minimum':subject.pass_mark,
                                    'mark': '',
                                    'status': ''
                                })
                            ctx_exam_marks.append({
                                'exam_name': exam.exam_name,                            
                                'id' : exam.id,                                
                                'subjects': ctx_subjects,                               
                            })
                            ctx_subjects = []
                    ctx_student.append({
                        'student_id': student.id,
                        'student_name': student.student_name,
                        'roll_no': student.roll_number,
                        'exam_marks': ctx_exam_marks,                
                        })
                    ctx_exam_marks = []
                res = {
                    'result': 'ok',
                    'students': ctx_student,
                }       
        
            except Exception as ex:
                print "Exception == ", str(ex),
                res = {
                    'result': 'error',
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, mimetype='application/json')



class DeleteExamSchedule(View):
    def get(self, request, *args, **kwargs):

        exam_schedule_id = kwargs['exam_schedule_id']       
        exam = Exam.objects.filter(id=exam_schedule_id)                          
        exam.delete()
        return HttpResponseRedirect(reverse('schedule_exam'))

class EditExamSchedule(View):

    def get(self, request, *args, **kwargs):
        
        exam_schedule_id = kwargs['exam_schedule_id']
        return render(request, 'edit_exam_schedule.html', {
            'exam_schedule_id': exam_schedule_id
        })

    def post(self, request, *args, **kwargs):
        
        exam_schedule_id = kwargs['exam_schedule_id']
        exam = Exam.objects.get(id=exam_schedule_id)
        exam.subjects = []
        exam.save()
        save_exam_schedule_details(exam, request)
        if request.is_ajax():
            res = {
                'result': 'Ok',
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, mimetype='application/json')
        return render(request, 'edit_exam_schedule.html', {
            'exam_schedule_id': exam_schedule_id
        })