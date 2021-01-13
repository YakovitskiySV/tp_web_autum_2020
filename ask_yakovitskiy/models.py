from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='id пользователя')
    avatar = models.ImageField(max_length=1024, default='question-mark.jpg',
                               verbose_name='Аватар', null=True, upload_to='avatar/%y/%m/%d')

    def __str__(self):
        return self.user.get_username()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Question(models.Model):
    author = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=258, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    tags = models.ManyToManyField(
        'Tag', verbose_name='Тэги', null=True, blank=True)
    rating = models.IntegerField(default=0, verbose_name='Рэйтинг')
    answers_number = models.IntegerField(
        default=0, verbose_name='Кол-во ответов')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    author = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, verbose_name='Автор')
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE, verbose_name='Вопрос')
    text = models.TextField(verbose_name='Текст')
    is_correct = models.BooleanField(verbose_name='Правильность', null=True)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг', null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.question.answers_number += 1
            self.question.save()
        super(Answer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.question.answers_number -= 1
        self.question.save()
        super(Answer, self).delete(*args, **kwargs)

    def __str__(self):
        return self.author.user.get_username()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class LikeQuestion(models.Model):
    user = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE, verbose_name='Вопрос')
    opinion = models.BooleanField(
        default=True, verbose_name='Мнение', null=True)

    def __str__(self):
        return self.user.user.get_username() + ' оценил ' + self.question.title

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.opinion:
                self.question.rating += 1
            else:
                self.question.rating -= 1
            self.question.save()
        super(LikeQuestion, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.opinion:
            self.question.rating -= 1
        else:
            self.question.rating += 1
        self.question.save()
        super(LikeQuestion, self).delete(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'question')
        verbose_name = 'Лайк на вопрос'
        verbose_name_plural = 'Лайки на вопросы'


class LikeAnswer(models.Model):
    user = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    answer = models.ForeignKey(
        'Answer', on_delete=models.CASCADE, verbose_name='Ответ')
    opinion = models.BooleanField(
        default=True, verbose_name='Мнение', null=True)

    def __str__(self):
        return self.user.user.get_username() + ' оценил ответ в ' + self.answer.question.title + ' пользователя ' + self.answer.author.user.get_username()

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.opinion:
                self.answer.rating += 1
            else:
                self.answer.rating -= 1
            self.answer.save()
        super(LikeAnswer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.opinion:
            self.answer.rating -= 1
        else:
            self.answer.rating += 1
        self.answer.save()
        super(LikeAnswer, self).delete(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'answer')
        verbose_name = 'Лайк на ответ'
        verbose_name_plural = 'Лайки на ответы'


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
