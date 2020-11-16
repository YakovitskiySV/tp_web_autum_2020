from django.shortcuts import render
from django.core.paginator import Paginator


questions = [
    {
        'id': idx,
        'title': f'title {idx}',
        'text': 'question text',
     } for idx in range(10)
]

answers = [
    {
        'id': idx,
        'author': f'author {idx}',
        'text': 'answer text',
     } for idx in range(10)
]

def index(request):
    paginator = Paginator(questions, 3)
    page_number = request.GET.get('page')
    page_questions = paginator.get_page(page_number) #1
    return render(request, 'index.html', {
        'questions': page_questions,
    })

def hot(request):
    paginator = Paginator(questions, 3)
    page_number = request.GET.get('page')
    page_questions = paginator.get_page(page_number) #1
    return render(request, 'index.html', {
        'questions': page_questions,
    })

def newQuestions(request):
    paginator = Paginator(questions, 3)
    page_number = request.GET.get('page')
    page_questions = paginator.get_page(page_number) #1
    return render(request, 'index.html', {
        'questions': page_questions,
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
    currentQuestion = questions[pk]
    return render(request, 'question.html', {
        'currentQuestion': currentQuestion,
        'answers': answers,
    })

def questionsByTag(request, tag):
    return index(request)
