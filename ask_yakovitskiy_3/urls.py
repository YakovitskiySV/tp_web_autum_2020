"""ask_yakovitskiy_3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ask_yakovitskiy import views
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hot, name='index'),
    path('hot/', views.hot, name='hot'),
    path('new-questions/', views.newQuestions, name='new-questions'),
    path('ask/', views.newQuestion, name='ask'),
    path('settings/', views.settings, name='settings'),
    path('sing-up/', views.singUp, name='sing-up'),
    path('sing-in/', views.singIn, name='sing-in'),
    path('log-out/', views.LogOut, name='log-out'),
    path('question/<int:pk>/', views.question, name='question'),
    path('questions-by-tag/<tag>/', views.questionsByTag, name='question-by-tag'),
    path('voteQuestion/', views.voteQuestion, name='voteQuestion'),
    path('voteAnswer/', views.voteAnswer, name='voteAnswer'),
    path('setRight/', views.setRight, name='setRight'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
