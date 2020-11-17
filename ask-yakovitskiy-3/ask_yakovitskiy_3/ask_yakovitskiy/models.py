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
        
class LikeQuestion(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name = 'Пользователь')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name = 'Вопрос') 
    opinion = models.IntegerField(verbose_name = 'Мнение')
    def __str__(self):
        return self.user.user_id.get_username() + ' оценил ' + self.question.title
    
    class Meta:
        verbose_name = 'Лайк на вопрос'
        verbose_name_plural = 'Лайки на вопросы'
        
class LikeAnswer(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name = 'Пользователь')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name = 'Вопрос') 
    opinion = models.IntegerField(verbose_name = 'Мнение')
    def __str__(self):
        return self.user.user_id.get_username() + ' оценил ответ в ' + self.answer.question.title + ' пользователя ' + self.answer.author.user_id.get_username()
    
    class Meta:
        verbose_name = 'Лайк на ответ'
        verbose_name_plural = 'Лайки на ответы' 


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name = 'Название')
    questions = models.ManyToManyField('Question', verbose_name = 'Вопрос')
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'    