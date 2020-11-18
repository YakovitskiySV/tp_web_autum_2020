from django.shortcuts import render
from django.core.paginator import Paginator
from ask_yakovitskiy.models import Question, Answer, Profile, LikeAnswer, LikeQuestion, Tag


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_num = request.GET.get('page')
    return paginator.get_page(page_num)

def hot(request):
    questions_page = paginate(Question.objects.all(), request)
    return render(request, 'index.html', {
        'questions': questions_page,
    })

def newQuestions(request):
    questions_page = paginate(Question.objects.all(), request)
    return render(request, 'index.html', {
        'questions': questions_page,
    })

def newQuestion(request):
    return render(request, 'new-question.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def singUp(request):
    return render(request, 'sing-up.html', {})

def singIn(request):
    return render(request, 'sing-in.html', {})

def question(request, pk):
    current_question = Question.objects.get(id=pk)
    answers_page = paginate(Answer.objects.filter(question=pk), request, 5)
    return render(request, 'question.html', {
        'currentQuestion': current_question,
        'answers': answers_page,
    })
    
def questionsByTag(request, tag):
    questions_page = paginate(Question.objects.filter(tags__name=tag), request)
    return render(request, 'index.html', {
        'questions': questions_page,
    })
    