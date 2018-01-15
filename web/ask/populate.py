import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask.settings')

import django
django.setup()

from faker import Faker
import random

fake = Faker()

users = []

from django.contrib.auth.models import User
for i in range(1,20):
    user = User.objects.create(username=fake.user_name(),email=fake.email(),password=fake.password())
    users.append(user)

questions = []
from qa.models import Question, Answer
for i in range(1, 50):
    question = Question.objects.create(title=fake.paragraph(),
                                        text=fake.text(),
                                        added_at=fake.date_time(),
                                        rating=random.randrange(1,101),
                                        author=random.choice(users))
    rand_users = random.sample(users, random.randrange(len(users)))
    for usr in rand_users:
        question.likes.add(usr)
    question.save()
    questions.append(question)

answers = []
for i in range(1,300):
    answer = Answer.objects.create(text=fake.text(),
                    added_at=fake.date_time(),
                    question=random.choice(questions),
                    author=random.choice(users))
    answers.append(answer)

# saving
