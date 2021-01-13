from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
from ask_yakovitskiy.models import Question, Answer, Profile, LikeAnswer, LikeQuestion, Tag
from ask_yakovitskiy.forms import LoginForm, UserForm, NewQuestionForm, AnswerForm, SettingsForm, ImageForm
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
    if request.method == 'GET':
        form = NewQuestionForm()
    else:
        form = NewQuestionForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = Profile.objects.get(user=request.user.pk)
            question.rating = 0
            question.answers_number = 0
            tags = form.cleaned_data.get('tags').split()
            question.save()
            if len(tags) <= 3:
                for tag in tags:
                    try:
                        Tag.objects.get(name=tag)
                    except Tag.DoesNotExist:
                        Tag.objects.create(name=tag)
                    question.tags.set(Tag.objects.filter(name__in=tags))
            else:
                question.delete()
                form.add_error(
                    'tags', 'Please, enter 3 or less tags for your question')
                ctx = {'form': form}
                return render(request, 'new-question.html', ctx)
            return redirect(reverse('question', kwargs={'pk': question.pk}))
        else:
            form.add_error(None, 'Please input valid data')
    ctx = {'form': form}
    return render(request, 'new-question.html', ctx)


@login_required
def settings(request):
    current_user = request.user
    if request.method == 'GET':
        image_form = ImageForm(
            initial={'avatar': Profile.objects.get(user=current_user).avatar},)
        form = SettingsForm(initial={
            'username': current_user.username,
            'email': current_user.email,
            'avatar': Profile.objects.get(user=current_user).avatar,
        })
    else:
        form = SettingsForm(data=request.POST, files=request.FILES)
        image_form = ImageForm(
            data=request.POST, files=request.FILES, instance=current_user.profile)
        if form.is_valid():
            ctx = {'form': form, 'image_form': image_form}
            if current_user.check_password(form.cleaned_data['old_password']):
                try:
                    if User.objects.get(username=form.cleaned_data['username']).username == current_user.username:
                        raise User.DoesNotExist
                    form.add_error(
                        'username', 'This username is already in use')
                    ctx = {'form': form}
                    return render(request, 'settings.html', ctx)
                except User.DoesNotExist:
                    current_user.username = form.cleaned_data['username']

                if not User.objects.filter(email=form.cleaned_data['email']).exists():
                    current_user.email = form.cleaned_data['email']
                elif User.objects.get(email=form.cleaned_data['email']) != current_user:
                    form.add_error('email', 'This email is already in use')

                if form.cleaned_data['new_password'] != '':
                    if form.cleaned_data['new_password'] == form.cleaned_data['confirm_new_password']:
                        current_user.set_password(
                            form.cleaned_data['new_password'])
                        auth.login(request, current_user)
                    else:
                        form.add_error('confirm_new_password',
                                       'Passwords should match')

                if image_form.data['avatar'] is not None:
                    image_form.save()
                current_user.save()
            else:
                form.add_error(
                    'old_password', 'Please, enter your CURRENT password correctly')
        else:
            form.add_error(None, 'Please, enter valid data')
    ctx = {'form': form, 'image_form': image_form}
    return render(request, 'settings.html', ctx)


def singUp(request):
    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(data=request.POST)
        ctx = {'form': form}
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error('username', 'This username is already in use')
                return render(request, 'sing-up.html', ctx)
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'This email is already in use')
                return render(request, 'sing-up.html', ctx)
            user = form.save()
            user.refresh_from_db()
            if User.objects.get(username=user.username):
                user.save()
                profile = Profile()
                profile.user = user
                if form.cleaned_data['avatar'] is not None:
                    profile.avatar = form.cleaned_data['avatar']
                else:
                    profile.avatar = "img/question-mark.jpg"
                profile.save()
                auth.authenticate(username=user.username,
                                  password=form.cleaned_data.get('password'))
                auth.login(request, user)
            else:
                form.add_error(None, 'Unknown error at creating user')
                return render(request, 'sing-up.html', ctx)
            return redirect("/")
    ctx = {'form': form}
    return render(request, 'sing-up.html', ctx)


def singIn(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            ctx = {'form': form}
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect("/")
            else:
                form.add_error(None, 'Incorrect login or password')
        else:
            form.add_error(None, 'Please, enter valid data')
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
    current_question = get_object_or_404(Question, pk=pk)
    answers_page = paginate(
        request, Answer.objects.filter(question=pk), STD_PER_PAGE)
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


@require_POST
@login_required
def voteQuestion(request):
    data = request.POST
    from pprint import pformat
    print('\n\n', '=' * 100)
    print(f'HERE: {pformat(data)}')
    print('=' * 100, '\n\n')
    current_profile = Profile.objects.get(user=request.user)
    current_question = Question.objects.get(pk=data['qpk'])
    if LikeQuestion.objects.filter(user=current_profile, question=current_question).exists():
        current_vote = LikeQuestion.objects.get(
            user=current_profile, question=current_question)
        if current_vote.opinion == True:
            if data['action'] == 'up-vote':
                print('\n\n up delete \n\n')
                current_vote.delete()
            elif data['action'] == 'down-vote':
                print('\n\n down rewrite \n\n')
                current_vote.opinion = False
                current_question.rating -= 2
                current_vote.save()
                current_question.save()

        elif current_vote.opinion == False:
            if data['action'] == 'up-vote':
                print('\n\n up rewrite \n\n')
                current_vote.opinion = True
                current_question.rating += 2
                current_vote.save()
                current_question.save()

            elif data['action'] == 'down-vote':
                print('\n\n down delete \n\n')
                current_vote.delete()
    else:
        if data['action'] == 'up-vote':
            print('\n\n up create \n\n')
            LikeQuestion.objects.create(question=current_question,
                                        user=current_profile,
                                        opinion=True
                                        )
        elif data['action'] == 'down-vote':
            print('\n\n down create \n\n')
            LikeQuestion.objects.create(question=current_question,
                                        user=current_profile,
                                        opinion=False
                                        )
    current_question = Question.objects.get(pk=data['qpk'])
    data_to_send = {'rating': current_question.rating}
    return JsonResponse(data_to_send)


@require_POST
@login_required
def voteAnswer(request):
    data = request.POST
    from pprint import pformat
    print('\n\n', '=' * 100)
    print(f'HERE: {pformat(data)}')
    print('=' * 100, '\n\n')
    current_profile = Profile.objects.get(user=request.user)
    current_answer = Answer.objects.get(pk=data['apk'])
    if LikeAnswer.objects.filter(user=current_profile, answer=current_answer).exists():
        current_vote = LikeAnswer.objects.get(
            user=current_profile, answer=current_answer)
        if current_vote.opinion == True:
            if data['action'] == 'up-vote':
                print('\n\n up delete \n\n')
                current_vote.delete()
            elif data['action'] == 'down-vote':
                print('\n\n down rewrite \n\n')
                current_vote.opinion = False
                current_answer.rating -= 2
                current_vote.save()
                current_answer.save()

        elif current_vote.opinion == False:
            if data['action'] == 'up-vote':
                print('\n\n up rewrite \n\n')
                current_vote.opinion = True
                current_answer.rating += 2
                current_vote.save()
                current_answer.save()

            elif data['action'] == 'down-vote':
                print('\n\n down delete \n\n')
                current_vote.delete()
    else:
        if data['action'] == 'up-vote':
            print('\n\n up create \n\n')
            LikeAnswer.objects.create(answer=current_answer,
                                      user=current_profile,
                                      opinion=True
                                      )
        elif data['action'] == 'down-vote':
            print('\n\n down create \n\n')
            LikeAnswer.objects.create(answer=current_answer,
                                      user=current_profile,
                                      opinion=False
                                      )
    current_answer = Answer.objects.get(pk=data['apk'])
    data_to_send = {'rating': current_answer.rating}
    return JsonResponse(data_to_send)


@require_POST
@login_required
def setRight(request):
    data = request.POST
    current_profile = Profile.objects.get(user=request.user)
    current_answer = Answer.objects.get(pk=data['apk'])
    current_question = current_answer.question
    if current_question.author == current_profile:
        if current_answer.is_correct:
            current_answer.is_correct = False
        else:
            current_answer.is_correct = True
        current_answer.save()
        data_to_send = {'checked': current_answer.is_correct}
        return JsonResponse(data_to_send)
    else:
        data_to_send = JsonResponse(
            {'error': 'You are not the question author to do it'})
        data_to_send.status_code = 403
        return data_to_send
