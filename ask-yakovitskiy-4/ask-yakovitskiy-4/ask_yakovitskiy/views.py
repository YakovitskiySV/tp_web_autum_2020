from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from ask_yakovitskiy.models import Question, Answer, Profile, LikeAnswer, LikeQuestion, Tag
from ask_yakovitskiy.forms import LoginForm, UserForm, NewQuestionForm, AnswerForm, SettingsForm
import datetime

STD_PER_PAGE = 5

def paginate(request, object_list, per_page):
    paginator = Paginator(object_list, per_page)
    page_num = request.GET.get('page')
    return paginator.get_page(page_num)

def hot(request):
    questions_page = paginate(request, Question.objects.all(), STD_PER_PAGE)
    return render(request, 'index.html', {
        'questions': questions_page,
    })

def newQuestions(request):
    questions_page = paginate(request, Question.objects.all(), STD_PER_PAGE)
    return render(request, 'index.html', {
        'questions': questions_page,
    })

@login_required
def newQuestion(request):
    form = NewQuestionForm()
    if request.method == 'GET':
        form = NewQuestionForm()
    else:
        form = NewQuestionForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = Profile.objects.get(user=request.user.pk)
            question.rating = 0
            question.answers_number = 0
            question.save()
            return redirect(reverse('question', kwargs={'pk': question.pk}))
    ctx = {'form': form}
    return render(request, 'new-question.html', ctx)

@login_required
def settings(request):
    current_user = request.user
    if request.method == 'GET':
        form = SettingsForm(initial={
            'username': current_user.username,
            'email': current_user.email,
            'avatar': Profile.objects.get(user=current_user).avatar,
        })
    else:
        form = SettingsForm(data=request.POST)
        if form.is_valid():
            if current_user.check_password(form.cleaned_data['old_password']):
                try:
                    if User.objects.get(username=form.cleaned_data['username']).username == form.cleaned_data['username']:
                        raise User.DoesNotExist 
                    ctx = {'form': form, 'error': 'This username already exists'}
                    return render(request, 'settings.html', ctx)
                except User.DoesNotExist:
                    current_user.username = form.cleaned_data['username']
                if form.cleaned_data['email'] != '':
                    if not User.objects.filter(email=form.cleaned_data['email']).exists():
                        current_user.email = form.cleaned_data['email']

                if form.cleaned_data['new_password'] != '' and form.cleaned_data['new_password'] == form.cleaned_data['confirm_new_password']:
                    current_user.set_password(form.cleaned_data['new_password'])
                    auth.login(request, current_user)
                if form.cleaned_data['avatar'] is not None:
                    current_user.avatar = form.cleaned_data['avatar']
                current_user.save()
    ctx = {'form': form}
    return render(request, 'settings.html', ctx)

def AddUser(request, form):
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        if User.objects.get(username=user.username):
            user.save()
            profile = Profile()
            profile.user = user
            if profile.avatar is not None:
                profile.avatar = form.cleaned_data['avatar']
            else:
                profile.avatar = "img/question-mark.jpg"
            profile.save()
            auth.authenticate(username=user.username, password=form.cleaned_data.get('password'))
            auth.login(request, user)
        else:
            pass

def singUp(request):
    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(data=request.POST)
        AddUser(request, form)
        return redirect("/")
    ctx = {'form': form}
    return render(request, 'sing-up.html', ctx)

def singIn(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect("/")
            else:
                pass
        else:
            pass
    ctx = {'form': form}
    return render(request, 'sing-in.html', ctx)

@login_required
def LogOut(request):
    auth.logout(request)
    previous_page = request.META.get('HTTP_REFERER')
    if previous_page is not None:
        return redirect(previous_page)
    return redirect("/")

@login_required
def AddAnswer(request, form, question_pk):
    if form.is_valid:
        answer = form.save(commit=False)
        answer.author = Profile.objects.get(user=request.user.pk)
        answer.question = Question.objects.get(pk=question_pk)
        answer.is_correct = False
        answer.rating = 0
        answer.save()

def question(request, pk):
    if request.method == 'GET':
        form = AnswerForm()
    else:
        if not request.user.is_authenticated:
            return redirect("/sing-in/?next=/question/%s" % (pk))
        form = AnswerForm(data=request.POST)
        AddAnswer(request, form, pk)
        answers_number = Answer.objects.filter(question=pk).count()
        pages_number = answers_number // STD_PER_PAGE
        if answers_number % STD_PER_PAGE != 0:
            pages_number = pages_number + 1
        return redirect('/question/%s/?page=%s' % (pk, pages_number))
    current_question = Question.objects.get(pk=pk)
    answers_page = paginate(request, Answer.objects.filter(question=pk), STD_PER_PAGE)
    ctx = {
        'form': form,
        'currentQuestion': current_question,
        'answers': answers_page,
        }
    return render(request, 'question.html', ctx)

    
def questionsByTag(request, tag):
    questions_page = paginate(request, Question.objects.filter(tags__name=tag))
    ctx = {'questions': questions_page}
    return render(request, 'index.html', ctx)
    