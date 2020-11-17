from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name = 'id пользователя')
    avatar = models.ImageField(max_length=1024, verbose_name = 'Аватар', null = True)

    def __str__(self):
        return self.user_id.get_user_name()
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
class Question(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name = 'Автор')
    title = models.CharField(max_length = 258, verbose_name = 'Заголовок')
    text = models.TextField(verbose_name = 'Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name = 'Автор')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name = 'Вопрос')
    text = models.TextField(verbose_name = 'Текст')
    is_correct = models.BooleanField(verbose_name = 'Правильность')
    
    def __str__(self):
        return self.author
        
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        
class Like(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name = 'Пользователь')
    questions = models.ManyToManyField('Question', verbose_name = 'Вопрос') 
    opinion = models.IntegerField(verbose_name = 'Мнение')
    def __str__(self):
        return self.opinion
    
    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки' 


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name = 'Название')
    questions = models.ManyToManyField('Question', verbose_name = 'Вопрос')
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'    