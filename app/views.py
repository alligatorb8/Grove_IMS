from django.db.models import Prefetch
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.template import loader
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from .models import Internship, OrgUnit, InternApplication, InternshipTask, InternshipTaskQuestion, \
    InternshipTaskProgress, InternshipTaskEndQuestion, Resources, InternshipTaskEndAnswers, NoInternSpots, \
    InternshipFocus, Counselor, SchoolGroups, PerformanceFeedback, PerformanceFeedbackAnswers
from .form import ProfileForm, UserFormCreation, UserFormUpdate, InternApplicationForm, InternshipForm, OrgNewForm, \
    TaskNewForm, TaskNewQuestionForm, TaskAnswerQuestionForm, TaskProgressForm, InternshipTaskEndAnswersForm, \
    ResourcesForm, FocusNewForm, InternshipFocusEndAnswersForm, PerformanceFeedbackNewForm, PerformanceFeedbackAnswersForm, \
    ContactForm


# Create your views here.
@login_required(login_url='/login/')
def internship_search(request):
    template = loader.get_template('app/internship_search.html')
    internship_list = Internship.objects.order_by('registration_start_date')
    context = {
        'internship_list': internship_list,
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def contact_us(request):
    title = 'Contact'
    form = ContactForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        subject = 'Message from InternManagementSystem'
        message = '%s %s' %(comment, name)
        emailFrom = form.cleaned_data['email']
        emailTo = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, emailFrom, emailTo, fail_silently=True)
        messages.success(request, ("Thank you for your message! We'll get back to you as soon as possible."))
    return render(request, 'app/contact_us.html', {'form': form})

@login_required(login_url='/login/')
def user_page(request, user_id):
    user_info = User.objects.get(pk=user_id)
    return render(request, 'app/user_page.html', {'user_info': user_info})


@login_required(login_url='/login/')
def internship_view(request, internship_id):
    internship_info = Internship.objects.get(id=internship_id)
    focuses = InternshipFocus.objects.filter(internship=internship_info)

    tasks = InternshipTask.objects.filter(internship=internship_id) \
        .prefetch_related('questions')
    if request.user.member.is_student:
        tasks = tasks.prefetch_related(
            Prefetch('progress', queryset=InternshipTaskProgress.objects.filter(intern=request.user))
        )
    elif request.user.member.is_supervisor:
        tasks = tasks.prefetch_related('progress')
        focuses = focuses.prefetch_related('focus_answers')

    application_info = InternApplication.objects.filter(internship=internship_id)
    spots = internship_info.openings - application_info.filter(state='approved').count()
    return render(request, 'app/internship_view.html', {
        'internship_info': internship_info,
        'focuses': focuses,
        'tasks': tasks,
        'application_info': application_info,
        'spots': spots,
    })


@login_required(login_url='/login/')
@transaction.atomic
def register_intern(request, internship_id):
    if request.method == 'POST':
        form = InternApplicationForm(request.POST)
        internship_info = Internship.objects.get(id=internship_id)
        if form.is_valid():
            post = form.save(commit=False)
            # post.internship.pk = internship_id
            post.applicant = request.user
            post.date_created = timezone.now()
            post.save()
            messages.success(request, ('Account has been created! Please check your email to verify account.'))
            return redirect('internship_view', internship_id)
        else:
            messages.error(request, ('Error creating user. Please correct the error below.'))
    else:
        form = InternApplicationForm()
        internship_info = Internship.objects.get(id=internship_id)
    return render(request, 'app/register_intern.html', {
        'form': form,
        'internship_info': internship_info,
    })


@login_required(login_url='/login/')
@transaction.atomic
def connect_intern(request):
    if request.method == 'POST':
        form = InternApplicationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.date_created = timezone.now()
            try:
                post.save()
            except NoInternSpots:
                messages.error(request, ('Error connecting intern with org. You are out of avalable intern spots.'))

            else:
                messages.success(request, (
                    'Intern ' + post.applicant.first_name + ' was successfully connected to ' + post.internship.title + '!'))
            return redirect('internship_my', )
        else:
            messages.error(request, ('Error connecting intern with org. Please correct the error below.'))
    else:
        form = InternApplicationForm()
    return render(request, 'app/register_intern.html',
                  {'form': form, }
                  )


@login_required(login_url='/login/')
def edit_application(request, application_id):
    post = get_object_or_404(InternApplication, pk=application_id)
    if request.method == 'POST':
        form = InternApplicationForm(request.POST, instance=post)
        internship_info = Internship.objects.get(id=internship_id)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, ('Internship application was successfully updated!'))
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, ('Error updating internship application. Please correct the error below.'))
    else:
        form = InternApplicationForm(instance=post)
        internship_info = Internship.objects.get(id=internship_id)
    return render(request, 'app/register_intern.html', {
        'form': form,
        'internship_info': internship_info,
    })


@login_required(login_url='/login/')
def my_dashboard(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    my_application_list = InternApplication.objects.select_related('internship').filter(applicant__id=user_id)
    my_internship_ids = [ia.internship_id for ia in my_application_list]
    my_supervisor_list = Internship.objects.filter(main_contact__id=user_id)
    tasks_and_questions = InternshipTask.objects.filter(internship_id__in=my_internship_ids).prefetch_related(
        'questions').order_by('-date_last_question_update')
    return render(request, 'app/dashboard.html', {
        'user': user,
        'my_application_list': my_application_list,
        'my_supervisor_list': my_supervisor_list,
        'tasks_and_questions': tasks_and_questions,
    })


@login_required(login_url='/login/')
def internship_my(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    my_internships_list = InternApplication.objects.filter(applicant__id=user_id)
    my_supervisor_list = Internship.objects.filter(main_contact__id=user_id)
    return render(request, 'app/internship_my.html', {
        'user': user,
        'my_internships_list': my_internships_list,
        'my_supervisor_list': my_supervisor_list,
    })


@login_required(login_url='/login/')
def internship_new(request):
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.main_contact = request.user
            # post.company =request.user
            post.date_created = timezone.now()
            post.save()
            messages.success(request, ('Internship ' + post.title + ' was successfully created!'))
            return redirect('internship_view', internship_id=post.pk)
        else:
            messages.error(request, ('Error Creating internship. Please correct the error below.'))
    else:
        form = InternshipForm()
    return render(request, 'app/internship_new.html', {'form': form})



    # ORG MANAGEMENT #


@login_required(login_url='/login/')
def org_new(request):
    if request.method == 'POST':
        form = OrgNewForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.date_created = timezone.now()
            post.save()
            messages.success(request, ('Organization ' + post.org_name + ' was successfully created!'))
            return redirect('org_info', org_name=post.org_name)
        else:
            messages.error(request, ('Error creating organization. Please correct the error below.'))
    else:
        form = OrgNewForm()
    return render(request, 'app/org_new.html', {'form': form})


@login_required(login_url='/login/')
def org_info(request, org_name):
    template = loader.get_template('app/org_info.html')
    org_details = OrgUnit.objects.get(org_name=org_name)
    internship_list = Internship.objects.filter(company__org_name=org_name)
    context = {
        'org_details': org_details,
        'internship_list': internship_list,
    }

    return HttpResponse(template.render(context, request))



    # TASK Management#


@login_required(login_url='/login/')
def task_new(request, internship_id):
    if request.method == 'POST':
        form = TaskNewForm(request.POST)
        internship_info = Internship.objects.get(id=internship_id)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.internship = internship_info
            post.date_created = timezone.now()
            post.save()
            messages.success(request, ('Task ' + post.name + ' was successfully created!'))
            return redirect('internship_view', internship_id=internship_id)
        else:
            messages.error(request, ('Error creating task. Please correct the error below.'))
    else:
        internship_info = Internship.objects.get(id=internship_id)
        form = TaskNewForm()
    return render(request, 'app/task_new.html', {
        'form': form, 'internship_info': internship_info
    })


@login_required(login_url='/login/')
def task_progress(request, task_id, progress_id=None):
    if progress_id == None:
        progress_item = None
        print('her')
    else:
        progress_item = InternshipTaskProgress.objects.get(id=progress_id)
    if request.method == 'POST':
        task_info = InternshipTask.objects.get(id=task_id)
        form = TaskProgressForm(request.POST, instance=progress_item)
        if form.is_valid():
            post = form.save(commit=False)
            post.intern = request.user
            post.task = task_info
            post.time_stamp = timezone.now()
            post.save()
            messages.success(request, ('Task ' + task_info.name + ' progress was successfully updated!'))
            if post.progress == 100:
                return redirect('task_progress_done', task_id=task_info.id)
            else:
                return redirect('internship_view', internship_id=task_info.internship.id)
        else:
            messages.error(request, ('Error creating task progress. Please correct the error below.'))
    else:
        task_info = InternshipTask.objects.get(id=task_id)
        form = TaskProgressForm(instance=progress_item)
    return render(request, 'app/task_progress.html', {
        'form': form, 'task_info': task_info
    })


@login_required(login_url='/login/')
def task_question_new(request, task_id):
    if request.method == 'POST':
        form = TaskNewQuestionForm(request.POST)
        task_info = InternshipTask.objects.get(id=task_id)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.task = task_info
            post.date_created = timezone.now()
            post.save()
            messages.success(request, ('Task question "' + post.question + '" was successfully created!'))
            return redirect('internship_view', internship_id=task_info.internship.id)
        else:
            messages.error(request, ('Error creating task question. Please correct the error.'))
    else:
        task_info = InternshipTask.objects.get(id=task_id)
        form = TaskNewQuestionForm()
    return render(request, 'app/question_new.html', {
        'form': form, 'task_info': task_info
    })


@login_required(login_url='/login/')
def task_question_answer(request, question_id):
    if request.method == 'POST':
        form = TaskAnswerQuestionForm(request.POST)
        question_info = InternshipTaskQuestion.objects.get(id=question_id)
        if form.is_valid():
            post = form.save(commit=False)
            post.question = question_info
            post.intern = request.user
            post.date_created = timezone.now()
            post.save()
            messages.success(request, ('Answer to "' + post.question.question + '" was successfully created!'))
            return redirect('internship_view', internship_id=question_info.task.internship.id)
        else:
            messages.error(request, ('Error with task answer. Please correct the error.'))
    else:
        question_info = InternshipTaskQuestion.objects.get(id=question_id)
        form = TaskAnswerQuestionForm()
    return render(request, 'app/question_answer.html', {
        'form': form, 'question_info': question_info
    })


@login_required(login_url='/login/')
@transaction.atomic
def task_progress_done(request, task_id):
    question_info = InternshipTaskEndQuestion.objects.filter(active=True).order_by('order')
    task_info = InternshipTask.objects.get(id=task_id)
    form = InternshipTaskEndAnswersForm(request.POST or None, extra=question_info)
    if request.method == 'POST':
        if form.is_valid():
            InternshipTaskEndAnswers.objects.filter(task=task_info).delete()
            for key, value in form.cleaned_data.items():
                post = InternshipTaskEndAnswers()
                post.task = task_info
                post.intern = request.user
                post.question_id = int(key.split('_')[1])
                post.answer = value
                post.save()
            messages.success(request, ('Answer to "' + task_info.name + '" was successfully created!'))
            return redirect('internship_view', internship_id=task_info.internship_id)
        else:
            messages.error(request, ('Error with wrap-up answers. Please correct the error.'))
            print(form.errors)
    else:
        print("--->>>> Nothing to find in task_progress_done <<<<---")
    return render(request, 'app/internship_TaskEndAnswers.html', {
        'form': form, 'question_info': question_info,
        'task_info': task_info
    })

    # PROFILE MANAGEMENT #


@transaction.atomic
def register_profile(request):
    if request.method == 'POST':
        user_form = UserFormCreation(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form2 = ProfileForm(request.POST, instance=user.member)
            profile_form2.save()
            messages.success(request,
                             ('Your account has been created! Please check your email and verify your account.'))
            return redirect('dashboard')
        else:
            messages.error(request, ('Error creating Account. Please correct the error below.'))
    else:
        user_form = UserFormCreation()
        profile_form = ProfileForm()
    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.internmember.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()


@login_required(login_url='/login/')
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserFormUpdate(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.member)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('update_profile')
        else:
            messages.error(request, ('Error updating profile. Please correct the error below.'))
    else:
        user_form = UserFormUpdate(instance=request.user)
        profile_form = ProfileForm(instance=request.user.member)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required(login_url='/login/')
def resources_my(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    my_resources_list = Resources.objects.filter(author__id=user_id)
    return render(request, 'app/resources_my.html', {
        'user': user,
        'my_resources_list': my_resources_list,
    })


@login_required(login_url='/login/')
def resources_new(request):
    if request.method == 'POST':
        form = ResourcesForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.state = 'SUBMITTED'
            post.date_created = timezone.now()
            post.save()
            messages.success(request, ('Created resource successfully!'))
            return redirect('resources_my')
        else:
            messages.error(request, ('Error with resource creation. Please correct the error.'))
    else:
        form = ResourcesForm()
    return render(request, 'app/resources_new.html', {
        'form': form,
    })


@login_required(login_url='/login/')
@transaction.atomic
def focus_new(request, internship_id):
    if request.method == 'POST':
        form = FocusNewForm(request.POST)
        internship_info = Internship.objects.get(id=internship_id)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.date_created = timezone.now()
            post.save()
            messages.success(request, ('Focus for task ' + post.internship.title + ' was successfully created!'))
            return redirect('internship_view', internship_id=internship_id)
        else:
            messages.error(request, ('Error creating focus. Please contact support.'))
    else:
        internship_info = Internship.objects.get(id=internship_id)
        form = FocusNewForm()
    return render(request, 'app/focus_new.html', {
        'form': form, 'internship_info': internship_info
    })


@login_required(login_url='/login/')
@transaction.atomic
def focus_answer(request, focus_id):
    if request.method == 'POST':
        form = InternshipFocusEndAnswersForm(request.POST)
        focus_info = InternshipFocus.objects.get(id=focus_id)
        if form.is_valid():
            post = form.save(commit=False)
            post.focus = focus_info
            post.focus = focus_info
            post.intern = request.user
            post.date_created = timezone.now()
            post.save()
            messages.success(request, ('Focus answer to "' + post.focus.internship.title + '" was successfully saved!'))
            return redirect('internship_view', internship_id=focus_info.internship.id)
        else:
            messages.error(request, ('Error with focus answer. Please contact support.'))
    else:
        focus_info = InternshipFocus.objects.get(id=focus_id)
        form = InternshipFocusEndAnswersForm()
    return render(request, 'app/focus_answer.html', {
        'form': form, 'focus_info': focus_info
    })


@login_required(login_url='/login/')
@transaction.atomic
def performance_new(request, internship_id):
    if request.method == 'POST':
        form = PerformanceFeedbackNewForm(request.POST)
        internship_info = Internship.objects.get(id=internship_id)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.date_created = timezone.now()
            post.save()
            messages.success(request, ('Performance Report for ' + post.internship.title + ' was successfully created!'))
            return redirect('internship_view', internship_id=internship_id)
        else:
            messages.error(request, ('Error creating feedback. Please contact support.'))
    else:
        internship_info = Internship.objects.get(id=internship_id)
        form = PerformanceFeedbackNewForm()
    return render(request, 'app/performance_new.html', {
                  'form': form, 'internship_info': internship_info
                  })

@login_required(login_url='/login/')
@transaction.atomic
def performance_answer(request, feedback_id):
    if request.method == 'POST':
        form = PerformanceFeedbackAnswersForm(request.POST)
        feedback_info = PerformanceFeedback.objects.get(id=feedback_id)
        if form.is_valid():
            post = form.save(commit=False)
            post.feedback = feedback_info
            post.feedback = feedback_info
            post.supervisor = request.user
            post.date_created = timezone.now()
            post.save()
            messages.success(request, ('Performance Feedback answer to "' + post.feedback.internship.title + '" was successfully saved!'))
            return redirect('internship_view', internship_id=feedback_info.internship.id)
        else:
            messages.error(request, ('Error with feedback answer. Please contact support.'))
    else:
        feedback_info = PerformanceFeedback.objects.get(id=feedback_id)
        form = PerformanceFeedbackAnswersForm()
    return render(request, 'app/performance_answer.html', {
                  'form': form, 'feedback_info': feedback_info
                  })


@login_required(login_url='/login/')
def counselor_view(request):
    user_id = request.user.id
    counselor_info = User.objects.get(pk=user_id)
    counselor_site = Counselor.objects.get(counselor=counselor_info)
    counselor_students = SchoolGroups.objects.filter(school=counselor_site.school)
    print(counselor_students)
    student_internship_ids = [ia.intern_id for ia in counselor_students]
    print(student_internship_ids)
    student_internships = InternApplication.objects.select_related('internship').filter(
        applicant__id__in=student_internship_ids)

    # student_internships = InternApplication.objects.filter(applicant=counselor_students.intern)
    return render(request, 'app/counselor_view.html', {
        'counselor_info': counselor_info,
        'counselor_site': counselor_site,
        'counselor_students': counselor_students,
        'student_internships': student_internships,
    })
