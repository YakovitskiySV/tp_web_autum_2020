from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ask_yakovitskiy.models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer
from random import choice, sample, randint
from faker import Faker

f = Faker()

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--users', nargs='+', type=int)
        parser.add_argument('--questions', nargs='+', type=int)
        parser.add_argument('--answers', nargs='+', type=int)
        parser.add_argument('--tags', nargs='+', type=int)
        parser.add_argument('--likes', nargs='+', type=int)

        parser.add_argument('--db_size', nargs='+', type=str)

    def handle(self, *args, **options):
        if options['users']:
            self.fill_profile(options['users'][0])

        if options['tags']:
            self.fill_tag(options['tags'][0])

        if options['questions']:
            self.fill_questions(options['questions'][0])

        if options['answers']:
            self.fill_answers(options['answers'][0])

        if options['likes']:
            #self.fill_likes_questions(options['likes'][0])
            self.fill_likes_answers(options['likes'][0])

        self.stdout.write(self.style.SUCCESS('Successfully closed poll '))

    @staticmethod
    def fill_profile(cnt):
        for i in range(cnt):
            Profile.objects.create(
                user=User.objects.create(
                    username=f.user_name(),
                    email=f.email(),
                    password=f.password(length=8, digits=True)
                ),
                avatar="img/question-mark.jpg",
            )

    @staticmethod
    def fill_tag(cnt):
        for i in range(cnt):
            Tag.objects.create(
                name=f.word(),
            )

    @staticmethod
    def fill_questions(cnt):
        tag_ids = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )
        for profile in Profile.objects.all():
            q = Question.objects.create(
                author=profile,
                title=f.sentence(),
                text=f.text(),
            )
            q.tags.set(Tag.objects.filter(id__in=sample(tag_ids, k=randint(1, 3)))),

    @staticmethod
    def fill_answers(cnt):
        profile_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        question_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            Answer.objects.create(
                author=Profile.objects.get(pk=choice(profile_ids)),
                question=Question.objects.get(pk=choice(question_ids)),
                text=f.text(),
            )

    @staticmethod
    def fill_likes_questions(cnt):
        profile_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        count = 0
        for cur_question in Question.objects.all():
            for profile in Profile.objects.filter(id__in=sample(profile_ids, k=randint(0, 10))):
                LikeQuestion.objects.create(
                    question=cur_question,
                    user=profile,
                )
                count += 1
                if count == cnt:
                    break
            if count == cnt:
                break

    @staticmethod
    def fill_likes_answers(cnt):
        profile_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        count = 0
        for cur_answer in Answer.objects.all():
            for profile in Profile.objects.filter(id__in=sample(profile_ids, k=randint(0, 10))):
                LikeAnswer.objects.create(
                    answer=cur_answer,
                    user=profile,
                )
                count += 1
                if count == cnt:
                    break
            if count == cnt:
                break