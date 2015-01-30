
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
                    'semester': exam.semester.semester,
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


class CreateQuestion(View):
    def get(self, request, *args, **kwargs):             
        return render(request, 'create_questions.html', {})

class SaveMarks(View):
    def post(self, request, *args, **kwargs):
        questions = ast.literal_eval(request.POST['question_details'])
        course = Course.objects.get(id = questions['course'])
        semester = Semester.objects.get(id = questions['semester'])
        exam = Exam.objects.get(id = questions['exam'])
        subject = Subject.objects.get(id = questions['subject'])
        total_mark = 0
        if request.is_ajax(): 
            # try:
            for question_detail in questions['questions']:
                question = Question.objects.create(exam=exam,subject=subject)
                question_data = question.set_attributes(question_detail)
            res = {
                'result': 'ok',
            } 
            # except:
            #     res = {
            #             'result': 'error',
            #         } 
            status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")
        return render(request, 'create_questions.html', {})


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
        if request.is_ajax():
            try:
                exam = Exam.objects.get(id = exam_schedule_id)
                exam_schedule = exam.get_json_data()
                res = {
                    'result': 'ok',
                    'exam_schedule': exam_schedule,
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
        exams = {}
        if request.is_ajax():
            try:
                exams = Exam.objects.filter(course=course_id, semester=semester_id)
                for exam in exams:
                    exams = exam.get_json_data()
                print exams
                res = {
                    'result': 'ok',
                    'exams': exams,
                }       
        
            except Exception as ex:
                print "Exception == ", str(ex),
                res = {
                    'result': 'error',
                    'message': str(ex),
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

class QuestionPaper(View):

    def get(self, request, *args, **kwargs):
        questions_list = []
        if request.is_ajax():
            try:
                answer_sheet = AnswerSheet.objetcs.get(student__user=request.user, exam=request.GET.get('exam', ''), subject=request.GET.get('subject', ''))
                res = {
                    'result': 'error',
                    'message': 'Already Wrote the exam'
                }
                
            except Exception as ex:
                questions = Question.objects.filter(exam=request.GET.get('exam', ''),subject=request.GET.get('subject', ''))
                print questions
                for question in questions:
                    questions_list.append(question.get_json_data())
                print questions_list
                res = {
                    'result': 'Ok',
                    'questions': questions_list,
                }

            response = simplejson.dumps(res)
        return HttpResponse(response, mimetype='application/json')

class CreateAnswerSheet(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            answer_sheet_details =  ast.literal_eval(request.POST['answer_details'])
            try:
                exam = Exam.objects.get(id=answer_sheet_details['exam'])
                subject = Subject.objects.get(id=answer_sheet_details['subject'])
                student = Student.objects.get(user=request.user)
                answer_sheet = AnswerSheet.objects.create(student=student, exam=exam, subject=subject)
                answer_sheet.is_attempted = True;
                answer_sheet.save()
                res = {
                    'result': 'Ok',
                }
            except Exception as ex:
                res = {
                    'result': 'error',
                    'message': str(ex),
                }
                
        response = simplejson.dumps(res)
        return HttpResponse(response, mimetype='application/json')

class WriteExam(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                student = Student.objects.get(user=request.user)
                student_details = student.get_json_data()
                res = {
                    'result': 'Ok',
                    'student': student_details,
                }
            except Exception as ex:
                res = {
                        'result': 'error',
                        'message': str(ex),
                    }
            response = simplejson.dumps(res)
            return HttpResponse(response, mimetype='application/json')
        return render(request, 'write_exam.html', {})

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            answer_sheet_details =  ast.literal_eval(request.POST['answer_sheet'])
            try:
                answer_sheet = AnswerSheet()
                answer_sheet_data = answer_sheet.set_attributes(answer_sheet_details)
                res = {
                    'result': 'Ok',
                }
            except Exception as ex:
                res = {
                    'result': 'error',
                    'message': str(ex),
                }
        response = simplejson.dumps(res)
        return HttpResponse(response, mimetype='application/json')