from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse, HttpResponse

from students.models import *
from django.utils import timezone
import json
from django.views.generic import ListView,DetailView,View,CreateView,UpdateView

from .forms import TestCreateFrom,SubjectCreateFrom,QuestionCreateFrom,StudentVerificationFrom
from django.contrib import messages

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required




def allow_to_hod(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_hod:
                print('verified hod')
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse('not a hod')

    return wrapper_func



def allow_to_teacher(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_teacher: 
                return view_func(request,*args, **kwargs)
            else:
            	if request.user.is_hod:
            		pass
            	return HttpResponse('not a taecher')
        else:
         	return redirect("login")

    return wrapper_func


@allow_to_teacher
@login_required
def create_new_test(request,pk):
	subject=Subject.objects.get(pk=pk)
	testcreatefrom = TestCreateFrom()
	if request.method == 'POST':
		testcreatefrom = TestCreateFrom(request.POST)
		if testcreatefrom.is_valid():

			edit_testcreatefrom=testcreatefrom.save(commit=False)
			edit_testcreatefrom.subject=subject
			edit_testcreatefrom.teacher=request.user
			
			edit_testcreatefrom.save()

			messages.success(request, f"Test {edit_testcreatefrom.test_title} has been created add question in it")
			return redirect("subject_detail",pk=subject.id)

	return render(request,'teachers/create_new_test.html',
		{'testcreatefrom':testcreatefrom})


@allow_to_hod
@login_required
# @allow_to_hod
def create_new_subject(request):
	subjectcreatefrom = SubjectCreateFrom()
	if request.method == 'POST':
		subjectcreatefrom = SubjectCreateFrom(request.POST)
		if subjectcreatefrom.is_valid():
			edit_subjectcreatefrom=subjectcreatefrom.save(commit=False)
			edit_subjectcreatefrom.hod=request.user
			edit_subjectcreatefrom.save()
			messages.success(request, f"New Subject :: {edit_subjectcreatefrom.subject_name} has been created successfully")
			return redirect("my_subject")

	return render(request,'teachers/create_new_subject.html',{'subjectcreatefrom':SubjectCreateFrom})



@allow_to_teacher
@login_required
def subject_list_view(request):
    all_subject=Subject.objects.filter(teachers__in=[request.user,])
    return render(request,'teachers/all_subject_list.html',
    			{'all_subject':all_subject})

# def show():
# 	pass



@allow_to_hod
@login_required
def for_hod_subject_list_view(request):
    all_subject=Subject.objects.all()
    return render(request,'teachers/all_subject_list.html',
    			{'all_subject':all_subject})

@allow_to_teacher
@login_required
def subject_detail_view(request,pk):
    subject=Subject.objects.get(pk=pk)
    test_in_subject=Test.objects.filter(subject=subject)
    return render(request,'teachers/subject_detail.html',
    			{'subject':subject,'test_in_subject':test_in_subject})

@allow_to_teacher
@login_required
def test_detail_view(request,pk):
    test=Test.objects.get(pk=pk)
    ques_in_test=Question.objects.filter(test=test)
    return render(request,'teachers/test_detail.html',
    			{'test':test,'ques_in_test':ques_in_test})

@allow_to_teacher
@login_required
def create_new_question(request,test_id,add_another=False):
	print(add_another,'555555555555555')
	test=Test.objects.get(id=test_id)
	questioncreatefrom = QuestionCreateFrom()
	if request.method == 'POST':
		questioncreatefrom = QuestionCreateFrom(request.POST)
		if questioncreatefrom.is_valid():
			edit_questioncreatefrom=questioncreatefrom.save(commit=False)
			edit_questioncreatefrom.teacher=request.user
			edit_questioncreatefrom.test=test
			edit_questioncreatefrom.save()
			messages.success(request, f"New Question creaeted :: {edit_questioncreatefrom.question_title} has been created successfully")
			if not add_another:
				return redirect("test_detail",pk=test.id)
			else:
				return redirect("question_create",test_id=test.id)

	return render(request,'teachers/create_new_question.html',{'questioncreatefrom':questioncreatefrom,'test':test})

@allow_to_teacher
@login_required
# @allow_to_hod
def subject_update_view(request, pk):
 
    subject_object = get_object_or_404(Subject, id = pk)
 
    subject_update_form = SubjectCreateFrom(request.POST or None, 
    	instance = subject_object)

    if subject_update_form.is_valid():
    	edit_subject_update_form=subject_update_form.save(commit=False)
    	edit_subject_update_form.hod=request.user
    	edit_subject_update_form.save()
    	messages.success(request, f"{edit_subject_update_form.subject_name} has been Updated successfully !!")
    	return redirect("my_subject")

 
    return render(request, "teachers/subject_update_form.html", {
    			'subject_update_form':subject_update_form,
    			'subject':subject_object})


@allow_to_teacher
@login_required
def test_update_view(request, pk):
 
    test_object = get_object_or_404(Test, id = pk)
 
    test_update_form = TestCreateFrom(request.POST or None, instance = test_object)

    if test_update_form.is_valid():
    	edit_test_update_form=test_update_form.save(commit=False)
    	edit_test_update_form.subject=test_object.subject
    	edit_test_update_form.teacher=request.user
    	edit_test_update_form.save()
    	messages.success(request, f"{test_object.test_title} has been Updated successfully !!")
    	return redirect("subject_detail",pk=test_object.subject.id)

 
    return render(request, "teachers/test_update_form.html", {
    			'test_update_form':test_update_form,'test':test_object})

@allow_to_teacher
@login_required
def question_update_view(request, pk):
 
    question_object = get_object_or_404(Question, id = pk)
 
    question_update_form = QuestionCreateFrom(request.POST or None, 
    	instance = question_object)

    if question_update_form.is_valid():
    	edit_question_update_form=question_update_form.save(commit=False)
    	edit_question_update_form.teacher=request.user
    	edit_question_update_form.test=question_object.test
    	edit_question_update_form.save()
    	messages.success(request, f"{question_object.question_title} has been Updated successfully !!")
    	return redirect("test_detail",pk=question_object.test.id)

 
    return render(request, "teachers/question_update_form.html", {
    			'question_update_form':question_update_form,'question':question_object})



@allow_to_teacher
@login_required
def show_all_student(request):
	current_teacher=Teacher.objects.get(user=request.user)
	my_students=Student.objects.filter(college_rollno__icontains=current_teacher.class_teacher_roll)
	return render(request, "teachers/my_students.html", {
    			'my_students':my_students})

@allow_to_teacher
@login_required
def verify_the_student(request,pk):

	current_student=get_object_or_404(Student, pk = pk)
	if current_student.verify:
		current_student.verify=False
		messages.error(request, f" Roll No:{current_student.college_rollno} has been Unverified successfully !!")
	else:
		current_student.verify=True
		messages.success(request, f" Roll No:{current_student.college_rollno} has been Verified successfully !!")
	current_student.save()
	#email to student that verification is done
	return redirect("my_students")


@allow_to_teacher
@login_required
def student_update_view(request, pk):
 
    current_student=get_object_or_404(Student, pk = pk)
 
    student_verfiy_form = StudentVerificationFrom(request.POST or None, instance = current_student)

    if student_verfiy_form.is_valid():
    	edit_student_verfiy_form=student_verfiy_form.save(commit=False)
    	edit_student_verfiy_form.save()
    	messages.success(request, f"{edit_student_verfiy_form.college_rollno} has been Updated successfully !!")
    	# return redirect("subject_detail",pk=test_object.subject.id)

 
    return render(request, "teachers/student_update_form.html", {
    			'student_verfiy_form':student_verfiy_form,'current_student':current_student})

