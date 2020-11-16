from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('hot/', views.hot, name = 'hot'),
    path('new-questions/', views.newQuestions, name = 'new-questions'),
    path('ask/', views.newQuestion, name = 'ask'),
    path('settings/', views.settings, name = 'settings'),
    path('sing-up/', views.singUp, name = 'sing-up'),
    path('sing-in/', views.singIn, name = 'sing-in'),
    path('question/<int:pk>/', views.question, name = 'question'),
    path('questions-by-tag/<tag>/', views.questionsByTag, name = 'question-by-tag')
]